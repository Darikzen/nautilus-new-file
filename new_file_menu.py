"""
Nautilus extension: "New File…" context menu item.
Launches a standalone Adwaita dialog with GTK_IM_MODULE=simple
to bypass input method issues when spawned from Nautilus on Wayland.

Part of: https://github.com/darikzen/nautilus-new-file
License: MIT
"""

import os
import subprocess
from gi.repository import Nautilus, GObject


DIALOG_SCRIPT = os.path.expanduser(
    "~/.local/share/nautilus-python/extensions/new_file_dialog.py"
)


class NewFileExtension(GObject.GObject, Nautilus.MenuProvider):
    """Adds a 'New File…' entry to the Nautilus background (right-click) menu."""

    def _show_dialog(self, directory):
        env = os.environ.copy()
        env["GTK_IM_MODULE"] = "simple"
        subprocess.Popen(
            ["python3", DIALOG_SCRIPT, directory],
            env=env,
        )

    def get_background_items(self, *args):
        current_folder = args[0] if args else None
        if current_folder is None:
            return []
        location = current_folder.get_location()
        if location is None:
            return []
        directory = location.get_path()
        if directory is None:
            return []

        item = Nautilus.MenuItem(
            name="NewFileExtension::new_file",
            label="New File…",
            tip="Create a new empty file",
        )
        item.connect("activate", lambda _i: self._show_dialog(directory))
        return [item]
