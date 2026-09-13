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

# Translation helper: tr(key, fallback)
try:
    from .languages import tr
except Exception:
    # Fallback if languages module is unavailable
    def tr(key: str, fallback: str = "") -> str:
        return fallback or key


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

    # Deselect all, select targets
    for o in list(bpy.context.selected_objects):
        try:
            o.select_set(False)
        except Exception:
            pass

    for o in objs:
        try:
            o.select_set(True)
        except Exception:
            pass

    # Set an active
    try:
        view_layer.objects.active = objs[0]
    except Exception:
        pass

    # Enter Edit Mode (multi-object)
    try:
        bpy.ops.object.mode_set(mode='EDIT')
    except Exception:
        return

    # Face select mode
    try:
        bpy.context.tool_settings.mesh_select_mode = (False, False, True)
        bpy.ops.mesh.select_mode(type='FACE')
    except Exception:
        pass

    # Clear existing edit selection on all edit meshes
    try:
        bpy.ops.mesh.select_all(action='DESELECT')
    except Exception:
        pass


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
        try:
            bpy.ops.object.mode_set(mode='EDIT')
        except Exception:
            return

    # 2) Face select mode
    try:
        bpy.context.tool_settings.mesh_select_mode = (False, False, True)
        bpy.ops.mesh.select_mode(type='FACE')
    except Exception:
        pass

    # 3) Operate directly on the active edit mesh (obj)
    try:
        bm = bmesh.from_edit_mesh(me)
    except Exception:
        # Fallback if BMesh not available for some reason
        try:
            bpy.ops.mesh.select_all(action='DESELECT')
            me.polygons[face_index].select = True
            bpy.ops.mesh.select_mode(type='EDGE')
            bpy.ops.mesh.select_mode(type='FACE')
            me.update()
        except Exception:
            pass
        return

    # Clear selection on this mesh, then select target face
    for f in bm.faces:
        f.select = False

    try:
        bm_face = bm.faces[face_index]
    except Exception:
        poly = me.polygons[face_index]
        poly_verts = set(poly.vertices)
        bm_face = None
        for f in bm.faces:
            if set(v.index for v in f.verts) == poly_verts:
                bm_face = f
                break
        if bm_face is None:
            return

    bm_face.select = True

    # 4) Flush to viewport
    bm.select_mode = {'FACE'}
    bm.select_flush_mode()
    try:
        bmesh.update_edit_mesh(me, loop_triangles=False, destructive=False)
    except Exception:
        try:
            bpy.ops.mesh.select_mode(type='EDGE')
            bpy.ops.mesh.select_mode(type='FACE')
        except Exception:
            pass
        try:
            me.update()
        except Exception:
            pass

    # 5) Optionally restore previous active edit object if it differs
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
# Modal pick operators (Object Mode, normal cursor)
# ---------------------------

class SNAP_OT_pick_face_a(Operator):
    """Pick target face (A) in Object Mode"""
    bl_idname = "snapsplit.pick_face_a"
    bl_label = tr("ui.pick_face_a", "Pick Face A")
    bl_options = {'REGISTER', 'UNDO'}

    def modal(self, context, event):
        if event.type in {'RIGHTMOUSE', 'ESC'}:
            report_user(self, 'INFO',
                        tr("MSG_CANCELLED", "Canceled."),
                        tr("MSG_CANCELLED", "Canceled."))
            return {'CANCELLED'}

        if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
            hit = _raycast_pick_face(context, event)
            if not hit:
                report_user(self, 'INFO',
                            tr("HINT_RAYCAST_NO_FACE", "No face hit. Orbit/zoom and click directly on a visible mesh."),
                            tr("HINT_RAYCAST_NO_FACE", "No face hit. Orbit/zoom and click directly on a visible mesh."))
                return {'RUNNING_MODAL'}
            obj, pos, nrm, fidx = hit
            wm = context.window_manager
            wm.snapsplit_face_a_obj = obj.name
            wm.snapsplit_face_a_index = fidx

            # If B already exists, keep both highlighted; else highlight only A
            nameB = getattr(wm, "snapsplit_face_b_obj", "")
            idxB = getattr(wm, "snapsplit_face_b_index", -1)
            objB = bpy.data.objects.get(nameB) if nameB else None

            _highlight_picked_face_persistent(objA=obj, idxA=fidx, objB=objB, idxB=idxB)

            try:
                context.view_layer.objects.active = bpy.data.objects.get(wm.snapsplit_face_b_obj)
            except Exception:
                pass

            report_user(self, 'INFO',
                        tr("INFO_PICKED_A", f"Picked A: {obj.name} face {fidx}"),
                        tr("INFO_PICKED_A", f"Picked A: {obj.name} face {fidx}"))
            return {'FINISHED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        if context.space_data is None or context.space_data.type != 'VIEW_3D':
            report_user(self, 'ERROR',
                        tr("ERR_RUN_IN_3DVIEW", "Run in a 3D View."),
                        tr("ERR_RUN_IN_3DVIEW", "Run in a 3D View."))
            return {'CANCELLED'}
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}


