"""
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
"""

# ops_split.py

import bpy
import bmesh
from bpy.types import Operator
from bpy.app.handlers import persistent
from mathutils import Vector, Matrix
from datetime import datetime

from .utils import (
    ensure_collection,
    report_user,
    is_lang_de,
    unit_mm,
)

from .utils import _trf

# ---------------------------
# Preview naming
# ---------------------------

PREVIEW_COLL_NAME = "_SnapSplit_Preview"
PREVIEW_PLANE_PREFIX = "_SnapSplit_PreviewPlane_"
PREVIEW_MAT_NAME = "_SnapSplit_Preview_MAT"

# ---------------------------
# bpy.ops fallback policy (documented for Extensions review)
# ---------------------------
# Blender's own "Select Edge Loop" walker (bpy.ops.mesh.loop_multi_select) is
# implemented in C and has no 1:1 public Python/BMesh equivalent.
# SnapSplit therefore first tries a conservative pure-BMesh loop walker
# (_walk_edge_loop_closed) that only accepts results which form a CLOSED cycle.
# Only if the walker cannot prove a closed cycle (e.g. n-gon stars, triangle
# fans, non-manifold pinch points) we fall back to the operator for exactly
# this single special case. Set to False to disable the fallback entirely.
_ALLOW_OPS_LOOP_FALLBACK = True

# ---------------------------
# Helpers: AABB / axes / eps / context / normals
# ---------------------------

def axis_index_for(axis):
    """Return axis index 0/1/2 for axis string X/Y/Z."""
    return {"X": 0, "Y": 1, "Z": 2}[axis]

def world_aabb(obj):
    """Return world-space axis-aligned bounding-box (min,max) for object."""
    corners = [obj.matrix_world @ Vector(c) for c in obj.bound_box]
    min_v = Vector((min(v.x for v in corners), min(v.y for v in corners), min(v.z for v in corners)))
    max_v = Vector((max(v.x for v in corners), max(v.y for v in corners), max(v.z for v in corners)))
    return min_v, max_v

def aabb_center(min_v, max_v):
    """Return center point of an AABB defined by min_v and max_v."""
    return 0.5 * (min_v + max_v)

def world_pos_from_norm(obj, axis, t_norm):
    """Map t_norm in [-1, 1] to a world position along the object's AABB on the given axis."""
    min_v, max_v = world_aabb(obj)
    ax = axis_index_for(axis)
    lo = min_v[ax]; hi = max_v[ax]
    mid = 0.5 * (lo + hi); half = 0.5 * (hi - lo)
    return mid + t_norm * half, (lo, hi, mid, half)

def size_on_tangential_axes(obj, axis):
    """Return lengths on the two tangential axes relative to the split axis."""
    min_v, max_v = world_aabb(obj)
    ax = axis_index_for(axis)
    t1 = (ax + 1) % 3; t2 = (ax + 2) % 3
    return (abs(max_v[t1] - min_v[t1]), abs(max_v[t2] - min_v[t2])), (t1, t2), (min_v, max_v)

def _diag_eps(obj, k=1e-6, min_eps=1e-6):
    """Return an epsilon scaled by the object's diagonal length (clamped by min_eps)."""
    min_v, max_v = world_aabb(obj)
    diag = (max_v - min_v).length
    return max(min_eps, diag * k)

def _ensure_object_mode():
    """Ensure Blender is in OBJECT mode (safe switch if needed)."""
    # NOTE: bpy.ops.object.mode_set has no public non-operator equivalent; kept on purpose.
    try:
        ob = bpy.context.object
        if ob and ob.mode != 'OBJECT':
            bpy.ops.object.mode_set(mode='OBJECT')
    except Exception:
        pass

def _deselect_all_objects():
    """Deselect all objects of the current view layer via RNA (replaces bpy.ops.object.select_all)."""
    try:
        view_layer = bpy.context.view_layer
        for o in list(view_layer.objects):
            try:
                # select_set() is a cheap RNA call; hidden objects may refuse it, which is fine
                o.select_set(False)
            except Exception:
                pass
    except Exception:
        pass

def _activate_single_object(obj):
    """Activate and exclusively select a single object."""
    _ensure_object_mode()
    _deselect_all_objects()
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj

def _enter_edit_mode_edges(obj):
    """Enter EDIT mode on obj and switch selection mode to EDGE."""
    _activate_single_object(obj)
    # Set the EDGE select mode through tool settings BEFORE entering Edit Mode.
    # The edit-mesh is created with this mode, so the operator
    # bpy.ops.mesh.select_mode(type='EDGE') is no longer needed.
    try:
        bpy.context.tool_settings.mesh_select_mode = (False, True, False)
    except Exception:
        pass
    # NOTE: bpy.ops.object.mode_set has no public non-operator equivalent; kept on purpose.
    bpy.ops.object.mode_set(mode='EDIT')

def _leave_edit_mode():
    """Leave EDIT mode if currently active."""
    try:
        if bpy.context.object and bpy.context.object.mode == 'EDIT':
            bpy.ops.object.mode_set(mode='OBJECT')
    except Exception:
        pass

def warn_if_unapplied_transforms(obj, operator=None):
    """Report a non-blocking info message if object has unapplied transforms that may affect splitting."""
    if not obj or obj.type != 'MESH':
        return
    try:
        loc = tuple(getattr(obj, "location", (0.0, 0.0, 0.0)))
        has_loc = any(abs(v) > 1e-7 for v in loc)

        has_rot = False
        rot_mode = getattr(obj, "rotation_mode", "QUATERNION")
        if rot_mode == 'QUATERNION':
            q = getattr(obj, "rotation_quaternion", None)
            if q is not None:
                has_rot = (abs(q.w - 1.0) > 1e-7) or (abs(q.x) > 1e-7) or (abs(q.y) > 1e-7) or (abs(q.z) > 1e-7)
        else:
            e = getattr(obj, "rotation_euler", None)
            if e is not None:
                has_rot = any(abs(a) > 1e-7 for a in (e.x, e.y, e.z))

        sx, sy, sz = getattr(obj, "scale", (1.0, 1.0, 1.0))
        non_uniform = (abs(sx - sy) > 1e-7) or (abs(sy - sz) > 1e-7) or (abs(sx - sz) > 1e-7)
        det = obj.matrix_world.to_3x3().determinant()
        negative_scale = det < 0.0

        if has_loc or has_rot or non_uniform or negative_scale:
            # Build bilingual message via translation keys
            details = []
            if has_loc: details.append('Location')
            if has_rot: details.append('Rotation')
            if non_uniform: details.append('Non-uniform Scale')
            if negative_scale: details.append('Negative Scale')
            details_str = ", ".join(details)

            msg = 'Object has unapplied transforms'
            hint = 'Consider Apply All Transforms (Ctrl+A) for exact and predictable split results.'
            msg_all = f"{msg}: {details_str}. {hint}"

            if operator is not None:
                report_user(operator, 'INFO', msg_all)
            else:
                print(f"[SnapSplit] {msg_all}")
    except Exception:
        pass

# ---------------------------
# Depsgraph handler
# ---------------------------

_last_preview_active_obj = None

# Separate, independent state for the connector live-preview branch below.
# Kept as a simple tuple signature of selected mesh object names so we can
# cheaply detect "selection changed" without depending on the split-preview
# state above. None means "not initialized yet" (forces an initial check).
_last_connector_preview_selection_key = None

@persistent  # survive file loads; lifetime is managed by sync_depsgraph_handler()
def _snapsplit_depsgraph_update(scene, depsgraph):
    """Depsgraph post-update handler to refresh preview planes/objects on relevant data changes.

    This handler drives two fully independent preview systems:
      1) The split-plane preview (unchanged, reacts to active-object changes
         and depsgraph updates on that object/its mesh data).
      2) The connector placement live preview (new), which reacts only to
         changes in the current selection set and is entirely gated by its
         own 'connector_live_preview' toggle. Neither branch's early-return
         affects the other, so turning off "Show split preview" no longer
         disables the connector live preview and vice versa.
    """
    global _last_preview_active_obj, _last_connector_preview_selection_key

    props = getattr(scene, "snapsplit", None)
    ctx = bpy.context

    # --- Branch 1: split-plane preview (unchanged behavior) ---
    if 'update_split_preview_plane' not in globals():
        pass
    elif not props or not getattr(props, "show_split_preview", False):
        _last_preview_active_obj = None
    else:
        obj = ctx.active_object

        if obj is not _last_preview_active_obj:
            try:
                update_split_preview_plane(ctx)
            except Exception:
                pass
            _last_preview_active_obj = obj
        elif obj:
            try:
                for up in depsgraph.updates:
                    id_orig = getattr(up.id, "original", None)
                    if id_orig is obj or id_orig is obj.data:
                        update_split_preview_plane(ctx)
                        break
            except Exception:
                pass

    # --- Branch 2: connector placement live preview (new, independent) ---
    if not props or not getattr(props, "connector_live_preview", False):
        # Reset the tracked selection so a fresh selection is always detected
        # once the toggle is switched back on.
        _last_connector_preview_selection_key = None
        return

    try:
        sel_key = tuple(sorted(o.name for o in ctx.selected_objects if o.type == 'MESH'))
    except Exception:
        sel_key = None

    if sel_key != _last_connector_preview_selection_key:
        _last_connector_preview_selection_key = sel_key
        try:
            from . import ops_connectors
            ops_connectors.update_connector_placement_preview(ctx)
        except Exception:
            pass

_DEPSGRAPH_HANDLER_NAME = "_snapsplit_depsgraph_update"
_LOAD_HANDLER_NAME = "_snapsplit_load_post"


def _find_handlers_named(handler_list, name):
    """Return all handlers in 'handler_list' with the given function name defined in THIS module.

    Matching by name + module (not by object identity) also catches stale function
    objects left over from importlib.reload() during development.
    """
    return [h for h in handler_list
            if getattr(h, "__name__", "") == name
            and getattr(h, "__module__", "") == __name__]


def _remove_handlers_named(handler_list, name):
    """Remove every SnapSplit handler called 'name' from 'handler_list'. Returns the count removed."""
    found = _find_handlers_named(handler_list, name)
    for h in found:
        try:
            handler_list.remove(h)
        except ValueError:
            pass
    return len(found)


def _any_live_preview_enabled():
    """Return True if any scene has the split preview or the connector live preview enabled."""
    try:
        for sc in bpy.data.scenes:
            p = getattr(sc, "snapsplit", None)
            if p and (getattr(p, "show_split_preview", False)
                      or getattr(p, "connector_live_preview", False)):
                return True
    except Exception:
        # bpy.data can be restricted while an add-on registers; treat as "nothing enabled".
        # The load_post handler (or the next toggle) re-syncs later.
        pass
    return False


def sync_depsgraph_handler():
    """Attach the depsgraph handler while a live preview is enabled, detach it otherwise.

    Called from the update callbacks of the two preview toggles, from the load_post
    handler and from register(). Cheap: it only scans the scenes for two booleans.
    """
    global _last_preview_active_obj, _last_connector_preview_selection_key

    handlers = bpy.app.handlers.depsgraph_update_post
    wanted = _any_live_preview_enabled()
    present = bool(_find_handlers_named(handlers, _DEPSGRAPH_HANDLER_NAME))

    if wanted and not present:
        handlers.append(_snapsplit_depsgraph_update)
    elif not wanted and present:
        _remove_handlers_named(handlers, _DEPSGRAPH_HANDLER_NAME)
        # Reset the change-tracking state so the next enable starts with a fresh initial check
        _last_preview_active_obj = None
        _last_connector_preview_selection_key = None


@persistent  # must outlive file loads, otherwise it would be removed right when it is needed
def _snapsplit_load_post(_filepath=None):
    """After a file load, re-sync the depsgraph handler with the preview toggles saved in the file.

    Property update callbacks do not fire when a .blend is loaded, so a file saved with
    a preview enabled would otherwise come back without a working handler.
    """
    try:
        sync_depsgraph_handler()
    except Exception as e:
        print(f"[SnapSplit] Could not sync depsgraph handler after load: {e}")

