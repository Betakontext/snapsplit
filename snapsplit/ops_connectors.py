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

import bpy
import bmesh
from mathutils import Vector, Matrix
from bpy.types import Operator
from bpy_extras import view3d_utils

from .utils import ensure_collection, unit_mm, report_user

# ---------------------------
# BBox and projection
# ---------------------------

def _bb_world(obj):
    return [obj.matrix_world @ Vector(c) for c in obj.bound_box]

def _proj_interval(points, axis_dir, origin):
    a = axis_dir.normalized()
    return (min((p - origin).dot(a) for p in points),
            max((p - origin).dot(a) for p in points))

def _axis_index(axis):
    return {"X": 0, "Y": 1, "Z": 2}[axis]

def _axis_vectors(axis):
    if axis == "X":
        return Vector((1,0,0)), Vector((0,1,0)), Vector((0,0,1))
    if axis == "Y":
        return Vector((0,1,0)), Vector((1,0,0)), Vector((0,0,1))
    return Vector((0,0,1)), Vector((1,0,0)), Vector((0,1,0))

def _pair_seam_plane_pos(obj_a, obj_b, axis, props):
    """World-space seam plane coordinate for a specific adjacent pair (A,B)."""
    idx = _axis_index(axis)
    bb_a = _bb_world(obj_a); bb_b = _bb_world(obj_b)
    vals_a = [c[idx] for c in bb_a]; vals_b = [c[idx] for c in bb_b]
    lo = min(min(vals_a), min(vals_b))
    hi = max(max(vals_a), max(vals_b))
    if not (lo < hi):
        return lo  # degenerate but safe

    mid = 0.5 * (lo + hi)
    off_scene = float(getattr(props, "split_offset_mm", 0.0)) * unit_mm()
    return max(lo, min(hi, mid + off_scene))

# ---------------------------
# Distribution helpers honoring seam plane
# ---------------------------

def distribute_points_line_on_seam(obj_a, obj_b, count, axis, seam_pos, margin_pct=10.0):
    """
    Distribute 'count' points along the overlap of (A,B) on the given seam plane (world coord).
    """
    n_axis, t1, t2 = _axis_vectors(axis)
    bb_a = _bb_world(obj_a)
    bb_b = _bb_world(obj_b)

    # Origin on seam plane (centered in tangential directions)
    ca = sum(bb_a, Vector()) / 8.0
    cb = sum(bb_b, Vector()) / 8.0
    origin = (ca + cb) * 0.5
    oi = _axis_index(axis)
    origin = Vector((origin.x, origin.y, origin.z))
    origin[oi] = seam_pos

    def overlap_len(a_min, a_max, b_min, b_max):
        return max(0.0, min(a_max, b_max) - max(a_min, b_min))

    t1_min_a, t1_max_a = _proj_interval(bb_a, t1, origin)
    t1_min_b, t1_max_b = _proj_interval(bb_b, t1, origin)
    t2_min_a, t2_max_a = _proj_interval(bb_a, t2, origin)
    t2_min_b, t2_max_b = _proj_interval(bb_b, t2, origin)

    ol1 = overlap_len(t1_min_a, t1_max_a, t1_min_b, t1_max_b)
    ol2 = overlap_len(t2_min_a, t2_max_a, t2_min_b, t2_max_b)

    if ol1 >= ol2:
        t = t1.normalized()
        lo = max(t1_min_a, t1_min_b)
        hi = min(t1_max_a, t1_max_b)
        span = ol1
    else:
        t = t2.normalized()
        lo = max(t2_min_a, t2_min_b)
        hi = min(t2_max_a, t2_max_b)
        span = ol2

    if span <= 0.0:
        return [origin for _ in range(max(1, count))]

    m = max(0.0, float(margin_pct)) * 0.01 * span
    lo_i, hi_i = lo + m, hi - m
    if hi_i < lo_i:
        mid = (lo + hi) * 0.5
        return [origin + t * mid for _ in range(max(1, count))]

    if count <= 1:
        mid = (lo_i + hi_i) * 0.5
        return [origin + t * mid]

    pts = []
    for i in range(count):
        f = i / (count - 1)
        s = lo_i * (1.0 - f) + hi_i * f
        pts.append(origin + t * s)
    return pts

