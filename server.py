#!/usr/bin/env python3
"""
discogs-cleaner — server.py

Local bridge server that lets the web UI browse and rename folders on disk.

Usage:
    python server.py
    python server.py --port 7842

Then open http://localhost:7842 in your browser.
The UI will have a folder picker and an "Apply on disk" button.
"""

import os
import sys
import json
import argparse
import threading
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

PORT = 7842
ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
INDEX_FILE = os.path.join(ROOT_DIR, 'index.html')  # overridden by --index arg


def sanitize_name(name):
    invalid = '<>:"/\\|?*'
    for ch in invalid:
        name = name.replace(ch, "")
    return name.strip()


class Handler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # suppress request logs

    def send_json(self, data, status=200):
        body = json.dumps(data).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", len(body))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def send_file(self, path, mime):
        with open(path, "rb") as f:
            data = f.read()
        self.send_response(200)
        self.send_header("Content-Type", mime)
        self.send_header("Content-Length", len(data))
        self.end_headers()
        self.wfile.write(data)

    def do_OPTIONS(self):
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/" or path == "/index.html":
            self.send_file(INDEX_FILE, "text/html; charset=utf-8")
            return

        # API: list subfolders in a directory
        if path == "/api/ls":
            qs = parse_qs(parsed.query)
            target = qs.get("path", [None])[0]
            if not target:
                self.send_json({"error": "No path provided"}, 400)
                return
            target = os.path.abspath(target)
            if not os.path.isdir(target):
                self.send_json({"error": f"Not a directory: {target}"}, 400)
                return
            try:
                entries = [
                    e for e in os.listdir(target)
                    if os.path.isdir(os.path.join(target, e))
                ]
                entries.sort()
                self.send_json({"path": target, "folders": entries})
            except Exception as e:
                self.send_json({"error": str(e)}, 500)
            return

        self.send_response(404)
        self.end_headers()

    def do_POST(self):
        parsed = urlparse(self.path)
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)

        # API: apply renames on disk
        if parsed.path == "/api/rename":
            try:
                data = json.loads(body)
                root = os.path.abspath(data.get("path", "."))
                renames = data.get("renames", [])
                dry_run = data.get("dry_run", False)

                if not os.path.isdir(root):
                    self.send_json({"error": f"Directory not found: {root}"}, 400)
                    return

                results = []
                for item in renames:
                    old_name = item.get("original", "")
                    new_name = sanitize_name(item.get("newName", ""))

                    if not old_name or not new_name or old_name == new_name:
                        results.append({"original": old_name, "newName": new_name, "result": "skip", "reason": "unchanged"})
                        continue

                    old_path = os.path.join(root, old_name)
                    new_path = os.path.join(root, new_name)

                    if not os.path.exists(old_path):
                        results.append({"original": old_name, "newName": new_name, "result": "skip", "reason": "not found on disk"})
                        continue

                    if os.path.exists(new_path) and os.path.abspath(old_path) != os.path.abspath(new_path):
                        results.append({"original": old_name, "newName": new_name, "result": "skip", "reason": "target already exists"})
                        continue

                    if dry_run:
                        results.append({"original": old_name, "newName": new_name, "result": "dry_run"})
                    else:
                        try:
                            os.rename(old_path, new_path)
                            results.append({"original": old_name, "newName": new_name, "result": "ok"})
                            # Write stamp file if requested
                            if data.get("stamp", False):
                                stamp_entries = {s["original"]: s for s in data.get("stamp_data", [])}
                                entry = stamp_entries.get(old_name, {})
                                stamp_path = os.path.join(new_path, "discogs-cleaner.txt")
                                from datetime import datetime
                                stamp_lines = [
                                    "This folder was renamed by discogs-cleaner",
                                    "https://github.com/nmyriad/discogs-cleaner-desktop",
                                    "",
                                    "Date: " + datetime.now().strftime("%Y-%m-%d %H:%M"),
                                    "Original name: " + old_name,
                                    "Renamed to: " + new_name,
                                ]
                                if entry.get("discogsUrl"):
                                    stamp_lines.append("Discogs release: " + entry["discogsUrl"])
                                try:
                                    with open(stamp_path, "w", encoding="utf-8") as sf:
                                        sf.write("
".join(stamp_lines) + "
")
                                except Exception:
                                    pass
                        except OSError as e:
                            results.append({"original": old_name, "newName": new_name, "result": "error", "reason": str(e)})

                self.send_json({"root": root, "dry_run": dry_run, "results": results})
            except Exception as e:
                self.send_json({"error": str(e)}, 500)
            return

        # API: get config (cached keys + stats)
        if parsed.path == '/api/config/get':
            cfg = load_config()
            self.send_json(cfg)
            return

        # API: save config (keys + increment stats)
        if parsed.path == '/api/config/save':
            try:
                data = json.loads(body)
                cfg = load_config()
                if 'key' in data: cfg['key'] = data['key']
                if 'secret' in data: cfg['secret'] = data['secret']
                if 'add_renamed' in data:
                    cfg['lifetime_renamed'] = cfg.get('lifetime_renamed', 0) + int(data['add_renamed'])
                save_config(cfg)
                self.send_json({'ok': True, 'config': cfg})
            except Exception as e:
                self.send_json({'error': str(e)}, 500)
            return

        self.send_response(404)
        self.end_headers()


def get_config_path():
    home = os.path.expanduser('~')
    cfg_dir = os.path.join(home, '.discogs-cleaner')
    os.makedirs(cfg_dir, exist_ok=True)
    return os.path.join(cfg_dir, 'config.json')

def load_config():
    try:
        with open(get_config_path(), 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception:
        return {'key': '', 'secret': '', 'lifetime_renamed': 0}

def save_config(cfg):
    with open(get_config_path(), 'w', encoding='utf-8') as f:
        json.dump(cfg, f, indent=2)


def main():
    import io
    if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

    parser = argparse.ArgumentParser(description="discogs-cleaner local server")
    parser.add_argument("--port", type=int, default=PORT)
    parser.add_argument("--no-browser", action="store_true")
    parser.add_argument("--index", type=str, default=None, help="Path to index.html")
    args = parser.parse_args()

    global INDEX_FILE
    if args.index:
        INDEX_FILE = os.path.abspath(args.index)

    server = HTTPServer(("127.0.0.1", args.port), Handler)
    url = f"http://localhost:{args.port}"
    print(f"\n  discogs-cleaner server running")
    print(f"  -> {url}\n")
    print("  Press Ctrl+C to stop.\n")

    if not args.no_browser:
        threading.Timer(0.5, lambda: webbrowser.open(url)).start()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n  Server stopped.")


if __name__ == "__main__":
    main()