# ---------------------------
# Preview material/planes
# ---------------------------

def update_split_preview_plane(context):
    """Create/refresh or remove split preview planes when UI properties change."""
    try:
        scene = context.scene
        props = getattr(scene, "snapsplit", None)
        obj = context.active_object
        if not props:
            return

        show = bool(getattr(props, "show_split_preview", False))
        axis = getattr(props, "split_axis", "Z")
        parts_count = max(2, int(getattr(props, "parts_count", 2)))
        offset_scene = float(getattr(props, "split_offset_mm", 0.0)) * unit_mm()

        if show and obj and obj.type == 'MESH':
            # Build/refresh preview planes for the current active object
            position_preview_planes_for_object(context, obj, axis, parts_count, offset_scene, force_rebuild=True)
        else:
            # Turn off and clean up any preview planes
            _disable_split_preview_and_cleanup(context)
    except Exception:
        # Be robust against any context changes
        pass

def build_orange_preview_material():
    """Create or reuse the translucent orange preview material."""
    name = PREVIEW_MAT_NAME
    mat = bpy.data.materials.get(name)
    if mat: return mat
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nt = mat.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    out = nt.nodes.new("ShaderNodeOutputMaterial"); out.location = (200, 0)
    mix = nt.nodes.new("ShaderNodeMixShader"); mix.location = (0, 0)
    transp = nt.nodes.new("ShaderNodeBsdfTransparent"); transp.location = (-200, -100)
    emis = nt.nodes.new("ShaderNodeEmission"); emis.location = (-200, 100)
    emis.inputs["Color"].default_value = (1.0, 0.5, 0.0, 1.0)
    emis.inputs["Strength"].default_value = 3.0
    fac = nt.nodes.new("ShaderNodeValue"); fac.location = (-400, 0)
    fac.outputs[0].default_value = 0.3
    nt.links.new(fac.outputs[0], mix.inputs[0])
    nt.links.new(transp.outputs[0], mix.inputs[1])
    nt.links.new(emis.outputs[0], mix.inputs[2])
    nt.links.new(mix.outputs[0], out.inputs[0])
    mat.blend_method = 'BLEND'
    mat.shadow_method = 'NONE'
    mat.use_backface_culling = False
    return mat

def ensure_preview_collection():
    """Ensure the preview collection exists and return it."""
    coll = bpy.data.collections.get(PREVIEW_COLL_NAME)
    if coll is None:
        coll = bpy.data.collections.new(PREVIEW_COLL_NAME)
        bpy.context.scene.collection.children.link(coll)
    return coll

def create_or_get_preview_plane(context, obj, axis, name):
    """Create or fetch a named preview plane and ensure it has the preview material."""
    coll = ensure_preview_collection()
    plane = bpy.data.objects.get(name)
    if plane is None or plane.type != 'MESH':
        me = bpy.data.meshes.new(name)
        bm = bmesh.new()
        bmesh.ops.create_grid(bm, x_segments=1, y_segments=1, size=0.5)
        bm.to_mesh(me); bm.free()
        plane = bpy.data.objects.new(name, me)
        coll.objects.link(plane)

    mat = build_orange_preview_material()
    if not plane.data.materials:
        plane.data.materials.append(mat)
    else:
        plane.data.materials[0] = mat

    plane.hide_set(False)
    plane.hide_viewport = False
    plane.show_in_front = False
    plane.display_type = 'TEXTURED'
    plane.show_wire = True
    plane.show_all_edges = True
    plane.hide_select = True
    try: plane.color = (1.0, 0.1, 0.1, 1.0)
    except Exception: pass
    return plane

def preview_plane_name_for(obj_name: str, idx: int) -> str:
    """Return a unique preview plane name for an object and index."""
    return f"{PREVIEW_PLANE_PREFIX}{obj_name}_{idx}"

def preview_plane_names_for_object(obj_name: str, parts_count: int):
    """Return all expected preview plane names for an object given parts_count."""
    n = max(0, int(parts_count) - 1)
    return [preview_plane_name_for(obj_name, i+1) for i in range(n)]

def build_preview_matrix(obj, axis, pos):
    """Build a world matrix for a preview plane sized to object tangential extents at position pos."""
    (size_t1, size_t2), (t1_idx, t2_idx), (min_v, max_v) = size_on_tangential_axes(obj, axis)
    size_t1 = max(size_t1, 1e-9); size_t2 = max(size_t2, 1e-9)
    ax = axis_index_for(axis); c = aabb_center(min_v, max_v)
    world_axes = (Vector((1,0,0)), Vector((0,1,0)), Vector((0,0,1)))
    z_dir = world_axes[ax].copy().normalized()
    x_dir = world_axes[t1_idx].copy().normalized()
    if abs(z_dir.dot(x_dir)) > 0.999:
        x_dir = world_axes[(ax + 2) % 3].copy().normalized()
    y_dir = z_dir.cross(x_dir)
    if y_dir.length_squared == 0.0:
        x_dir = world_axes[(ax + 2) % 3].copy().normalized()
        y_dir = z_dir.cross(x_dir)
    y_dir.normalize(); x_dir = y_dir.cross(z_dir); x_dir.normalize()
    R = Matrix(((x_dir.x, y_dir.x, z_dir.x, 0.0),
                (x_dir.y, y_dir.y, z_dir.y, 0.0),
                (x_dir.z, y_dir.z, z_dir.z, 0.0),
                (0.0,     0.0,     0.0,     1.0)))
    S = Matrix.Diagonal(Vector((size_t1, size_t2, 1.0, 1.0)))
    tloc = Vector((c.x, c.y, c.z)); tloc[ax] = pos
    T = Matrix.Translation(tloc)
    return T @ R @ S

def position_preview_planes_for_object(context, obj, axis, parts_count, offset_scene, force_rebuild=False):
    """Create/update preview planes for an object based on axis, parts_count and offset."""
    if not obj or obj.type != 'MESH':
        return
    obj_name = obj.name
    min_v, max_v = world_aabb(obj)
    ax = axis_index_for(axis)
    length = max_v[ax] - min_v[ax]

    targets = []
    if length > 0.0 and parts_count >= 2:
        for i in range(1, parts_count):
            t = i / parts_count
            pos = min_v[ax] + t * length + offset_scene
            pos = max(min_v[ax], min(max_v[ax], pos))
            targets.append(pos)

    want_names = preview_plane_names_for_object(obj_name, parts_count)

    if force_rebuild:
        for o in [o for o in bpy.data.objects if o.name.startswith(f"{PREVIEW_PLANE_PREFIX}{obj_name}_")]:
            for coll in list(o.users_collection):
                try: coll.objects.unlink(o)
                except Exception: pass
            try: bpy.data.objects.remove(o)
            except Exception: pass

    for name, pos in zip(want_names, targets):
        plane = bpy.data.objects.get(name)
        if plane is None:
            plane = create_or_get_preview_plane(context, obj, axis, name)
        plane.matrix_world = build_preview_matrix(obj, axis, pos)
        plane.hide_set(False)
        plane.hide_viewport = False
        plane.display_type = 'TEXTURED'
        plane.show_wire = True
        plane.show_all_edges = True
        try: plane.color = (1.0, 0.1, 0.1, 1.0)
        except Exception: pass

    existing_scoped = [o for o in bpy.data.objects if o.name.startswith(f"{PREVIEW_PLANE_PREFIX}{obj_name}_")]
    for o in existing_scoped:
        if o.name not in want_names:
            for coll in list(o.users_collection):
                try: coll.objects.unlink(o)
                except Exception: pass
            try: bpy.data.objects.remove(o)
            except Exception: pass

    stray = [o for o in bpy.data.objects if o.name.startswith(PREVIEW_PLANE_PREFIX) and f"{obj_name}_" not in o.name]
    for o in stray:
        for coll in list(o.users_collection):
            try: coll.objects.unlink(o)
            except Exception: pass
        try:
            bpy.data.objects.remove(o)
        except Exception: pass

def _disable_split_preview_and_cleanup(context):
    """Disable the split preview toggle and remove all preview planes and empty collections."""
    # Give the viewport's X-Ray state back (no-op if the cut preview never switched it on)
    try:
        from .utils import xray_release
        xray_release("split_preview")
    except Exception:
        pass
    try:
        props = getattr(context.scene, "snapsplit", None)

        if props and getattr(props, "show_split_preview", False):
            props.show_split_preview = False
    except Exception:
        pass
    try:
        for o in [o for o in bpy.data.objects if o.name.startswith(PREVIEW_PLANE_PREFIX)]:
            for coll in list(o.users_collection):
                try: coll.objects.unlink(o)
                except Exception: pass
            try: bpy.data.objects.remove(o)
            except Exception: pass
    except Exception:
        pass
    try:
        pc = bpy.data.collections.get(PREVIEW_COLL_NAME)
        if pc and len(pc.objects) == 0:
            for sc in bpy.data.scenes:
                try:
                    if pc in sc.collection.children:
                        sc.collection.children.unlink(pc)
                except Exception:
                    pass
            try: bpy.data.collections.remove(pc)
            except Exception: pass
    except Exception:
        pass

# ---------------------------
# Job collection management (Parts / Helpers)
# ---------------------------

def _ensure_root_collection(name, hide=False):
    """Ensure a top-level root collection exists (optionally hidden in viewport)."""
    coll = bpy.data.collections.get(name)
    if coll is None:
        coll = bpy.data.collections.new(name)
        bpy.context.scene.collection.children.link(coll)
    # Best-effort: set viewport hidden state on the LayerCollection
    try:
        for sc in bpy.data.scenes:
            lay = sc.view_layers[0] if sc.view_layers else None
            if not lay:
                continue
            def _mark(layer_coll, target, hide_flag):
                if layer_coll.collection == target:
                    layer_coll.hide_viewport = hide_flag
                    return True
                for ch in layer_coll.children:
                    if _mark(ch, target, hide_flag):
                        return True
                return False
            _mark(lay.layer_collection, coll, hide)
    except Exception:
        pass
    return coll

def _ensure_job_collections(source_name):
    """Create per-job Parts and Helpers collections under SnapSplit_Parts and SnapSplit_Helpers roots."""
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    parts_root   = _ensure_root_collection("SnapSplit_Parts",   hide=False)
    helpers_root = _ensure_root_collection("SnapSplit_Helpers", hide=True)

    parts_job   = bpy.data.collections.new(f"{source_name}_{ts}")
    helpers_job = bpy.data.collections.new(f"{source_name}_{ts}")

    parts_root.children.link(parts_job)
    helpers_root.children.link(helpers_job)

    # Ensure visibility flags: parts visible, helpers hidden
    try:
        for sc in bpy.data.scenes:
            lay = sc.view_layers[0] if sc.view_layers else None
            if not lay:
                continue
            def _mark(layer_coll, target, hide_flag):
                if layer_coll.collection == target:
                    layer_coll.hide_viewport = hide_flag
                    return True
                for ch in layer_coll.children:
                    if _mark(ch, target, hide_flag):
                        return True
                return False
            _mark(lay.layer_collection, parts_job,   False)
            _mark(lay.layer_collection, helpers_job, True)
    except Exception:
        pass

    return parts_job, helpers_job

def _move_objs_to_collection(objs, target_coll, hide=True, unlink_first=True):
    """Move objects to target collection and set object viewport hidden if requested."""
    for o in list(objs):
        if not o or o.__class__.__name__ != "Object":
            continue
        if unlink_first:
            for c in list(o.users_collection):
                try: c.objects.unlink(o)
                except Exception: pass
        try:
            if target_coll not in o.users_collection:
                target_coll.objects.link(o)
        except Exception:
            pass
        try:
            o.hide_set(bool(hide))
        except Exception:
            pass

# ---------------------------
# Hollow Preparation (modifier or separate inner/outer object)
# ---------------------------

