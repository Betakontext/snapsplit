# ops_connectors.py
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
from math import radians, tan
from mathutils import Vector, Matrix
from bpy.types import Operator
from bpy_extras import view3d_utils

from .utils import ensure_collection, unit_mm, report_user
from .profiles import MATERIAL_PROFILES

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
    idx = _axis_index(axis)
    bb_a = _bb_world(obj_a); bb_b = _bb_world(obj_b)
    vals_a = [c[idx] for c in bb_a]; vals_b = [c[idx] for c in bb_b]
    lo = min(min(vals_a), min(vals_b))
    hi = max(max(vals_a), max(vals_b))
    if not (lo < hi):
        return lo
    mid = 0.5 * (lo + hi)
    off_scene = float(getattr(props, "split_offset_mm", 0.0)) * unit_mm()
    return max(lo, min(hi, mid + off_scene))

# ---------------------------
# Margins
# ---------------------------

def _edge_margins_scene(props):
    mm = unit_mm()
    pct = max(0.0, float(getattr(props, "connector_margin_pct", 0.0)))
    edge_mm = max(0.0, float(getattr(props, "edge_margin_mm", 0.0))) * mm
    return pct, edge_mm

# ---------------------------
# Distributions
# ---------------------------

def distribute_points_line_on_seam(obj_a, obj_b, count, axis, seam_pos, margin_pct=0.0, edge_margin_scene=0.0):
    n_axis, t1, t2 = _axis_vectors(axis)
    bb_a = _bb_world(obj_a); bb_b = _bb_world(obj_b)

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

    m_pct = max(0.0, float(margin_pct)) * 0.01 * span
    m_abs = max(0.0, float(edge_margin_scene))
    lo_i, hi_i = lo + m_pct + m_abs, hi - m_pct - m_abs

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

def distribute_points_grid_on_seam(obj_a, obj_b, cols, rows, axis, seam_pos, margin_pct=0.0, edge_margin_scene=0.0):
    n_axis, t1, t2 = _axis_vectors(axis)
    bb_a = _bb_world(obj_a); bb_b = _bb_world(obj_b)

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
        return distribute_points_line_on_seam(obj_a, obj_b, cols, axis, seam_pos, margin_pct, edge_margin_scene)

    m1 = max(0.0, float(margin_pct)) * 0.01 * span1
    m2 = max(0.0, float(margin_pct)) * 0.01 * span2
    e = max(0.0, float(edge_margin_scene))

    lo1_i, hi1_i = lo1 + m1 + e, hi1 - m1 - e
    lo2_i, hi2_i = lo2 + m2 + e, hi2 - m2 - e

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
# Orthonormal frames
# ---------------------------

def _orthonormal_frame_from_z(z: Vector):
    z = z.normalized()
    x = Vector((1, 0, 0))
    if abs(z.dot(x)) > 0.99:
        x = Vector((0, 1, 0))
    y = z.cross(x); y.normalize()
    x = y.cross(z); x.normalize()
    return x, y, z

def _rotate_frame_for_slide_dir(M, slide_dir):
    if slide_dir not in {"+X", "-X", "+Y", "-Y"}:
        return M
    x = Vector((M[0][0], M[1][0], M[2][0]))
    y = Vector((M[0][1], M[1][1], M[2][1]))
    z = Vector((M[0][2], M[1][2], M[2][2]))
    tgt = {"+X": x, "-X": -x, "+Y": y, "-Y": -y}[slide_dir].normalized()
    new_x = tgt
    new_y = z.cross(new_x)
    if new_y.length_squared < 1e-12:
        new_y = y
    new_y.normalize()
    new_x = new_y.cross(z).normalized()
    R = Matrix(((new_x.x, new_y.x, z.x, 0.0),
                (new_x.y, new_y.y, z.y, 0.0),
                (new_x.z, new_y.z, z.z, 0.0),
                (0.0,     0.0,     0.0, 1.0)))
    T = Matrix.Translation(Vector((M[0][3], M[1][3], M[2][3])))
    return T @ R

# ---------------------------
# Boolean helpers
# ---------------------------

def boolean_apply(target_obj, mod):
    bpy.context.view_layer.objects.active = target_obj
    try:
        for o in bpy.context.selected_objects:
            o.select_set(False)
    except Exception:
        pass
    target_obj.select_set(True)
    try:
        bpy.ops.object.modifier_apply(modifier=mod.name)
    except Exception as e:
        report_user(None, 'WARNING', f"Modifier apply failed ({mod.name}): {e}", "Modifier-Anwenden fehlgeschlagen.")
    target_obj.select_set(False)
    try:
        target_obj.data.validate(verbose=False); target_obj.data.update()
    except:
        pass

