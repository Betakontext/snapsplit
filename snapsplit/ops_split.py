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
# Helpers: BB / axes / preview material / modifier apply / loops
# ---------------------------

def axis_index_for(axis):
    return {"X": 0, "Y": 1, "Z": 2}[axis]

def world_aabb(obj):
    corners = [obj.matrix_world @ Vector(c) for c in obj.bound_box]
    min_v = Vector((min(v.x for v in corners), min(v.y for v in corners), min(v.z for v in corners)))
    max_v = Vector((max(v.x for v in corners), max(v.y for v in corners), max(v.z for v in corners)))
    return min_v, max_v

def aabb_center(min_v, max_v):
    return 0.5 * (min_v + max_v)

def world_pos_from_norm(obj, axis, t_norm):
    min_v, max_v = world_aabb(obj)
    ax = axis_index_for(axis)
    lo = min_v[ax]; hi = max_v[ax]
    mid = 0.5 * (lo + hi); half = 0.5 * (hi - lo)
    return mid + t_norm * half, (lo, hi, mid, half)

def size_on_tangential_axes(obj, axis):
    min_v, max_v = world_aabb(obj)
    ax = axis_index_for(axis)
    t1 = (ax + 1) % 3; t2 = (ax + 2) % 3
    return (abs(max_v[t1] - min_v[t1]), abs(max_v[t2] - min_v[t2])), (t1, t2), (min_v, max_v)

def warn_if_unapplied_transforms(obj, operator=None):
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

def _apply_modifier_with_ops(obj, mod_name):
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    try:
        bpy.ops.object.modifier_apply(modifier=mod_name)
        return True
    except Exception as e:
        print(f"[SnapSplit] Could not apply modifier '{mod_name}': {e}")
        return False

def _is_hollow_like(mod):
    n = (mod.name or "").lower()
    return (mod.type == 'NODES') and ("hollow" in n or "print3d" in n or "print 3d" in n)

def _diag_eps(obj, k=1e-6, min_eps=1e-6):
    min_v, max_v = world_aabb(obj)
    diag = (max_v - min_v).length
    return max(min_eps, diag * k)

def _loops_from_edges_connected(edges):
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
    p = 0.0
    for e in loop:
        v0, v1 = e.verts
        p += (v0.co - v1.co).length
    return p

# ---------------------------
# Preview material/planes
# ---------------------------

def build_orange_preview_material():
    name = PREVIEW_MAT_NAME
    mat = bpy.data.materials.get(name)
    if mat:
        return mat
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
    return ensure_collection(PREVIEW_COLL_NAME)

def create_or_get_preview_plane(context, obj, axis, name):
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
    try:
        plane.color = (1.0, 0.1, 0.1, 1.0)
    except Exception:
        pass
    return plane

def preview_plane_name_for(obj_name: str, idx: int) -> str:
    return f"{PREVIEW_PLANE_PREFIX}{obj_name}_{idx}"

def preview_plane_names_for_object(obj_name: str, parts_count: int):
    n = max(0, int(parts_count) - 1)
    return [preview_plane_name_for(obj_name, i+1) for i in range(n)]

def build_preview_matrix(obj, axis, pos):
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
    tloc = Vector((c.x, c.y, c.z)); tloc[ax] = pos
    T = Matrix.Translation(tloc)
    return T @ R @ S

def position_preview_planes_for_object(context, obj, axis, parts_count, offset_scene, force_rebuild=False):
    if not obj or obj.type != 'MESH':
        return
    obj_name = obj.name
    min_v, max_v = world_aabb(obj); ax = axis_index_for(axis)
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
        try:
            plane.color = (1.0, 0.1, 0.1, 1.0)
        except Exception:
            pass

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
        except Exception:
            pass