def _is_hollow_like_modifier(m):
    """Return True for modifiers considered 'hollow-like' (certain node groups or Solidify)."""
    n = (m.name or "").lower()
    # Treat nodes-based Hollow/Print3D by name
    if (m.type == 'NODES') and ("hollow" in n or "print3d" in n or "print 3d" in n):
        return True
    # Explicitly treat Solidify as hollow-like
    if m.type == 'SOLIDIFY':
        return True
    return False

def _try_apply_hollow_modifier(obj):
    """Attempt to apply all hollow-like modifiers on obj; return True if any was applied."""
    # Note: applying in reverse order to respect modifier stack
    mods = [m for m in obj.modifiers if _is_hollow_like_modifier(m)]
    ok_any = False
    for m in reversed(mods):
        ok_any |= _apply_modifier(obj, m)
    return ok_any

def _apply_modifier(obj, mod):
    """Apply a single modifier and report success."""
    _activate_single_object(obj)
    try:
        # Kept on purpose as bpy.ops: Hollow/Solidify/Geometry-Nodes results are not yet
        # verified with the data-based apply (see apply_modifier_data in utils.py).

        bpy.ops.object.modifier_apply(modifier=mod.name)
        return True
    except Exception as e:
        print(f"[SnapSplit] Apply modifier '{mod.name}' failed: {e}")
        return False

def _find_paired_inner_object_for(obj):
    """Heuristic to find inner/outer paired mesh: similar name, same location, similar AABB center, slightly smaller/larger."""
    base = obj.name.lower()
    min_v, max_v = world_aabb(obj)
    diag = (max_v - min_v).length
    cand = []
    for o in bpy.context.scene.objects:
        if o is obj or o.type != 'MESH':
            continue
        n = o.name.lower()
        if base in n or n.replace(" ", "").startswith(base.replace(" ", "")):
            min_i, max_i = world_aabb(o)
            diag_i = (max_i - min_i).length
            # inner: 0.2*diag < diag_i < 0.98*diag, outer possibly > 1.02*diag
            if (0.2 * diag < diag_i < 0.98 * diag) or (diag_i > 1.02 * diag):
                if (o.location - obj.location).length < max(1e-6, diag * 1e-4):
                    cand.append((abs(diag - diag_i), o))
    cand.sort(key=lambda t: t[0])
    return cand[0][1] if cand else None

def _join_objects_via_operator(main_obj, other_obj):
    """DOCUMENTED FALLBACK: join via bpy.ops.object.join (only used if the BMesh join fails)."""
    _activate_single_object(main_obj)
    other_obj.select_set(True)
    try:
        bpy.ops.object.join()
    except Exception as e:
        print(f"[SnapSplit] Join failed: {e}")
    return main_obj


def _join_objects(main_obj, other_obj):
    """Join other_obj into main_obj with BMesh (replaces object.join) and return main_obj.

    other_obj is transformed into the local space of main_obj, appended to its mesh and
    then removed from the file (like the operator does). Materials are merged by slot.
    On any error nothing is written and the operator fallback is used.
    """
    # Keep the side effect of the old code: main_obj ends up active and selected
    _activate_single_object(main_obj)

    if (other_obj is None or other_obj is main_obj
            or main_obj.type != 'MESH' or other_obj.type != 'MESH'):
        return main_obj

    tmp_mesh = None
    try:
        # BMesh I/O only works on Object Mode mesh data
        if main_obj.mode != 'OBJECT' or other_obj.mode != 'OBJECT':
            raise RuntimeError("objects must be in Object Mode")

        # Shared mesh data would change other users too: give main_obj its own copy
        if main_obj.data.users > 1:
            main_obj.data = main_obj.data.copy()

        # Map the material slots of other_obj onto main_obj (append missing ones)
        remap = {}
        main_mats = main_obj.data.materials
        for i, mat in enumerate(other_obj.data.materials):
            if mat is None:
                continue
            existing = [m for m in main_mats]
            if mat in existing:
                remap[i] = existing.index(mat)
            else:
                main_mats.append(mat)
                remap[i] = len(main_mats) - 1

        # Copy other_obj's mesh into main_obj's local space
        rel = main_obj.matrix_world.inverted() @ other_obj.matrix_world
        bm_other = bmesh.new()
        try:
            bm_other.from_mesh(other_obj.data)
            bmesh.ops.transform(bm_other, matrix=rel, verts=bm_other.verts)
            if rel.determinant() < 0.0:
                # Mirrored transform flips the winding: restore outward-facing faces
                bmesh.ops.reverse_faces(bm_other, faces=bm_other.faces[:])
            for f in bm_other.faces:
                f.material_index = remap.get(f.material_index, f.material_index)
            tmp_mesh = bpy.data.meshes.new("_SnapSplit_join_tmp")
            bm_other.to_mesh(tmp_mesh)
        finally:
            bm_other.free()

        # Append to main_obj's mesh (BMesh.from_mesh adds to existing geometry)
        bm = bmesh.new()
        try:
            bm.from_mesh(main_obj.data)
            bm.from_mesh(tmp_mesh)
            bm.to_mesh(main_obj.data)
        finally:
            bm.free()
        main_obj.data.update()

        # Remove the joined object and its orphaned mesh, like the operator does
        other_mesh = other_obj.data
        bpy.data.objects.remove(other_obj, do_unlink=True)
        if other_mesh is not None and other_mesh.users == 0:
            bpy.data.meshes.remove(other_mesh)
        return main_obj

    except Exception as e:
        print(f"[SnapSplit] BMesh join failed ({e}); falling back to bpy.ops.object.join")
        return _join_objects_via_operator(main_obj, other_obj)
    finally:
        if tmp_mesh is not None:
            try:
                bpy.data.meshes.remove(tmp_mesh)
            except Exception:
                pass


def _recalc_normals_outside(obj):
    """Recalculate face normals to point outward using BMesh only.

    Replaces the former sequence
        bpy.ops.mesh.select_all(action='SELECT') + bpy.ops.mesh.normals_make_consistent(inside=False)
    No Edit Mode round trip is needed. Works in OBJECT mode (mesh datablock is
    read into a temporary BMesh and written back) and, if the object happens to be
    in EDIT mode, directly on the edit BMesh.
    """
    if not obj or obj.type != 'MESH' or obj.data is None:
        return
    try:
        if obj.mode == 'EDIT':
            bm = bmesh.from_edit_mesh(obj.data)
            bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
            bmesh.update_edit_mesh(obj.data)
        else:
            bm = bmesh.new()
            try:
                bm.from_mesh(obj.data)
                bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
                bm.to_mesh(obj.data)
            finally:
                bm.free()
            obj.data.update()
    except Exception as ex:
        print(f"[SnapSplit DEBUG] _recalc_normals_outside failed on '{getattr(obj, 'name', '?')}': {ex}")

def robust_prepare_hollow(obj, operator=None):
    """Normalize 'hollow' preparation: apply hollow-like modifiers or join detected inner/outer shell; return (obj, used_hollow)."""
    if not obj or obj.type != 'MESH':
        return obj, False

    used_hollow = False

    applied = _try_apply_hollow_modifier(obj)
    if applied:
        used_hollow = True

    partner = _find_paired_inner_object_for(obj) if not applied else None
    if partner is not None:
        used_hollow = True
        obj = _join_objects(obj, partner)
        try:
            obj.data.validate(); obj.data.update()
        except Exception:
            pass
        _enter_edit_mode_edges(obj)
        bm = bmesh.from_edit_mesh(obj.data)
        try:
            bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=_diag_eps(obj, k=2e-6, min_eps=1e-6))
        except Exception:
            pass
        bmesh.update_edit_mesh(obj.data)
        _leave_edit_mode()

    _recalc_normals_outside(obj)
    return obj, used_hollow

# ---------------------------
# Cuts with global offset
# ---------------------------

def create_cut_data_with_offset(obj, axis, parts_count, global_offset_scene=0.0):
    """Create a list of (plane_point_world, plane_normal_world) cuts with an additional global offset."""
    min_v, max_v = world_aabb(obj)
    ax = axis_index_for(axis)
    length = max_v[ax] - min_v[ax]
    if length <= 0.0 or parts_count < 2:
        return []
    cuts = []
    for i in range(1, parts_count):
        t = i / parts_count
        pos = min_v[ax] + t * length + global_offset_scene
        pos = max(min_v[ax], min(max_v[ax], pos))
        if axis == "X":
            no_world = Vector((1, 0, 0)); co_world = Vector((pos, 0, 0))
        elif axis == "Y":
            no_world = Vector((0, 1, 0)); co_world = Vector((0, pos, 0))
        else:
            no_world = Vector((0, 0, 1)); co_world = Vector((0, 0, pos))
        cuts.append((co_world, no_world))
    return cuts

# ---------------------------
# Split (BMesh)
# ---------------------------

def _order_cycle_verts(loop_edges):
    """Return the vertices of a closed edge cycle in walking order, or None if it is not a simple cycle."""
    adj = {}
    for e in loop_edges:
        a, b = e.verts
        adj.setdefault(a, []).append(b)
        adj.setdefault(b, []).append(a)
    # A simple closed cycle has exactly two neighbours per vertex
    if not adj or any(len(n) != 2 for n in adj.values()):
        return None
    start = next(iter(adj))
    ordered = [start]
    prev, cur = None, start
    while True:
        n0, n1 = adj[cur]
        # NOTE: use == (not 'is'): BMesh Python wrappers are not guaranteed to be identical objects
        nxt = n0 if (prev is None or n0 != prev) else n1
        if nxt == start:
            break
        ordered.append(nxt)
        prev, cur = cur, nxt
        if len(ordered) > len(adj):
            return None
    return ordered if len(ordered) == len(adj) else None


def _poly_area_2d(pts):
    """Return the absolute area of a 2D polygon (shoelace formula)."""
    s = 0.0
    n = len(pts)
    for i in range(n):
        x0, y0 = pts[i]
        x1, y1 = pts[(i + 1) % n]
        s += x0 * y1 - x1 * y0
    return abs(s) * 0.5


def _point_in_poly_2d(pt, poly):
    """Return True if a 2D point lies inside a 2D polygon (ray casting)."""
    x, y = pt
    inside = False
    n = len(poly)
    j = n - 1
    for i in range(n):
        xi, yi = poly[i]
        xj, yj = poly[j]
        if (yi > y) != (yj > y):
            x_cross = (xj - xi) * (y - yi) / (yj - yi) + xi
            if x < x_cross:
                inside = not inside
        j = i
    return inside


def _group_loops_by_nesting(loops, ax):
    """Group closed loops of ONE cut plane into 'outer loop + its direct holes'.

    Loops are projected to 2D by dropping the split axis 'ax'. A loop is a hole
    when it is enclosed by an odd number of other loops, an outer boundary when
    enclosed by an even number (islands inside cavities are handled correctly).
    Returns a list of dicts {'edges', 'n_holes', 'expected_area'} or None when a
    loop cannot be ordered (caller then falls back to the legacy behaviour).
    """
    t1, t2 = (ax + 1) % 3, (ax + 2) % 3
    infos = []
    for lp in loops:
        ordered = _order_cycle_verts(lp)
        if ordered is None or len(ordered) < 3:
            return None
        pts = [(v.co[t1], v.co[t2]) for v in ordered]
        infos.append({'edges': lp, 'pts': pts, 'area': _poly_area_2d(pts)})

    n = len(infos)
    for j in range(n):
        containers = [i for i in range(n)
                      if i != j
                      and infos[i]['area'] > infos[j]['area']
                      and _point_in_poly_2d(infos[j]['pts'][0], infos[i]['pts'])]
        infos[j]['depth'] = len(containers)
        # Direct parent = smallest loop that still contains this one
        infos[j]['parent'] = min(containers, key=lambda i: infos[i]['area']) if containers else None

    groups = []
    for j, info in enumerate(infos):
        if info['depth'] % 2 != 0:
            continue  # holes are attached to their outer loop below
        holes = [k for k, o in enumerate(infos) if o['depth'] % 2 == 1 and o['parent'] == j]
        edges = list(info['edges'])
        for k in holes:
            edges += infos[k]['edges']
        expected = info['area'] - sum(infos[k]['area'] for k in holes)
        groups.append({'edges': edges, 'n_holes': len(holes), 'expected_area': expected})
        print(f"[SnapSplit DEBUG]   nesting: outer loop #{j} (area={info['area']:.5f}) "
              f"with {len(holes)} hole(s), expected cap area={expected:.5f}")
    return groups