def _dispose_object(obj, remove_data=True):
    if not obj:
        return
    try:
        for coll in list(obj.users_collection):
            coll.objects.unlink(obj)
    except Exception:
        pass
    try:
        md = getattr(obj, "data", None)
        if remove_data and md and hasattr(md, "users") and md.users == 1:
            try:
                if md.__class__.__name__ == "Mesh":
                    bpy.data.meshes.remove(md)
                else:
                    bpy.data.batch_remove((md,))
            except Exception:
                pass
            try:
                obj.data = None
            except Exception:
                pass
    except Exception:
        pass
    try:
        bpy.data.objects.remove(obj)
    except Exception:
        pass

def cut_socket_with_cutter_and_dispose(target_obj, cutter_obj):
    mod = target_obj.modifiers.new("SnapSplit_Socket", 'BOOLEAN')
    mod.operation = 'DIFFERENCE'
    mod.solver = 'EXACT'
    mod.object = cutter_obj
    boolean_apply(target_obj, mod)
    _dispose_object(cutter_obj, remove_data=True)

def union_and_dispose(target_obj, union_obj, name="SnapSplit_Union"):
    mod = target_obj.modifiers.new(name, 'BOOLEAN')
    mod.operation = 'UNION'
    mod.solver = 'EXACT'
    mod.object = union_obj
    boolean_apply(target_obj, mod)
    _dispose_object(union_obj, remove_data=True)

# ---------------------------
# Base primitives
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
    bmesh.ops.transform(bm, matrix=Matrix.Translation((0, 0, L * 0.5)), verts=bm.verts)

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

def create_rect_tenon_quader(w_mm=6.0, length_mm=10.0, chamfer_mm=0.0, name="SnapSplit_Tenon"):
    mm = unit_mm()
    w = float(w_mm) * mm
    L = float(length_mm) * mm
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    from mathutils import Vector as V
    bmesh.ops.transform(bm, matrix=Matrix.Diagonal(V((w, w, L, 1.0))), verts=bm.verts)
    bmesh.ops.transform(bm, matrix=Matrix.Translation((0, 0, L * 0.5)), verts=bm.verts)
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me); bm.free()
    obj = bpy.data.objects.new(name, me)
    if chamfer_mm and chamfer_mm > 0.0:
        bev = obj.modifiers.new("Bevel", 'BEVEL')
        bev.width = float(chamfer_mm) * mm
        bev.segments = 1
        bev.limit_method = 'NONE'
    return obj

def create_dovetail_tongue(width_mm, depth_mm, length_mm, draft_deg, leadin_chamfer_mm=0.0, name="SnapSplit_DovetailTongue"):
    mm = unit_mm()
    w0 = float(width_mm) * mm
    D  = float(depth_mm) * mm
    L  = float(length_mm) * mm
    t  = tan(radians(float(draft_deg))) if float(draft_deg) != 0.0 else 0.0
    w1 = max(1e-6, w0 + 2.0 * t * L)

    bm = bmesh.new()

    def add_rect_layer(z, w, d):
        hx = 0.5 * w; hy = 0.5 * d
        from mathutils import Vector as V
        return [
            bm.verts.new(V((-hx, -hy, z))),
            bm.verts.new(V(( hx, -hy, z))),
            bm.verts.new(V(( hx,  hy, z))),
            bm.verts.new(V((-hx,  hy, z))),
        ]

    v0 = add_rect_layer(0.0, w0, D)
    v1 = add_rect_layer(L,   w1, D)
    bm.verts.index_update(); bm.verts.ensure_lookup_table()

    for i in range(4):
        a = v0[i]; b = v0[(i + 1) % 4]; c = v1[(i + 1) % 4]; d = v1[i]
        try: bm.faces.new([a, b, c, d])
        except ValueError: pass

    try: bm.faces.new(v0)
    except ValueError: pass
    try: bm.faces.new(v1[::-1])
    except ValueError: pass

    bm.normal_update()
    me = bpy.data.meshes.new(name); bm.to_mesh(me); bm.free()
    obj = bpy.data.objects.new(name, me)

    if leadin_chamfer_mm and leadin_chamfer_mm > 0.0:
        bev = obj.modifiers.new("Bevel", 'BEVEL')
        bev.width = float(leadin_chamfer_mm) * mm
        bev.segments = 1
        bev.limit_method = 'ANGLE'

    return obj

def create_dovetail_socket_cutter(width_mm, depth_mm, length_mm, clearance_per_side_mm, draft_deg, name="SnapSplit_DovetailSocketCutter"):
    w = float(width_mm) + 2.0 * float(clearance_per_side_mm)
    D = float(depth_mm)
    L = float(length_mm)
    return create_dovetail_tongue(w, D, L, draft_deg, leadin_chamfer_mm=0.0, name=name)

