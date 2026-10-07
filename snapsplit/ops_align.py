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

# ops_align.py

import bpy
import bmesh
from bpy.types import Operator
from mathutils import Vector, Matrix
from bpy_extras import view3d_utils

from .utils import report_user
from .utils import _trf

_FACE_TO_FACE_LOCAL_FLIP = True


# ---------------------------
# Raycast and math utilities
# ---------------------------

def _raycast_pick_face(context, event):
    """
    Raycast from mouse cursor to get (obj, hit_position, hit_normal_world, face_index) for mesh faces.
    Returns None if no face is hit or not in a 3D View.
    """
    if context.space_data is None or context.space_data.type != 'VIEW_3D':
        return None

    region = context.region
    rv3d = context.space_data.region_3d
    co2d = Vector((event.mouse_region_x, event.mouse_region_y))

    ray_origin = view3d_utils.region_2d_to_origin_3d(region, rv3d, co2d)
    ray_dir = view3d_utils.region_2d_to_vector_3d(region, rv3d, co2d).normalized()

    depsgraph = context.evaluated_depsgraph_get()
    scene = context.scene

    hit, loc, norm, face_index, obj, _ = scene.ray_cast(depsgraph, ray_origin, ray_dir, distance=1e6)
    if not hit or not obj or obj.type != 'MESH' or face_index < 0:
        return None

    # norm from scene.ray_cast is already world-space
    return obj, loc, norm.normalized(), face_index


def _object_face_frame_world(obj, face_index):
    """
    Compute a stable face frame in world space:
    - z_world: face normal (world)
    - x_world: robust in-plane tangent from averaged projected edges; fallback projects a world axis
    - y_world: z x x (right-handed)
    """
    me = obj.data
    if face_index < 0 or face_index >= len(me.polygons):
        raise ValueError("Invalid face index")
    poly = me.polygons[face_index]

    origin = obj.matrix_world @ poly.center

    # Normal (world) via inverse-transpose
    n_local = poly.normal
    N = obj.matrix_world.to_3x3().inverted().transposed()
    z_world = (N @ n_local).normalized()

    Mw3 = obj.matrix_world.to_3x3()

    # Robust tangent: average all edge directions projected into the face plane
    verts = me.vertices
    idxs = poly.vertices
    tan = Vector((0.0, 0.0, 0.0))
    for i in range(len(idxs)):
        v0 = verts[idxs[i]].co
        v1 = verts[(idxs[(i + 1) % len(idxs)])].co
        e = Mw3 @ (v1 - v0)
        e_proj = e - e.dot(z_world) * z_world
        if e_proj.length_squared > 1e-16:
            tan += e_proj.normalized()

    if tan.length_squared <= 1e-16:
        # Fallback: project world +X (or +Y if near parallel) into plane
        ref = Vector((1, 0, 0))
        if abs(ref.dot(z_world)) > 0.9:
            ref = Vector((0, 1, 0))
        tan = (ref - ref.dot(z_world) * z_world)

    x_world = tan.normalized()
    y_world = z_world.cross(x_world).normalized()
    x_world = y_world.cross(z_world).normalized()

    R = Matrix((x_world, y_world, z_world)).transposed()  # columns as axes
    return origin, R


def _make_frame_matrix(origin, R):
    """Build a 4x4 matrix from origin and a 3x3 rotation/axes matrix."""
    M = Matrix.Identity(4)
    M[0][0], M[0][1], M[0][2] = R[0][0], R[0][1], R[0][2]
    M[1][0], M[1][1], M[1][2] = R[1][0], R[1][1], R[1][2]
    M[2][0], M[2][1], M[2][2] = R[2][0], R[2][1], R[2][2]
    M.translation = origin
    return M


# ---------------------------
# Selection helpers (RNA / BMesh only, no selection operators)
# ---------------------------

def _deselect_all_objects():
    """Deselect all objects of the current view layer via RNA (replaces bpy.ops.object.select_all)."""
    try:
        for o in list(bpy.context.view_layer.objects):
            try:
                # select_set() can raise for objects that cannot be selected (e.g. hidden); ignore
                o.select_set(False)
            except Exception:
                pass
    except Exception:
        pass


