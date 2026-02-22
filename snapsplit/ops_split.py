"""
Copyright (C) 2026 Christoph Medicus
https://dev.betakontext.de
dev@betakontext.de

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
along with this program; if not, see <https://www.gnu.org/licenses>.
"""
import bpy
import bmesh
from bpy.types import Operator
from mathutils import Vector, Matrix

from .utils import (
    ensure_collection,
    report_user,
    is_lang_de,
    unit_mm,
)

# ---------------------------
# Preview naming
# ---------------------------

PREVIEW_COLL_NAME = "_SnapSplit_Preview"
PREVIEW_PLANE_PREFIX = "_SnapSplit_PreviewPlane_"  # final name: _SnapSplit_PreviewPlane_<ObjName>_<i>
PREVIEW_MAT_NAME = "_SnapSplit_Preview_MAT"

# ---------------------------
# Helpers: BB / axes / preview material
# ---------------------------

def axis_index_for(axis):
    return {"X": 0, "Y": 1, "Z": 2}[axis]

def world_aabb(obj):
    # Compute min/max in world space from bound_box transformed by matrix_world
    corners = [obj.matrix_world @ Vector(c) for c in obj.bound_box]
    min_v = Vector((min(v.x for v in corners), min(v.y for v in corners), min(v.z for v in corners)))
    max_v = Vector((max(v.x for v in corners), max(v.y for v in corners), max(v.z for v in corners)))
    return min_v, max_v

def aabb_center(min_v, max_v):
    return 0.5 * (min_v + max_v)

def world_pos_from_norm(obj, axis, t_norm):
    """
    Map normalized t_norm in [-1,1] to world position along object's AABB on 'axis'.
    Returns (pos, (lo, hi, mid, half)).
    """
    min_v, max_v = world_aabb(obj)
    ax = axis_index_for(axis)
    lo = min_v[ax]
    hi = max_v[ax]
    mid = 0.5 * (lo + hi)
    half = 0.5 * (hi - lo)
    return mid + t_norm * half, (lo, hi, mid, half)

def size_on_tangential_axes(obj, axis):
    """
    Return extents (size_t1, size_t2) and tangential axis indices (t1, t2),
    based on the object's world-space AABB.
    """
    min_v, max_v = world_aabb(obj)
    ax = axis_index_for(axis)
    t1 = (ax + 1) % 3
    t2 = (ax + 2) % 3
    return (abs(max_v[t1] - min_v[t1]), abs(max_v[t2] - min_v[t2])), (t1, t2), (min_v, max_v)

def warn_if_unapplied_transforms(obj, operator=None):
    """
    Prüft auf negative/non-uniforme Skalierung, nicht-null Location, nicht-Identitätsrotation.
    Gibt eine user-freundliche Warnung aus, die 'Apply All Transforms (Ctrl+A)' vorschlägt.
    """
    if not obj or obj.type != 'MESH':
        return

    try:
        # Location
        loc = tuple(getattr(obj, "location", (0.0, 0.0, 0.0)))
        has_loc = any(abs(v) > 1e-7 for v in loc)

        # Rotation (Euler oder Quaternion)
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

        # Scale
        sx, sy, sz = getattr(obj, "scale", (1.0, 1.0, 1.0))
        non_uniform = (abs(sx - sy) > 1e-7) or (abs(sy - sz) > 1e-7) or (abs(sx - sz) > 1e-7)
        det = obj.matrix_world.to_3x3().determinant()
        negative_scale = det < 0.0

        if has_loc or has_rot or non_uniform or negative_scale:
            msg_en = "Object has unapplied transforms"
            details_en = []
            if has_loc: details_en.append("Location")
            if has_rot: details_en.append("Rotation")
            if non_uniform: details_en.append("Non-uniform Scale")
            if negative_scale: details_en.append("Negative Scale")
            details_str_en = ", ".join(details_en)

            msg_de = "Objekt hat nicht angewendete Transformationen"
            details_de = []
            if has_loc: details_de.append("Position")
            if has_rot: details_de.append("Rotation")
            if non_uniform: details_de.append("nicht-uniforme Skalierung")
            if negative_scale: details_de.append("negative Skalierung")
            details_str_de = ", ".join(details_de)

            hint_en = "Consider Apply All Transforms (Ctrl+A) for exact and predictable split results."
            hint_de = "Für exakte und vorhersagbare Schnittergebnisse ggf. 'Apply All Transforms' (Strg+A) anwenden."

            full_en = f"{msg_en}: {details_str_en}. {hint_en}"
            full_de = f"{msg_de}: {details_str_de}. {hint_de}"

            if operator is not None:
                report_user(operator, 'INFO', full_en, full_de)
            else:
                print(f"[SnapSplit] {full_en} / {full_de}")
    except Exception:
        pass