# ---------------------------
# Dovetail sizing helpers
# ---------------------------

def _apply_margins_to_span(lo, hi, span, pct_margin, edge_margin_scene, end_inset_scene):
    m_pct = max(0.0, float(pct_margin)) * 0.01 * span
    e = max(0.0, float(edge_margin_scene))
    ins = max(0.0, float(end_inset_scene))
    lo2, hi2 = lo + m_pct + e + ins, hi - m_pct - e - ins
    if hi2 < lo2:
        mid = (lo + hi) * 0.5
        return mid, mid, 0.0
    return lo2, hi2, max(0.0, hi2 - lo2)

def _seam_overlap_axes(obj_a, obj_b, axis, seam_pos):
    n_axis, t1, t2 = _axis_vectors(axis)
    bb_a = _bb_world(obj_a); bb_b = _bb_world(obj_b)
    ca = sum(bb_a, Vector()) / 8.0; cb = sum(bb_b, Vector()) / 8.0
    origin = (ca + cb) * 0.5; oi = _axis_index(axis)
    origin = Vector((origin.x, origin.y, origin.z)); origin[oi] = seam_pos

    def interval(points, dirv):
        lo, hi = _proj_interval(points, dirv, origin)
        return lo, hi, max(0.0, hi - lo)

    lo1a, hi1a, _ = interval(bb_a, t1); lo1b, hi1b, _ = interval(bb_b, t1)
    lo2a, hi2a, _ = interval(bb_a, t2); lo2b, hi2b, _ = interval(bb_b, t2)

    lo1, hi1 = max(lo1a, lo1b), min(hi1a, hi1b); span1 = max(0.0, hi1 - lo1)
    lo2, hi2 = max(lo2a, lo2b), min(hi2a, hi2b); span2 = max(0.0, hi2 - lo2)
    return (t1, lo1, hi1, span1), (t2, lo2, hi2, span2), origin

def _calc_normal_axis_span(obj_a, obj_b, axis, seam_pos, pct_margin, edge_margin_scene):
    n_axis, t1, t2 = _axis_vectors(axis)
    bb_a = _bb_world(obj_a); bb_b = _bb_world(obj_b)
    ca = sum(bb_a, Vector()) / 8.0; cb = sum(bb_b, Vector()) / 8.0
    origin = (ca + cb) * 0.5; oi = _axis_index(axis)
    origin = Vector((origin.x, origin.y, origin.z)); origin[oi] = seam_pos

    lo_a, hi_a = _proj_interval(bb_a, n_axis, origin)
    lo_b, hi_b = _proj_interval(bb_b, n_axis, origin)
    lo, hi = min(lo_a, lo_b), max(hi_a, hi_b)
    span = max(0.0, hi - lo)
    lo2, hi2, use = _apply_margins_to_span(lo, hi, span, pct_margin, edge_margin_scene, 0.0)
    return use

def _calc_dovetail_dims_from_spans(a, b, axis, props):
    mm = unit_mm()
    seam_pos = _pair_seam_plane_pos(a, b, axis, props)
    (t1, lo1, hi1, span1), (t2, lo2, hi2, span2), origin = _seam_overlap_axes(a, b, axis, seam_pos)
    pct, edge_abs = _edge_margins_scene(props)
    end_inset_scene = float(getattr(props, "dovetail_end_inset_mm", 0.0)) * mm

    if span1 >= span2:
        len_lo, len_hi, len_span = lo1, hi1, span1
        wid_lo, wid_hi, wid_span = lo2, hi2, span2
    else:
        len_lo, len_hi, len_span = lo2, hi2, span2
        wid_lo, wid_hi, wid_span = lo1, hi1, span1

    _, _, len_use = _apply_margins_to_span(len_lo, len_hi, len_span, pct, edge_abs, end_inset_scene)
    wid_lo2, wid_hi2, wid_use = _apply_margins_to_span(wid_lo, wid_hi, wid_span, pct, edge_abs, 0.0)
    n_use = _calc_normal_axis_span(a, b, axis, seam_pos, pct, edge_abs)

    length_mm = max(4.0, float(len_use / mm))
    if getattr(props, "dovetail_fit_width_mode", "PERCENT_SHORT") == "PERCENT_SHORT":
        width_mm = max(2.0, float(wid_use / mm) * (float(getattr(props, "dovetail_fit_width_pct", 100.0)) * 0.01))
    else:
        width_mm = float(props.dovetail_width_mm)

    dmode = getattr(props, "dovetail_fit_depth_mode", "PERCENT_NORMAL")
    dpc   = float(getattr(props, "dovetail_fit_depth_pct", 25.0)) * 0.01
    if dmode == "PERCENT_NORMAL":
        depth_mm = max(2.0, float(n_use / mm) * dpc)
    elif dmode == "PERCENT_SHORT":
        depth_mm = max(2.0, float(wid_use / mm) * dpc)
    else:
        depth_mm = float(props.dovetail_depth_mm)

    return length_mm, width_mm, depth_mm, (t1, t2, span1, span2)