def _bm_clear_selection(bm):
    """Deselect every vertex, edge and face of an edit BMesh (replaces bpy.ops.mesh.select_all)."""
    for f in bm.faces:
        f.select_set(False)
    for e in bm.edges:
        e.select_set(False)
    for v in bm.verts:
        v.select_set(False)
    try:
        bm.select_history.clear()
    except Exception:
        pass


def _edit_bmesh_deselect_all(obj):
    """Deselect all elements of obj's live edit BMesh and flush to the viewport.

    Returns True on success, False if obj is not in Edit Mode or BMesh access failed.
    """
    if not obj or obj.type != 'MESH' or obj.mode != 'EDIT':
        return False
    try:
        bm = bmesh.from_edit_mesh(obj.data)
        # Keep the BMesh itself in face select mode (matches the tool setting)
        bm.select_mode = {'FACE'}
        _bm_clear_selection(bm)
        bmesh.update_edit_mesh(obj.data, loop_triangles=False, destructive=False)
        return True
    except Exception:
        return False


def _set_face_select_mode_tool_setting():
    """Set FACE select mode via tool settings (must happen BEFORE entering Edit Mode)."""
    try:
        bpy.context.tool_settings.mesh_select_mode = (False, False, True)
    except Exception:
        pass


# ---------------------------
# Highlight utilities (persistent until alignment) — BMesh based
# ---------------------------

def _ensure_multi_object_edit(obj_list):
    """
    Ensure all provided mesh objects are selected and in Edit Mode together,
    set face select mode, and clear edit selection so the next face selection is visible.
    """
    if not obj_list:
        return

    objs = [o for o in dict.fromkeys(obj_list) if o and o.type == 'MESH']
    if not objs:
        return

    view_layer = bpy.context.view_layer

    # Deselect all objects (RNA), then select targets
    _deselect_all_objects()
    for o in objs:
        try:
            o.select_set(True)
        except Exception:
            pass

    # Set an active object
    try:
        view_layer.objects.active = objs[0]
    except Exception:
        pass

    # Face select mode through tool settings; the edit mesh is created with this mode,
    # so bpy.ops.mesh.select_mode(type='FACE') is no longer needed.
    _set_face_select_mode_tool_setting()

    # Enter Edit Mode (multi-object). No public non-operator equivalent exists.
    try:
        bpy.ops.object.mode_set(mode='EDIT')
    except Exception:
        return

    # Clear existing edit selection on every edit mesh (replaces mesh.select_all DESELECT,
    # which only worked on the meshes the operator context happened to cover).
    for o in objs:
        _edit_bmesh_deselect_all(o)


def _select_single_face(obj, face_index):
    """
    Select only the specified face on obj using the live Edit BMesh and flush immediately.
    Ensures obj is the active edit object while changing its selection so the viewport shows orange.
    """
    if not obj or obj.type != 'MESH' or face_index < 0:
        return
    me = obj.data
    if not (0 <= face_index < len(me.polygons)):
        return

    view_layer = bpy.context.view_layer
    prev_active = view_layer.objects.active

    # 1) Make obj active and ensure we're in Edit Mode (multi-object edit supported)
    try:
        obj.select_set(True)
        view_layer.objects.active = obj
    except Exception:
        pass
    if obj.mode != 'EDIT':
        _set_face_select_mode_tool_setting()
        try:
            bpy.ops.object.mode_set(mode='EDIT')
        except Exception:
            return

    # 2) Operate directly on the live edit BMesh (obj is in Edit Mode here)
    try:
        bm = bmesh.from_edit_mesh(me)
    except Exception:
        # No BMesh available: nothing sensible left to do without selection operators
        return

    # Face select mode on the BMesh itself (replaces bpy.ops.mesh.select_mode(type='FACE'))
    bm.select_mode = {'FACE'}

    # Lookup tables are required for index access on BMesh sequences
    bm.verts.ensure_lookup_table()
    bm.edges.ensure_lookup_table()
    bm.faces.ensure_lookup_table()

    # Clear selection on this mesh, then select target face
    _bm_clear_selection(bm)

    bm_face = None
    try:
        bm_face = bm.faces[face_index]
    except Exception:
        # Fallback: match by vertex index set (only valid while topology is unchanged)
        bm.verts.index_update()
        poly_verts = set(me.polygons[face_index].vertices)
        for f in bm.faces:
            if set(v.index for v in f.verts) == poly_verts:
                bm_face = f
                break
    if bm_face is None:
        return

    # select_set(True) also selects the face's edges and vertices
    bm_face.select_set(True)

    # 3) Flush to viewport (replaces the old EDGE/FACE select_mode toggle trick)
    bm.select_flush_mode()
    try:
        bmesh.update_edit_mesh(me, loop_triangles=False, destructive=False)
    except Exception:
        try:
            me.update()
        except Exception:
            pass

    # 4) Optionally restore previous active edit object if it differs
    try:
        if prev_active and prev_active != obj and prev_active.type == 'MESH' and prev_active.select_get():
            view_layer.objects.active = prev_active
    except Exception:
        pass