def distribute_points_grid_on_seam(obj_a, obj_b, cols, rows, axis, seam_pos, margin_pct=10.0):
    """
    Distribute cols*rows points across the 2D overlap of (A,B) on the given seam plane (world coord).
    """
    n_axis, t1, t2 = _axis_vectors(axis)
    bb_a = _bb_world(obj_a)
    bb_b = _bb_world(obj_b)

    ca = sum(bb_a, Vector()) / 8.0
    cb = sum(bb_b, Vector()) / 8.0
    origin = (ca + cb) * 0.5
    oi = _axis_index(axis)
    origin = Vector((origin.x, origin.y, origin.z))
    origin[oi] = seam_pos

    def interval_overlap(a_min, a_max, b_min, b_max):
        lo = max(a_min, b_min); hi = min(a_max, b_max)
        return lo, hi, max(0.0, hi - lo)

    t1_min_a, t1_max_a = _proj_interval(bb_a, t1, origin)
    t1_min_b, t1_max_b = _proj_interval(bb_b, t1, origin)
    t2_min_a, t2_max_a = _proj_interval(bb_a, t2, origin)
    t2_min_b, t2_max_b = _proj_interval(bb_b, t2, origin)

    lo1, hi1, span1 = interval_overlap(t1_min_a, t1_max_a, t1_min_b, t1_max_b)
    lo2, hi2, span2 = interval_overlap(t2_min_a, t2_max_a, t2_min_b, t2_max_b)

    if span1 <= 0.0 or span2 <= 0.0:
        return distribute_points_line_on_seam(obj_a, obj_b, cols, axis, seam_pos, margin_pct)

    m1 = max(0.0, float(margin_pct)) * 0.01 * span1
    m2 = max(0.0, float(margin_pct)) * 0.01 * span2
    lo1_i, hi1_i = lo1 + m1, hi1 - m1
    lo2_i, hi2_i = lo2 + m2, lo2 + (span2 - m2)
    if hi1_i < lo1_i or hi2_i < lo2_i:
        c = origin + t1.normalized() * ((lo1 + hi1) * 0.5) + t2.normalized() * ((lo2 + hi2) * 0.5)
        return [c for _ in range(max(1, cols * rows))]

    t1n = t1.normalized(); t2n = t2.normalized()

    pts = []
    for r in range(rows):
        fr = r / (rows - 1) if rows > 1 else 0.5
        sr = lo2_i * (1.0 - fr) + hi2_i * fr
        for c in range(cols):
            fc = c / (cols - 1) if cols > 1 else 0.5
            sc = lo1_i * (1.0 - fc) + hi1_i * fc
            pts.append(origin + t1n * sc + t2n * sr)
    return pts

# ---------------------------
# Geometry: pins / tenons
# ---------------------------

def create_cyl_pin(d_mm=5.0, length_mm=10.0, chamfer_mm=0.0, segments=32, name="SnapSplit_Pin"):
    mm = unit_mm()
    d = float(d_mm) * mm
    L = float(length_mm) * mm
    r = max(1e-9, d * 0.5)

    bm = bmesh.new()
    bmesh.ops.create_cone(
        bm, cap_ends=True, cap_tris=False,
        segments=max(8, int(segments)),
        radius1=r, radius2=r, depth=L
    )
    # Bottom at z=0, top at z=L
    bmesh.ops.transform(bm, matrix=Matrix.Translation((0, 0, L * 0.5)), verts=bm.verts)

    # Optional top chamfer (simple approx)
    if chamfer_mm and chamfer_mm > 0.0:
        chamfer = float(chamfer_mm) * mm
        top_z = max(v.co.z for v in bm.verts)
        top_verts = [v for v in bm.verts if abs(v.co.z - top_z) < 1e-7]
        scale = max(0.0, (r - chamfer) / r) if r > 1e-12 else 1.0
        for v in top_verts:
            v.co.x *= scale
            v.co.y *= scale
            v.co.z -= chamfer

    me = bpy.data.meshes.new(name)
    bm.to_mesh(me); bm.free()
    obj = bpy.data.objects.new(name, me)
    return obj

