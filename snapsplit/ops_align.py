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

"""
SnapSplit — Object-Mode Face Picker + Align
- Pick Face A (target) and Face B (moving) in Object Mode
- Align B to A: coplanar, face-to-face, centers coincident
- No gap, no clocking, no Edit Mode required
"""

import bpy
from bpy.types import Operator
from mathutils import Vector, Matrix
from bpy_extras import view3d_utils

from .utils import report_user, is_lang_de


# ---------------------------
# Face pick utils (Object Mode) — scene.ray_cast
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
    """Compute face frame in world space from object mesh data."""
    me = obj.data
    if face_index < 0 or face_index >= len(me.polygons):
        raise ValueError("Invalid face index")
    poly = me.polygons[face_index]

    origin = obj.matrix_world @ poly.center

    # Normal (world) using inverse-transpose
    n_local = poly.normal
    N = obj.matrix_world.to_3x3().inverted().transposed()
    z_world = (N @ n_local).normalized()

    # Tangent X from longest edge
    x_world = None
    max_len = -1.0
    verts = me.vertices
    idxs = poly.vertices
    for i in range(len(idxs)):
        v0 = verts[idxs[i]].co
        v1 = verts[(idxs[(i + 1) % len(idxs)])].co
        d = v1 - v0
        ln = d.length
        if ln > max_len and ln > 1e-12:
            max_len = ln
            x_world = obj.matrix_world.to_3x3() @ d

    if x_world is None or x_world.length_squared <= 1e-18:
        # Fallback axis not aligned with normal
        t = Vector((1, 0, 0))
        if abs(t.dot(z_world)) > 0.9:
            t = Vector((0, 1, 0))
        x_world = t

    # Orthonormalize
    x_world = (x_world - x_world.dot(z_world) * z_world)
    if x_world.length_squared <= 1e-18:
        t = Vector((0, 1, 0))
        if abs(t.dot(z_world)) > 0.9:
            t = Vector((0, 0, 1))
        x_world = (t - t.dot(z_world) * z_world)
    x_world.normalize()

    y_world = z_world.cross(x_world).normalized()
    x_world = y_world.cross(z_world).normalized()

    R = Matrix((x_world, y_world, z_world)).transposed()
    return origin, R


def _make_frame_matrix(origin, R):
    M = Matrix.Identity(4)
    M[0][0], M[0][1], M[0][2] = R[0][0], R[0][1], R[0][2]
    M[1][0], M[1][1], M[1][2] = R[1][0], R[1][1], R[1][2]
    M[2][0], M[2][1], M[2][2] = R[2][0], R[2][1], R[2][2]
    M.translation = origin
    return M


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
            report_user(self, 'INFO', "Canceled.", "Abgebrochen.")
            return {'CANCELLED'}

        if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
            hit = _raycast_pick_face(context, event)
            if not hit:
                report_user(self, 'INFO',
                            "No face hit. Orbit/zoom and click directly on a visible mesh.",
                            "Keine Fläche getroffen. Drehen/zoomen und direkt auf ein sichtbares Mesh klicken.")
                return {'RUNNING_MODAL'}
            obj, pos, nrm, fidx = hit
            wm = context.window_manager
            wm.snapsplit_face_a_obj = obj.name
            wm.snapsplit_face_a_index = fidx
            report_user(self, 'INFO',
                        f"Picked A: {obj.name} face {fidx}",
                        f"A gewählt: {obj.name} Fläche {fidx}")
            return {'FINISHED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        if context.space_data is None or context.space_data.type != 'VIEW_3D':
            report_user(self, 'ERROR', "Run in a 3D View.", "In einer 3D-Ansicht ausführen.")
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
            report_user(self, 'INFO', "Canceled.", "Abgebrochen.")
            return {'CANCELLED'}

        if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
            hit = _raycast_pick_face(context, event)
            if not hit:
                report_user(self, 'INFO',
                            "No face hit. Orbit/zoom and click directly on a visible mesh.",
                            "Keine Fläche getroffen. Drehen/zoomen und direkt auf ein sichtbares Mesh klicken.")
                return {'RUNNING_MODAL'}
            obj, pos, nrm, fidx = hit
            wm = context.window_manager
            wm.snapsplit_face_b_obj = obj.name
            wm.snapsplit_face_b_index = fidx
            report_user(self, 'INFO',
                        f"Picked B: {obj.name} face {fidx}",
                        f"B gewählt: {obj.name} Fläche {fidx}")
            return {'FINISHED'}

        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        if context.space_data is None or context.space_data.type != 'VIEW_3D':
            report_user(self, 'ERROR', "Run in a 3D View.", "In einer 3D-Ansicht ausführen.")
            return {'CANCELLED'}
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}


