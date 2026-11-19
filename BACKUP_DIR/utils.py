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

# utils.py

import bpy
from mathutils import Vector


# ---------------------------
# Collections / objects
# ---------------------------

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


# ---------------------------
# Units: keep compatibility with the working scene
# ---------------------------

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


# ---------------------------
# Modifier handling
# ---------------------------

def apply_modifier_data(obj, mod):
    """Apply ONE modifier to obj's mesh without bpy.ops.object.modifier_apply.

    The stack is evaluated with only this modifier enabled, the evaluated mesh replaces
    obj.data and the modifier is removed. Other modifiers keep their state.
    Raises RuntimeError on failure so the caller's existing try/except can report it;
    on failure the object is left as it was (the modifier stays on the stack).
    """
    if obj is None or obj.type != 'MESH' or obj.data is None:
        raise RuntimeError("apply_modifier_data: object is not a mesh")
    mod_name = mod.name
    if obj.modifiers.get(mod_name) is None:
        raise RuntimeError(f"modifier '{mod_name}' not found on '{obj.name}'")

    # Shared mesh data would change other users too: give this object its own copy
    if obj.data.users > 1:
        obj.data = obj.data.copy()

    # Evaluate with ONLY this modifier enabled; restore the other flags in any case
    saved = [(m.name, m.show_viewport) for m in obj.modifiers]
    new_mesh = None
    try:
        for m in obj.modifiers:
            m.show_viewport = (m.name == mod_name)
        depsgraph = bpy.context.evaluated_depsgraph_get()
        obj_eval = obj.evaluated_get(depsgraph)
        new_mesh = bpy.data.meshes.new_from_object(
            obj_eval, preserve_all_data_layers=True, depsgraph=depsgraph)
    finally:
        for name, visible in saved:
            m = obj.modifiers.get(name)
            if m is not None:
                m.show_viewport = visible

    if new_mesh is None:
        raise RuntimeError(f"modifier '{mod_name}' produced no mesh")

    # Swap the mesh, drop the modifier, keep the old data-block name
    old_mesh = obj.data
    old_name = old_mesh.name
    obj.data = new_mesh
    obj.modifiers.remove(obj.modifiers.get(mod_name))
    if old_mesh.users == 0:
        bpy.data.meshes.remove(old_mesh)
        new_mesh.name = old_name


# ---------------------------
# Localization (Blender-native)
# ---------------------------
# The English text is the lookup key. Static labels (bl_label, name=, description=,
# layout.label(text="...")) are translated by Blender itself via the dictionary that
# __init__.py registers from localization.py. The helpers below are only needed for
# strings that contain {placeholders}, because Blender cannot translate a string
# after it has been formatted.

def _translate(kind: str, msgid: str) -> str:
    """Translate 'msgid' with the pgettext variant for 'kind' ('iface' or 'rpt').

    Returns 'msgid' unchanged if translation support is missing or anything fails.
    """
    try:
        trans = bpy.app.translations
        func = trans.pgettext_rpt if kind == "rpt" else trans.pgettext_iface
        return func(msgid)
    except Exception:
        return msgid


def _format_safe(translated: str, template: str, fmt: dict) -> str:
    """Fill {placeholders} of a translated text; fall back to the English template.

    A translation with a missing or broken placeholder must never raise an error
    or show raw braces to the user.
    """
    try:
        return translated.format(**fmt)
    except (KeyError, IndexError, ValueError):
        try:
            return template.format(**fmt)
        except (KeyError, IndexError, ValueError):
            return translated


def _trf(msgid, default=None, /, **fmt) -> str:
    """Translate an English TEMPLATE for UI text and fill its placeholders.

    New style: _trf("Created {count} parts.", count=n)
    Old style (transitional): _trf("some.key", "Created {count} parts.", count=n)
    In the old style the key is ignored and 'default' is used as the template.
    Both parameters are positional-only, so placeholders may use any name.
    """
    template = str(default if default is not None else msgid)
    return _format_safe(_translate("iface", template), template, fmt)



def tr(key, default=""):
    """DEPRECATED compatibility shim for the old key-based tr().

    Translates the English 'default' (or the key if no default is given) through
    Blender's dictionary. Remove it once no module calls tr() anymore.
    """
    return _translate("iface", default or key)


def current_language():
    """Return the active Blender UI locale like 'en_US' or 'de_DE'; 'en_US' as fallback."""
    try:
        return bpy.app.translations.locale or "en_US"
    except Exception:
        return "en_US"


def is_lang_de():
    """Return True if the current UI language starts with 'de' (German)."""
    try:
        return current_language().lower().startswith("de")
    except Exception:
        return False