def create_rect_tenon(w_mm, depth_mm, chamfer_mm, name="RectTenon"):
    mm = unit_mm()
    w = float(w_mm) * mm
    d = float(depth_mm) * mm
    ch = max(0.0, min(float(chamfer_mm), min(float(w_mm), float(depth_mm)) * 0.5)) * mm
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.transform(bm, matrix=Matrix.Diagonal(Vector((w, w, d, 1.0))), verts=bm.verts)
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me); bm.free()
    obj = bpy.data.objects.new(name, me)
    if ch > 0.0:
        mod = obj.modifiers.new("Bevel", 'BEVEL')
        mod.width = ch; mod.segments = 1; mod.limit_method = 'NONE'
    return obj

# ---------------------------
# Single-placement helpers (click)
# ---------------------------

def _orthonormal_frame_from_z(z: Vector):
    z = z.normalized()
    x = Vector((1, 0, 0))
    if abs(z.dot(x)) > 0.99:
        x = Vector((0, 1, 0))
    y = z.cross(x); y.normalize()
    x = y.cross(z); x.normalize()
    return x, y, z

def place_one_cyl_pin_at(a, b, axis, point_world, frame_z=None, props=None, name_prefix="Pin_Click"):
    """
    Place exactly one cylindrical pin at point_world on the seam plane between (a,b),
    oriented with Z along axis normal. Returns (pin_obj, socket_cutter_obj).
    """
    if props is None:
        props = bpy.context.scene.snapsplit
    z = {"X": Vector((1,0,0)), "Y": Vector((0,1,0)), "Z": Vector((0,0,1))}[axis].normalized()
    if frame_z is not None:
        z = frame_z.normalized()
    x, y, z = _orthonormal_frame_from_z(z)

    L_scene = float(props.pin_length_mm) * unit_mm()
    embed_pct = float(getattr(props, "pin_embed_pct", 50.0)) * 0.01
    p_embed = point_world - z * (embed_pct * L_scene)

    M = Matrix((
        (x.x, y.x, z.x, p_embed.x),
        (x.y, y.y, z.y, p_embed.y),
        (x.z, y.z, z.z, p_embed.z),
        (0,   0,   0,   1.0),
    ))

    seg = int(getattr(props, "pin_segments", 32))
    cutters_coll = ensure_collection("_SnapSplit_Cutters")

    pin = create_cyl_pin(props.pin_diameter_mm, props.pin_length_mm, props.add_chamfer_mm,
                         segments=seg, name=f"{name_prefix}")
    pin.matrix_world = M
    cutters_coll.objects.link(pin)

    um = a.modifiers.new(f"{name_prefix}_Union", 'BOOLEAN')
    um.operation = 'UNION'; um.solver = 'EXACT'; um.object = pin
    boolean_apply(a, um)

    tol = float(props.effective_tolerance())
    socket_d = float(props.pin_diameter_mm) + 2.0 * tol
    socket = create_cyl_pin(socket_d, props.pin_length_mm, 0.0, segments=seg, name=f"{name_prefix}_SocketCutter")
    socket.matrix_world = M
    cutters_coll.objects.link(socket)
    cut_socket_with_cutter(b, socket)

    return pin, socket