def build_orange_preview_material():
    name = PREVIEW_MAT_NAME
    mat = bpy.data.materials.get(name)
    if mat:
        return mat
    mat = bpy.data.materials.new(name=name)
    mat.use_nodes = True
    nt = mat.node_tree
    # clear nodes
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    out = nt.nodes.new("ShaderNodeOutputMaterial"); out.location = (200, 0)
    mix = nt.nodes.new("ShaderNodeMixShader"); mix.location = (0, 0)
    transp = nt.nodes.new("ShaderNodeBsdfTransparent"); transp.location = (-200, -100)
    emis = nt.nodes.new("ShaderNodeEmission"); emis.location = (-200, 100)
    emis.inputs["Color"].default_value = (1.0, 0.5, 0.0, 1.0)  # orange
    emis.inputs["Strength"].default_value = 3.0
    fac = nt.nodes.new("ShaderNodeValue"); fac.location = (-400, 0)
    fac.outputs[0].default_value = 0.3  # 30% fill
    nt.links.new(fac.outputs[0], mix.inputs[0])
    nt.links.new(transp.outputs[0], mix.inputs[1])
    nt.links.new(emis.outputs[0], mix.inputs[2])
    nt.links.new(mix.outputs[0], out.inputs[0])
    mat.blend_method = 'BLEND'
    mat.shadow_method = 'NONE'
    mat.use_backface_culling = False
    return mat

def ensure_preview_collection():
    return ensure_collection(PREVIEW_COLL_NAME)

def create_or_get_preview_plane(context, obj, axis, name):
    """
    Create (or reuse) a plane mesh object. Material is ensured here.
    Final orientation/scale/position is set elsewhere via build_preview_matrix.
    """
    coll = ensure_preview_collection()
    plane = bpy.data.objects.get(name)
    if plane is None or plane.type != 'MESH':
        me = bpy.data.meshes.new(name)
        bm = bmesh.new()
        bmesh.ops.create_grid(bm, x_segments=1, y_segments=1, size=0.5)  # 1x1 in local XY, normal +Z
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
        # Viewport overlay: red outline in Wireframe and Solid (no in-front)
    plane.display_type = 'TEXTURED'   # Solid shows faces as Blender’s grey; Material Preview shows your orange
    plane.show_wire = True            # draw wire overlay on top of the object’s shading
    plane.show_all_edges = True       # all edges, not only sharp
    plane.hide_select = True          # prevent accidental selection

    # Use object color for wire color (requires Overlays → Geometry → "Object Color" enabled)
    try:
        plane.color = (1.0, 0.1, 0.1, 1.0)  # red wire/outline in viewport
    except Exception:
        pass

    return plane

# Object-scoped naming
def preview_plane_name_for(obj_name: str, idx: int) -> str:
    return f"{PREVIEW_PLANE_PREFIX}{obj_name}_{idx}"

def preview_plane_names_for_object(obj_name: str, parts_count: int):
    n = max(0, int(parts_count) - 1)
    return [preview_plane_name_for(obj_name, i+1) for i in range(n)]