def _highlight_picked_face_persistent(objA, idxA, objB=None, idxB=-1):
    """
    Keep highlights for A (and optionally B) by ensuring both are in multi-object Edit Mode
    and their faces are selected. Call this after each pick.
    """
    objs = [objA] + ([objB] if (objB and objB != objA) else [])
    _ensure_multi_object_edit(objs)

    # Re-assert selections (entering Edit Mode can clear selection)
    _select_single_face(objA, idxA)
    if objB and objB != objA and idxB >= 0:
        _select_single_face(objB, idxB)

# ---------------------------
# Pick storage (PropertyGroup on WindowManager)
# ---------------------------

class SNAP_PG_picks(bpy.types.PropertyGroup):
    """Stores the picked Face A (target) and Face B (moving) for the align tool."""

    face_a_obj: bpy.props.StringProperty(name='Face A Object')
    face_a_index: bpy.props.IntProperty(name='Face A Index', default=-1)
    face_b_obj: bpy.props.StringProperty(name='Face B Object')
    face_b_index: bpy.props.IntProperty(name='Face B Index', default=-1)


# ---------------------------
# Modal pick operators (Object Mode, normal cursor)
# ---------------------------

class SNAP_OT_pick_face_a(Operator):
    """Pick target face (A) in Object Mode"""
    bl_idname = "snapsplit.pick_face_a"
    bl_label = "Pick Face A"
    bl_options = {'REGISTER', 'UNDO'}

    def modal(self, context, event):
        if event.type in {'RIGHTMOUSE', 'ESC'}:
            report_user(self, 'INFO',
                        'Canceled.')
            return {'CANCELLED'}

        if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
            hit = _raycast_pick_face(context, event)
            if not hit:
                report_user(self, 'INFO',
                            'No face hit. Orbit/zoom and click directly on a visible mesh.')
                return {'RUNNING_MODAL'}
            obj, pos, nrm, fidx = hit
            picks = context.window_manager.snapsplit_picks
            picks.face_a_obj = obj.name
            picks.face_a_index = fidx

            # If B already exists, keep both highlighted; else highlight only A
            nameB = picks.face_b_obj
            idxB = picks.face_b_index
            objB = bpy.data.objects.get(nameB) if nameB else None


            _highlight_picked_face_persistent(objA=obj, idxA=fidx, objB=objB, idxB=idxB)

            # Make B the active object if it exists (guarded: never set active to None)
            try:
                if objB is not None:
                    context.view_layer.objects.active = objB
            except Exception:
                pass

            report_user(self, 'INFO',
                        _trf('Picked A: {name} face {fidx}', name=obj.name, fidx=fidx))
            return {'FINISHED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        if context.space_data is None or context.space_data.type != 'VIEW_3D':
            report_user(self, 'ERROR',
                        'Run in a 3D View.')
            return {'CANCELLED'}
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}