def place_one_rect_tenon_at(a, b, axis, point_world, props=None, name_prefix="Tenon_Click"):
    """
    Place one rectangular tenon at point_world on the seam plane between (a,b).
    Creates tenon (union into A) and socket cutter (difference in B). Returns (tenon, socket_cutter).
    """
    if props is None:
        props = bpy.context.scene.snapsplit

    z = {"X": Vector((1,0,0)), "Y": Vector((0,1,0)), "Z": Vector((0,0,1))}[axis].normalized()
    x, y, z = _orthonormal_frame_from_z(z)

    L_scene = float(props.tenon_depth_mm) * unit_mm()
    embed_pct = float(getattr(props, "pin_embed_pct", 50.0)) * 0.01
    p_embed = point_world - z * (embed_pct * L_scene)

    M = Matrix((
        (x.x, y.x, z.x, p_embed.x),
        (x.y, y.y, z.y, p_embed.y),
        (x.z, y.z, z.z, p_embed.z),
        (0,   0,   0,   1.0),
    ))

    cutters_coll = ensure_collection("_SnapSplit_Cutters")

    tenon = create_rect_tenon(props.tenon_width_mm, props.tenon_depth_mm, props.add_chamfer_mm, name=f"{name_prefix}")
    tenon.matrix_world = M
    cutters_coll.objects.link(tenon)

    for mod in list(tenon.modifiers):
        if mod.type == 'BEVEL':
            bpy.context.view_layer.objects.active = tenon
            tenon.select_set(True)
            try:
                bpy.ops.object.modifier_apply(modifier=mod.name)
            except Exception as e:
                report_user(None, 'WARNING', f"Bevel apply failure: {e}")
            tenon.select_set(False)

    um = a.modifiers.new(f"{name_prefix}_Union", 'BOOLEAN')
    um.operation = 'UNION'; um.solver = 'EXACT'; um.object = tenon
    boolean_apply(a, um)

    mm = unit_mm()
    tol = float(props.effective_tolerance())
    hx = max(tenon.dimensions.x * 0.5, 1e-9)
    hy = max(tenon.dimensions.y * 0.5, 1e-9)
    hz = max(tenon.dimensions.z * 0.5, 1e-9)
    sx = 1.0 + (tol * mm) / hx
    sy = 1.0 + (tol * mm) / hy
    sz = 1.0 + (tol * mm) / hz

    socket = tenon.copy()
    socket.data = tenon.data.copy()
    socket.name = f"{name_prefix}_SocketCutter"
    cutters_coll.objects.link(socket)
    socket.matrix_world = M @ Matrix.Diagonal(Vector((sx, sy, sz, 1.0)))
    cut_socket_with_cutter(b, socket)

    return tenon, socket

# ---------------------------
# Boolean helpers
# ---------------------------

def boolean_apply(target_obj, mod):
    bpy.context.view_layer.objects.active = target_obj
    target_obj.select_set(True)
    try:
        bpy.ops.object.modifier_apply(modifier=mod.name)
    except Exception as e:
        report_user(None, 'WARNING', f"Modifier apply failed ({mod.name}): {e}")
    target_obj.select_set(False)
    try:
        target_obj.data.validate(verbose=False)
        target_obj.data.update()
    except:
        pass

def cut_socket_with_cutter(target_obj, cutter_obj):
    mod = target_obj.modifiers.new("SnapSplit_Socket", 'BOOLEAN')
    mod.operation = 'DIFFERENCE'
    mod.solver = 'EXACT'
    mod.object = cutter_obj
    boolean_apply(target_obj, mod)

# ---------------------------
# Placement & connect (pairwise seam plane)
# ---------------------------