class SNAP_OT_pick_face_b(Operator):
    """Pick moving face (B) in Object Mode"""
    bl_idname = "snapsplit.pick_face_b"
    bl_label = tr("ui.pick_face_b", "Pick Face B")
    bl_options = {'REGISTER', 'UNDO'}

    def modal(self, context, event):
        if event.type in {'RIGHTMOUSE', 'ESC'}:
            report_user(self, 'INFO',
                        tr("MSG_CANCELLED", "Canceled."),
                        tr("MSG_CANCELLED", "Canceled."))
            return {'CANCELLED'}

        if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
            hit = _raycast_pick_face(context, event)
            if not hit:
                report_user(self, 'INFO',
                            tr("HINT_RAYCAST_NO_FACE", "No face hit. Orbit/zoom and click directly on a visible mesh."),
                            tr("HINT_RAYCAST_NO_FACE", "No face hit. Orbit/zoom and click directly on a visible mesh."))
                return {'RUNNING_MODAL'}
            obj, pos, nrm, fidx = hit
            wm = context.window_manager
            wm.snapsplit_face_b_obj = obj.name
            wm.snapsplit_face_b_index = fidx

            # If A already exists, keep both highlighted; else highlight only B
            nameA = getattr(wm, "snapsplit_face_a_obj", "")
            idxA = getattr(wm, "snapsplit_face_a_index", -1)
            objA = bpy.data.objects.get(nameA) if nameA else None

            _highlight_picked_face_persistent(objA=(objA or obj), idxA=(idxA if objA else fidx),
                                              objB=(obj if objA else None), idxB=(fidx if objA else -1))

            report_user(self, 'INFO',
                        tr("INFO_PICKED_B", f"Picked B: {obj.name} face {fidx}"),
                        tr("INFO_PICKED_B", f"Picked B: {obj.name} face {fidx}"))
            return {'FINISHED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        if context.space_data is None or context.space_data.type != 'VIEW_3D':
            report_user(self, 'ERROR',
                        tr("ERR_RUN_IN_3DVIEW", "Run in a 3D View."),
                        tr("ERR_RUN_IN_3DVIEW", "Run in a 3D View."))
            return {'CANCELLED'}
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}


# ---------------------------
# Align operator (Object Mode driving transform)
# ---------------------------

class SNAP_OT_align_faces(Operator):
    """Align moving face B to target face A (face-to-face, centers matched)"""
    bl_idname = "snapsplit.align_faces"
    bl_label = tr("ALIGN_FACES_LABEL", "Align Faces")
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        wm = context.window_manager
        nameA = getattr(wm, "snapsplit_face_a_obj", "")
        idxA = getattr(wm, "snapsplit_face_a_index", -1)
        nameB = getattr(wm, "snapsplit_face_b_obj", "")
        idxB = getattr(wm, "snapsplit_face_b_index", -1)

        if not nameA or idxA < 0 or not nameB or idxB < 0:
            report_user(self, 'ERROR',
                        tr("ERR_PICK_A_B_FIRST", "Pick Face A and Face B first (Object Mode)."),
                        tr("ERR_PICK_A_B_FIRST", "Pick Face A and Face B first (Object Mode)."))
            return {'CANCELLED'}

        objA = bpy.data.objects.get(nameA)
        objB = bpy.data.objects.get(nameB)
        if not objA or not objB or objA.type != 'MESH' or objB.type != 'MESH':
            report_user(self, 'ERROR',
                        tr("ERR_STORED_FACES_NOT_FOUND", "Stored faces not found or not meshes."),
                        tr("ERR_STORED_FACES_NOT_FOUND", "Stored faces not found or not meshes."))
            return {'CANCELLED'}

        try:
            originA, RA = _object_face_frame_world(objA, idxA)
            originB, RB = _object_face_frame_world(objB, idxB)

        except Exception as e:
            report_user(self, 'ERROR',
                tr("ERR_FACE_FRAMES_COMPUTE", f"Could not compute face frames: {e}"),
                tr("ERR_FACE_FRAMES_COMPUTE", f"Could not compute face frames: {e}"))
            return {'CANCELLED'}

        # Face-to-face: flip B’s Z and Y to keep right-handed
        RB_ff = Matrix((RB[0], -RB[1], -RB[2]))

        FA = _make_frame_matrix(originA, RA)
        FB = _make_frame_matrix(originB, RB_ff)

        try:
            M_align = FA @ FB.inverted()
        except Exception:
            report_user(self, 'ERROR',
                        tr("ERR_ALIGN_SINGULAR", "Alignment transform invalid (singular frame)."),
                        tr("ERR_ALIGN_SINGULAR", "Alignment transform invalid (singular frame)."))
            return {'CANCELLED'}

        # Apply to moving object B
        objB.matrix_world = M_align @ objB.matrix_world

        try:
            objB.data.validate(); objB.data.update()
        except Exception:
            pass

        # Return to Object Mode after alignment so users continue object-level workflow
        try:
            bpy.ops.object.mode_set(mode='OBJECT')
        except Exception:
            pass

        report_user(self, 'INFO',
                    tr("INFO_ALIGNED", f"Aligned {objB.name} to {objA.name}."),
                    tr("INFO_ALIGNED", f"Aligned {objB.name} to {objA.name}."))
        return {'FINISHED'}