def _disable_split_preview_and_cleanup(context):
    try:
        props = getattr(context.scene, "snapsplit", None)
        if props and getattr(props, "show_split_preview", False):
            props.show_split_preview = False
    except Exception:
        pass
    try:
        for o in [o for o in bpy.data.objects if o.name.startswith(PREVIEW_PLANE_PREFIX)]:
            for coll in list(o.users_collection):
                try:
                    coll.objects.unlink(o)
                except Exception: pass
            try:
                bpy.data.objects.remove(o)
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
        _disable_split_preview_and_cleanup(context)
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

    props = getattr(bpy.context.scene, "snapsplit", None)
    do_fill = bool(getattr(props, "fill_seams_during_split", False)) if props else False

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

                M = part.matrix_world
                M_inv = M.inverted()
                co_obj = M_inv @ co_world
                no_obj = (M_inv.to_3x3().transposed() @ no_world)
                if no_obj.length_squared == 0.0:
                    continue
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
        context.window_manager.modal_handler_add(self)

        if self._area: self._area.tag_redraw()
        if self._region:
            try: self._region.tag_redraw()
            except Exception: pass

        return {'RUNNING_MODAL'}

    def finish(self, context, cancelled=False):
        keep = False
        try:
            keep = bool(getattr(context.scene.snapsplit, "show_split_preview", False))
        except Exception:
            pass

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

        report_user(self, 'INFO',
                    "Adjust split axis cancelled." if cancelled else "Split axis adjusted.",
                    "Schnittachsen-Anpassung abgebrochen." if cancelled else "Schnittachse angepasst.")

    def modal(self, context, event):
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
# Operator: Planar Split (uses split_offset_mm) – APPLY MODIFIERS FIRST
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

        warn_if_unapplied_transforms(obj, operator=self)

        # Apply Hollow and optional compatible modifiers BEFORE splitting
        try:
            hollow_mods = [m for m in obj.modifiers if _is_hollow_like(m)]
            for m in reversed(hollow_mods):
                _apply_modifier_with_ops(obj, m.name)
            # optional: weitere typische, mesh-bildende Mods
            for m in list(obj.modifiers):
                if m.name not in obj.modifiers:
                    continue
                if _is_hollow_like(m):
                    continue
                if m.type in {'NODES', 'SUBSURF', 'SOLIDIFY', 'BEVEL', 'MASK', 'TRIANGULATE', 'WELD', 'REMESH'}:
                    _apply_modifier_with_ops(obj, m.name)
            try: obj.data.validate(); obj.data.update()
            except Exception: pass
        except Exception as e:
            print(f"[SnapSplit] Modifier apply pre-step failed: {e}")

        props = context.scene.snapsplit
        axis = props.split_axis
        count = max(2, int(props.parts_count))

        if count >= 12:
            self.report({'INFO'}, f"Splitting into {count} parts can take a while on dense meshes...")

        offset_scene = float(getattr(props, "split_offset_mm", 0.0)) * unit_mm()
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
# Cap seams now – Edit Mode, mehrere Ebenen, Seeds unterstützt
# ---------------------------