def build_preview_matrix(obj, axis, pos):
    """
    Build full matrix T @ R @ S for a preview plane:
    - R: world axes with Z along 'axis' and X/Y as tangential world axes
    - S: scale to active object's tangential extents
    - T: translate to active object's AABB center in tangential axes and 'pos' along 'axis'
    """
    (size_t1, size_t2), (t1_idx, t2_idx), (min_v, max_v) = size_on_tangential_axes(obj, axis)
    size_t1 = max(size_t1, 1e-9); size_t2 = max(size_t2, 1e-9)

    ax = axis_index_for(axis)
    c = aabb_center(min_v, max_v)

    world_axes = (Vector((1,0,0)), Vector((0,1,0)), Vector((0,0,1)))
    z_dir = world_axes[ax].copy().normalized()
    x_dir = world_axes[t1_idx].copy().normalized()
    if abs(z_dir.dot(x_dir)) > 0.999:
        x_dir = world_axes[t2_idx].copy().normalized()
    y_dir = z_dir.cross(x_dir)
    if y_dir.length_squared == 0.0:
        x_dir = world_axes[t2_idx].copy().normalized()
        y_dir = z_dir.cross(x_dir)
    y_dir.normalize()
    x_dir = y_dir.cross(z_dir); x_dir.normalize()

    R = Matrix((
        (x_dir.x, y_dir.x, z_dir.x, 0.0),
        (x_dir.y, y_dir.y, z_dir.y, 0.0),
        (x_dir.z, y_dir.z, z_dir.z, 0.0),
        (0.0,     0.0,     0.0,     1.0),
    ))
    S = Matrix.Diagonal(Vector((size_t1, size_t2, 1.0, 1.0)))

    tloc = Vector((c.x, c.y, c.z))
    tloc[ax] = pos
    T = Matrix.Translation(tloc)
    return T @ R @ S

def position_preview_planes_for_object(context, obj, axis, parts_count, offset_scene, force_rebuild=False):
    """
    Build exactly (parts_count - 1) preview planes for ACTIVE object and axis.
    Names are object-scoped. Compose full matrices per plane each update.
    """
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

        # Ensure red outline overlay in viewport (no in-front)
        plane.display_type = 'TEXTURED'
        plane.show_wire = True
        plane.show_all_edges = True
        try:
            plane.color = (1.0, 0.1, 0.1, 1.0)
        except Exception:
            pass


    # Cleanup excess planes of this object
    existing_scoped = [o for o in bpy.data.objects if o.name.startswith(f"{PREVIEW_PLANE_PREFIX}{obj_name}_")]
    for o in existing_scoped:
        if o.name not in want_names:
            for coll in list(o.users_collection):
                try: coll.objects.unlink(o)
                except Exception: pass
            try: bpy.data.objects.remove(o)
            except Exception: pass

    # Clean stray legacy planes (without object scoping)
    stray = [o for o in bpy.data.objects if o.name.startswith(PREVIEW_PLANE_PREFIX) and f"{obj_name}_" not in o.name]
    for o in stray:
        for coll in list(o.users_collection):
            try: coll.objects.unlink(o)
            except Exception: pass
        try: bpy.data.objects.remove(o)
        except Exception:
            pass

def _disable_split_preview_and_cleanup(context):
    """Turn off the 'show_split_preview' toggle and remove all preview planes and the empty collection."""
    # 1) Toggle off
    try:
        props = getattr(context.scene, "snapsplit", None)
        if props and getattr(props, "show_split_preview", False):
            props.show_split_preview = False
    except Exception:
        pass

    # 2) Remove all preview plane objects
    try:
        for o in [o for o in bpy.data.objects if o.name.startswith(PREVIEW_PLANE_PREFIX)]:
            for coll in list(o.users_collection):
                try:
                    coll.objects.unlink(o)
                except Exception:
                    pass
            try:
                bpy.data.objects.remove(o)
            except Exception:
                pass
    except Exception:
        pass

    # 3) Remove the (now) empty preview collection
    try:
        _remove_empty_preview_collection()
    except Exception:
        pass



def _remove_empty_preview_collection():
    try:
        pc = bpy.data.collections.get(PREVIEW_COLL_NAME)
        if not pc:
            return
        if len(pc.objects) > 0:
            return  # still in use
        # Unlink from all scene roots (in case it was linked)
        for sc in bpy.data.scenes:
            try:
                if pc in sc.collection.children:
                    sc.collection.children.unlink(pc)
            except Exception:
                pass
        # Try removing it; ignore if still used somewhere
        try:
            bpy.data.collections.remove(pc)
        except Exception:
            pass
    except Exception:
        pass


# ---------------------------
# Top-level updater
# ---------------------------

