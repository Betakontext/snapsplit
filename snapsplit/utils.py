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


import bpy
from mathutils import Vector

def ensure_collection(name):
    coll = bpy.data.collections.get(name)
    if not coll:
        coll = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(coll)
    return coll

def link_to_collection(obj, coll):
    # unlink from all top-level collections (safe), then link to target
    for c in obj.users_collection:
        c.objects.unlink(obj)
    coll.objects.link(obj)

def obj_world_bb(obj):
    # World-space bounding box min/max
    mat = obj.matrix_world
    coords = [mat @ Vector(corner) for corner in obj.bound_box]
    min_v = Vector((min(c.x for c in coords), min(c.y for c in coords), min(c.z for c in coords)))
    max_v = Vector((max(c.x for c in coords), max(c.y for c in coords), max(c.z for c in coords)))
    return min_v, max_v

def unit_mm():
    # Returns scale factor to convert mm -> meters (Blender units)
    # Blender default unit scale is meters. 1 mm = 0.001 m.
    return 0.001

def report_user(self, level, msg):
    if hasattr(self, "report"):
        self.report({level}, msg)
    print(f"[SnapSplit][{level}] {msg}")

def register():
    pass

def unregister():
    pass