def _fill_nested_group_bmesh(bm, edges, n_plane, n_holes, expected_area):
    """Fill 'outer loop + holes' and verify the result, leaving holes open.

    Tries several triangle_fill variants (the first mimics Mesh > Fill, which works
    in the manual 'Cap seams now' path). After each attempt the created face area is
    compared with the expected ring area; a cap that also covers a hole is deleted
    again. The last resort for exactly one hole is bridge_loops, which can never fill
    the hole. Returns True on success, False if the group was left open.
    """
    variants = (
        dict(use_beauty=True, use_dissolve=False),
        dict(use_beauty=True, use_dissolve=False, normal=n_plane),
        dict(use_beauty=True, use_dissolve=True, normal=n_plane),
    )
    for vi, kwargs in enumerate(variants):
        try:
            res = bmesh.ops.triangle_fill(bm, edges=edges, **kwargs)
        except Exception as ex:
            print(f"[SnapSplit DEBUG]     triangle_fill variant {vi} raised: {ex}")
            continue
        faces = [g for g in res.get('geom', []) if isinstance(g, bmesh.types.BMFace)]
        if not faces:
            print(f"[SnapSplit DEBUG]     triangle_fill variant {vi}: no faces created")
            continue
        area = sum(f.calc_area() for f in faces)
        if expected_area is None or abs(area - expected_area) <= max(0.02 * abs(expected_area), 1e-12):
            print(f"[SnapSplit DEBUG]     triangle_fill variant {vi} OK: {len(faces)} face(s), area={area:.5f}")
            return True
        print(f"[SnapSplit DEBUG]     triangle_fill variant {vi} REJECTED: area={area:.5f} "
              f"but expected {expected_area:.5f} (a hole was probably filled) -> removing faces")
        try:
            # context='FACES' also removes the diagonal edges created by the fill;
            # the loop edges survive because they still belong to the wall faces.
            bmesh.ops.delete(bm, geom=faces, context='FACES')
        except Exception as ex:
            print(f"[SnapSplit DEBUG]     could not remove rejected faces: {ex}")
            return False

    if n_holes == 1:
        try:
            res = bmesh.ops.bridge_loops(bm, edges=edges, use_pairs=False, use_cyclic=False,
                                         use_merge=False, merge_factor=0.5, twist_offset=0)
            if res.get('faces'):
                print(f"[SnapSplit DEBUG]     bridge_loops fallback OK: {len(res['faces'])} face(s)")
                return True
        except Exception as ex:
            print(f"[SnapSplit DEBUG]     bridge_loops fallback raised: {ex}")

    print("[SnapSplit][INFO]     group left OPEN (no fill variant produced a correct ring cap)")
    return False

def _fill_edges_bmesh(bm, edges, prefer_ngon=False, normal=None):
    """Fill the given boundary edges with BMesh only (replaces mesh.fill / fill_grid / edge_face_add).

    prefer_ngon=True : try contextual_create first (one N-gon, like edge_face_add),
                       then triangle_fill.
    prefer_ngon=False: triangle_fill only (what Mesh > Fill does; nested loops become
                       a ring with a hole).
    'normal' is an optional plane normal for a second triangle_fill attempt.
    Works on the given BMesh and ignores the selection. Returns True if a face was created.
    """
    edges = [e for e in edges if e.is_valid]
    if not edges:
        return False

    if prefer_ngon:
        try:
            res = bmesh.ops.contextual_create(bm, geom=edges)
            if [f for f in res.get('faces', []) if f.is_valid]:
                return True
        except Exception as ex:
            print(f"[SnapSplit DEBUG]   contextual_create raised: {ex}")

    variants = [dict(use_beauty=True, use_dissolve=False)]
    if normal is not None:
        variants.append(dict(use_beauty=True, use_dissolve=False, normal=normal))
    for kwargs in variants:
        try:
            res = bmesh.ops.triangle_fill(bm, edges=edges, **kwargs)
        except Exception as ex:
            print(f"[SnapSplit DEBUG]   triangle_fill raised: {ex}")
            continue
        if [g for g in res.get('geom', []) if isinstance(g, bmesh.types.BMFace)]:
            return True
    return False


def split_mesh_bmesh_into_two(source_obj, plane_co_obj, plane_no_obj, name_suffix="", do_fill=False):
    """Split a mesh into two halves by a plane in object space; optionally cap boundaries on each half."""
    _activate_single_object(source_obj)

    # Nudge the cutting plane by a tiny epsilon along its normal, BEFORE
    # bisecting, applied identically to both halves below. This resolves a
    # known bisect_plane degeneracy: if the requested plane coordinate
    # happens to pass EXACTLY through existing mesh vertices (e.g. a round
    # user-entered offset like 0 mm coinciding with Suzanne's own X=0
    # mirror-symmetry seam, or 400 mm coinciding by chance with an existing
    # cavity boundary edge loop), the resulting boundary can contain "pinch"
    # vertices where two otherwise-separate loops (outer silhouette and an
    # inner cavity/island contour) touch at exactly one point (degree 4
    # instead of 2). That breaks the strict-cycle assumption used by the
    # auto-cap loop detection, which either drops the affected loop entirely
    # or merges outer+inner into one loop that gets filled as a single solid
    # face -- sealing the whole cut plane shut. Nearby "non-round" offsets
    # (e.g. -10 mm, 350 mm) never hit this exact coincidence and therefore
    # worked correctly already. The nudge is far smaller than any meaningful
    # print tolerance, so it has no visible/dimensional effect.
    diag = max(source_obj.dimensions.length, 1e-6)
    eps_nudge = diag * 1e-5
    n_unit = plane_no_obj.normalized()
    plane_co_obj = plane_co_obj + n_unit * eps_nudge

    def make_half(keep_positive: bool):
        """Create one half (positive/negative side) of the split and return its Mesh datablock."""
        bm = bmesh.new()
        bm.from_mesh(source_obj.data)
        geom = bm.verts[:] + bm.edges[:] + bm.faces[:]
        bmesh.ops.bisect_plane(
            bm, geom=geom,
            plane_co=plane_co_obj, plane_no=plane_no_obj,
            use_snap_center=False,
            clear_outer=not keep_positive,
            clear_inner=keep_positive
        )
        if do_fill:
            boundary_edges = [e for e in bm.edges if e.is_boundary]
            if boundary_edges:
                try:
                    bmesh.ops.holes_fill(bm, edges=boundary_edges, sides=0)
                except Exception:
                    pass
        bm.normal_update()
        me = bpy.data.meshes.new(f"{source_obj.name}_{'POS' if keep_positive else 'NEG'}{name_suffix}")
        bm.to_mesh(me); bm.free()
        return me

    me_pos = make_half(True)
    me_neg = make_half(False)

    target_coll = source_obj.users_collection[0] if source_obj.users_collection else bpy.context.scene.collection
    o_pos = bpy.data.objects.new(f"{source_obj.name}_A{name_suffix}", me_pos)
    o_neg = bpy.data.objects.new(f"{source_obj.name}_B{name_suffix}", me_neg)
    target_coll.objects.link(o_pos); target_coll.objects.link(o_neg)
    o_pos.matrix_world = source_obj.matrix_world.copy()
    o_neg.matrix_world = source_obj.matrix_world.copy()
    source_obj.hide_set(True)

    for o in (o_pos, o_neg):
        try:
            o.data.validate(False); o.data.update()
        except Exception:
            pass

    return o_pos, o_neg

def apply_bmesh_split_sequence(root_obj, axis, parts_count, cuts_override=None, operator=None):
    """Apply a sequence of planar splits on root_obj and return the resulting parts."""
    cuts = cuts_override if cuts_override is not None else create_cut_data_with_offset(root_obj, axis, parts_count, 0.0)
    if not cuts:
        return [root_obj]

    wm = bpy.context.window_manager
    wm.progress_begin(0, len(cuts))
    try:
        current_parts = [root_obj]
        for idx, (co_world, no_world) in enumerate(cuts, start=1):
            next_parts = []
            for part in current_parts:
                if part is None or part.type != 'MESH' or part.data is None:
                    continue

                try:
                    warn_if_unapplied_transforms(part, operator=operator)
                except Exception:
                    pass

                M = part.matrix_world; M_inv = M.inverted()
                co_obj = M_inv @ co_world
                no_obj = (M_inv.to_3x3().transposed() @ no_world)
                if no_obj.length_squared == 0.0:
                    continue
                if M.to_3x3().determinant() < 0.0:
                    no_obj.negate()
                no_obj.normalize()

                a, b = split_mesh_bmesh_into_two(part, co_obj, no_obj, name_suffix=f"_S{idx}", do_fill=False)
                if a and a.type == 'MESH': next_parts.append(a)
                if b and b.type == 'MESH': next_parts.append(b)

            current_parts = [p for p in next_parts if p and p.type == 'MESH' and p.data]

            wm.progress_update(idx)
            # Ask every 3D View to redraw (replaces bpy.ops.wm.redraw_timer).
            # NOTE: tag_redraw() only schedules the redraw. While execute() is blocking,
            # Blender may not repaint until the operator returns.
            try:
                for win in wm.windows:
                    for area in win.screen.areas:
                        if area.type == 'VIEW_3D':
                            area.tag_redraw()
            except Exception:
                pass


        return [o for o in current_parts if o and o.type == 'MESH' and o.data and len(o.data.polygons) > 0]
    finally:
        wm.progress_end()

# ---------------------------
# Adjust split axis (modal preview)
# ---------------------------

