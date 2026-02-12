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

# ---------------------------
# Localization / language
# ---------------------------

def current_language():
    """
    Return Blender UI language as a BCP-47-like code (e.g., 'en_US', 'de_DE').
    If Blender language is 'Automatic', derive from system language.
    """
    prefs = bpy.context.preferences
    intl = prefs.view
    # Blender 3.x/4.x exposes language in preferences as a code like 'en_US'
    lang = getattr(intl, "language", "") or ""
    if lang.lower() in {"default", "automatic", ""}:
        # Try system language setting exposed by Blender
        lang = getattr(intl, "language_flag", "") or "en_US"
    return lang or "en_US"

def is_lang_de():
    """Convenience: True if UI language is German."""
    return current_language().lower().startswith(("de", "de_de"))

# ---------------------------
# Collections
# ---------------------------

def ensure_collection(name: str):
    """
    Ensure a collection of given name exists and is linked to the scene.
    Returns the collection.
    """
    coll = bpy.data.collections.get(name)
    if not coll:
        coll = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(coll)
    return coll

def link_to_collection(obj, coll):
    """
    Unlink obj from all current collections and link it to the provided collection.
    Safe for typical add-on workflows.
    """
    for c in list(obj.users_collection):
        try:
            c.objects.unlink(obj)
        except Exception:
            pass
    try:
        coll.objects.link(obj)
    except Exception:
        pass

# ---------------------------
# Bounding boxes
# ---------------------------

def obj_world_bb(obj):
    """
    World-space bounding box of an object.
    Returns (min_vec, max_vec).
    """
    mat = obj.matrix_world
    coords = [mat @ Vector(corner) for corner in obj.bound_box]
    min_v = Vector((
        min(c.x for c in coords),
        min(c.y for c in coords),
        min(c.z for c in coords),
    ))
    max_v = Vector((
        max(c.x for c in coords),
        max(c.y for c in coords),
        max(c.z for c in coords),
    ))
    return min_v, max_v

# ---------------------------
# Units: adaptive mm <-> scene
# ---------------------------

def unit_mm():
    """
    Legacy helper: how many scene units correspond to 1 mm.
    - Millimeters + Unit Scale 1.0 -> 1.0 (1 BU = 1 mm)
    - Otherwise (meter-based)      -> 0.001 (1 mm = 0.001 m)
    Prefer using mm_to_scene/scene_to_mm in new code.
    """
    us = bpy.context.scene.unit_settings
    if (us.system == 'METRIC'
        and getattr(us, "length_unit", "MILLIMETERS") == 'MILLIMETERS'
        and abs(us.scale_length - 1.0) < 1e-9):
        return 1.0
    return 0.001

def mm_to_scene(mm_value: float) -> float:
    """
    Convert millimeters to scene units robustly.
    - If scene is Metric, Length=Millimeters, Unit Scale=1.0: 1 BU = 1 mm
    - Else (e.g., meter-based): 1 mm = 0.001 m
    """
    us = bpy.context.scene.unit_settings
    if (us.system == 'METRIC'
        and getattr(us, "length_unit", "MILLIMETERS") == 'MILLIMETERS'
        and abs(us.scale_length - 1.0) < 1e-9):
        return float(mm_value)
    return float(mm_value) * 0.001

def scene_to_mm(scene_value: float) -> float:
    """
    Convert scene units back to millimeters (inverse of mm_to_scene for common setups).
    """
    us = bpy.context.scene.unit_settings
    if (us.system == 'METRIC'
        and getattr(us, "length_unit", "MILLIMETERS") == 'MILLIMETERS'
        and abs(us.scale_length - 1.0) < 1e-9):
        return float(scene_value)
    return float(scene_value) / 0.001

# ---------------------------
# Reporting
# ---------------------------

def report_user(self, level: str, msg_en: str, msg_de: str = None):
    """
    Report to Blender UI and console. If a German UI is detected and msg_de is provided,
    it will be used; otherwise msg_en is used.
    level: 'INFO' | 'WARNING' | 'ERROR'
    """
    text = (msg_de if (msg_de and is_lang_de()) else msg_en) or ""
    if hasattr(self, "report"):
        try:
            self.report({level}, text)
        except Exception:
            pass
    print(f"[SnapSplit][{level}] {text}")

# ---------------------------
# Misc robustness helpers
# ---------------------------

def apply_scale_if_needed(obj, apply_location=False, apply_rotation=False, apply_scale=True):
    """
    Apply transforms on an object if needed (primarily scale) to stabilize booleans.
    """
    if not obj:
        return
    sx, sy, sz = obj.scale
    need_scale = apply_scale and (abs(sx - 1.0) > 1e-6 or abs(sy - 1.0) > 1e-6 or abs(sz - 1.0) > 1e-6)
    if not (need_scale or apply_rotation or apply_location):
        return
    try:
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)
        bpy.ops.object.transform_apply(
            location=apply_location,
            rotation=apply_rotation,
            scale=apply_scale
        )
    except Exception:
        pass
    finally:
        try:
            obj.select_set(False)
        except Exception:
            pass

def validate_mesh(obj):
    """Validate and update mesh data safely."""
    try:
        obj.data.validate(verbose=False)
        obj.data.update()
    except Exception:
        pass

# ---------------------------
# Add-on register hooks
# ---------------------------

def register():
    # Nothing to register in utils
    pass

def unregister():
    # Nothing to unregister in utils
    pass