# ---------------------------
# Align operator (Object Mode)
# ---------------------------

class SNAP_OT_align_faces(Operator):
    """Align moving face B to target face A (face-to-face, centers matched)"""
    bl_idname = "snapsplit.align_faces"
    bl_label = "Align Faces"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        wm = context.window_manager
        nameA = getattr(wm, "snapsplit_face_a_obj", "")
        idxA = getattr(wm, "snapsplit_face_a_index", -1)
        nameB = getattr(wm, "snapsplit_face_b_obj", "")
        idxB = getattr(wm, "snapsplit_face_b_index", -1)

        if not nameA or idxA < 0 or not nameB or idxB < 0:
            report_user(self, 'ERROR',
                        "Pick Face A and Face B first (Object Mode).",
                        "Zuerst Fläche A und B wählen (Objektmodus).")
            return {'CANCELLED'}

        objA = bpy.data.objects.get(nameA)
        objB = bpy.data.objects.get(nameB)
        if not objA or not objB or objA.type != 'MESH' or objB.type != 'MESH':
            report_user(self, 'ERROR',
                        "Stored faces not found or not meshes.",
                        "Gespeicherte Flächen nicht gefunden oder keine Meshes.")
            return {'CANCELLED'}

        try:
            originA, RA = _object_face_frame_world(objA, idxA)
            originB, RB = _object_face_frame_world(objB, idxB)
        except Exception as e:
            report_user(self, 'ERROR',
                        f"Could not compute face frames: {e}",
                        f"Flächenkoordinaten konnten nicht berechnet werden: {e}")
            return {'CANCELLED'}

        # Face-to-face: flip B’s Z (and Y to keep right-handed)
        RB_ff = Matrix((RB[0], -RB[1], -RB[2]))

        FA = _make_frame_matrix(originA, RA)
        FB = _make_frame_matrix(originB, RB_ff)

        try:
            M_align = FA @ FB.inverted()
        except Exception:
            report_user(self, 'ERROR',
                        "Alignment transform invalid (singular frame).",
                        "Ausrichtungstransformation ungültig (singulärer Frame).")
            return {'CANCELLED'}

        # Apply to moving object B
        objB.matrix_world = M_align @ objB.matrix_world

        try:
            objB.data.validate(); objB.data.update()
        except Exception:
            pass

        report_user(self, 'INFO',
                    f"Aligned {objB.name} to {objA.name}.",
                    f"{objB.name} an {objA.name} ausgerichtet.")
        return {'FINISHED'}


# ---------------------------
# WindowManager storage for picks
# ---------------------------

def _register_picker_storage():
    wm = bpy.types.WindowManager
    if not hasattr(wm, "snapsplit_face_a_obj"):
        wm.snapsplit_face_a_obj = bpy.props.StringProperty(name="Face A Object")
    if not hasattr(wm, "snapsplit_face_a_index"):
        wm.snapsplit_face_a_index = bpy.props.IntProperty(name="Face A Index", default=-1)
    if not hasattr(wm, "snapsplit_face_b_obj"):
        wm.snapsplit_face_b_obj = bpy.props.StringProperty(name="Face B Object")
    if not hasattr(wm, "snapsplit_face_b_index"):
        wm.snapsplit_face_b_index = bpy.props.IntProperty(name="Face B Index", default=-1)


classes = (
    SNAP_OT_pick_face_a,
    SNAP_OT_pick_face_b,
    SNAP_OT_align_faces,
)

def register():
    for c in classes:
        bpy.utils.register_class(c)
    _register_picker_storage()

def unregister():
    for c in reversed(classes):
        bpy.utils.unregister_class(c)
