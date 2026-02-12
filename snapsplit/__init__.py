'''
Copyright (C) 2026 Betakontext
https://dev.betakontext.de
info@betakontext.de

Created by Christoph Medicus

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
    "name": "SnapSplit - Druckgerechte Segmentierung mit Steckverbindern",
    "author": "fobizz (Assistant)",
    "version": (0, 1, 0),
    "blender": (5, 0, 1),
    "location": "View3D > N-Panel > SnapSplit",
    "description": "Zerlegt Meshes in Teile und erzeugt passgenaue Steckverbindungen für 3D-Druck.",
    "warning": "",
    "doc_url": "",
    "tracker_url": "",
    "category": "Object",
}

import importlib
from . import ui, prefs, ops_split, ops_connectors, profiles, utils

modules = [ui, prefs, ops_split, ops_connectors, profiles, utils]

def register():
    for m in modules:
        importlib.reload(m)
    for m in modules:
        if hasattr(m, "register"):
            m.register()

def unregister():
    for m in reversed(modules):
        if hasattr(m, "unregister"):
            m.unregister()
