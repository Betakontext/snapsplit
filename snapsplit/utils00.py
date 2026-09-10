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
import bpy
from mathutils import Vector

def ensure_collection(name):
    """Ensure a collection with the given name exists; create and link it if missing."""
    coll = bpy.data.collections.get(name)
    if not coll:
        coll = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(coll)
    return coll

def link_to_collection(obj, coll):
    """Unlink object from its collections (safe) and link it to the target collection."""
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
    """Return (min, max) of the object's world-space axis-aligned bounding box."""
    mat = obj.matrix_world
    coords = [mat @ Vector(corner) for corner in obj.bound_box]
    min_v = Vector((min(c.x for c in coords), min(c.y for c in coords), min(c.z for c in coords)))
    max_v = Vector((max(c.x for c in coords), max(c.y for c in coords), max(c.z for c in coords)))
    return min_v, max_v

# Units: keep compatibility with the working scene
def unit_mm():
    """Return the scene units per millimeter (1.0 for mm scenes, 0.001 for meter-based scenes)."""
    us = bpy.context.scene.unit_settings
    if (us.system == 'METRIC'
        and getattr(us, "length_unit", "MILLIMETERS") == 'MILLIMETERS'
        and abs(us.scale_length - 1.0) < 1e-9):
            return 1.0
    return 0.001

def mm_to_scene(mm_value: float) -> float:
    """Convert a length in millimeters to scene units, honoring metric settings."""
    us = bpy.context.scene.unit_settings
    if (us.system == 'METRIC'
        and getattr(us, "length_unit", "MILLIMETERS") == 'MILLIMETERS'
        and abs(us.scale_length - 1.0) < 1e-9):
        return float(mm_value)
    return float(mm_value) * 0.001

def scene_to_mm(scene_value: float) -> float:
    """Convert a length in scene units to millimeters, honoring metric settings."""
    us = bpy.context.scene.unit_settings
    if (us.system == 'METRIC'
        and getattr(us, "length_unit", "MILLIMETERS") == 'MILLIMETERS'
        and abs(us.scale_length - 1.0) < 1e-9):
        return float(scene_value)
    return float(scene_value) / 0.001

# Localization helpers — explicitly use current_language()
def current_language():
    """Return Blender UI language like 'en_US', 'de_DE'; fallback to 'en_US' on failure."""
    try:
        lang = bpy.context.preferences.view.language or ""
        return lang or "en_US"
    except Exception:
        return "en_US"

def is_lang_de():
    """Return True if the current UI language starts with 'de' (German)."""
    try:
        return current_language().lower().startswith("de")
    except Exception:
        return False

def report_user(self, level, msg_en, msg_de=None):
    """Report a localized message to the user, falling back to English; also print to console."""
    text = msg_de if (msg_de and is_lang_de()) else msg_en
    if hasattr(self, "report"):
        try:
            self.report({level}, text)
        except Exception:
            pass
    print(f"[SnapSplit][{level}] {text}")

def register():
    """Required add-on hook (no-op for utilities)."""
    pass

def unregister():
    """Required add-on hook (no-op for utilities)."""
    pass
