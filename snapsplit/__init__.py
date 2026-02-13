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
    along with this program; if not, see <https://www.gnu.org
/licenses>.
'''


bl_info = {
    "name": "SnapSplit – Print-ready segmentation with connectors",
    "author": "https://dev.betakontext.de | Christoph Medicus | dev@betakontext.de",
    "version": (0, 1, 0),
    "blender": (5, 0, 1),
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

# Import submodules
from . import utils
from . import profiles
from . import prefs
from . import ops_split
from . import ops_connectors
from . import ui

# Registration order matters if modules reference each other in register()
_modules = [utils, profiles, prefs, ops_split, ops_connectors, ui]

def register():
    # Reload modules during dev to pick up edits without Blender restart
    for m in _modules:
        try:
            importlib.reload(m)
        except Exception:
            # On first load, reload may fail harmlessly
            pass

    for m in _modules:
        if hasattr(m, "register"):
            m.register()

def unregister():
    for m in reversed(_modules):
        if hasattr(m, "unregister"):
            m.unregister()