class SNAP_OT_adjust_split_axis(Operator):
    """Interactively adjust split axis/offset with a live plane preview."""
    bl_idname = "snapsplit.adjust_split_axis"
    bl_label = "Adjust split axis"
    bl_options = {'REGISTER', 'UNDO', 'BLOCKING'}

    def invoke(self, context, event):
        """Start modal adjustment, initialize preview planes and internal state."""
        obj = context.active_object
        if not obj or obj.type != 'MESH':
            report_user(self, 'ERROR',
                        'Please select a mesh object.')
            return {'CANCELLED'}

        warn_if_unapplied_transforms(obj, operator=self)

        self.obj = obj
        self.props = context.scene.snapsplit
        self.axis = self.props.split_axis

        min_v, max_v = world_aabb(obj)
        ax = axis_index_for(self.axis)
        self.lo, self.hi = min_v[ax], max_v[ax]
        self.mid_world = 0.5 * (self.lo + self.hi)

        self.t_norm = 0.0
        try:
            offset_scene = float(getattr(self.props, "split_offset_mm", 0.0)) * unit_mm()
            half = 0.5 * (self.hi - self.lo)
            if half > 1e-12:
                self.t_norm = max(-1.0, min(1.0, offset_scene / half))
        except Exception:
            pass

        self.current_world_pos, _ = world_pos_from_norm(self.obj, self.axis, self.t_norm)

        parts_cnt = max(2, int(getattr(self.props, "parts_count", 2)))
        offset_scene = float(getattr(self.props, "split_offset_mm", 0.0)) * unit_mm()
        try:
            position_preview_planes_for_object(context, self.obj, self.axis, parts_cnt, offset_scene, force_rebuild=True)
        except Exception:
            pass

        lead_name = preview_plane_name_for(self.obj.name, 1)
        try:
            self.preview_plane = create_or_get_preview_plane(context, self.obj, self.axis, lead_name)
            self.preview_plane.matrix_world = build_preview_matrix(self.obj, self.axis, self.current_world_pos)
        except Exception:
            self.preview_plane = None

        self._area = context.area; self._region = context.region

        # Keep the preview planes visible inside solid objects while adjusting
        try:
            from .utils import xray_acquire
            xray_acquire(context, "adjust_axis")
        except Exception:
            pass


        context.window_manager.modal_handler_add(self)
        if self._area: self._area.tag_redraw()
        if self._region:
            try: self._region.tag_redraw()
            except Exception: pass

        return {'RUNNING_MODAL'}

    def finish(self, context, cancelled=False):
        """Stop modal mode, optionally remove preview planes and report status."""
        keep = False
        # Restore X-Ray (finish() is called on every exit path of the modal operator)
        try:
            from .utils import xray_release
            xray_release("adjust_axis")
        except Exception:
            pass

        try: keep = bool(getattr(context.scene.snapsplit, "show_split_preview", False))
        except Exception: pass
        if not keep:
            try:
                for o in [o for o in bpy.data.objects if o.name.startswith(PREVIEW_PLANE_PREFIX)]:
                    for coll in list(o.users_collection):
                        try: coll.objects.unlink(o)
                        except Exception: pass
                    try: bpy.data.objects.remove(o)
                    except Exception: pass
            except Exception: pass
            _disable_split_preview_and_cleanup(context)

        if self._area: self._area.tag_redraw()
        if self._region:
            try: self._region.tag_redraw()
            except Exception: pass

        msg_ok = 'Split axis adjusted.'
        msg_cancel = 'Adjust split axis cancelled.'
        report_user(self, 'INFO', msg_cancel if cancelled else msg_ok)

    def modal(self, context, event):
        """Handle mouse/keyboard events to adjust offset and update the preview."""
        if not self.obj or self.obj.name not in bpy.data.objects:
            self.finish(context, cancelled=True); return {'CANCELLED'}
        if event.type in {'ESC'}:
            self.finish(context, cancelled=True); return {'CANCELLED'}

        updated = False
        try:
            typed_mm = float(getattr(self.props, "split_offset_mm", 0.0))
            typed_scene = typed_mm * unit_mm()
            clamped_scene = max(self.lo - self.mid_world, min(self.hi - self.mid_world, typed_scene))
            half = 0.5 * (self.hi - self.lo) if (self.hi - self.lo) > 1e-12 else 1.0
            new_t = max(-1.0, min(1.0, clamped_scene / half))
            if abs(new_t - self.t_norm) > 1e-6:
                self.t_norm = new_t
                self.current_world_pos = self.mid_world + clamped_scene
                updated = True
        except Exception:
            pass

        if event.type in {'LEFTMOUSE', 'RET', 'NUMPAD_ENTER'} and event.value == 'PRESS':
            self.finish(context, cancelled=False); return {'FINISHED'}

        if event.type == 'MOUSEMOVE':
            dy = event.mouse_prev_y - event.mouse_y
            if dy != 0:
                self.t_norm = max(-1.0, min(1.0, self.t_norm - dy * 0.001))
                self.current_world_pos, _ = world_pos_from_norm(self.obj, self.axis, self.t_norm)
                scene_units_offset = self.current_world_pos - self.mid_world
                self.props.split_offset_mm = float(scene_units_offset) * (1.0 / unit_mm())
                updated = True

        step = 0.01
        if event.type in {'WHEELUPMOUSE', 'UP_ARROW'} and event.value == 'PRESS':
            self.t_norm = min(1.0, self.t_norm + step)
            self.current_world_pos, _ = world_pos_from_norm(self.obj, self.axis, self.t_norm)
            scene_units_offset = self.current_world_pos - self.mid_world
            self.props.split_offset_mm = float(scene_units_offset) * (1.0 / unit_mm())
            updated = True

        if event.type in {'WHEELDOWNMOUSE', 'DOWN_ARROW'} and event.value == 'PRESS':
            self.t_norm = max(-1.0, self.t_norm - step)
            self.current_world_pos, _ = world_pos_from_norm(self.obj, self.axis, self.t_norm)
            scene_units_offset = self.current_world_pos - self.mid_world
            self.props.split_offset_mm = float(scene_units_offset) * (1.0 / unit_mm())
            updated = True

        if updated:
            if getattr(self, "preview_plane", None):
                try: self.preview_plane.matrix_world = build_preview_matrix(self.obj, self.axis, self.current_world_pos)
                except ReferenceError: pass

            parts_cnt = max(2, int(getattr(self.props, "parts_count", 2)))
            offset_scene = float(getattr(self.props, "split_offset_mm", 0.0)) * unit_mm()
            try: position_preview_planes_for_object(context, self.obj, self.axis, parts_cnt, offset_scene)
            except Exception: pass

            try:
                if getattr(context.scene.snapsplit, "show_split_preview", False):
                    update_split_preview_plane(context)
            except Exception: pass

            if self._area: self._area.tag_redraw()
            if self._region:
                try: self._region.tag_redraw()
                except Exception: pass

        return {'RUNNING_MODAL'}

# ---------------------------
# Planar Split – prepare hollow, then split (+ optional auto-cap)
# ---------------------------

def _cap_single_object_simple_fill(obj) -> bool:
    """Fast legacy method: fill boundary loops using bmesh.ops.holes_fill."""
    try:
        me = obj.data
        bm = bmesh.new()
        bm.from_mesh(me)
        boundary_edges = [e for e in bm.edges if e.is_boundary]
        if boundary_edges:
            bmesh.ops.holes_fill(bm, edges=boundary_edges, sides=0)
            bm.normal_update()
            bm.to_mesh(me)
            me.update()
            bm.free()
            return True
        bm.free()
        return False
    except Exception:
        return False