def update_split_preview_plane(context):
    props = getattr(context.scene, "snapsplit", None)
    if props is None:
        return

    obj = context.active_object
    want_show = bool(getattr(props, "show_split_preview", False) and obj and obj.type == 'MESH')

    if not want_show:
        for o in [o for o in bpy.data.objects if o.name.startswith(PREVIEW_PLANE_PREFIX)]:
            for coll in list(o.users_collection):
                try: coll.objects.unlink(o)
                except Exception: pass
            try: bpy.data.objects.remove(o)
            except Exception: pass
        context.scene["_snapsplit_preview_last_obj"] = ""
        context.scene["_snapsplit_preview_last_axis"] = ""
        # also remove the empty preview collection
        _remove_empty_preview_collection()
        return

    last_obj_name = context.scene.get("_snapsplit_preview_last_obj", "")
    last_axis = context.scene.get("_snapsplit_preview_last_axis", "")
    axis = props.split_axis
    parts_count = max(2, int(getattr(props, "parts_count", 2)))
    offset_scene = float(getattr(props, "split_offset_mm", 0.0)) * unit_mm()

    need_rebuild = (obj.name != last_obj_name) or (axis != last_axis)

    position_preview_planes_for_object(context, obj, axis, parts_count, offset_scene, force_rebuild=need_rebuild)

    context.scene["_snapsplit_preview_last_obj"] = obj.name
    context.scene["_snapsplit_preview_last_axis"] = axis

# ---------------------------
# Create cuts with global offset (scene units)
# ---------------------------

def create_cut_data_with_offset(obj, axis, parts_count, global_offset_scene=0.0):
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
# Split performance policy
# ---------------------------

def _should_fill_seams(parts_count: int) -> bool:
    return parts_count <= 6

# ---------------------------
# BMesh-based splitting
# ---------------------------

