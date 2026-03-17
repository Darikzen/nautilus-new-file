#!/bin/bash
# Uninstall nautilus-new-file extension
set -e

EXTENSIONS_DIR="$HOME/.local/share/nautilus-python/extensions"

echo "Removing extension files..."
rm -f "$EXTENSIONS_DIR/new_file_menu.py"
rm -f "$EXTENSIONS_DIR/new_file_dialog.py"

echo "Restarting Nautilus..."
nautilus -q 2>/dev/null || true

echo "Done! Extension removed."