def report_user(self, level, msg, *_legacy, **fmt):
    """Report a message to the user and print it to the console.

    'msg' is an English text or an English template with {placeholders}.
    It is translated with the 'reports' variant of Blender's translation lookup.
    Placeholders are only filled when keyword arguments are given, e.g.:
        report_user(self, 'ERROR', "Modal error: {error}", error=e)

    Extra positional arguments (the removed 'msg_de' parameter) are ignored so that
    leftover old calls keep working.
    """
    template = str(msg)
    text = _translate("rpt", template)
    if fmt:
        text = _format_safe(text, template, fmt)

    if hasattr(self, "report"):
        try:
            self.report({level}, text)
        except Exception:
            pass
    print(f"[SnapSplit][{level}] {text}")


# ---------------------------
# Viewport X-Ray management (reference counted per 3D viewport)
# ---------------------------

# Maps a viewport key (SpaceView3D pointer) to its saved state:
#   {"attr": "show_xray" | "show_xray_wireframe", "saved": bool, "reasons": set of str}
# Several previews can be active at once; X-Ray is only restored when the last one ends.
_XRAY_STATES = {}


def _xray_attr_for_space(space):
    """Return the X-Ray property name valid for the viewport's shading mode, or None."""
    shading_type = space.shading.type
    if shading_type == 'SOLID':
        return "show_xray"
    if shading_type == 'WIREFRAME':
        return "show_xray_wireframe"
    # Material Preview / Rendered have no X-Ray, nothing is hidden there anyway
    return None


def _xray_find_view3d_space(context):
    """Find the 3D viewport the user is working in (context first, then the window's screen)."""
    try:
        space = getattr(context, "space_data", None)
        if space is not None and getattr(space, "type", "") == 'VIEW_3D':
            return space
    except Exception:
        pass
    try:
        area = getattr(context, "area", None)
        if area is not None and area.type == 'VIEW_3D':
            return area.spaces.active
    except Exception:
        pass
    try:
        window = getattr(context, "window", None) or bpy.context.window
        screen = getattr(window, "screen", None)
        if screen is not None:
            for area in screen.areas:
                if area.type == 'VIEW_3D':
                    return area.spaces.active
    except Exception:
        pass
    return None


def _xray_space_from_key(key):
    """Find a live SpaceView3D by its pointer key; return None if it no longer exists."""
    try:
        for window in bpy.context.window_manager.windows:
            for area in window.screen.areas:
                if area.type != 'VIEW_3D':
                    continue
                for sp in area.spaces:
                    if sp.type == 'VIEW_3D' and sp.as_pointer() == key:
                        return sp
    except Exception:
        pass
    return None


def xray_acquire(context, reason):
    """Switch X-Ray on in the clicked 3D viewport and remember its previous state.

    'reason' identifies the preview that needs X-Ray (e.g. "split_preview").
    The previous state is stored once per viewport, so it is never overwritten by
    a second preview. Returns True if X-Ray is active for this reason.
    """
    try:
        space = _xray_find_view3d_space(context)
        if space is None:
            return False
        attr = _xray_attr_for_space(space)
        if attr is None:
            return False

        key = space.as_pointer()
        state = _XRAY_STATES.get(key)
        if state is not None and state["attr"] != attr:
            # Shading mode changed since the first acquire: restore the old property first
            try:
                setattr(space.shading, state["attr"], state["saved"])
            except Exception:
                pass
            state = None
        if state is None:
            state = {"attr": attr, "saved": bool(getattr(space.shading, attr)), "reasons": set()}
            _XRAY_STATES[key] = state

        state["reasons"].add(reason)
        # Set it again every time, in case it was switched off by hand in the meantime
        setattr(space.shading, attr, True)
        return True
    except Exception as ex:
        print(f"[SnapSplit] X-Ray acquire failed: {ex}")
        return False


def xray_release(reason=None):
    """Drop one reason for X-Ray; restore the saved state when no reason is left.

    reason=None drops all reasons (used on unregister). Safe to call at any time,
    it does nothing if the reason is not active.
    """
    try:
        for key in list(_XRAY_STATES.keys()):
            state = _XRAY_STATES[key]
            if reason is None:
                state["reasons"].clear()
            elif reason in state["reasons"]:
                state["reasons"].discard(reason)
            else:
                continue
            if state["reasons"]:
                continue  # another preview still needs X-Ray
            space = _xray_space_from_key(key)
            if space is not None:
                try:
                    setattr(space.shading, state["attr"], state["saved"])
                except Exception:
                    pass
            del _XRAY_STATES[key]
    except Exception as ex:
        print(f"[SnapSplit] X-Ray release failed: {ex}")



# ---------------------------
# Add-on hooks
# ---------------------------

def register():
    """Required add-on hook (no-op for utilities)."""
    pass


def unregister():
    """Required add-on hook (no-op for utilities)."""
    pass

