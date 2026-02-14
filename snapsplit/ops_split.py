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
    obj_world_bb,
    report_user,
    is_lang_de,
    unit_mm,
)

# ---------------------------
# Preview naming
# ---------------------------

PREVIEW_COLL_NAME = "_SnapSplit_Preview"
PREVIEW_PLANE_PREFIX = "_SnapSplit_PreviewPlane_"  # numbered planes
PREVIEW_MAT_NAME = "_SnapSplit_Preview_MAT"

# ---------------------------
# Helpers: BB / axes / preview material
# ---------------------------

def axis_index_for(axis):
    return {"X": 0, "Y": 1, "Z": 2}[axis]

def world_pos_from_norm(obj, axis, t_norm):
    """
    Map normalized t_norm in [-1,1] to world position along object's AABB on 'axis'.
    Returns (pos, (lo, hi, mid, half)).
    """
    min_v, max_v = obj_world_bb(obj)
    ax = axis_index_for(axis)
    lo = min_v[ax]
    hi = max_v[ax]
    mid = 0.5 * (lo + hi)
    half = 0.5 * (hi - lo)
    return mid + t_norm * half, (lo, hi, mid, half)

def size_on_tangential_axes(obj, axis):
    """
    Return extents (size_t1, size_t2) and tangential axis indices (t1, t2).
    """
    min_v, max_v = obj_world_bb(obj)
    ax = axis_index_for(axis)
    t1 = (ax + 1) % 3
    t2 = (ax + 2) % 3
    return (abs(max_v[t1] - min_v[t1]), abs(max_v[t2] - min_v[t2])), (t1, t2), (min_v, max_v)

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
    Create (or reuse) a plane object aligned to the split axis, scaled to BB tangential extents.
    Local Z points along the split axis; local X,Y span the tangential AABB axes.
    """
    coll = ensure_preview_collection()
    plane = bpy.data.objects.get(name)
    if plane is None or plane.type != 'MESH':
        me = bpy.data.meshes.new(name)
        bm = bmesh.new()
        # Unit plane in XY (normal +Z)
        bmesh.ops.create_grid(bm, x_segments=1, y_segments=1, size=0.5)  # 1x1
        bm.to_mesh(me); bm.free()
        plane = bpy.data.objects.new(name, me)
        coll.objects.link(plane)

    # Material
    mat = build_orange_preview_material()
    if not plane.data.materials:
        plane.data.materials.append(mat)
    else:
        plane.data.materials[0] = mat

    # Extents and tangential indices from AABB
    (size_t1, size_t2), (t1_idx, t2_idx), _ = size_on_tangential_axes(obj, axis)

    # World basis axes
    world_axes = (Vector((1,0,0)), Vector((0,1,0)), Vector((0,0,1)))

    # z_dir = split axis (plane normal)
    z_dir = world_axes[axis_index_for(axis)].copy().normalized()
    # x_dir = first tangential axis
    x_dir = world_axes[t1_idx].copy().normalized()
    # If nearly parallel, switch to second tangential axis
    if abs(z_dir.dot(x_dir)) > 0.999:
        x_dir = world_axes[t2_idx].copy().normalized()
    # y_dir orthogonal completion
    y_dir = z_dir.cross(x_dir)
    if y_dir.length_squared == 0.0:
        x_dir = world_axes[t2_idx].copy().normalized()
        y_dir = z_dir.cross(x_dir)
    y_dir.normalize()
    # Re-orthogonalize x_dir
    x_dir = y_dir.cross(z_dir); x_dir.normalize()

    # Build 4x4 with columns (x,y,z)
    R = Matrix((
        (x_dir.x, y_dir.x, z_dir.x, 0.0),
        (x_dir.y, y_dir.y, z_dir.y, 0.0),
        (x_dir.z, y_dir.z, z_dir.z, 0.0),
        (0.0,     0.0,     0.0,     1.0),
    ))
    # Scale in local plane: X=size_t1, Y=size_t2
    S = Matrix.Diagonal(Vector((max(size_t1, 1e-9), max(size_t2, 1e-9), 1.0, 1.0)))

    plane.matrix_world = R @ S

    plane.hide_set(False)
    plane.hide_viewport = False
    plane.show_in_front = True
    plane.display_type = 'TEXTURED'
    return plane

def set_preview_plane_position(plane, obj, axis, world_pos):
    """
    Sets the plane's world translation so that its local Z (aligned to split axis) sits at world_pos.
    """
    M = plane.matrix_world.copy()
    current_origin = Vector((M[0][3], M[1][3], M[2][3]))
    new_loc = list(current_origin)
    ax = axis_index_for(axis)
    new_loc[ax] = world_pos
    M[0][3], M[1][3], M[2][3] = new_loc[0], new_loc[1], new_loc[2]
    plane.matrix_world = M

def preview_plane_names_for(parts_count):
    # Number of cuts is parts_count - 1
    n = max(0, int(parts_count) - 1)
    return [f"{PREVIEW_PLANE_PREFIX}{i+1}" for i in range(n)]

def position_preview_planes_for_object(context, obj, axis, parts_count, offset_scene):
    """
    Create/update multiple preview planes (one per planned cut) on current object.
    Orients/scales each plane to object AABB tangents; positions each at its cut world position.
    Removes any excess planes if parts_count decreased.
    """
    min_v, max_v = obj_world_bb(obj)
    ax = axis_index_for(axis)
    length = max_v[ax] - min_v[ax]

    targets = []
    if length > 0.0 and parts_count >= 2:
        for i in range(1, parts_count):
            t = i / parts_count
            pos = min_v[ax] + t * length + offset_scene
            pos = max(min_v[ax], min(max_v[ax], pos))  # clamp
            targets.append(pos)

    want_names = preview_plane_names_for(parts_count)

    # Ensure/create or update planes for each target position
    for name, pos in zip(want_names, targets):
        plane = bpy.data.objects.get(name) or create_or_get_preview_plane(context, obj, axis, name)
        # Verify alignment; if misaligned (axis changed), rebuild
        z_world = Vector((plane.matrix_world[0][2], plane.matrix_world[1][2], plane.matrix_world[2][2])).normalized()
        axis_vec = Vector((1,0,0)) if axis == "X" else (Vector((0,1,0)) if axis == "Y" else Vector((0,0,1)))
        if z_world.dot(axis_vec) < 0.999:
            for coll in list(plane.users_collection):
                try: coll.objects.unlink(plane)
                except Exception: pass
            try: bpy.data.objects.remove(plane)
            except Exception: pass
            plane = create_or_get_preview_plane(context, obj, axis, name)

        set_preview_plane_position(plane, obj, axis, pos)
        plane.hide_set(False)
        plane.hide_viewport = False
        plane.show_in_front = True

    # Remove any extra preview planes not needed now
    all_existing = [o for o in bpy.data.objects if o.name.startswith(PREVIEW_PLANE_PREFIX)]
    for o in all_existing:
        if o.name not in want_names:
            for coll in list(o.users_collection):
                try: coll.objects.unlink(o)
                except Exception: pass
            try: bpy.data.objects.remove(o)
            except Exception: pass

# ---------------------------
# Top-level updater so profiles.py and handlers can call it
# ---------------------------

def update_split_preview_plane(context):
    """
    Create/update/remove the preview plane(s) based on current props and active object.
    Creates one plane per planned cut (parts_count-1).
    Removes any leftover planes when preview is disabled or no valid object.
    """
    props = getattr(context.scene, "snapsplit", None)
    if props is None:
        return

    obj = context.active_object
    want_show = bool(getattr(props, "show_split_preview", False) and obj and obj.type == 'MESH')

    # If no preview wanted or no valid mesh, remove all preview planes
    if not want_show:
        for o in [o for o in bpy.data.objects if o.name.startswith(PREVIEW_PLANE_PREFIX)]:
            for coll in list(o.users_collection):
                try: coll.objects.unlink(o)
                except Exception: pass
            try: bpy.data.objects.remove(o)
            except Exception: pass
        # Clear tracking
        context.scene["_snapsplit_preview_last_obj"] = ""
        context.scene["_snapsplit_preview_last_axis"] = ""
        return

    # Track which object/axis we last used
    last_obj_name = context.scene.get("_snapsplit_preview_last_obj", "")
    last_axis = context.scene.get("_snapsplit_preview_last_axis", "")
    axis = props.split_axis
    parts_count = max(2, int(getattr(props, "parts_count", 2)))
    offset_scene = float(getattr(props, "split_offset_mm", 0.0)) * unit_mm()

    # If object or axis changed, easiest: drop all planes and rebuild
    need_rebuild = (obj.name != last_obj_name) or (axis != last_axis)
    if need_rebuild:
        for o in [o for o in bpy.data.objects if o.name.startswith(PREVIEW_PLANE_PREFIX)]:
            for coll in list(o.users_collection):
                try: coll.objects.unlink(o)
                except Exception: pass
            try: bpy.data.objects.remove(o)
            except Exception: pass

    # Create/update all planes for current state
    position_preview_planes_for_object(context, obj, axis, parts_count, offset_scene)

    # Persist tracking
    context.scene["_snapsplit_preview_last_obj"] = obj.name
    context.scene["_snapsplit_preview_last_axis"] = axis

# ---------------------------
# Create cuts with global offset (scene units)
# ---------------------------

def create_cut_data_with_offset(obj, axis, parts_count, global_offset_scene=0.0):
    min_v, max_v = obj_world_bb(obj)
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
# BMesh-based splitting
# ---------------------------

def split_mesh_bmesh_into_two(source_obj, plane_co_obj, plane_no_obj, name_suffix=""):
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

def apply_bmesh_split_sequence(root_obj, axis, parts_count, cuts_override=None):
    if cuts_override is None:
        min_v, max_v = obj_world_bb(root_obj)
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

    current_parts = [root_obj]
    for idx, (co_world, no_world) in enumerate(cuts, start=1):
        next_parts = []
        for part in current_parts:
            M = part.matrix_world; M_inv = M.inverted()
            co_obj = M_inv @ co_world
            no_obj = (M_inv.to_3x3().transposed() @ no_world).normalized()
            a, b = split_mesh_bmesh_into_two(part, co_obj, no_obj, name_suffix=f"_S{idx}")
            next_parts.extend([a, b])
        current_parts = [p for p in next_parts if p and p.type == 'MESH']

    return [o for o in current_parts if o and o.type == 'MESH' and o.data and len(o.data.polygons) > 0]

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

        self.obj = obj
        self.props = context.scene.snapsplit
        self.axis = self.props.split_axis

        min_v, max_v = obj_world_bb(obj)
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

        # Modale Vorschau initialisieren:
        parts_cnt = max(2, int(getattr(self.props, "parts_count", 2)))
        offset_scene = float(getattr(self.props, "split_offset_mm", 0.0)) * unit_mm()

        if getattr(context.scene.snapsplit, "show_split_preview", False):
            # Persistente (globale) Vorschau ist aktiv -> zentrale Multi-Vorschau aufziehen
            try:
                position_preview_planes_for_object(context, self.obj, self.axis, parts_cnt, offset_scene)
            except Exception:
                pass
        else:
            # Checkbox aus -> modale, temporäre Multi-Vorschau selbst aufbauen (x-1 Ebenen)
            try:
                position_preview_planes_for_object(context, self.obj, self.axis, parts_cnt, offset_scene)
            except Exception:
                pass

        # Zusätzlich eine "führende" Ebene merken, um bei Mausbewegung sofort zu verschieben
        lead_name = f"{PREVIEW_PLANE_PREFIX}1"
        try:
            self.preview_plane = create_or_get_preview_plane(context, self.obj, self.axis, lead_name)
            set_preview_plane_position(self.preview_plane, self.obj, self.axis, self.current_world_pos)
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
        # Nur löschen, wenn persistente Vorschau deaktiviert ist
        keep = False
        try:
            keep = bool(getattr(context.scene.snapsplit, "show_split_preview", False))
        except Exception:
            pass

        if not keep:
            # Alle temporären Preview-Planes (mit Prefix) entfernen
            try:
                for o in [o for o in bpy.data.objects if o.name.startswith(PREVIEW_PLANE_PREFIX)]:
                    for coll in list(o.users_collection):
                        try: coll.objects.unlink(o)
                        except Exception: pass
                    try: bpy.data.objects.remove(o)
                    except Exception: pass
            except Exception:
                pass

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
                self.t_norm = max(-1.0, min(1.0, self.t_norm + dy * 0.001))
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
            # Ensure leading plane exists; recreate if it was removed externally
            plane_ok = False
            if getattr(self, "preview_plane", None):
                try:
                    _ = self.preview_plane.matrix_world
                    plane_ok = True
                except ReferenceError:
                    plane_ok = False
            if not plane_ok:
                lead_name = f"{PREVIEW_PLANE_PREFIX}1"
                try:
                    self.preview_plane = create_or_get_preview_plane(context, self.obj, self.axis, lead_name)
                except Exception:
                    self.preview_plane = None

            # Move the leading plane if available
            if getattr(self, "preview_plane", None):
                try:
                    set_preview_plane_position(self.preview_plane, self.obj, self.axis, self.current_world_pos)
                except ReferenceError:
                    pass

            # Update all modal preview planes to current offset/axis/parts
            parts_cnt = max(2, int(getattr(self.props, "parts_count", 2)))
            offset_scene = float(getattr(self.props, "split_offset_mm", 0.0)) * unit_mm()
            try:
                position_preview_planes_for_object(context, self.obj, self.axis, parts_cnt, offset_scene)
            except Exception:
                pass

            # Only if persistent preview is enabled, update the global multi-plane preview state as well
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

        props = context.scene.snapsplit
        axis = props.split_axis
        count = max(2, int(props.parts_count))

        # Convert user offset (mm) to scene units
        offset_scene = float(getattr(props, "split_offset_mm", 0.0)) * unit_mm()

        # Build offset cuts once
        cuts = create_cut_data_with_offset(obj, axis, count, global_offset_scene=offset_scene)

        parts = apply_bmesh_split_sequence(obj, axis, count, cuts_override=cuts)

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

classes = (SNAP_OT_adjust_split_axis, SNAP_OT_planar_split)

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
