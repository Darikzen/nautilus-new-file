#!/bin/bash
# Install nautilus-new-file extension
set -e

EXTENSIONS_DIR="$HOME/.local/share/nautilus-python/extensions"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "Installing dependencies..."
sudo apt install -y python3-nautilus gir1.2-adw-1

echo "Installing extension..."
mkdir -p "$EXTENSIONS_DIR"
cp "$SCRIPT_DIR/new_file_menu.py" "$EXTENSIONS_DIR/"
cp "$SCRIPT_DIR/new_file_dialog.py" "$EXTENSIONS_DIR/"

echo "Restarting Nautilus..."
nautilus -q 2>/dev/null || true

echo ""
echo "Done! Right-click any folder background → \"New File…\""