def cap_single_object_hollow_style(obj) -> bool:
    """Cap boundary loops after Planar Split, correctly leaving cavities open.

    ARCHITECTURE CHANGE vs. previous session: instead of grouping raw
    boundary edges into position-based "cut-plane buckets" BEFORE trying to
    form loops (which fragments any boundary chain that drifts in position,
    e.g. an open mesh feature like Suzanne's un-capped nose hole, into many
    tiny non-cyclic buckets that get silently dropped), we now:

      1. Decompose ALL boundary edges into closed cycles and open chains
         GLOBALLY first (position-agnostic).
      2. Classify each closed cycle by its own planarity (max spread along
         the split axis). Planar cycles are real cut-plane loops and are
         kept. Non-planar cycles are closed rings that wander off the cut
         plane and back (e.g. a closed rim of a slanted pre-existing
         opening) and are explicitly excluded, with an INFO message instead
         of a silent drop.
      3. Open chains can never be filled (no closed loop exists), and are
         now explicitly reported via INFO instead of vanishing unnoticed
         inside the old per-bucket cycle decomposer. This is exactly the
         case of Suzanne's un-capped nose hole: its rim gets cut by the
         split into an open chain that is correctly left open, and the user
         now gets told why.
      4. Only the surviving planar closed loops are grouped into cut-plane
         buckets (by average position) for the existing single-loop /
         multi-loop (cavity ring) fill logic.

    Gap-stitching (bridging tiny EXACT-solver float gaps) now also runs
    ONCE globally instead of per tiny bucket, using bmesh.utils.edge_exists()
    (the correct API -- BMEdgeSeq has no .get() method).

    The whole body runs inside try/finally so _leave_edit_mode() is ALWAYS
    called, even on exception, to avoid corrupting the operator context for
    subsequent bpy.ops calls (previously observed crash in select_all).

    Step 1a/1b: the final select_all + normals_make_consistent operators were
    replaced by bmesh.ops.recalc_face_normals on the edit BMesh.
    """
    print(f"[SnapSplit DEBUG] ---- cap_single_object_hollow_style: {obj.name} ----")
    _enter_edit_mode_edges(obj)
    bm = bmesh.from_edit_mesh(obj.data)
    bm.verts.ensure_lookup_table(); bm.edges.ensure_lookup_table(); bm.faces.ensure_lookup_table()

    any_ok = False
    try:
        # Boundary vertex dedupe (unchanged from current version)
        boundary_verts = [v for v in bm.verts if any(e.is_boundary for e in v.link_edges)]
        print(f"[SnapSplit DEBUG] boundary verts before dedupe: {len(boundary_verts)}")
        if boundary_verts:
            try:
                dist = _diag_eps(obj, k=3e-6, min_eps=3e-7)
                bmesh.ops.remove_doubles(bm, verts=boundary_verts, dist=dist)
                bmesh.update_edit_mesh(obj.data)
                bm.verts.ensure_lookup_table(); bm.edges.ensure_lookup_table(); bm.faces.ensure_lookup_table()
                boundary_verts_after = [v for v in bm.verts if any(e.is_boundary for e in v.link_edges)]
                print(f"[SnapSplit DEBUG] boundary vertex dedupe: dist={dist:.6g}, "
                      f"boundary verts after={len(boundary_verts_after)}")
            except Exception as ex:
                print(f"[SnapSplit DEBUG] remove_doubles on boundary verts raised: {ex}")

        props = getattr(bpy.context.scene, "snapsplit", None)
        plane_axis = props.split_axis if props else "Z"

        ax = axis_index_for(plane_axis)
        axis_vecs = (Vector((1, 0, 0)), Vector((0, 1, 0)), Vector((0, 0, 1)))
        split_no = axis_vecs[ax].normalized()

        cand = [e for e in bm.edges if e.is_boundary]
        print(f"[SnapSplit DEBUG] total boundary edges (no direction filter): {len(cand)}")
        if not cand:
            print("[SnapSplit DEBUG] no candidate edges found -> abort")
            return False

        # ------------------------------------------------------------------
        # Global gap-stitching (runs ONCE over all boundary edges, not per
        # tiny position bucket -- avoids skewed min-edge-length thresholds).
        # ------------------------------------------------------------------
        def _stitch_dangling_endpoints_global(edges, bmesh_ref):
            """Bridge small gaps left by the EXACT boolean solver by
            connecting mutually-nearest dangling loop endpoints (odd-degree
            vertices) with new synthetic edges -- but only if the distance
            is small relative to the smallest existing boundary edge, so we
            never bridge a real, unrelated large gap (e.g. a pre-existing
            drain/access opening or an un-capped mesh feature like Suzanne's
            nose hole).
            """
            degree = {}
            for e in edges:
                for v in e.verts:
                    degree[v] = degree.get(v, 0) + 1
            dangling = [v for v, d in degree.items() if d % 2 == 1]
            print(f"[SnapSplit DEBUG]   dangling endpoints (global): {len(dangling)}")
            if len(dangling) < 2:
                return edges

            nearest = {}
            for v in dangling:
                best, bd = None, None
                for w in dangling:
                    if w is v:
                        continue
                    d = (v.co - w.co).length
                    if bd is None or d < bd:
                        bd, best = d, w
                nearest[v] = (best, bd)

            pairs, paired = [], set()
            for v in dangling:
                if v in paired:
                    continue
                w, d = nearest[v]
                if w is None or w in paired:
                    continue
                w_best, _ = nearest[w]
                if w_best is v:
                    pairs.append((v, w, d))
                    paired.add(v); paired.add(w)

            lens = [(e.verts[0].co - e.verts[1].co).length for e in edges]
            min_len = min(lens) if lens else 0.0
            max_stitch = max(min_len * 0.5, 1e-9)
            print(f"[SnapSplit DEBUG]   stitch safety threshold: {max_stitch:.6g} "
                  f"(global min boundary edge length: {min_len:.6g})")

            new_edges = list(edges)
            n_stitched = 0
            for v, w, d in pairs:
                ok = d <= max_stitch
                if ok:
                    existing = bmesh.utils.edge_exists(v, w)
                    new_e = existing if existing is not None else bmesh_ref.edges.new((v, w))
                    new_edges.append(new_e)
                    n_stitched += 1
            print(f"[SnapSplit DEBUG]   stitched {n_stitched} gap(s), "
                  f"rejected {len(pairs) - n_stitched} pair(s) as too far")
            bmesh_ref.edges.ensure_lookup_table()
            return new_edges

        cand = _stitch_dangling_endpoints_global(cand, bm)

        # ------------------------------------------------------------------
        # Global decomposition into closed cycles + open chains.
        # ------------------------------------------------------------------
        def _decompose_all_into_loops_and_chains_local(edges):
            """Split the full boundary edge set into closed cycles and open
            chains, globally (position-agnostic). Any connected chain that
            never closes back on itself (e.g. the rim of an un-capped mesh
            feature cut open by the split, such as Suzanne's nose hole) is
            returned separately as an "open chain" instead of being silently
            absorbed and lost, as the previous per-bucket decomposer did.
            """
            adj = {}
            remaining = set(edges)
            for e in edges:
                v0, v1 = e.verts
                adj.setdefault(v0, []).append((e, v1))
                adj.setdefault(v1, []).append((e, v0))

            def degree_in_remaining(v):
                return sum(1 for e, _ in adj.get(v, []) if e in remaining)

            # Step 1: peel off open chains starting at degree-1 vertices.
            open_chains = []
            while True:
                start_v = None
                for v in adj:
                    if degree_in_remaining(v) == 1:
                        start_v = v
                        break
                if start_v is None:
                    break
                chain_edges = []
                cur = start_v
                prev_edge = None
                while True:
                    nxt = None
                    for e, other in adj.get(cur, []):
                        if e in remaining and e is not prev_edge:
                            nxt = (e, other)
                            break
                    if nxt is None:
                        break
                    e, other = nxt
                    remaining.discard(e)
                    chain_edges.append(e)
                    prev_edge = e
                    cur = other
                    if degree_in_remaining(cur) != 2:
                        # Reached the opposite dangling end (or a branch
                        # point in degenerate non-manifold geometry) -> stop.
                        break
                if not chain_edges:
                    break
                open_chains.append(chain_edges)

            # Step 2: everything left should now form only closed cycles
            # (all remaining vertices have degree 2).
            cycles = []
            guard = 0
            max_guard = len(edges) * 4 + 16
            while remaining and guard < max_guard:
                guard += 1
                start_edge = next(iter(remaining))
                v0 = start_edge.verts[0]
                stack_v = [v0]
                stack_e = []
                cur = v0
                progressed = False
                while True:
                    nxt_edge = nxt_vert = None
                    for e, other in adj.get(cur, []):
                        if e in remaining:
                            nxt_edge, nxt_vert = e, other
                            break
                    if nxt_edge is None:
                        break
                    remaining.discard(nxt_edge)
                    progressed = True
                    if nxt_vert in stack_v:
                        idx = stack_v.index(nxt_vert)
                        cyc = stack_e[idx:] + [nxt_edge]
                        if len(cyc) >= 3:
                            cycles.append(cyc)
                        stack_v = stack_v[:idx + 1]
                        stack_e = stack_e[:idx]
                        cur = nxt_vert
                    else:
                        stack_v.append(nxt_vert)
                        stack_e.append(nxt_edge)
                        cur = nxt_vert
                if not progressed:
                    remaining.discard(start_edge)

            leftover = len(remaining)
            return cycles, open_chains, leftover

        def _loop_planar_extent_local(loop_edges, n_plane):
            """Return (extent, avg_coord) of a loop's spread along n_plane."""
            verts = set()
            for e in loop_edges:
                verts.add(e.verts[0]); verts.add(e.verts[1])
            vals = [v.co.dot(n_plane) for v in verts]
            return (max(vals) - min(vals)), (sum(vals) / len(vals))

        def _perimeter_local(loop_edges):
            p = 0.0
            for e in loop_edges:
                v0, v1 = e.verts
                p += (v0.co - v1.co).length
            return p


        n_plane = split_no
        eps_plane = _diag_eps(obj, k=5e-6, min_eps=5e-7)
        eps_plane_loop = _diag_eps(obj, k=8e-6, min_eps=8e-7)

        cycles, open_chains, leftover = _decompose_all_into_loops_and_chains_local(cand)
        print(f"[SnapSplit DEBUG] global decomposition: {len(cycles)} closed cycle(s), "
              f"{len(open_chains)} open chain(s), leftover edges={leftover}")
        if leftover:
            print(f"[SnapSplit DEBUG] WARNING: {leftover} boundary edge(s) could not be "
                  f"resolved into cycles or chains (decomposition guard limit hit)")

        # Open chains can never be capped (no closed loop exists) -- report
        # explicitly instead of letting them vanish silently. This is the
        # expected outcome for a mesh feature like Suzanne's nose hole that
        # the split plane happens to cut through.
        for ci, chain in enumerate(open_chains):
            verts = set()
            for e in chain:
                verts.add(e.verts[0]); verts.add(e.verts[1])
            ends = [v for v in verts if sum(1 for e in chain if v in e.verts) == 1]
            per = _perimeter_local(chain)
            print(f"[SnapSplit][INFO] open boundary chain #{ci}: {len(chain)} edge(s), "
                  f"length~{per:.4f} -- cannot form a closed loop, leaving open "
                  f"(likely rim of a pre-existing mesh opening, e.g. an un-capped "
                  f"nose hole or drain)")
            for v in ends:
                print(f"[SnapSplit][INFO]   chain endpoint at {tuple(round(c, 6) for c in v.co)}")

        # Classify closed cycles: planar (real cut-plane loop) vs. wandering
        # non-planar (closed ring that drifts off the cut plane, e.g. a
        # slanted rim of a wall opening) -- the latter is excluded from
        # capping with an explicit INFO message instead of a silent drop.
        planar_loops = []
        for cy in cycles:
            extent, avg_coord = _loop_planar_extent_local(cy, n_plane)
            per = _perimeter_local(cy)
            if extent <= eps_plane_loop:
                planar_loops.append({'edges': cy, 'coord': avg_coord})
                print(f"[SnapSplit DEBUG] closed cycle: {len(cy)} edge(s), perimeter={per:.4f}, "
                      f"extent along axis={extent:.6g} -> PLANAR, kept for capping")
            else:
                print(f"[SnapSplit][INFO] closed cycle: {len(cy)} edge(s), perimeter={per:.4f}, "
                      f"extent along axis={extent:.6g} (threshold={eps_plane_loop:.6g}) -> "
                      f"NON-PLANAR wandering ring, excluding from capping "
                      f"(likely rim of a pre-existing wall opening rather than the cut plane)")

        if not planar_loops:
            print("[SnapSplit DEBUG] no planar closed loops found -> nothing to cap")
            return False

        # Group surviving planar loops into cut-plane buckets by position,
        # for the existing single-loop / multi-loop (cavity ring) fill logic.
        planar_loops.sort(key=lambda d: d['coord'])
        buckets = []
        for pl in planar_loops:
            matched = False
            for b in buckets:
                if abs(pl['coord'] - b['v']) <= eps_plane:
                    b['loops'].append(pl['edges'])
                    b['v'] = (b['v'] * 0.9) + (pl['coord'] * 0.1)
                    matched = True
                    break
            if not matched:
                buckets.append({'v': pl['coord'], 'loops': [pl['edges']]})
        print(f"[SnapSplit DEBUG] {len(buckets)} cut-plane bucket(s) from planar loops "
              f"(eps_plane={eps_plane:.6g}):")
        for i, b in enumerate(buckets):
            print(f"[SnapSplit DEBUG]   bucket[{i}] coord~{b['v']:.5f} loop_count={len(b['loops'])}")

        for bi, bucket in enumerate(buckets):
            loops = bucket['loops']
            print(f"[SnapSplit DEBUG] -- filling bucket[{bi}]: {len(loops)} loop(s) --")

            # Group loops into 'outer + holes' by 2D nesting (None -> legacy behaviour)
            groups = _group_loops_by_nesting(loops, ax)
            if groups is None:
                print("[SnapSplit DEBUG]   nesting analysis failed -> legacy single group")
                groups = [{'edges': [e for lp in loops for e in lp],
                           'n_holes': len(loops) - 1,
                           'expected_area': None}]

            for gi, grp in enumerate(groups):
                g_edges = grp['edges']

                if grp['n_holes'] == 0:
                    print(f"[SnapSplit DEBUG]   group {gi}: plain loop -> BMesh fill (N-gon first)")
                    # No selection needed anymore: the edges are passed to the BMesh op directly
                    did = _fill_edges_bmesh(bm, g_edges, prefer_ngon=True, normal=n_plane)
                    bmesh.update_edit_mesh(obj.data)

                else:
                    print(f"[SnapSplit DEBUG]   group {gi}: outer loop + {grp['n_holes']} hole(s) "
                          f"-> verified triangle_fill")
                    did = _fill_nested_group_bmesh(bm, g_edges, n_plane,
                                                   grp['n_holes'], grp['expected_area'])
                    bmesh.update_edit_mesh(obj.data)
                print(f"[SnapSplit DEBUG]   group {gi} fill result: {did}")
                any_ok = any_ok or did

        if any_ok:
            # Recalculate normals directly on the edit BMesh
            # (replaces select_all + normals_make_consistent operators).
            try:
                bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
                bmesh.update_edit_mesh(obj.data)
            except Exception as ex:
                print(f"[SnapSplit DEBUG] recalc_face_normals raised: {ex}")

        return any_ok

    except Exception as ex:
        print(f"[SnapSplit DEBUG] EXCEPTION inside cap_single_object_hollow_style: {ex}")
        raise
    finally:
        # Safety net: guarantee we always leave edit mode, even if an
        # exception occurs above, to avoid corrupting the operator context
        # for subsequent bpy.ops calls (observed crash in select_all).
        _leave_edit_mode()
        try:
            obj.data.validate(); obj.data.update()
        except Exception:
            pass
        print(f"[SnapSplit DEBUG] ---- cap_single_object_hollow_style: {obj.name} DONE, any_ok={any_ok} ----")

# ---------------------------
# Auto "Apply Rotation & Scale" before the planar split
# ---------------------------

def apply_rotation_and_scale(obj):
    """Bake rotation and scale of obj into its mesh data. Location is NOT applied.

    The result is the same as Ctrl+A > Rotation & Scale: the object keeps its world
    position and shape, but its local axes become the world axes. Cut planes,
    capping and seam detection (all world-axis based) then work in the same space.

    Handles parents (detached while keeping the world matrix), children (world
    matrix restored), shared mesh data (own copy is made), shape keys and
    mirrored (negative determinant) transforms.
    Returns True if the object was modified, False if nothing was done or the
    object could not be baked safely.
    """
    from mathutils import Matrix  # local import: no change to the module header needed

    if obj is None or obj.type != 'MESH' or obj.data is None:
        return False
    # Mesh.transform() cannot be used while the mesh is in Edit Mode
    if obj.mode != 'OBJECT':
        return False

    # Make sure matrix_world is up to date before reading it
    try:
        bpy.context.view_layer.update()
    except Exception:
        pass

    M = obj.matrix_world.copy()
    rs = M.to_3x3()  # rotation + scale (+ parent contribution), without translation

    # Nothing to do if the object space is already aligned with the world axes
    dev = max(abs(rs[i][j] - (1.0 if i == j else 0.0)) for i in range(3) for j in range(3))
    if dev < 1e-6:
        return False

    # Remember the world matrices of children so they do not move afterwards
    children = [(c, c.matrix_world.copy()) for c in obj.children]

    # Detach from the parent while keeping the world transform
    if obj.parent is not None:
        obj.parent = None
        obj.matrix_world = M

    # Shared mesh data would change other objects too: give this object its own copy
    if obj.data.users > 1:
        obj.data = obj.data.copy()

    if rs.determinant() < 0.0:
        # DOCUMENTED FALLBACK (same reason as in _apply_object_scale_if_needed):
        # a mirroring transform flips the winding, so use Blender's own operator.
        # The context override restricts the operator to this single object.
        try:
            with bpy.context.temp_override(active_object=obj, object=obj,
                                           selected_objects=[obj],
                                           selected_editable_objects=[obj]):
                bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
        except Exception as ex:
            print(f"[SnapSplit] transform_apply fallback failed: {ex}")
            return False
    else:
        has_keys = getattr(obj.data, "shape_keys", None) is not None
        m4 = rs.to_4x4()
        try:
            # Transform shape keys together with the base mesh
            obj.data.transform(m4, shape_keys=True)
        except TypeError:
            # 'shape_keys' argument not available: only safe without shape keys
            if has_keys:
                print("[SnapSplit] Object has shape keys; transform not applied.")
                return False
            obj.data.transform(m4)
        obj.data.update()
        # Keep only the world position on the object (rotation 0, scale 1)
        obj.matrix_world = Matrix.Translation(M.translation)

    try:
        bpy.context.view_layer.update()
    except Exception:
        pass

    # Restore the world matrices of the children
    for c, mw in children:
        try:
            c.matrix_world = mw
        except Exception:
            pass
    return True



