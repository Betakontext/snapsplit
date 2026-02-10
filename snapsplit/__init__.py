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