def place_connectors_between(parts, axis, count, ctype, props):
    """
    Connect adjacent parts along 'axis' with distribution per props.connector_distribution.
    For each adjacent pair (A,B), compute a seam plane from the pair AABB midpoint plus split_offset_mm (clamped),
    and place/connect on that plane. This keeps connectors aligned to actual seams even after offset changes.
    """
    if not parts:
        return []

    idx = _axis_index(axis)
    ordered = sorted(parts, key=lambda o: o.location[idx])
    pairs = [(ordered[i], ordered[i + 1]) for i in range(len(ordered) - 1)]
    if not pairs:
        return []

    created = []
    cutters_coll = ensure_collection("_SnapSplit_Cutters")

    naxis = {"X": Vector((1, 0, 0)), "Y": Vector((0, 1, 0)), "Z": Vector((0, 0, 1))}[axis]
    tol = float(props.effective_tolerance())
    embed_pct = float(getattr(props, "pin_embed_pct", 50.0)) * 0.01
    margin_pct = float(getattr(props, "connector_margin_pct", 10.0))
    cols = max(1, int(getattr(props, "connectors_per_seam", count)))

    for a, b in pairs:
        seam_pos = _pair_seam_plane_pos(a, b, axis, props)

        if getattr(props, "connector_distribution", "LINE") == "GRID":
            rows = max(1, int(getattr(props, "connectors_rows", 2)))
            points = distribute_points_grid_on_seam(a, b, cols, rows, axis, seam_pos, margin_pct=margin_pct)
        else:
            points = distribute_points_line_on_seam(a, b, cols, axis, seam_pos, margin_pct=margin_pct)

        for i, p in enumerate(points):
            z = naxis.normalized()
            x = Vector((1, 0, 0))
            if abs(z.dot(x)) > 0.99:
                x = Vector((0, 1, 0))
            y = z.cross(x); y.normalize()
            x = y.cross(z); x.normalize()

            L_scene = float(props.pin_length_mm if getattr(props, "connector_type", "CYL_PIN") == "CYL_PIN" else props.tenon_depth_mm) * unit_mm()
            p_embed = p - z * (embed_pct * L_scene)

            M = Matrix((
                (x.x, y.x, z.x, p_embed.x),
                (x.y, y.y, z.y, p_embed.y),
                (x.z, y.z, z.z, p_embed.z),
                (0,   0,   0,   1.0),
            ))

            if getattr(props, "connector_type", "CYL_PIN") == "CYL_PIN":
                seg = int(getattr(props, "pin_segments", 32))
                pin = create_cyl_pin(props.pin_diameter_mm, props.pin_length_mm, props.add_chamfer_mm,
                                     segments=seg, name=f"Pin_{i}")
                pin.matrix_world = M
                cutters_coll.objects.link(pin)

                um = a.modifiers.new(f"PinUnion_{i}", 'BOOLEAN')
                um.operation = 'UNION'; um.solver = 'EXACT'; um.object = pin
                boolean_apply(a, um)

                socket_d = float(props.pin_diameter_mm) + 2.0 * tol
                socket = create_cyl_pin(socket_d, props.pin_length_mm, 0.0, segments=seg, name=f"SocketCutter_{i}")
                socket.matrix_world = M
                cutters_coll.objects.link(socket)
                cut_socket_with_cutter(b, socket)

                created.append(pin)

            else:
                tenon = create_rect_tenon(props.tenon_width_mm, props.tenon_depth_mm, props.add_chamfer_mm)
                tenon.matrix_world = M
                cutters_coll.objects.link(tenon)

                for mod in list(tenon.modifiers):
                    if mod.type == 'BEVEL':
                        bpy.context.view_layer.objects.active = tenon
                        tenon.select_set(True)
                        try:
                            bpy.ops.object.modifier_apply(modifier=mod.name)
                        except Exception as e:
                            report_user(None, 'WARNING', f"Bevel apply failure: {e}")
                        tenon.select_set(False)

                um = a.modifiers.new(f"TenonUnion_{i}", 'BOOLEAN')
                um.operation = 'UNION'; um.solver = 'EXACT'; um.object = tenon
                boolean_apply(a, um)

                mm = unit_mm()
                hx = max(tenon.dimensions.x * 0.5, 1e-9)
                hy = max(tenon.dimensions.y * 0.5, 1e-9)
                hz = max(tenon.dimensions.z * 0.5, 1e-9)
                sx = 1.0 + (tol * mm) / hx
                sy = 1.0 + (tol * mm) / hy
                sz = 1.0 + (tol * mm) / hz

                socket = tenon.copy()
                socket.data = tenon.data.copy()
                socket.name = f"TenonSocketCutter_{i}"
                cutters_coll.objects.link(socket)
                socket.matrix_world = M @ Matrix.Diagonal(Vector((sx, sy, sz, 1.0)))
                cut_socket_with_cutter(b, socket)

                created.append(tenon)

    return created

