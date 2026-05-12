#!/bin/bash

echo ""
echo " discogs-cleaner — setup"
echo " ========================"
echo ""

install_python_mac() {
    echo " [..] Attempting to install Python via Homebrew..."
    if ! command -v brew &>/dev/null; then
        echo " [..] Homebrew not found. Installing Homebrew first..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    fi
    brew install python3
}

install_python_linux() {
    echo " [..] Installing Python via apt..."
    sudo apt-get update && sudo apt-get install -y python3 python3-pip
}

# Check for python3
if command -v python3 &>/dev/null; then
    echo " [OK] Python is already installed: $(python3 --version)"
elif command -v python &>/dev/null; then
    PY_VER=$(python --version 2>&1)
    echo " [OK] Python is already installed: $PY_VER"
else
    echo " [!!] Python not found."
    OS="$(uname -s)"
    case "$OS" in
        Darwin)
            install_python_mac
            ;;
        Linux)
            install_python_linux
            ;;
        *)
            echo " [!!] Unknown OS: $OS"
            echo "      Please install Python manually: https://www.python.org/downloads/"
            exit 1
            ;;
    esac

    if ! command -v python3 &>/dev/null; then
        echo " [!!] Installation may have failed. Please install Python manually:"
        echo "      https://www.python.org/downloads/"
        exit 1
    fi
    echo " [OK] Python installed: $(python3 --version)"
fi

echo ""
echo " [OK] Starting discogs-cleaner server at http://localhost:7842"
echo "      Press Ctrl+C to stop."
echo ""

# Use whichever python is available
if command -v python3 &>/dev/null; then
    python3 server.py
else
    python server.py
fi