class SNAP_OT_cap_open_seams_now(Operator):
    bl_idname = "snapsplit.cap_open_seams_now"
    bl_label = "Cap seams now" if not is_lang_de() else "Nähte jetzt schließen"
    bl_description = ("Per cut plane: select outer+inner rim loops and Alt+F fill (works on multiple planes, uses seeds if present)."
                      if not is_lang_de() else
                      "Pro Schnittebene: Außen- und Innenloop wählen und Alt+F füllen (mehrere Ebenen, nutzt Seeds falls vorhanden).")
    bl_options = {'REGISTER', 'UNDO'}

    only_selected: bpy.props.BoolProperty(
        name="Only selected objects" if not is_lang_de() else "Nur ausgewählte Objekte",
        default=True
    )
    max_planes: bpy.props.IntProperty(
        name="Max planes",
        description="0 = alle erkannten Ebenen, 1 = nur größte Ebene",
        default=0, min=0, soft_max=12
    )

    # ---- Kernlogik ----

    def _cluster_boundary_planes(self, obj, bm):
        bedges = [e for e in bm.edges if e.is_boundary]
        if not bedges:
            return []

        eps_plane = _diag_eps(obj, k=2e-6, min_eps=1e-7)

        items = []
        for e in bedges:
            m = 0.5 * (e.verts[0].co + e.verts[1].co)
            lf = e.link_faces[0] if e.link_faces else None
            n = lf.normal.copy().normalized() if lf else Vector((0, 0, 1))
            items.append((e, m, n))

        planes = []
        for e, c, n in items:
            matched = False
            for pl in planes:
                if abs(n.dot(pl['n'])) > 0.985:
                    d = (c - pl['c']).dot(pl['n'])
                    if abs(d) <= eps_plane:
                        pl['edges'].append(e)
                        pl['c'] = (pl['c'] * 0.9) + (c * 0.1)
                        pl['n'] = ((pl['n'] * 0.9) + (n * 0.1)).normalized()
                        matched = True
                        break
            if not matched:
                planes.append({'c': c, 'n': n, 'edges': [e]})

        planes.sort(key=lambda d: len(d['edges']), reverse=True)
        return [pl['edges'] for pl in planes]

    def _seeds_from_selection(self, bm):
        """
        Nutzt existierende Edit-Mode-Edge-Selektion als Seeds.
        Rückgabe: Liste von (outer_edges_list, inner_edges_list) Paaren pro Ebene,
        wenn genau zwei getrennte Loop-Komponenten in der Selektion gefunden werden.
        """
        sel_edges = [e for e in bm.edges if e.select]
        if len(sel_edges) < 2:
            return []

        comps = _loops_from_edges_connected(sel_edges)
        if len(comps) < 2:
            return []

        comps.sort(key=_perimeter_of_edges, reverse=True)
        # Wir nehmen je zwei Größte als Paar. Falls mehr vorhanden: in 2er-Paketen weitergeben.
        pairs = []
        i = 0
        while i + 1 < len(comps):
            pairs.append((comps[i], comps[i+1]))
            i += 2
        return pairs

    def _expand_selection_to_loop(self):
        try:
            bpy.ops.mesh.loop_multi_select(ring=False)
        except Exception:
            pass

    def _fill_like_altf(self):
        try:
            bpy.ops.mesh.fill(use_beauty=True)
            return True
        except Exception:
            try:
                bpy.ops.mesh.fill_grid()
                return True
            except Exception:
                return False

    def _cap_object_on_planes(self, obj, max_planes=0) -> bool:
        """
        Falls Seeds existieren: benutze sie.
        Sonst: automatische Erkennung pro Ebene und Füllen je Außen/Innen-Paar.
        """
        bpy.ops.object.select_all(action='DESELECT')
        obj.select_set(True)
        bpy.context.view_layer.objects.active = obj
        if obj.mode != 'EDIT':
            bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='EDGE')

        bm = bmesh.from_edit_mesh(obj.data)
        bm.verts.ensure_lookup_table(); bm.edges.ensure_lookup_table(); bm.faces.ensure_lookup_table()

        # 1) Seed-gestützt?
        seed_pairs = self._seeds_from_selection(bm)
        if seed_pairs:
            filled_any = False
            for outer_loop, inner_loop in seed_pairs:
                # Außen selektieren
                for e in bm.edges: e.select = False
                for e in outer_loop: e.select = True
                bmesh.update_edit_mesh(obj.data, False, False)
                self._expand_selection_to_loop()
                # Shift-Add Innen
                for e in inner_loop: e.select = True
                bmesh.update_edit_mesh(obj.data, False, False)
                self._expand_selection_to_loop()
                # Fill
                ok = self._fill_like_altf()
                filled_any |= ok
            bpy.ops.object.mode_set(mode='OBJECT')
            try:
                obj.data.validate(); obj.data.update()
            except Exception:
                pass
            return filled_any

        # 2) Automatik (alle Ebenen)
        plane_groups = self._cluster_boundary_planes(obj, bm)
        if not plane_groups:
            bpy.ops.object.mode_set(mode='OBJECT')
            return False

        processed = 0
        filled_all = True

        for edges_on_plane in plane_groups:
            if max_planes and processed >= max_planes:
                break

            comps = _loops_from_edges_connected(edges_on_plane)
            # Erwartet mindestens 2 (Außen/Innen) pro Teil. Es können aber auch 4 total sein (oben+unten).
            if len(comps) < 2:
                filled_all = False
                continue

            # Sortieren nach Umfang
            comps.sort(key=_perimeter_of_edges, reverse=True)

            # Strategie: Wir gehen paarweise vor: (0,1), (2,3), ...
            i = 0
            plane_ok = True
            while i + 1 < len(comps):
                outer_loop = comps[i]
                inner_loop = comps[i+1]

                # Außen selektieren
                for e in bm.edges: e.select = False
                for e in outer_loop: e.select = True
                bmesh.update_edit_mesh(obj.data, False, False)
                self._expand_selection_to_loop()

                # Innen addieren
                for e in inner_loop: e.select = True
                bmesh.update_edit_mesh(obj.data, False, False)
                self._expand_selection_to_loop()

                ok = self._fill_like_altf()
                plane_ok = plane_ok and ok
                i += 2

            filled_all = filled_all and plane_ok
            processed += 1

        bpy.ops.object.mode_set(mode='OBJECT')
        try:
            obj.data.validate(); obj.data.update()
        except Exception:
            pass
        return filled_all and processed > 0

    def execute(self, context):
        if self.only_selected:
            targets = [o for o in context.selected_objects if o.type == 'MESH']
        else:
            parts_coll = bpy.data.collections.get("_SnapSplit_Parts")
            targets = [o for o in (list(parts_coll.objects) if parts_coll else []) if o and o.type == 'MESH']

        if not targets:
            report_user(self, 'ERROR',
                        "No mesh objects to cap. Select split parts or use the parts collection.",
                        "Keine Mesh-Objekte gefunden. Teile auswählen oder die Teile-Sammlung nutzen.")
            return {'CANCELLED'}

        capped = 0
        for obj in targets:
            try:
                if self._cap_object_on_planes(obj, max_planes=self.max_planes):
                    capped += 1
            except Exception as e:
                report_user(self, 'WARNING',
                            f"Processing failed on '{obj.name}': {e}",
                            f"Verarbeitung fehlgeschlagen bei '{obj.name}': {e}")

        if capped == 0:
            report_user(self, 'WARNING',
                        "Could not determine and fill rim loops on selected objects.",
                        "Rand-Loops konnten nicht ermittelt/gefüllt werden.")
        else:
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

    if obj is not _last_preview_active_obj:
        try:
            update_split_preview_plane(ctx)
        except Exception:
            pass
        _last_preview_active_obj = obj
    else:
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
    if _snapsplit_depsgraph_update not in bpy.app.handlers.depsgraph_update_post:
        bpy.app.handlers.depsgraph_update_post.append(_snapsplit_depsgraph_update)

def unregister():
    if _snapsplit_depsgraph_update in bpy.app.handlers.depsgraph_update_post:
        bpy.app.handlers.depsgraph_update_post.remove(_snapsplit_depsgraph_update)
    for c in reversed(classes):
        bpy.utils.unregister_class(c)