# ---------------------------
# Placements
# ---------------------------

def place_one_cyl_pin_at(a, b, axis, point_world, frame_z=None, props=None, name_prefix="Pin_Click", override_fit_mode=False):
    if props is None:
        props = bpy.context.scene.snapsplit

    z = {"X": Vector((1,0,0)), "Y": Vector((0,1,0)), "Z": Vector((0,0,1))}[axis].normalized()
    if frame_z is not None:
        z = frame_z.normalized()
    x = Vector((1,0,0))
    if abs(z.dot(x)) > 0.99:
        x = Vector((0,1,0))
    y = z.cross(x); y.normalize()
    x = y.cross(z); x.normalize()

    L_scene = float(props.pin_length_mm) * unit_mm()
    embed_pct = float(getattr(props, "pin_embed_pct", 50.0)) * 0.01
    p_embed = point_world - z * (embed_pct * L_scene)

    M = Matrix(((x.x, y.x, z.x, p_embed.x),
                (x.y, y.y, z.y, p_embed.y),
                (x.z, y.z, z.z, p_embed.z),
                (0,   0,   0,   1.0)))

    seg = int(getattr(props, "pin_segments", 32))
    cutters_coll = ensure_collection("_SnapSplit_Cutters")

    hole_only = bool(getattr(props, "pin_hole_only", False)) if override_fit_mode else False
    if not hole_only:
        pin = create_cyl_pin(props.pin_diameter_mm, props.pin_length_mm, props.add_chamfer_mm, segments=seg, name=f"{name_prefix}")
        pin.matrix_world = M
        cutters_coll.objects.link(pin)
        union_and_dispose(b, pin, name=f"{name_prefix}_Union")

    if override_fit_mode:
        mat = getattr(props, "material_profile", "PETG")
        mode = getattr(props, "pin_fit_mode", "snug")
        fdm = {"snug": 0.25, "sliding": 0.45, "glue_ready": 0.60}
        sla = {"snug": 0.08, "sliding": 0.12, "glue_ready": 0.18}
        c_mm = (sla if mat == "SLA" else fdm).get(mode, 0.25)
        socket_d = float(props.pin_diameter_mm) + 2.0 * c_mm
    else:
        tol = float(props.effective_tolerance())
        socket_d = float(props.pin_diameter_mm) + 2.0 * tol

    socket = create_cyl_pin(socket_d, props.pin_length_mm, 0.0, segments=seg, name=f"{name_prefix}_SocketCutter")
    socket.matrix_world = M
    cutters_coll.objects.link(socket)
    cut_socket_with_cutter_and_dispose(a, socket)
    return None, None

def place_one_tenon_at(a, b, axis, point_world, props=None, name_prefix="Tenon_Click"):
    if props is None:
        props = bpy.context.scene.snapsplit

    z = {"X": Vector((1,0,0)), "Y": Vector((0,1,0)), "Z": Vector((0,0,1))}[axis].normalized()
    x = Vector((1,0,0))
    if abs(z.dot(x)) > 0.99:
        x = Vector((0,1,0))
    y = z.cross(x); y.normalize()
    x = y.cross(z); x.normalize()

    L_scene = float(props.tenon_depth_mm) * unit_mm()
    embed_pct = float(getattr(props, "pin_embed_pct", 50.0)) * 0.01
    p_embed = point_world - z * (embed_pct * L_scene)

    M = Matrix(((x.x, y.x, z.x, p_embed.x),
                (x.y, y.y, z.y, p_embed.y),
                (x.z, y.z, z.z, p_embed.z),
                (0,   0,   0,   1.0)))

    cutters_coll = ensure_collection("_SnapSplit_Cutters")
    tenon = create_rect_tenon_quader(props.tenon_width_mm, props.tenon_depth_mm, props.add_chamfer_mm, name=f"{name_prefix}")
    tenon.matrix_world = M
    cutters_coll.objects.link(tenon)
    for mod in list(tenon.modifiers):
        if mod.type == 'BEVEL':
            bpy.context.view_layer.objects.active = tenon
            tenon.select_set(True)
            try: bpy.ops.object.modifier_apply(modifier=mod.name)
            except Exception as e:
                report_user(None, 'WARNING', f"Bevel apply failure: {e}", "Bevel anwenden fehlgeschlagen.")
            tenon.select_set(False)
    union_and_dispose(b, tenon, name=f"{name_prefix}_Union")

    tol = float(props.effective_tolerance())
    mm = unit_mm()
    half_w = max(0.5 * float(props.tenon_width_mm) * mm, 1e-9)
    sx = 1.0 + (tol * mm) / half_w
    sy = sx
    sz = 1.0
    socket = create_rect_tenon_quader(props.tenon_width_mm, props.tenon_depth_mm, 0.0, name=f"{name_prefix}_SocketCutter")
    socket.matrix_world = M @ Matrix.Diagonal(Vector((sx, sy, sz, 1.0)))
    cutters_coll.objects.link(socket)
    cut_socket_with_cutter_and_dispose(a, socket)
    return None, None

