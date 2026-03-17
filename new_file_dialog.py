#!/usr/bin/env python3
"""
Standalone Adwaita dialog for creating a new file.
Matches the native GNOME "New Folder" dialog style.

Called by new_file_menu.py (Nautilus extension).
Part of: https://github.com/darikzen/nautilus-new-file
License: MIT
"""

import sys
import os
import gi
gi.require_version("Gtk", "4.0")
gi.require_version("Adw", "1")
from gi.repository import Gtk, Adw, GLib


class NewFileApp(Gtk.Application):
    def __init__(self, directory):
        super().__init__(application_id="dev.darikzen.nautilus-new-file")
        self.directory = directory

    def do_activate(self):
        win = Adw.Window(application=self, title="New File",
                         default_width=450, default_height=0, resizable=False)

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)

        # Header bar matching GNOME's New Folder style
        header = Adw.HeaderBar()
        header.set_show_end_title_buttons(False)
        header.set_show_start_title_buttons(False)
        title_label = Gtk.Label(label="New File")
        title_label.add_css_class("title")
        header.set_title_widget(title_label)

        cancel_btn = Gtk.Button(label="Cancel")
        cancel_btn.add_css_class("flat")
        header.pack_start(cancel_btn)

        create_btn = Gtk.Button(label="Create")
        create_btn.add_css_class("suggested-action")
        create_btn.set_sensitive(False)
        header.pack_end(create_btn)

        vbox.append(header)

        # Content
        content = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        content.set_margin_top(18)
        content.set_margin_bottom(18)
        content.set_margin_start(18)
        content.set_margin_end(18)

        label = Gtk.Label(label="File Name", halign=Gtk.Align.START)
        content.append(label)

        entry = Gtk.Entry(placeholder_text="example.txt", hexpand=True)
        content.append(entry)

        vbox.append(content)
        win.set_content(vbox)

        def on_create(*_args):
            name = entry.get_text().strip()
            if name:
                filepath = os.path.join(self.directory, name)
                if os.path.exists(filepath):
                    base, ext = os.path.splitext(name)
                    counter = 1
                    while os.path.exists(filepath):
                        filepath = os.path.join(self.directory,
                                                f"{base} ({counter}){ext}")
                        counter += 1
                open(filepath, "a").close()
            self.quit()

        def on_text_changed(*_args):
            create_btn.set_sensitive(bool(entry.get_text().strip()))

        entry.connect("activate", on_create)
        entry.connect("changed", on_text_changed)
        cancel_btn.connect("clicked", lambda _: self.quit())
        create_btn.connect("clicked", on_create)
        win.connect("close-request", lambda _: self.quit())

        win.present()
        entry.grab_focus()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: new_file_dialog.py <directory>", file=sys.stderr)
        sys.exit(1)
    directory = sys.argv[1]
    app = NewFileApp(directory)
    app.run([sys.argv[0]])