def split_mesh_bmesh_into_two(source_obj, plane_co_obj, plane_no_obj, name_suffix="", do_fill=True):
    bpy.ops.object.select_all(action='DESELECT')
    source_obj.select_set(True)
    bpy.context.view_layer.objects.active = source_obj

    def make_half(keep_positive: bool):
        bm = bmesh.new()
        bm.from_mesh(source_obj.data)
        geom = bm.verts[:] + bm.edges[:] + bm.faces[:]
        bmesh.ops.bisect_plane(
            bm,
            geom=geom,
            plane_co=plane_co_obj,
            plane_no=plane_no_obj,
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
            o.data.validate(verbose=False); o.data.update()
        except Exception:
            pass

    return o_pos, o_neg

def apply_bmesh_split_sequence(root_obj, axis, parts_count, cuts_override=None, operator=None):
    if cuts_override is None:
        min_v, max_v = world_aabb(root_obj)
        ax = axis_index_for(axis)
        length = max_v[ax] - min_v[ax]
        if length <= 0.0 or parts_count < 2:
            return [root_obj]
        cuts = []
        for i in range(1, parts_count):
            t = i / parts_count
            pos_world = min_v[ax] + t * length
            if axis == "X":
                no_world = Vector((1, 0, 0)); co_world = Vector((pos_world, 0, 0))
            elif axis == "Y":
                no_world = Vector((0, 1, 0)); co_world = Vector((0, pos_world, 0))
            else:
                no_world = Vector((0, 0, 1)); co_world = Vector((0, 0, pos_world))
            cuts.append((co_world, no_world))
    else:
        cuts = cuts_override

    # EXPLICIT BEHAVIOR: fill strictly follows the UI toggle
    props = getattr(bpy.context.scene, "snapsplit", None)
    do_fill = bool(getattr(props, "fill_seams_during_split", False)) if props else False

    wm = bpy.context.window_manager
    wm.progress_begin(0, len(cuts))
    try:
        current_parts = [root_obj]
        for idx, (co_world, no_world) in enumerate(cuts, start=1):
            next_parts = []
            for part in current_parts:
                # Robustheitscheck
                if part is None or part.type != 'MESH' or part.data is None:
                    continue

                # Warnung: unapplied transforms (immer wenn nötig)
                try:
                    warn_if_unapplied_transforms(part, operator=operator)
                except Exception:
                    pass

                # Welt -> Objekt-Raum transformieren (inverse-Transpose für Normalen)
                M = part.matrix_world
                M_inv = M.inverted()
                co_obj = M_inv @ co_world
                no_obj = (M_inv.to_3x3().transposed() @ no_world)
                # Degenerate guard
                if no_obj.length_squared == 0.0:
                    continue
                # Orientierungskorrektur bei negativer Determinante (Spiegelung)
                if M.to_3x3().determinant() < 0.0:
                    no_obj.negate()
                no_obj.normalize()

                a, b = split_mesh_bmesh_into_two(part, co_obj, no_obj, name_suffix=f"_S{idx}", do_fill=do_fill)
                if a and a.type == 'MESH':
                    next_parts.append(a)
                if b and b.type == 'MESH':
                    next_parts.append(b)

            current_parts = [p for p in next_parts if p and p.type == 'MESH' and p.data]

            wm.progress_update(idx)
            try:
                bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
            except Exception:
                pass

        return [o for o in current_parts if o and o.type == 'MESH' and o.data and len(o.data.polygons) > 0]
    finally:
        wm.progress_end()



# ---------------------------
# Interactive operator: Adjust split axis (preview as real object)
# ---------------------------

class SNAP_OT_adjust_split_axis(Operator):
    bl_idname = "snapsplit.adjust_split_axis"
    bl_label = "Adjust split axis" if not is_lang_de() else "Schnittachse anpassen"
    bl_options = {'REGISTER', 'UNDO', 'BLOCKING'}

    def invoke(self, context, event):
        obj = context.active_object
        if not obj or obj.type != 'MESH':
            report_user(self, 'ERROR',
                        "Please select a mesh object.",
                        "Bitte ein Mesh-Objekt auswählen.")
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

        # Initialize modal multi-plane preview for the active object (force rebuild)
        parts_cnt = max(2, int(getattr(self.props, "parts_count", 2)))
        offset_scene = float(getattr(self.props, "split_offset_mm", 0.0)) * unit_mm()
        try:
            position_preview_planes_for_object(context, self.obj, self.axis, parts_cnt, offset_scene, force_rebuild=True)
        except Exception:
            pass

        # Leading plane for immediate feedback
        lead_name = preview_plane_name_for(self.obj.name, 1)
        try:
            self.preview_plane = create_or_get_preview_plane(context, self.obj, self.axis, lead_name)
            self.preview_plane.matrix_world = build_preview_matrix(self.obj, self.axis, self.current_world_pos)
        except Exception:
            self.preview_plane = None

        self._area = context.area; self._region = context.region
        context.window_manager.modal_handler_add(self)

        if self._area: self._area.tag_redraw()
        if self._region:
            try: self._region.tag_redraw()
            except Exception: pass

        return {'RUNNING_MODAL'}

    def finish(self, context, cancelled=False):
        # Keep planes only if persistent preview is enabled
        keep = False
        try:
            keep = bool(getattr(context.scene.snapsplit, "show_split_preview", False))
        except Exception:
            pass

        if not keep:
            # Remove all preview planes
            try:
                for o in [o for o in bpy.data.objects if o.name.startswith(PREVIEW_PLANE_PREFIX)]:
                    for coll in list(o.users_collection):
                        try: coll.objects.unlink(o)
                        except Exception: pass
                    try: bpy.data.objects.remove(o)
                    except Exception: pass
            except Exception:
                pass
            # also remove the empty preview collection
            _remove_empty_preview_collection()

        if self._area: self._area.tag_redraw()
        if self._region:
            try: self._region.tag_redraw()
            except Exception: pass

        if cancelled:
            report_user(self, 'INFO',
                        "Adjust split axis cancelled.",
                        "Schnittachsen-Anpassung abgebrochen.")
        else:
            report_user(self, 'INFO',
                        "Split axis adjusted.",
                        "Schnittachse angepasst.")

    def modal(self, context, event):
        if not self.obj or self.obj.name not in bpy.data.objects:
            self.finish(context, cancelled=True); return {'CANCELLED'}

        if event.type in {'ESC'}:
            self.finish(context, cancelled=True); return {'CANCELLED'}

        updated = False

        # Poll Split Offset (mm) typed in UI and sync preview each tick
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

        # Mouse move: adjust normalized t (vertical movement)
        if event.type == 'MOUSEMOVE':
            dy = event.mouse_prev_y - event.mouse_y
            if dy != 0:
                self.t_norm = max(-1.0, min(1.0, self.t_norm - dy * 0.001))
                self.current_world_pos, _ = world_pos_from_norm(self.obj, self.axis, self.t_norm)
                scene_units_offset = self.current_world_pos - self.mid_world
                self.props.split_offset_mm = float(scene_units_offset) * (1.0 / unit_mm())
                updated = True

        # Wheel / arrow fine steps
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

        # Apply preview movement once if anything changed (works for all inputs)
        if updated:
            # Move the leading plane with a full matrix (centered on active part)
            if getattr(self, "preview_plane", None):
                try:
                    self.preview_plane.matrix_world = build_preview_matrix(self.obj, self.axis, self.current_world_pos)
                except ReferenceError:
                    pass

            # Update all modal preview planes to current offset/axis/parts
            parts_cnt = max(2, int(getattr(self.props, "parts_count", 2)))
            offset_scene = float(getattr(self.props, "split_offset_mm", 0.0)) * unit_mm()
            try:
                position_preview_planes_for_object(context, self.obj, self.axis, parts_cnt, offset_scene)
            except Exception:
                pass

            # Sync persistent preview if enabled
            try:
                if getattr(context.scene.snapsplit, "show_split_preview", False):
                    update_split_preview_plane(context)
            except Exception:
                pass

            if self._area: self._area.tag_redraw()
            if self._region:
                try: self._region.tag_redraw()
                except Exception: pass

        return {'RUNNING_MODAL'}

# ---------------------------
# Operator: Planar Split (uses split_offset_mm)
# ---------------------------

class SNAP_OT_planar_split(Operator):
    bl_idname = "snapsplit.planar_split"
    bl_label = "Planar Split" if not is_lang_de() else "Planarer Schnitt"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.active_object
        if not obj or obj.type != 'MESH':
            report_user(self, 'ERROR',
                        "Please select a mesh object.",
                        "Bitte ein Mesh-Objekt auswählen.")
            return {'CANCELLED'}

        # Vorab-Warnung für nicht angewendete Transformationen
        warn_if_unapplied_transforms(obj, operator=self)

        props = context.scene.snapsplit
        axis = props.split_axis
        count = max(2, int(props.parts_count))

        # Warn for large counts (optional)
        if count >= 12:
            self.report({'INFO'}, f"Splitting into {count} parts can take a while on dense meshes...")

        # Convert user offset (mm) to scene units
        offset_scene = float(getattr(props, "split_offset_mm", 0.0)) * unit_mm()

        # Build offset cuts once
        cuts = create_cut_data_with_offset(obj, axis, count, global_offset_scene=offset_scene)

        parts = apply_bmesh_split_sequence(obj, axis, count, cuts_override=cuts, operator=self)

        if len(parts) < count:
            report_user(self, 'WARNING',
                        f"Fewer parts created than expected ({len(parts)} < {count}).",
                        f"Weniger Teile erstellt als erwartet ({len(parts)} < {count}).")
        else:
            report_user(self, 'INFO',
                        f"{len(parts)} parts created.",
                        f"{len(parts)} Teile erstellt.")

        parts_coll = ensure_collection("_SnapSplit_Parts")
        bpy.ops.object.select_all(action='DESELECT')
        for p in parts:
            if parts_coll not in p.users_collection:
                try:
                    parts_coll.objects.link(p)
                except Exception:
                    pass
            p.hide_set(False)
            p.select_set(True)

        if parts:
            bpy.context.view_layer.objects.active = parts[0]

        # Refresh/remove preview planes depending on toggle and new active object
        try:
            update_split_preview_plane(context)
        except Exception:
            pass

                # Auto-disable split preview after the cut and clean up planes/collection
        try:
            _disable_split_preview_and_cleanup(context)
        except Exception:
            pass

        return {'FINISHED'}


        return {'FINISHED'}

# ---------------------------
# Cap open seams / Seams closing hanlder
# ---------------------------

class SNAP_OT_cap_open_seams_now(Operator):
    bl_idname = "snapsplit.cap_open_seams_now"
    bl_label = "Cap seams now" if not is_lang_de() else "Nähte jetzt schließen"
    bl_description = ("Fill open boundary loops on selected parts (faster than capping during split)"
                      if not is_lang_de() else
                      "Offene Randkanten auf ausgewählten Teilen schließen (schneller als beim Schneiden)")
    bl_options = {'REGISTER', 'UNDO'}

    only_selected: bpy.props.BoolProperty(
        name="Only selected objects" if not is_lang_de() else "Nur ausgewählte Objekte",
        default=True
    )

    def execute(self, context):
        # Collect targets
        if self.only_selected:
            targets = [o for o in context.selected_objects if o.type == 'MESH']
        else:
            # Optionally scan a parts collection
            parts_coll = bpy.data.collections.get("_SnapSplit_Parts")
            targets = list(parts_coll.objects) if parts_coll else []
            targets = [o for o in targets if o and o.type == 'MESH']

        if not targets:
            report_user(self, 'ERROR',
                        "No mesh objects to cap. Select split parts or use the parts collection.",
                        "Keine Mesh-Objekte gefunden. Teile auswählen oder die Teile-Sammlung nutzen.")
            return {'CANCELLED'}

        capped = 0
        for obj in targets:
            try:
                me = obj.data
                bm = bmesh.new()
                bm.from_mesh(me)

                boundary_edges = [e for e in bm.edges if e.is_boundary]
                if boundary_edges:
                    try:
                        bmesh.ops.holes_fill(bm, edges=boundary_edges, sides=0)
                        bm.normal_update()
                        bm.to_mesh(me)
                        me.update()
                        capped += 1
                    except Exception as e:
                        report_user(self, 'WARNING',
                                    f"Cap failed on '{obj.name}': {e}",
                                    f"Schließen fehlgeschlagen bei '{obj.name}': {e}")
                bm.free()
            except Exception as e:
                report_user(self, 'WARNING',
                            f"Processing failed on '{obj.name}': {e}",
                            f"Verarbeitung fehlgeschlagen bei '{obj.name}': {e}")

        report_user(self, 'INFO',
                    f"Capped seams on {capped} object(s).",
                    f"Nähte bei {capped} Objekt(en) geschlossen.")
        return {'FINISHED'}


# ---------------------------
# Depsgraph handler (keeps preview in sync on active-object change)
# ---------------------------

_last_preview_active_obj = None

def _snapsplit_depsgraph_update(scene, depsgraph):
    global _last_preview_active_obj
    props = getattr(scene, "snapsplit", None)
    if not props:
        _last_preview_active_obj = None
        return
    if not getattr(props, "show_split_preview", False):
        _last_preview_active_obj = None
        return

    ctx = bpy.context
    obj = ctx.active_object

    # Update when active object changed
    if obj is not _last_preview_active_obj:
        try:
            update_split_preview_plane(ctx)
        except Exception:
            pass
        _last_preview_active_obj = obj
    else:
        # Optional: also refresh if geometry updates hit the active object
        try:
            if obj:
                for up in depsgraph.updates:
                    id_orig = getattr(up.id, "original", None)
                    if id_orig is obj.data or id_orig is obj:
                        update_split_preview_plane(ctx)
                        break
        except Exception:
            pass

# ---------------------------
# Registration
# ---------------------------

classes = (SNAP_OT_adjust_split_axis, SNAP_OT_planar_split, SNAP_OT_cap_open_seams_now)

def register():
    for c in classes:
        bpy.utils.register_class(c)
    # add depsgraph handler once
    if _snapsplit_depsgraph_update not in bpy.app.handlers.depsgraph_update_post:
        bpy.app.handlers.depsgraph_update_post.append(_snapsplit_depsgraph_update)

def unregister():
    # remove handler
    if _snapsplit_depsgraph_update in bpy.app.handlers.depsgraph_update_post:
        bpy.app.handlers.depsgraph_update_post.remove(_snapsplit_depsgraph_update)
    for c in reversed(classes):
        bpy.utils.unregister_class(c)
