'''
Copyright (C) 2026 Christoph Medicus
https://dev.betakontext.de
dev@betakontext.de

This file is part of SnapSplit

SnapSplit is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 3
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, see <https://www.gnu.org/licenses>.
'''
# __init__.py

bl_info = {
    "name": "SnapSplit  Print-ready segmentation with connectors",
    "author": "Christoph Medicus",
    "email": "dev@betakontext.de",
    "website": "https://dev.betakontext.de",
    "version": (0, 1, 9),
    "blender": (5, 2, 0),
    "location": "View3D > N-Panel > SnapSplit",
    "description": (
        "Split meshes into printable parts and generate fitting connectors for 3D printing."
    ),
    "warning": "",
    "doc_url": "",
    "tracker_url": "",
    "category": "Object",
}

import importlib

import bpy

# Import submodules
from . import localization  # translation data (DICTIONARY), no register() of its own
from . import utils
from . import profiles
from . import prefs
from . import ops_split
from . import ops_connectors
from . import ops_align
from . import ui

# Set to False for release builds to skip the development hot-reload.
DEV_RELOAD = False

_modules = [
    localization,
    utils,
    profiles,
    prefs,
    ops_split,
    ops_connectors,
    ops_align,
    ui,
]

# Modules whose register() completed successfully (in registration order)
_registered = []


# ---------------------------
# Translations
# ---------------------------

def _unregister_translations():
    """Remove the add-on's translation dictionary (safe to call when not registered)."""
    try:
        bpy.app.translations.unregister(__name__)
    except Exception:
        # Not registered (first start) or translation support not built in: ignore
        pass


def _register_translations():
    """Register localization.DICTIONARY with Blender's translation system.

    A failure here must never prevent the add-on from loading; the UI then
    simply stays in English.
    """
    known = set(bpy.app.translations.locales)
    dictionary = {
        locale: entries
        for locale, entries in localization.DICTIONARY.items()
        if locale in known
    }

    skipped = sorted(set(localization.DICTIONARY) - set(dictionary))
    if skipped:
        print(f"SnapSplit: locales unknown to this Blender build were skipped: {skipped}")

    # Hot-reload safety: drop a stale registration before registering again
    _unregister_translations()
    try:
        bpy.app.translations.register(__name__, dictionary)
    except Exception as exc:
        print(f"SnapSplit: translation registration failed, UI stays English: {exc}")


# ---------------------------
# Registration
# ---------------------------

def register():
    """Register translations and all SnapSplit submodules (hot-reload aware)."""
    # Reload modules during development to pick up edits without restarting Blender
    if DEV_RELOAD:
        for m in _modules:
            try:
                importlib.reload(m)
            except Exception:
                # On first load, reload may fail harmlessly
                pass

    # Translations first, so labels are translatable as soon as the classes exist
    _register_translations()

    _registered.clear()
    try:
        for m in _modules:
            if hasattr(m, "register"):
                m.register()
                _registered.append(m)
    except Exception:
        # Roll back everything that was registered so far, then re-raise
        unregister()
        raise


def unregister():
    """Unregister all submodules in reverse order, then the translations."""
    while _registered:
        m = _registered.pop()
        try:
            m.unregister()
        except Exception as exc:
            # Keep going: one failing module must not block the others
            print(f"SnapSplit: unregister failed in {m.__name__}: {exc}")

    _unregister_translations()