def _calc_dovetail_dims_from_spans(a, b, axis, props):
    mm = unit_mm()
    seam_pos = _pair_seam_plane_pos(a, b, axis, props)
    (t1, lo1, hi1, span1), (t2, lo2, hi2, span2), origin = _seam_overlap_axes(a, b, axis, seam_pos)
    pct, edge_abs = _edge_margins_scene(props)
    end_inset_scene = float(getattr(props, "dovetail_end_inset_mm", 0.0)) * mm

    if span1 >= span2:
        len_lo, len_hi, len_span = lo1, hi1, span1
        wid_lo, wid_hi, wid_span = lo2, hi2, span2
    else:
        len_lo, len_hi, len_span = lo2, hi2, span2
        wid_lo, wid_hi, wid_span = lo1, hi1, span1

    _, _, len_use = _apply_margins_to_span(len_lo, len_hi, len_span, pct, edge_abs, end_inset_scene)
    wid_lo2, wid_hi2, wid_use = _apply_margins_to_span(wid_lo, wid_hi, wid_span, pct, edge_abs, 0.0)
    n_use = _calc_normal_axis_span(a, b, axis, seam_pos, pct, edge_abs)

    length_mm = max(4.0, float(len_use / mm))
    if getattr(props, "dovetail_fit_width_mode", "PERCENT_SHORT") == "PERCENT_SHORT":
        width_mm = max(2.0, float(wid_use / mm) * (float(getattr(props, "dovetail_fit_width_pct", 100.0)) * 0.01))
    else:
        width_mm = float(props.dovetail_width_mm)

    dmode = getattr(props, "dovetail_fit_depth_mode", "PERCENT_NORMAL")
    dpc   = float(getattr(props, "dovetail_fit_depth_pct", 25.0)) * 0.01
    if dmode == "PERCENT_NORMAL":
        depth_mm = max(2.0, float(n_use / mm) * dpc)
    elif dmode == "PERCENT_SHORT":
        depth_mm = max(2.0, float(wid_use / mm) * dpc)
    else:
        depth_mm = float(props.dovetail_depth_mm)

    return length_mm, width_mm, depth_mm, (t1, t2, span1, span2)