class SNAP_OT_planar_split(Operator):
    """Split the active mesh into multiple parts along a selected axis, with optional auto-capping."""
    bl_idname = "snapsplit.planar_split"
    bl_label = "Planar Split"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        """Execute the split operation and optionally cap seams depending on settings."""
        obj = context.active_object
        if not obj or obj.type != 'MESH':
            report_user(self, 'ERROR',
                        'Please select a mesh object.')
            return {'CANCELLED'}

        # Normalize hollow and record used_hollow flag
        used_hollow = False

        try:
            obj, used_hollow = robust_prepare_hollow(obj, operator=self)
            obj.data.validate(); obj.data.update()
        except Exception as e:
            print(f"[SnapSplit] Hollow prepare failed: {e}")

        props = context.scene.snapsplit
        # Auto-cap toggle (reads from scene props)
        auto_cap = bool(getattr(props, "cap_seams_during_split", False))

        axis = props.split_axis
        count = max(2, int(props.parts_count))
        if count >= 12:
            self.report({'INFO'}, _trf('Splitting into many parts can take a while on dense meshes...'))

        offset_scene = float(getattr(props, "split_offset_mm", 0.0)) * unit_mm()
        # Apply rotation and scale AFTER the cuts were computed (so they match the orange
        # preview exactly) and BEFORE the split (so mesh space == world space).
        # The cut planes are world coordinates and the object keeps its world position
        # and shape, so the cuts stay valid. A failure must never block the split.
        try:
            if apply_rotation_and_scale(obj):
                report_user(self, 'INFO',
                            'Rotation and scale were applied before splitting.')
        except Exception as ex:
            print(f"[SnapSplit] Auto apply rotation/scale failed: {ex}")


        cuts = create_cut_data_with_offset(obj, axis, count, global_offset_scene=offset_scene)

        parts = apply_bmesh_split_sequence(obj, axis, count, cuts_override=cuts, operator=self)

        # Auto-cap after splitting if enabled
        if auto_cap and parts:
            capped_cnt = 0
            # NOTE: always use the ring-aware capping algorithm now, regardless
            # of used_hollow. Reliably detecting "this object has a hollow
            # cavity" up front is not feasible for arbitrary user setups (e.g.
            # a manually applied Boolean modifier using an unrelated source
            # object, such as a Sphere carving a cavity into a Cube) -- neither
            # _try_apply_hollow_modifier's Solidify/named-NODES check nor
            # _find_paired_inner_object_for's name-matching heuristic can
            # detect that case. cap_single_object_hollow_style() now correctly
            # handles both plain solid cross-sections (single loop per plane)
            # and cavity rings (two loops per plane), so it is safe and
            # correct to use unconditionally, replacing the previous
            # used_hollow-gated fallback to _cap_single_object_simple_fill()
            # (which could not distinguish outer from inner loops and sealed
            # cavities shut).
            for p in parts:
                try:
                    if cap_single_object_hollow_style(p):
                        capped_cnt += 1
                except Exception:
                    pass

            if capped_cnt == 0:
                report_user(self, 'WARNING',
                            'Auto-cap during split did not find valid loops to fill.')
            else:
                msg = _trf("Auto-capped seams on {n} part(s).", n=capped_cnt)
                report_user(self, 'INFO', msg)


        if len(parts) < count:
            msg = _trf("Fewer parts created than expected ({have} < {want}).",
                       have=len(parts), want=count)
            report_user(self, 'WARNING', msg)
        else:
            msg = _trf("{n} parts created.", n=len(parts))
            report_user(self, 'INFO', msg)

        # ---------------------------
        # Route results into per-job collections (visible Parts, hidden Helpers)
        # ---------------------------

        parts_job_coll, helpers_job_coll = _ensure_job_collections(obj.name)

        # Build sets to separate final vs intermediate
        final_parts_set = set(parts)

        # Heuristic: any mesh whose name starts with the source name and isn't a final is considered intermediate
        candidates = [o for o in bpy.data.objects if o.type == 'MESH' and o.name.startswith(obj.name)]
        intermediates = [o for o in candidates if o not in final_parts_set]

        # 1) Link only the final parts to the visible Parts job collection
        # (RNA-based deselect instead of bpy.ops.object.select_all)
        _deselect_all_objects()
        for p in parts:
            # Unlink from any other collections to keep Outliner clean
            try:
                for c in list(p.users_collection):
                    try:
                        c.objects.unlink(p)
                    except Exception:
                        pass
            except Exception:
                pass
            try:
                parts_job_coll.objects.link(p)
            except Exception:
                pass
            p.hide_set(False)
            p.select_set(True)

        if parts:
            bpy.context.view_layer.objects.active = parts[0]

        # 2) Move preview planes (if any left) to Helpers and hide
        try:
            preview_objs = [o for o in bpy.data.objects if o.name.startswith(PREVIEW_PLANE_PREFIX)]
            _move_objs_to_collection(preview_objs, helpers_job_coll, hide=True, unlink_first=True)
        except Exception:
            pass

        # 3) Move intermediate artifacts to Helpers and hide
        try:
            _move_objs_to_collection(intermediates, helpers_job_coll, hide=True, unlink_first=True)
        except Exception:
            pass

        # 4) Move service objects (e.g., cutters) to Helpers and optionally remove now-empty service collections
        for svc_name in ("_SnapSplit_Cutters",):
            try:
                c = bpy.data.collections.get(svc_name)
                if c:
                    _move_objs_to_collection(list(c.objects), helpers_job_coll, hide=True, unlink_first=True)
                    # Optionally remove the empty service collection to reduce clutter
                    if len(c.objects) == 0:
                        for sc in bpy.data.scenes:
                            try:
                                if c in sc.collection.children:
                                    sc.collection.children.unlink(c)
                            except Exception:
                                pass
                        try:
                            bpy.data.collections.remove(c)
                        except Exception:
                            pass
            except Exception:
                pass

        # Keep your preview system cleanup (safe)
        try:
            update_split_preview_plane(context)
        except Exception:
            pass
        try:
            _disable_split_preview_and_cleanup(context)
        except Exception:
            pass

        return {'FINISHED'}

# ---------------------------
# Cap seams now – precise outer/inner loop detection (manual)
# ---------------------------

def _loops_from_edges_connected(edges):
    """Return connected components of edges as lists (for loop detection)."""
    rem = set(edges)
    comps = []
    while rem:
        start = rem.pop()
        comp = {start}
        stack = [start]
        while stack:
            e = stack.pop()
            for v in e.verts:
                for e2 in v.link_edges:
                    if e2 in rem:
                        rem.remove(e2)
                        comp.add(e2)
                        stack.append(e2)
        if len(comp) >= 3:
            comps.append(list(comp))
    return comps

def _perimeter_of_edges(loop):
    """Return approximate perimeter of a given edge loop list."""
    p = 0.0
    for e in loop:
        v0, v1 = e.verts
        p += (v0.co - v1.co).length
    return p

# ---------------------------
# Conservative pure-BMesh edge-loop walker (replaces bpy.ops.mesh.loop_multi_select)
# ---------------------------

def _next_edge_in_loop(edge, vert, boundary_mode):
    """Return the next edge when walking an edge loop through 'vert', or None if ambiguous.

    Rules (deliberately strict; any ambiguity returns None):
      - boundary_mode (seed edge is a boundary edge): the next edge is the ONLY
        other boundary edge at 'vert'. More than one or none -> ambiguous.
      - interior mode: 'vert' must have exactly 4 edges and the current edge must
        have exactly 2 faces. The next edge is the single edge at 'vert' that shares
        no face with the current edge (the "opposite" edge in a quad grid).
    """
    if boundary_mode:
        cands = [e for e in vert.link_edges if e != edge and e.is_boundary]
        return cands[0] if len(cands) == 1 else None

    if len(vert.link_edges) != 4:
        return None
    edge_faces = set(edge.link_faces)
    if len(edge_faces) != 2:
        return None
    cands = [e for e in vert.link_edges
             if e != edge and not (edge_faces & set(e.link_faces))]
    return cands[0] if len(cands) == 1 else None

def _walk_edge_loop_closed(seed_edge, max_steps):
    """Walk an edge loop through 'seed_edge' and return its edges ONLY if it is a closed cycle.

    Returns a list of BMEdge objects forming a closed loop, or None when the loop
    cannot be proven closed (open chain, ambiguous vertex, revisited edge, step
    limit reached). The walker never modifies the mesh or the selection.
    """
    try:
        if seed_edge is None or not seed_edge.is_valid:
            return None

        boundary_mode = bool(seed_edge.is_boundary)
        start_vert = seed_edge.verts[0]
        cur_vert = seed_edge.verts[1]
        cur_edge = seed_edge

        loop = [seed_edge]
        visited = {seed_edge}

        for _ in range(max(4, int(max_steps))):
            nxt = _next_edge_in_loop(cur_edge, cur_vert, boundary_mode)
            if nxt is None:
                return None
            if nxt == seed_edge:
                # Closed only if we came back through the start vertex of the seed edge
                return loop if (cur_vert == start_vert and len(loop) >= 3) else None
            if nxt in visited:
                # Revisiting an edge that is not the seed -> pinch/figure-eight, reject
                return None
            loop.append(nxt)
            visited.add(nxt)
            cur_vert = nxt.other_vert(cur_vert)
            cur_edge = nxt
        return None
    except Exception:
        return None


