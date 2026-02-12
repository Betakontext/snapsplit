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
import bmesh
from bpy.types import Operator
from mathutils import Vector
from .utils import ensure_collection, obj_world_bb, report_user

# ---------------------------
# BMesh-based core split
# ---------------------------

def split_mesh_bmesh_into_two(source_obj, plane_co_obj, plane_no_obj, name_suffix=""):
    """
    Split 'source_obj' by a plane (given in source_obj's local space).
    Creates two new meshes:
      - POS: geometry on the positive side of the plane normal
      - NEG: geometry on the negative side
    Returns two new OBJECTS. The source object is hidden (not deleted).
    """
    # Make sure source is active/selected for dependable data access
    bpy.ops.object.select_all(action='DESELECT')
    source_obj.select_set(True)
    bpy.context.view_layer.objects.active = source_obj

    # Do NOT apply transforms destructively here; we convert plane into local space instead.
    # Build halves via BMesh
    def make_half(keep_positive: bool):
        bm = bmesh.new()
        bm.from_mesh(source_obj.data)
        geom = bm.verts[:] + bm.edges[:] + bm.faces[:]

        # Bisect and clear one side
        bmesh.ops.bisect_plane(
            bm,
            geom=geom,
            plane_co=plane_co_obj,
            plane_no=plane_no_obj,
            use_snap_center=False,
            clear_outer=not keep_positive,   # delete "negative" side relative to normal
            clear_inner=keep_positive        # delete "positive" side
        )

        # Cap the open cut edges to keep the halves manifold if possible
        boundary_edges = [e for e in bm.edges if e.is_boundary]
        if boundary_edges:
            try:
                bmesh.ops.holes_fill(bm, edges=boundary_edges, sides=0)
            except Exception:
                # If fill fails, we still keep the split result
                pass

        bm.normal_update()

        me = bpy.data.meshes.new(f"{source_obj.name}_{'POS' if keep_positive else 'NEG'}{name_suffix}")
        bm.to_mesh(me)
        bm.free()
        return me

    me_pos = make_half(True)
    me_neg = make_half(False)

    # Link new objects alongside the source object's first collection (or scene collection)
    target_coll = source_obj.users_collection[0] if source_obj.users_collection else bpy.context.scene.collection
    o_pos = bpy.data.objects.new(f"{source_obj.name}_A{name_suffix}", me_pos)
    o_neg = bpy.data.objects.new(f"{source_obj.name}_B{name_suffix}", me_neg)
    target_coll.objects.link(o_pos)
    target_coll.objects.link(o_neg)

    # Inherit world transform so the halves stay in place
    o_pos.matrix_world = source_obj.matrix_world.copy()
    o_neg.matrix_world = source_obj.matrix_world.copy()

    # Hide the source so only results remain visible
    source_obj.hide_set(True)

    # Validate/update result meshes
    for o in (o_pos, o_neg):
        try:
            o.data.validate(verbose=False)
            o.data.update()
        except Exception:
            pass

    return o_pos, o_neg

# ---------------------------
# Plane data from world-space BB
# ---------------------------

def create_cut_data(obj, axis, parts_count):
    """
    Returns a list of world-space cutting planes (co_world, no_world) for
    evenly spaced cuts along the object's bounding-box axis.
    """
    min_v, max_v = obj_world_bb(obj)
    axis_index = {"X": 0, "Y": 1, "Z": 2}[axis]
    length = max_v[axis_index] - min_v[axis_index]
    if length <= 0.0 or parts_count < 2:
        return []

    cuts = []
    for i in range(1, parts_count):
        t = i / parts_count
        pos_world = min_v[axis_index] + t * length
        if axis == "X":
            no_world = Vector((1, 0, 0))
            co_world = Vector((pos_world, 0, 0))
        elif axis == "Y":
            no_world = Vector((0, 1, 0))
            co_world = Vector((0, pos_world, 0))
        else:
            no_world = Vector((0, 0, 1))
            co_world = Vector((0, 0, pos_world))
        cuts.append((co_world, no_world))
    return cuts

# ---------------------------
# Split sequence across parts
# ---------------------------

def apply_bmesh_split_sequence(root_obj, axis, parts_count):
    """
    Perform a sequence of BMesh splits across the active set of parts.
    After each plane, all current parts are split again by the next plane.
    This allows recursive splitting (e.g., taking a half and splitting it again).
    """
    cuts = create_cut_data(root_obj, axis, parts_count)
    if not cuts:
        return [root_obj]

    # Start with the provided object only (visible or not)
    current_parts = [root_obj]

    for idx, (co_world, no_world) in enumerate(cuts, start=1):
        next_parts = []
        for part in current_parts:
            # Convert world plane into this part's local space
            M = part.matrix_world
            M_inv = M.inverted()
            co_obj = M_inv @ co_world
            no_obj = (M_inv.to_3x3().transposed() @ no_world).normalized()

            # Split part into two new objects (this hides 'part')
            a, b = split_mesh_bmesh_into_two(part, co_obj, no_obj, name_suffix=f"_S{idx}")
            next_parts.extend([a, b])

        # Continue with the newly created parts for the next cut
        current_parts = [p for p in next_parts if p and p.type == 'MESH']

    # Return only valid mesh objects with faces
    valid = [o for o in current_parts if o and o.type == 'MESH' and o.data and len(o.data.polygons) > 0]
    return valid

# ---------------------------
# Operator
# ---------------------------

class SNAP_OT_planar_split(Operator):
    bl_idname = "snapsplit.planar_split"
    bl_label = "Planar Split"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.active_object
        if not obj or obj.type != 'MESH':
            report_user(self, 'ERROR', "Please select a mesh object.")
            return {'CANCELLED'}

        props = context.scene.snapsplit
        axis = props.split_axis
        count = max(2, int(props.parts_count))

        # Important: Work on the selected (possibly already-split) object directly.
        # This supports recursive splits: select any resulting half and run again.
        parts = apply_bmesh_split_sequence(obj, axis, count)

        if len(parts) < count:
            report_user(self, 'WARNING', f"Fewer parts created than expected ({len(parts)} < {count}).")
        else:
            report_user(self, 'INFO', f"{len(parts)} parts created.")

        # Organize in collection and select
        parts_coll = ensure_collection("_SnapSplit_Parts")
        bpy.ops.object.select_all(action='DESELECT')
        for p in parts:
            if parts_coll not in p.users_collection:
                parts_coll.objects.link(p)
            p.hide_set(False)
            p.select_set(True)

        if parts:
            bpy.context.view_layer.objects.active = parts[0]

        return {'FINISHED'}

classes = (SNAP_OT_planar_split,)

def register():
    for c in classes:
        bpy.utils.register_class(c)

def unregister():
    for c in reversed(classes):
        bpy.utils.unregister_class(c)