def place_one_dovetail_at(a, b, axis, point_world, frame_z=None, props=None, name_prefix="Dovetail_Click"):
    if props is None:
        props = bpy.context.scene.snapsplit
    mm = unit_mm()

    length_mm, width_mm, depth_mm, (t1, t2, span1, span2) = _calc_dovetail_dims_from_spans(a, b, axis, props)

    if span1 >= span2:
        z_dir = t1.normalized()
        y_dir = t2.normalized()
    else:
        z_dir = t2.normalized()
        y_dir = t1.normalized()
    x_dir = y_dir.cross(z_dir)
    if x_dir.length_squared < 1e-12:
        x_dir = Vector((1,0,0))
        if abs(x_dir.dot(z_dir)) > 0.99:
            x_dir = Vector((0,1,0))
        y_dir = z_dir.cross(x_dir).normalized()
        x_dir = y_dir.cross(z_dir).normalized()
    else:
        x_dir.normalize()

    embed_pct = float(getattr(props, "pin_embed_pct", 50.0)) * 0.01
    L_scene = float(length_mm) * mm
    p_embed = point_world - z_dir * (embed_pct * L_scene)

    M = Matrix(((x_dir.x, y_dir.x, z_dir.x, p_embed.x),
                (x_dir.y, y_dir.y, z_dir.y, p_embed.y),
                (x_dir.z, y_dir.z, z_dir.z, p_embed.z),
                (0,       0,       0,       1.0)))
    M = _rotate_frame_for_slide_dir(M, getattr(props, "dovetail_slide_dir", "+X"))

    props.dovetail_length_mm = length_mm
    props.dovetail_width_mm  = width_mm
    props.dovetail_depth_mm  = depth_mm

    cutters_coll = ensure_collection("_SnapSplit_Cutters")
    tong = create_dovetail_tongue(width_mm=width_mm, depth_mm=depth_mm, length_mm=length_mm,
                                  draft_deg=props.dovetail_draft_deg, leadin_chamfer_mm=props.dovetail_leadin_chamfer_mm,
                                  name=f"{name_prefix}_Tongue")
    tong.matrix_world = M
    cutters_coll.objects.link(tong)

    for mod in list(tong.modifiers):
        if mod.type == 'BEVEL':
            bpy.context.view_layer.objects.active = tong
            tong.select_set(True)
            try: bpy.ops.object.modifier_apply(modifier=mod.name)
            except Exception as e:
                report_user(None, 'WARNING', f"Bevel apply failure: {e}", "Bevel anwenden fehlgeschlagen.")
            tong.select_set(False)

    union_and_dispose(b, tong, name=f"{name_prefix}_Union")

    base_tol = float(props.effective_tolerance())
    clr_scale = float(getattr(props, "dovetail_clearance_scale", 1.0))
    c_mm = base_tol * clr_scale
    sock = create_dovetail_socket_cutter(width_mm=width_mm, depth_mm=depth_mm, length_mm=length_mm,
                                         clearance_per_side_mm=c_mm, draft_deg=props.dovetail_draft_deg,
                                         name=f"{name_prefix}_SocketCutter")
    sock.matrix_world = M
    cutters_coll.objects.link(sock)
    cut_socket_with_cutter_and_dispose(a, sock)
    return None, None

# ---------------------------
# Batch placement
# ---------------------------

def place_connectors_between(parts, axis, count, ctype, props):
    if not parts:
        return []
    idx = _axis_index(axis)
    ordered = sorted(parts, key=lambda o: o.location[idx])
    pairs = [(ordered[i], ordered[i + 1]) for i in range(len(ordered) - 1)]
    if not pairs:
        return []

    created = []
    pct, edge_abs = _edge_margins_scene(props)
    cols = max(1, int(getattr(props, "connectors_per_seam", count)))

    for a, b in pairs:
        seam_pos = _pair_seam_plane_pos(a, b, axis, props)

        if getattr(props, "connector_distribution", "LINE") == "GRID":
            rows = max(1, int(getattr(props, "connectors_rows", 2)))
            points = distribute_points_grid_on_seam(a, b, cols, rows, axis, seam_pos, margin_pct=pct, edge_margin_scene=edge_abs)
        else:
            points = distribute_points_line_on_seam(a, b, cols, axis, seam_pos, margin_pct=pct, edge_margin_scene=edge_abs)

        for i, p in enumerate(points):
            ctype_cur = getattr(props, "connector_type", "CYL_PIN")
            if ctype_cur == "DOVETAIL_TAPER":
                place_one_dovetail_at(a, b, axis, p, props=props, name_prefix=f"Dovetail_{i}")
                created.append(None)
            elif ctype_cur in {"CYL_PIN", "SNAP_PIN"}:
                place_one_cyl_pin_at(a, b, axis, p, props=props, name_prefix=f"Pin_{i}")
                created.append(None)
            elif ctype_cur in {"RECT_TENON", "SNAP_TENON"}:
                place_one_tenon_at(a, b, axis, p, props=props, name_prefix=f"Tenon_{i}")
                created.append(None)
            elif ctype_cur == "PIN_HOLE":
                place_one_cyl_pin_at(a, b, axis, p, props=props, name_prefix=f"PinHole_{i}", override_fit_mode=True)
                created.append(None)
            else:
                place_one_tenon_at(a, b, axis, p, props=props, name_prefix=f"Tenon_{i}")
                created.append(None)
    return created

# ---------------------------
# Modal click placement with robust preview
# ---------------------------