# ---------------------------
# Modal operator: place by click (pins or tenons)
# ---------------------------

class SNAP_OT_place_connectors_click(Operator):
    bl_idname = "snapsplit.place_connectors_click"
    bl_label = "Place connectors (click)"
    bl_options = {'REGISTER', 'UNDO', 'BLOCKING'}

    def invoke(self, context, event):
        props = context.scene.snapsplit
        sel = [o for o in context.selected_objects if o.type == 'MESH']
        if len(sel) != 2:
            report_user(self, 'ERROR', "Select exactly 2 adjacent split parts.",
                        "Genau 2 benachbarte Schnitt-Teile auswählen.")
            return {'CANCELLED'}

        self.a, self.b = sel
        self.axis = props.split_axis
        self.props = props

        try:
            self.seam_pos = _pair_seam_plane_pos(self.a, self.b, self.axis, props)
        except Exception:
            report_user(self, 'ERROR', "Could not compute seam plane.", "Naht-Ebene konnte nicht berechnet werden.")
            return {'CANCELLED'}

        # Preview object (wireframe) based on connector type
        try:
            if getattr(props, "connector_type", "CYL_PIN") == "CYL_PIN":
                seg = int(getattr(props, "pin_segments", 32))
                self.preview_obj = create_cyl_pin(props.pin_diameter_mm, props.pin_length_mm, props.add_chamfer_mm,
                                                  segments=seg, name="SnapSplit_Preview_Conn")
            else:
                self.preview_obj = create_rect_tenon(props.tenon_width_mm, props.tenon_depth_mm, props.add_chamfer_mm,
                                                     name="SnapSplit_Preview_Conn")
            prev_coll = ensure_collection("_SnapSplit_Preview")
            self.preview_obj.display_type = 'WIRE'
            self.preview_obj.hide_select = True
            prev_coll.objects.link(self.preview_obj)
        except Exception:
            self.preview_obj = None

        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def finish(self, context, cancelled=False):
        try:
            if self.preview_obj:
                for coll in list(self.preview_obj.users_collection):
                    coll.objects.unlink(self.preview_obj)
                bpy.data.objects.remove(self.preview_obj)
        except Exception:
            pass
        if cancelled:
            report_user(self, 'INFO', "Placement cancelled.", "Platzierung abgebrochen.")

    def modal(self, context, event):
        if event.type in {'ESC', 'RIGHTMOUSE'} and event.value == 'PRESS':
            self.finish(context, cancelled=True)
            return {'CANCELLED'}

        if event.type == 'MOUSEMOVE':
            hit = self._intersect_mouse_with_seam_plane(context, event)
            if hit is not None and self.preview_obj:
                self.preview_obj.matrix_world = self._build_frame_at(hit)
            return {'RUNNING_MODAL'}

        if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
            hit = self._intersect_mouse_with_seam_plane(context, event)
            if hit is not None:
                if getattr(self.props, "connector_type", "CYL_PIN") == "CYL_PIN":
                    place_one_cyl_pin_at(self.a, self.b, self.axis, hit, props=self.props, name_prefix="Pin_Click")
                else:
                    place_one_rect_tenon_at(self.a, self.b, self.axis, hit, props=self.props, name_prefix="Tenon_Click")
            return {'RUNNING_MODAL'}

        if event.type in {'RET', 'NUMPAD_ENTER'} and event.value == 'PRESS':
            self.finish(context, cancelled=False)
            return {'FINISHED'}

        return {'RUNNING_MODAL'}

    def _intersect_mouse_with_seam_plane(self, context, event):
        n = {"X": Vector((1,0,0)), "Y": Vector((0,1,0)), "Z": Vector((0,0,1))}[self.axis].normalized()

        ca = sum([self.a.matrix_world @ Vector(c) for c in self.a.bound_box], Vector()) / 8.0
        cb = sum([self.b.matrix_world @ Vector(c) for c in self.b.bound_box], Vector()) / 8.0
        c = 0.5 * (ca + cb)
        idx = _axis_index(self.axis)
        c[idx] = self.seam_pos
        plane_point = c
        plane_normal = n

        region = context.region
        rv3d = context.region_data
        if not rv3d:
            return None
        mx, my = event.mouse_region_x, event.mouse_region_y
        ray_origin = view3d_utils.region_2d_to_origin_3d(region, rv3d, (mx, my))
        view_vec = rv3d.view_rotation @ Vector((0.0, 0.0, -1.0))
        ray_target = view3d_utils.region_2d_to_location_3d(region, rv3d, (mx, my), view_vec)
        ray_dir = (ray_target - ray_origin).normalized()

        denom = ray_dir.dot(plane_normal)
        if abs(denom) < 1e-8:
            return None
        t = (plane_point - ray_origin).dot(plane_normal) / denom
        if t < 0:
            return None
        return ray_origin + ray_dir * t

    def _build_frame_at(self, point_world):
        z = {"X": Vector((1,0,0)), "Y": Vector((0,1,0)), "Z": Vector((0,0,1))}[self.axis].normalized()
        x = Vector((1,0,0))
        if abs(z.dot(x)) > 0.99:
            x = Vector((0,1,0))
        y = z.cross(x); y.normalize()
        x = y.cross(z); x.normalize()

        if getattr(self.props, "connector_type", "CYL_PIN") == "CYL_PIN":
            L_scene = float(self.props.pin_length_mm) * unit_mm()
        else:
            L_scene = float(self.props.tenon_depth_mm) * unit_mm()

        embed_pct = float(getattr(self.props, "pin_embed_pct", 50.0)) * 0.01
        p_embed = point_world - z * (embed_pct * L_scene)

        return Matrix((
            (x.x, y.x, z.x, p_embed.x),
            (x.y, y.y, z.y, p_embed.y),
            (x.z, y.z, z.z, p_embed.z),
            (0,   0,   0,   1.0),
        ))

# ---------------------------
# Batch placement operator (existing)
# ---------------------------

class SNAP_OT_add_connectors(Operator):
    bl_idname = "snapsplit.add_connectors"
    bl_label = "Add connectors"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        props = context.scene.snapsplit
        sel = [o for o in context.selected_objects if o.type == 'MESH']
        if len(sel) < 2:
            report_user(self, 'ERROR', "Select at least 2 cut mesh-pieces.",
                        "Mindestens 2 geschnittene Mesh-Teile auswählen.")
            return {'CANCELLED'}

        created = place_connectors_between(
            parts=sel,
            axis=props.split_axis,
            count=props.connectors_per_seam,
            ctype=props.connector_type,
            props=props
        )
        report_user(self, 'INFO', f"{len(created)} connectors created.",
                    f"{len(created)} Verbinder erstellt.")
        return {'FINISHED'}

# ---------------------------
# Registration
# ---------------------------

classes = (SNAP_OT_add_connectors, SNAP_OT_place_connectors_click)

def register():
    for c in classes:
        bpy.utils.register_class(c)

def unregister():
    for c in reversed(classes):
        bpy.utils.unregister_class(c)
