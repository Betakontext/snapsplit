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
        try:
            c.objects.unlink(obj)
        except Exception:
            pass
    try:
        coll.objects.link(obj)
    except Exception:
        pass

def obj_world_bb(obj):
    # World-space bounding box min/max
    mat = obj.matrix_world
    coords = [mat @ Vector(corner) for corner in obj.bound_box]
    min_v = Vector((min(c.x for c in coords), min(c.y for c in coords), min(c.z for c in coords)))
    max_v = Vector((max(c.x for c in coords), max(c.y for c in coords), max(c.z for c in coords)))
    return min_v, max_v

# Units: keep compatibility with your working scene
def unit_mm():
    """
    Return how many scene units correspond to 1 mm.
    - Millimeters + Unit Scale 1.0: 1.0 (1 BU = 1 mm)
    - Otherwise (meter-based): 0.001 (1 mm = 0.001 m)
    """
    us = bpy.context.scene.unit_settings
    if (us.system == 'METRIC'
        and getattr(us, "length_unit", "MILLIMETERS") == 'MILLIMETERS'
        and abs(us.scale_length - 1.0) < 1e-9):
            return 1.0
    return 0.001

def mm_to_scene(mm_value: float) -> float:
    """
    Helper for UI conversions; we do NOT replace existing unit_mm() usages
    in core logic to keep your working behavior unchanged.
    """
    us = bpy.context.scene.unit_settings
    if (us.system == 'METRIC'
        and getattr(us, "length_unit", "MILLIMETERS") == 'MILLIMETERS'
        and abs(us.scale_length - 1.0) < 1e-9):
        return float(mm_value)
    return float(mm_value) * 0.001

def scene_to_mm(scene_value: float) -> float:
    us = bpy.context.scene.unit_settings
    if (us.system == 'METRIC'
        and getattr(us, "length_unit", "MILLIMETERS") == 'MILLIMETERS'
        and abs(us.scale_length - 1.0) < 1e-9):
        return float(scene_value)
    return float(scene_value) / 0.001

# Localization helpers — explicitly use current_language()
def current_language():
    """
    Return Blender UI language like 'en_US', 'de_DE', etc.
    Falls back to 'en_US' if unavailable.
    """
    try:
        lang = bpy.context.preferences.view.language or ""
        return lang or "en_US"
    except Exception:
        return "en_US"

def is_lang_de():
    """Convenience: True if current UI language is German (starts with 'de')."""
    try:
        return current_language().lower().startswith("de")
    except Exception:
        return False

def report_user(self, level, msg_en, msg_de=None):
    """
    Localized reporting. If German UI and msg_de provided -> use it; else msg_en.
    Only affects text; does not change logic.
    """
    text = msg_de if (msg_de and is_lang_de()) else msg_en
    if hasattr(self, "report"):
        try:
            self.report({level}, text)
        except Exception:
            pass
    print(f"[SnapSplit][{level}] {text}")

def register():
    pass

def unregister():
    pass