class SNAP_OT_pick_face_b(Operator):
    """Pick moving face (B) in Object Mode"""
    bl_idname = "snapsplit.pick_face_b"
    bl_label = "Pick Face B"
    bl_options = {'REGISTER', 'UNDO'}

    def modal(self, context, event):
        if event.type in {'RIGHTMOUSE', 'ESC'}:
            report_user(self, 'INFO',
                        'Canceled.')
            return {'CANCELLED'}

        if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
            hit = _raycast_pick_face(context, event)
            if not hit:
                report_user(self, 'INFO',
                            'No face hit. Orbit/zoom and click directly on a visible mesh.')
                return {'RUNNING_MODAL'}
            obj, pos, nrm, fidx = hit
            picks = context.window_manager.snapsplit_picks
            picks.face_b_obj = obj.name
            picks.face_b_index = fidx

            # If A already exists, keep both highlighted; else highlight only B
            nameA = picks.face_a_obj
            idxA = picks.face_a_index
            objA = bpy.data.objects.get(nameA) if nameA else None


            _highlight_picked_face_persistent(objA=(objA or obj), idxA=(idxA if objA else fidx),
                                              objB=(obj if objA else None), idxB=(fidx if objA else -1))

            report_user(self, 'INFO',
                        _trf('Picked B: {name} face {fidx}', name=obj.name, fidx=fidx))
            return {'FINISHED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        if context.space_data is None or context.space_data.type != 'VIEW_3D':
            report_user(self, 'ERROR',
                        'Run in a 3D View.')
            return {'CANCELLED'}
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}


# ---------------------------
# Clear Picks helpers
# ---------------------------

def _exit_to_object_mode_safe():
    """Try to return to OBJECT mode ignoring errors."""
    # NOTE: bpy.ops.object.mode_set has no public non-operator equivalent; kept on purpose.
    try:
        bpy.ops.object.mode_set(mode='OBJECT')
    except Exception:
        pass


def _deselect_edit_mesh(obj):
    """Deselect all elements of obj's mesh (works in Edit Mode and in Object Mode).

    - Edit Mode:   live edit BMesh (replaces bpy.ops.mesh.select_all).
    - Object Mode: mesh data select flags through foreach_set, no mode switch needed.
    - If the RNA route is unavailable, enter Edit Mode and use the BMesh route.
    """
    if not obj or obj.type != 'MESH':
        return

    try:
        bpy.context.view_layer.objects.active = obj
    except Exception:
        pass

    # Edit Mode: use the live BMesh
    if obj.mode == 'EDIT':
        _edit_bmesh_deselect_all(obj)
        return

    # Object Mode: write select flags directly into the mesh data
    me = obj.data
    try:
        me.vertices.foreach_set("select", [False] * len(me.vertices))
        me.edges.foreach_set("select", [False] * len(me.edges))
        me.polygons.foreach_set("select", [False] * len(me.polygons))
        me.update()
        return
    except Exception:
        pass

    # Fallback: go through Edit Mode and the BMesh route
    try:
        bpy.ops.object.mode_set(mode='EDIT')
        _edit_bmesh_deselect_all(obj)
    except Exception:
        pass


# ---------------------------
# Align operator (Object Mode driving transform)
# ---------------------------