# ---------------------------
# Clear Picks operator
# ---------------------------

def _deselect_edit_mesh(obj):
    """Deselect all faces of obj in Edit Mode (safe-ops)."""
    if not obj or obj.type != 'MESH':
        return
    try:
        bpy.context.view_layer.objects.active = obj
        if obj.mode != 'EDIT':
            bpy.ops.object.mode_set(mode='EDIT')
        bpy.ops.mesh.select_all(action='DESELECT')
    except Exception:
        pass

def _exit_to_object_mode_safe():
    """Try to return to OBJECT mode ignoring errors."""
    try:
        bpy.ops.object.mode_set(mode='OBJECT')
    except Exception:
        pass


class SNAP_OT_clear_picks(bpy.types.Operator):
    """Clear stored Face A/B picks and remove their highlights."""
    bl_idname = "snapsplit.clear_picks"
    bl_label = tr("CLEAR_PICKS_LABEL", "Clear Picks")
    bl_options = {'INTERNAL', 'UNDO'}

    def execute(self, context):
        wm = context.window_manager

        # buffer names before clearing WM, so we can remove highlights
        nameA = getattr(wm, "snapsplit_face_a_obj", "")
        nameB = getattr(wm, "snapsplit_face_b_obj", "")
        objA = bpy.data.objects.get(nameA) if nameA else None
        objB = bpy.data.objects.get(nameB) if nameB else None

        # try to remove edit selections
        if objA:
            _deselect_edit_mesh(objA)
        if objB and objB is not objA:
            _deselect_edit_mesh(objB)

        # go back to Object Mode
        _exit_to_object_mode_safe()

        # clear WM fields
        try:
            wm.snapsplit_face_a_obj = ""
            wm.snapsplit_face_a_index = -1
            wm.snapsplit_face_b_obj = ""
            wm.snapsplit_face_b_index = -1
        except Exception:
            pass

        self.report({'INFO'}, tr("INFO_PICKS_CLEARED", "Picks cleared"))
        return {'FINISHED'}


# ---------------------------
# WindowManager storage for picks
# ---------------------------

def _register_picker_storage():
    """Ensure WindowManager properties for storing picks exist."""
    wm = bpy.types.WindowManager
    if not hasattr(wm, "snapsplit_face_a_obj"):
        wm.snapsplit_face_a_obj = bpy.props.StringProperty(name=tr("PROP_FACE_A_OBJECT", "Face A Object"))
    if not hasattr(wm, "snapsplit_face_a_index"):
        wm.snapsplit_face_a_index = bpy.props.IntProperty(name=tr("PROP_FACE_A_INDEX", "Face A Index"), default=-1)
    if not hasattr(wm, "snapsplit_face_b_obj"):
        wm.snapsplit_face_b_obj = bpy.props.StringProperty(name=tr("PROP_FACE_B_OBJECT", "Face B Object"))
    if not hasattr(wm, "snapsplit_face_b_index"):
        wm.snapsplit_face_b_index = bpy.props.IntProperty(name=tr("PROP_FACE_B_INDEX", "Face B Index"), default=-1)


classes = (
    SNAP_OT_pick_face_a,
    SNAP_OT_pick_face_b,
    SNAP_OT_align_faces,
    SNAP_OT_clear_picks,
)

def register():
    """Register operators and ensure WindowManager storage exists. Also refresh labels via tr()."""
    try:
        SNAP_OT_pick_face_a.bl_label = tr("PICK_FACE_A_LABEL", "Pick Face A")
        SNAP_OT_pick_face_b.bl_label = tr("PICK_FACE_B_LABEL", "Pick Face B")
        SNAP_OT_align_faces.bl_label = tr("ALIGN_FACES_LABEL", "Align Faces")
        SNAP_OT_clear_picks.bl_label = tr("CLEAR_PICKS_LABEL", "Clear Picks")
    except Exception:
        pass

    for c in classes:
        bpy.utils.register_class(c)
    _register_picker_storage()

def unregister():
    """Unregister operators."""
    for c in reversed(classes):
        bpy.utils.unregister_class(c)