class SNAP_OT_place_connectors_click(Operator):
    bl_idname = "snapsplit.place_connectors_click"
    bl_label = "Place connectors (click)"
    bl_options = {'REGISTER', 'UNDO', 'BLOCKING'}

    def invoke(self, context, event):
        props = context.scene.snapsplit
        sel = [o for o in context.selected_objects if o.type == 'MESH']
        if len(sel) != 2:
            report_user(self, 'ERROR', "Select exactly 2 adjacent split parts.", "Genau 2 benachbarte Schnitt-Teile auswählen.")
            return {'CANCELLED'}

        self.a, self.b = sel
        self.axis = props.split_axis
        self.props = props

        try:
            self.seam_pos = _pair_seam_plane_pos(self.a, self.b, self.axis, props)
        except Exception:
            report_user(self, 'ERROR', "Could not compute seam plane.", "Naht-Ebene konnte nicht berechnet werden.")
            return {'CANCELLED'}

        prev_coll = ensure_collection("_SnapSplit_Preview")
        self.preview_obj = None

        try:
            ctype_cur = getattr(props, "connector_type", "CYL_PIN")
            if ctype_cur == "DOVETAIL_TAPER":
                dov_prev = create_dovetail_tongue(props.dovetail_width_mm, props.dovetail_depth_mm, props.dovetail_length_mm,
                                                  props.dovetail_draft_deg, 0.0, name="SnapSplit_Preview_Dovetail")
                dov_prev.display_type = 'WIRE'; dov_prev.hide_select = True
                prev_coll.objects.link(dov_prev)
                self.preview_obj = dov_prev
            elif ctype_cur in {"CYL_PIN", "SNAP_PIN", "PIN_HOLE"}:
                seg = int(max(8, round(self.props.pin_segments)))
                pin_prev = create_cyl_pin(self.props.pin_diameter_mm, self.props.pin_length_mm, self.props.add_chamfer_mm,
                                          segments=seg, name="SnapSplit_Preview_Pin")
                pin_prev.display_type = 'WIRE'; pin_prev.hide_select = True
                prev_coll.objects.link(pin_prev)
                self.preview_obj = pin_prev
            elif ctype_cur in {"RECT_TENON", "SNAP_TENON"}:
                ten_prev = create_rect_tenon_quader(self.props.tenon_width_mm, self.props.tenon_depth_mm, self.props.add_chamfer_mm,
                                                    name="SnapSplit_Preview_Tenon")
                ten_prev.display_type = 'WIRE'; ten_prev.hide_select = True
                prev_coll.objects.link(ten_prev)
                self.preview_obj = ten_prev
        except Exception:
            self.preview_obj = None

        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def finish(self, context, cancelled=False):
        try:
            if getattr(self, "preview_obj", None) and self.preview_obj.name in bpy.data.objects:
                for coll in list(self.preview_obj.users_collection):
                    coll.objects.unlink(self.preview_obj)
                bpy.data.objects.remove(self.preview_obj)
        except Exception:
            pass
        if cancelled:
            report_user(self, 'INFO', "Placement cancelled.", "Platzierung abgebrochen.")

    def modal(self, context, event):
        try:
            if event.type in {'ESC', 'RIGHTMOUSE'} and event.value == 'PRESS':
                self.finish(context, cancelled=True)
                return {'CANCELLED'}

            if event.type == 'MOUSEMOVE':
                hit = self._intersect_mouse_with_seam_plane(context, event)
                if hit is not None and self.preview_obj:
                    M = self._build_frame_for_preview(hit)
                    if getattr(self.props, "connector_type", "") == "DOVETAIL_TAPER":
                        mm = unit_mm()
                        pct, edge_abs = _edge_margins_scene(self.props)
                        (t1, lo1, hi1, span1), (t2, lo2, hi2, span2), _ = _seam_overlap_axes(self.a, self.b, self.axis, self.seam_pos)
                        if span1 >= span2:
                            len_lo, len_hi, len_span = lo1, hi1, span1
                        else:
                            len_lo, len_hi, len_span = lo2, hi2, span2
                        use_full = bool(getattr(self.props, "dovetail_use_full_span", True)) or self.props.dovetail_auto_fit=="FIT_LENGTH"
                        end_inset_scene = float(getattr(self.props, "dovetail_end_inset_mm", 0.0)) * mm
                        _, _, len_use = _apply_margins_to_span(len_lo, len_hi, len_span, pct, edge_abs, end_inset_scene if use_full else 0.0)
                        new_len_mm = float(len_use / mm) if use_full else float(self.props.dovetail_length_mm)
                        try:
                            prev_M = self.preview_obj.matrix_world.copy()
                            tmp = create_dovetail_tongue(self.props.dovetail_width_mm, self.props.dovetail_depth_mm,
                                                         new_len_mm, self.props.dovetail_draft_deg, 0.0,
                                                         name="SnapSplit_Preview_Dovetail_TMP")
                            if self.preview_obj.data.users == 1:
                                bpy.data.meshes.remove(self.preview_obj.data, do_unlink=True)
                            self.preview_obj.data = tmp.data
                            tmp.data = None
                            bpy.data.objects.remove(tmp)
                            self.preview_obj.matrix_world = prev_M
                        except Exception:
                            pass
                    self.preview_obj.matrix_world = M
                    for coll in self.preview_obj.users_collection:
                        coll.hide_viewport = False
                return {'RUNNING_MODAL'}

            if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
                hit = self._intersect_mouse_with_seam_plane(context, event)
                if hit is not None:
                    ctype_cur = getattr(self.props, "connector_type", "CYL_PIN")
                    if ctype_cur == "CYL_PIN":
                        place_one_cyl_pin_at(self.a, self.b, self.axis, hit, props=self.props, name_prefix="Pin_Click")
                    elif ctype_cur == "RECT_TENON":
                        place_one_tenon_at(self.a, self.b, self.axis, hit, props=self.props, name_prefix="Tenon_Click")
                    elif ctype_cur == "SNAP_PIN":
                        place_one_cyl_pin_at(self.a, self.b, self.axis, hit, props=self.props, name_prefix="Pin_Click")
                    elif ctype_cur == "SNAP_TENON":
                        place_one_tenon_at(self.a, self.b, self.axis, hit, props=self.props, name_prefix="Tenon_Click")
                    elif ctype_cur == "PIN_HOLE":
                        place_one_cyl_pin_at(self.a, self.b, self.axis, hit, props=self.props, name_prefix="PinHole_Click", override_fit_mode=True)
                    elif ctype_cur == "DOVETAIL_TAPER":
                        place_one_dovetail_at(self.a, self.b, self.axis, hit, props=self.props, name_prefix="Dovetail_Click")
                    else:
                        report_user(self, 'INFO', "Use batch add for this connector.", "Für diesen Verbinder Batch verwenden.")
                return {'RUNNING_MODAL'}

            return {'RUNNING_MODAL'}

        except Exception as e:
            report_user(self, 'ERROR', f"Modal error: {e}", "Modal-Fehler.")
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

    def _build_frame_for_preview(self, point_world):
        if getattr(self.props, "connector_type", "") == "DOVETAIL_TAPER":
            (t1, lo1, hi1, span1), (t2, lo2, hi2, span2), _ = _seam_overlap_axes(self.a, self.b, self.axis, self.seam_pos)
            if span1 >= span2:
                z_dir = t1.normalized(); y_dir = t2.normalized()
            else:
                z_dir = t2.normalized(); y_dir = t1.normalized()
            x_dir = y_dir.cross(z_dir)
            if x_dir.length_squared < 1e-12:
                x_dir = Vector((1,0,0))
                if abs(x_dir.dot(z_dir)) > 0.99:
                    x_dir = Vector((0,1,0))
                y_dir = z_dir.cross(x_dir).normalized()
                x_dir = y_dir.cross(z_dir).normalized()
            else:
                x_dir.normalize()
            L_scene = float(self.props.dovetail_length_mm) * unit_mm()
            embed_pct = float(getattr(self.props, "pin_embed_pct", 50.0)) * 0.01
            p_embed = point_world - z_dir * (embed_pct * L_scene)
            M = Matrix(((x_dir.x, y_dir.x, z_dir.x, p_embed.x),
                        (x_dir.y, y_dir.y, z_dir.y, p_embed.y),
                        (x_dir.z, y_dir.z, z_dir.z, p_embed.z),
                        (0,       0,       0,       1.0)))
            return _rotate_frame_for_slide_dir(M, getattr(self.props, "dovetail_slide_dir", "+X"))

        z = {"X": Vector((1,0,0)), "Y": Vector((0,1,0)), "Z": Vector((0,0,1))}[self.axis].normalized()
        x = Vector((1,0,0))
        if abs(z.dot(x)) > 0.99:
            x = Vector((0,1,0))
        y = z.cross(x); y.normalize()
        x = y.cross(z); x.normalize()
        return Matrix(((x.x, y.x, z.x, point_world.x),
                       (x.y, y.y, z.y, point_world.y),
                       (x.z, y.z, z.z, point_world.z),
                       (0,   0,   0,   1.0)))

# ---------------------------
# Batch operator
# ---------------------------

class SNAP_OT_add_connectors(Operator):
    bl_idname = "snapsplit.add_connectors"
    bl_label = "Add connectors"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        props = context.scene.snapsplit
        sel = [o for o in context.selected_objects if o.type == 'MESH']
        if len(sel) < 2:
            report_user(self, 'ERROR', "Select at least 2 cut mesh-pieces.", "Mindestens 2 geschnittene Mesh-Teile auswählen.")
            return {'CANCELLED'}

        created = place_connectors_between(parts=sel, axis=props.split_axis, count=props.connectors_per_seam, ctype=props.connector_type, props=props)
        report_user(self, 'INFO', f"{len(created)} connectors created.", f"{len(created)} Verbinder erstellt.")
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