class SNAP_OT_align_faces(Operator):
    """Align moving face B to target face A (face-to-face, centers matched)"""
    bl_idname = "snapsplit.align_faces"
    bl_label = "Align Faces"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        picks = context.window_manager.snapsplit_picks
        nameA = picks.face_a_obj
        idxA = picks.face_a_index
        nameB = picks.face_b_obj
        idxB = picks.face_b_index


        if not nameA or idxA < 0 or not nameB or idxB < 0:
            report_user(self, 'ERROR',
                        'Pick Face A and Face B first (Object Mode).')
            return {'CANCELLED'}

        objA = bpy.data.objects.get(nameA)
        objB = bpy.data.objects.get(nameB)
        if not objA or not objB or objA.type != 'MESH' or objB.type != 'MESH':
            report_user(self, 'ERROR',
                        'Stored faces not found or not meshes.')
            return {'CANCELLED'}

        # Leave Edit Mode first (the persistent highlight keeps objects in Edit Mode).
        # Leaving flushes the face selection into the mesh data, so the highlight stays
        # visible, and the frame computation below reads up-to-date mesh data.
        _exit_to_object_mode_safe()

        try:
            originA, RA = _object_face_frame_world(objA, idxA)
            originB, RB = _object_face_frame_world(objB, idxB)

        except Exception as e:
            report_user(self, 'ERROR',
                _trf('Could not compute face frames: {error}', error=e))
            return {'CANCELLED'}

        # Face-to-face: flip B's frame by 180 degrees to keep it right-handed
        if _FACE_TO_FACE_LOCAL_FLIP:
            # Columns of RB are the face axes (x, y, z). Negating the Y and Z COLUMNS is a
            # local 180 degree rotation about the face X axis, so B's normal ends up
            # opposite to A's normal for any orientation.
            RB_ff = RB @ Matrix.Diagonal(Vector((1.0, -1.0, -1.0)))
        else:
            # Previous behaviour: negates the ROWS (world components). Only correct for some
            # orientations (e.g. normals along +/-Z). Kept for A/B comparison testing.
            RB_ff = Matrix((RB[0], -RB[1], -RB[2]))

        FA = _make_frame_matrix(originA, RA)
        FB = _make_frame_matrix(originB, RB_ff)

        try:
            M_align = FA @ FB.inverted()
        except Exception:
            report_user(self, 'ERROR',
                        'Alignment transform invalid (singular frame).')
            return {'CANCELLED'}

        # Apply to moving object B
        objB.matrix_world = M_align @ objB.matrix_world

        # Remember the seam plane of this alignment (world space) so that connectors can be
        # placed on slanted seams later. The data is validated against the real vertices
        # before every use, so stale values (parts moved afterwards) are simply ignored.
        # The sign of the normal does not matter: the consumer orients it itself.
        try:
            nA = RA.col[2].to_3d().normalized()   # normal of face A
            xA = RA.col[0].to_3d().normalized()   # stable tangent of face A
            objB["snapsplit_seam_origin"] = [float(originA[0]), float(originA[1]), float(originA[2])]
            objB["snapsplit_seam_normal"] = [float(nA[0]), float(nA[1]), float(nA[2])]
            objB["snapsplit_seam_xdir"] = [float(xA[0]), float(xA[1]), float(xA[2])]
            objB["snapsplit_seam_partner"] = objA.name
            print(f"[SnapSplit] seam stored on '{objB.name}': normal={tuple(round(c, 4) for c in nA)}")
        except Exception as ex:
            print(f"[SnapSplit] could not store seam data: {ex}")


        try:
            objB.data.validate(); objB.data.update()
        except Exception:
            pass

        report_user(self, 'INFO',
                    _trf('Aligned {name} to {name2}.', name=objB.name, name2=objA.name))
        return {'FINISHED'}


# ---------------------------
# Clear Picks operator
# ---------------------------

class SNAP_OT_clear_picks(bpy.types.Operator):
    """Clear stored Face A/B picks and remove their highlights."""
    bl_idname = "snapsplit.clear_picks"
    bl_label = "Clear Picks"
    bl_options = {'INTERNAL', 'UNDO'}

    def execute(self, context):
        picks = context.window_manager.snapsplit_picks

        # Buffer names before clearing, so we can remove highlights
        nameA = picks.face_a_obj
        nameB = picks.face_b_obj
        objA = bpy.data.objects.get(nameA) if nameA else None
        objB = bpy.data.objects.get(nameB) if nameB else None

        # remove the highlight selection (Edit Mode: BMesh, Object Mode: mesh data)
        if objA:
            _deselect_edit_mesh(objA)
        if objB and objB is not objA:
            _deselect_edit_mesh(objB)

        # go back to Object Mode
        _exit_to_object_mode_safe()

        # Reset the stored picks
        picks.face_a_obj = ""
        picks.face_a_index = -1
        picks.face_b_obj = ""
        picks.face_b_index = -1

        self.report({'INFO'}, 'Picks cleared')
        return {'FINISHED'}


classes = (
    SNAP_PG_picks,          # PropertyGroup must be registered before the operators and the pointer
    SNAP_OT_pick_face_a,
    SNAP_OT_pick_face_b,
    SNAP_OT_align_faces,
    SNAP_OT_clear_picks,
)


def register():
    """Register classes and attach the pick storage to bpy.types.WindowManager."""
    # Labels are plain class attributes; Blender translates them itself.
    for c in classes:
        bpy.utils.register_class(c)
    bpy.types.WindowManager.snapsplit_picks = bpy.props.PointerProperty(type=SNAP_PG_picks)


def unregister():
    """Detach the pick storage from bpy.types.WindowManager and unregister all classes."""
    # Remove the pointer first, then the PropertyGroup it references
    if hasattr(bpy.types.WindowManager, "snapsplit_picks"):
        del bpy.types.WindowManager.snapsplit_picks
    for c in reversed(classes):
        bpy.utils.unregister_class(c)