class SNAP_OT_cap_open_seams_now(Operator):
    """Fill between exactly two split edge loops (outer+inner) per plane; prefers seed edges if present."""
    bl_idname = "snapsplit.cap_open_seams_now"
    bl_label = "Cap seams now"
    bl_description = 'Fill between exactly two split edge loops (outer+inner) per plane. Seeds preferred.'
    bl_options = {'REGISTER', 'UNDO'}

    only_selected: bpy.props.BoolProperty(
        name='Only selected objects',
        default=True
    )
    max_planes: bpy.props.IntProperty(
        name='Max planes',
        description='0 = all planes per object, 1 = only largest',
        default=0, min=0, soft_max=12
    )
    select_only: bpy.props.BoolProperty(
        name='Select only (no fill)',
        default=False
    )
    require_two_seeds: bpy.props.BoolProperty(
        name='Require exactly two seed edges',
        description='If exactly two edges are selected in Edit Mode, use them as seeds only (no auto-detection).',
        default=False
    )

    def _plane_axis_for_object(self, obj):
        """Return the split axis for the given object from scene props."""
        props = getattr(bpy.context.scene, "snapsplit", None)
        return props.split_axis if props else "Z"

    def _seeds_exact_two_edges(self, bm):
        """Return the selected two edges if exactly two are selected, else None."""
        sel_edges = [e for e in bm.edges if e.select]
        return sel_edges if len(sel_edges) == 2 else None

    def _expand_edge_to_full_loop_ops(self, obj, bm, edge):
        """DOCUMENTED FALLBACK: expand an edge to a loop via bpy.ops.mesh.loop_multi_select.

        Only used when the pure-BMesh walker cannot prove a closed cycle.
        Blender's C edge-loop walker has no public Python equivalent, so this is
        the single remaining operator-based loop selection in SnapSplit.
        This fallback changes the BMesh selection (as the original code did).
        """
        for e in bm.edges:
            e.select = False
        edge.select = True
        bmesh.update_edit_mesh(obj.data)
        try:
            bpy.ops.mesh.loop_multi_select(ring=False)
        except Exception:
            pass
        return [e for e in bm.edges if e.select]

    def _expand_edge_to_full_loop(self, obj, bm, edge):
        """Expand a selected edge to a full edge loop and return the loop edges.

        Step 1: pure-BMesh walker (no operator, no selection change).
        Step 2: if no closed cycle could be proven, fall back to the operator
                (only if _ALLOW_OPS_LOOP_FALLBACK is True).
        """
        try:
            bm.edges.ensure_lookup_table()
            walked = _walk_edge_loop_closed(edge, max_steps=len(bm.edges) + 1)
        except Exception:
            walked = None
        if walked:
            return walked

        if _ALLOW_OPS_LOOP_FALLBACK:
            print("[SnapSplit DEBUG] edge-loop walker found no closed cycle -> "
                  "falling back to bpy.ops.mesh.loop_multi_select for this seed")
            return self._expand_edge_to_full_loop_ops(obj, bm, edge)

        # Fallback disabled: return only the seed edge (will fail the cyclic check)
        return [edge]

    def _loop_is_cyclic_degree2(self, loop_edges):
        """Check if edges form a simple cycle where every vertex has degree 2."""
        count = {}
        for e in loop_edges:
            for v in e.verts:
                count[v] = count.get(v, 0) + 1
        return all(c == 2 for c in count.values()) and len(loop_edges) >= 3

    def _fill_like_altf(self, obj, bm, edges):
        """Fill the given loops like Mesh > Fill (Alt+F) using BMesh only (no operator, no selection)."""
        ok = _fill_edges_bmesh(bm, edges, prefer_ngon=False)
        if ok:
            bmesh.update_edit_mesh(obj.data)
        return ok


    def _cluster_split_ring_edges(self, obj, bm, plane_axis):
        """Cluster boundary edges into groups per split plane along the given axis."""
        ax = axis_index_for(plane_axis)
        axis_vecs = (Vector((1,0,0)), Vector((0,1,0)), Vector((0,0,1)))
        split_no = axis_vecs[ax].normalized()

        eps_plane = _diag_eps(obj, k=5e-6, min_eps=5e-7)
        eps_dir = 0.12

        cand = []
        for e in bm.edges:
            if not e.is_boundary:
                continue
            d = (e.verts[1].co - e.verts[0].co)
            if d.length_squared == 0.0:
                continue
            d.normalize()
            if abs(d.dot(split_no)) > eps_dir:
                continue
            cand.append(e)

        if not cand:
            return []

        mvals = [(e, (0.5 * (e.verts[0].co + e.verts[1].co)).dot(split_no)) for e in cand]
        mvals.sort(key=lambda t: t[1])

        planes = []
        for e, val in mvals:
            matched = False
            for pl in planes:
                if abs(val - pl['v']) <= eps_plane:
                    pl['edges'].append(e)
                    pl['v'] = (pl['v'] * 0.9) + (val * 0.1)
                    matched = True
                    break
            if not matched:
                planes.append({'v': val, 'edges': [e]})

        planes.sort(key=lambda d: len(d['edges']), reverse=True)
        return [pl['edges'] for pl in planes]

    def _cap_single_object(self, obj, max_planes=0, select_only=False) -> bool:
        """Run the capping routine on a single mesh object, optionally only selecting loops."""
        _enter_edit_mode_edges(obj)
        bm = bmesh.from_edit_mesh(obj.data)
        bm.verts.ensure_lookup_table(); bm.edges.ensure_lookup_table(); bm.faces.ensure_lookup_table()

        # 1) Strict two-edge seeds
        if self.require_two_seeds:
            seeds = self._seeds_exact_two_edges(bm)
            if seeds:
                loop_a = self._expand_edge_to_full_loop(obj, bm, seeds[0])
                loop_b = self._expand_edge_to_full_loop(obj, bm, seeds[1])
                if self._loop_is_cyclic_degree2(loop_a) and self._loop_is_cyclic_degree2(loop_b):
                    for e in bm.edges: e.select = False
                    for e in loop_a + loop_b: e.select = True
                    bmesh.update_edit_mesh(obj.data)
                    if not select_only:
                        ok = self._fill_like_altf(obj, bm, loop_a + loop_b)
                        _leave_edit_mode()

                        if ok:
                            # Recalculate normals via BMesh (no Edit Mode round trip)
                            _recalc_normals_outside(obj)
                        return ok
                    else:
                        _leave_edit_mode()
                        return True
            _leave_edit_mode()
            return False

        # 2) Seeds preferred (>=2 edges): take two largest loops
        sel_edges = [e for e in bm.edges if e.select]
        if len(sel_edges) >= 2:
            loops = []
            seen = set()
            for e in sel_edges[:4]:
                if e in seen: continue
                loops.append(self._expand_edge_to_full_loop(obj, bm, e)); seen.add(e)
            loops = [lp for lp in loops if self._loop_is_cyclic_degree2(lp)]
            loops.sort(key=lambda lp: _perimeter_of_edges(lp), reverse=True)
            if len(loops) >= 2:
                loop_a, loop_b = loops[0], loops[1]
                for e in bm.edges: e.select = False
                for e in loop_a + loop_b: e.select = True
                bmesh.update_edit_mesh(obj.data)
                if not select_only:
                    ok = self._fill_like_altf(obj, bm, loop_a + loop_b)
                    _leave_edit_mode()

                    if ok:
                        # Recalculate normals via BMesh (no Edit Mode round trip)
                        _recalc_normals_outside(obj)
                    return ok
                else:
                    _leave_edit_mode()
                    return True

        # 3) Automatic detection – group true split rings per plane
        plane_axis = self._plane_axis_for_object(obj)
        ring_groups = self._cluster_split_ring_edges(obj, bm, plane_axis)
        if not ring_groups:
            _leave_edit_mode()
            return False

        ax = axis_index_for(plane_axis)
        n_plane = (Vector((1,0,0)), Vector((0,1,0)), Vector((0,0,1)))[ax].normalized()
        eps_plane_loop = _diag_eps(obj, k=8e-6, min_eps=8e-7)

        processed = 0
        all_ok = True
        any_selected = False

        for edges_on_plane in ring_groups:
            if max_planes and processed >= max_planes:
                break

            # Build connected edge sets (loop candidates) and keep only degree-2 cyclic loops
            comps = _loops_from_edges_connected(edges_on_plane)
            comps = [c for c in comps if self._loop_is_cyclic_degree2(c)]

            # Single-loop quick path (solid caps) BEFORE planarity tests (still fine for cubes)
            if len(comps) == 1:
                loop_a = comps[0]
                for e in bm.edges:
                    e.select = False
                for e in loop_a:
                    e.select = True
                bmesh.update_edit_mesh(obj.data)

                did = False
                if not select_only:
                    # N-gon first (like edge_face_add), then triangle fill; no operators
                    did = _fill_edges_bmesh(bm, loop_a, prefer_ngon=True, normal=n_plane)
                    if did:
                        bmesh.update_edit_mesh(obj.data)
                else:
                    did = True  # selection-only mode


                any_selected = True
                all_ok = all_ok and did
                processed += 1
                continue

            if len(comps) < 2:
                all_ok = False
                continue

            # Planarity filter
            mids = [(0.5 * (e.verts[0].co + e.verts[1].co)) for e in edges_on_plane]
            p_plane = sum(mids, Vector((0,0,0))) * (1.0 / max(1, len(mids)))

            comps = [c for c in comps if max(abs((v.co - p_plane).dot(n_plane)) for e in c for v in e.verts) <= eps_plane_loop]
            if len(comps) < 2:
                all_ok = False
                continue

            comps.sort(key=lambda lp: _perimeter_of_edges(lp), reverse=True)

            i = 0
            plane_ok = True
            while i + 1 < len(comps):
                loop_a, loop_b = comps[i], comps[i+1]
                for e in bm.edges: e.select = False
                for e in loop_a + loop_b: e.select = True
                bmesh.update_edit_mesh(obj.data)
                any_selected = True
                if not select_only:
                    ok = self._fill_like_altf(obj, bm, loop_a + loop_b)
                    plane_ok = plane_ok and ok

                i += 2

            all_ok = all_ok and plane_ok
            processed += 1

        _leave_edit_mode()
        if not select_only and all_ok and processed > 0:
            # Recalculate normals via BMesh (no Edit Mode round trip)
            _recalc_normals_outside(obj)

        try:
            obj.data.validate(); obj.data.update()
        except Exception:
            pass

        return (all_ok and processed > 0) or (select_only and any_selected)

    def execute(self, context):
        """Execute capping for selected targets or the parts collection."""
        if self.only_selected:
            targets = [o for o in context.selected_objects if o.type == 'MESH']
        else:
            parts_coll = bpy.data.collections.get("SnapSplit_Parts")
            targets = [o for o in (list(parts_coll.objects) if parts_coll else []) if o and o.type == 'MESH']

        if not targets:
            report_user(self, 'ERROR',
                        'No mesh objects to cap. Select split parts or use the parts collection.')
            return {'CANCELLED'}

        success = 0
        for obj in targets:
            try:
                if self._cap_single_object(obj, max_planes=self.max_planes, select_only=self.select_only):
                    success += 1
            except Exception as e:
                _leave_edit_mode()
                # Fill the {name}/{err} placeholders AFTER the translation lookup
                msg = _trf("Processing failed on '{name}': {err}",
                           name=obj.name, err=str(e))
                report_user(self, 'WARNING', msg)

        if success == 0:
            if self.select_only:
                report_user(self, 'WARNING',
                            'Could not determine split edge loops to select.')
            else:
                report_user(self, 'WARNING',
                            'Could not determine and fill split edge loops.')
            return {'CANCELLED'}

        # Fill the {n} placeholder AFTER the translation lookup
        if self.select_only:
            msg = _trf("Selected split edge loops on {n} object(s).", n=success)
        else:
            msg = _trf("Capped seams on {n} object(s).", n=success)
        report_user(self, 'INFO', msg)
        return {'FINISHED'}


# ---------------------------
# Registration
# ---------------------------

classes = (
    SNAP_OT_adjust_split_axis,
    SNAP_OT_planar_split,
    SNAP_OT_cap_open_seams_now,
)

def register():
    """Register operators. The depsgraph handler is NOT added unconditionally anymore."""
    # Labels and descriptions are plain class attributes; Blender translates them itself.
    for c in classes:
        bpy.utils.register_class(c)


    # Drop stale handlers first (e.g. left over from a hot reload), then install the
    # one-shot file-load check and attach the depsgraph handler only if a preview is on.
    _remove_handlers_named(bpy.app.handlers.depsgraph_update_post, _DEPSGRAPH_HANDLER_NAME)
    _remove_handlers_named(bpy.app.handlers.load_post, _LOAD_HANDLER_NAME)
    bpy.app.handlers.load_post.append(_snapsplit_load_post)
    sync_depsgraph_handler()


def unregister():
    """Unregister operators and make sure no SnapSplit handler stays behind."""
    global _last_preview_active_obj, _last_connector_preview_selection_key
    # Never leave X-Ray switched on when the add-on is disabled
    try:
        from .utils import xray_release
        xray_release(None)
    except Exception:
        pass
    _remove_handlers_named(bpy.app.handlers.depsgraph_update_post, _DEPSGRAPH_HANDLER_NAME)
    _remove_handlers_named(bpy.app.handlers.load_post, _LOAD_HANDLER_NAME)
    _last_preview_active_obj = None
    _last_connector_preview_selection_key = None

    for c in reversed(classes):
        bpy.utils.unregister_class(c)
