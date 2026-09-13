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
from math import tan, radians
from mathutils import Vector, Matrix
from bpy.types import Operator
from bpy_extras import view3d_utils

from .utils import ensure_collection, unit_mm, report_user
from .languages import tr  # centralized translation helper


# ---------------------------
# Collection cleanup utilities
# ---------------------------

def remove_collection_by_name(coll_name: str):
    """Unlink and remove a collection by name, including unlinking/removing all its objects."""
    coll = bpy.data.collections.get(coll_name)
    if not coll:
        return
    objs = list(coll.objects)
    for obj in objs:
        if not obj:
            continue
        # Unlink object from all collections first
        try:
            for c in list(obj.users_collection):
                try:
                    c.objects.unlink(obj)
                except Exception:
                    pass
        except Exception:
            pass

        mesh_data = getattr(obj, "data", None)
        # Remove object, try hard fallback
        try:
            bpy.data.objects.remove(obj)
        except Exception:
            try:
                _dispose_object(obj, remove_data=False)
            except Exception:
                pass

        # Remove orphaned mesh data
        try:
            if mesh_data and hasattr(mesh_data, "users") and mesh_data.users == 0:
                if mesh_data.__class__.__name__ == "Mesh":
                    bpy.data.meshes.remove(mesh_data)
                else:
                    try:
                        bpy.data.batch_remove((mesh_data,))
                    except Exception:
                        pass
        except Exception:
            pass

    # Unlink the collection from any parents and the scene root
    try:
        for parent in list(bpy.data.collections):
            try:
                if coll.name in [c.name for c in getattr(parent, "children", [])]:
                    parent.children.unlink(coll)
            except Exception:
                pass
    except Exception:
        pass
    try:
        scene_root = bpy.context.view_layer.layer_collection.collection
        if coll.name in [c.name for c in scene_root.children]:
            scene_root.children.unlink(coll)
    except Exception:
        pass
    # Remove collection
    try:
        bpy.data.collections.remove(coll)
    except Exception:
        pass


def remove_cutters_collection():
    """Remove the helper collection '_SnapSplit_Cutters' and its content completely."""
    remove_collection_by_name("_SnapSplit_Cutters")


# ---------------------------
# BBox and projection
# ---------------------------

def _bb_world(obj):
    """Return the world-space bounding box corner coordinates of an object."""
    return [obj.matrix_world @ Vector(c) for c in obj.bound_box]


def _proj_interval(points, axis_dir, origin):
    """Project points onto a direction (axis_dir) and return min/max distances from origin."""
    a = axis_dir.normalized()
    return (min((p - origin).dot(a) for p in points),
            max((p - origin).dot(a) for p in points))


def _axis_index(axis):
    """Return index 0/1/2 for X/Y/Z axis string."""
    return {"X": 0, "Y": 1, "Z": 2}[axis]


def _axis_vectors(axis):
    """Return normal and two tangential unit vectors for a given axis string."""
    # axis denotes seam normal here (split axis)
    if axis == "X":
        return Vector((1, 0, 0)), Vector((0, 1, 0)), Vector((0, 0, 1))
    if axis == "Y":
        return Vector((0, 1, 0)), Vector((1, 0, 0)), Vector((0, 0, 1))
    return Vector((0, 0, 1)), Vector((1, 0, 0)), Vector((0, 1, 0))


def _pair_seam_plane_pos(obj_a, obj_b, axis, props):
    """Return world-space seam plane coordinate along axis for a specific adjacent pair (A,B)."""
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
    """Distribute 'count' points along the overlap line of (A,B) on the given seam plane."""
    n_axis, t1, t2 = _axis_vectors(axis)
    bb_a = _bb_world(obj_a)
    bb_b = _bb_world(obj_b)

    ca = sum(bb_a, Vector()) / 8.0
    cb = sum(bb_b, Vector()) / 8.0
    origin = (ca + cb) * 0.5
    oi = _axis_index(axis)
    origin = Vector((origin.x, origin.y, origin.z))
    origin[oi] = seam_pos

    t1_min_a, t1_max_a = _proj_interval(bb_a, t1, origin)
    t1_min_b, t1_max_b = _proj_interval(bb_b, t1, origin)
    t2_min_a, t2_max_a = _proj_interval(bb_a, t2, origin)
    t2_min_b, t2_max_b = _proj_interval(bb_b, t2, origin)

    ol1 = max(0.0, min(t1_max_a, t1_max_b) - max(t1_min_a, t1_min_b))
    ol2 = max(0.0, min(t2_max_a, t2_max_b) - max(t2_min_a, t2_min_b))

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
    """Distribute cols*rows points over the 2D overlap of (A,B) on the given seam plane."""
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
        return distribute_points_line_on_seam(obj_a, obj_b, cols, axis, seam_pos, margin_pct)

    m1 = max(0.0, float(margin_pct)) * 0.01 * span1
    m2 = max(0.0, float(margin_pct)) * 0.01 * span2
    lo1_i, hi1_i = lo1 + m1, hi1 - m1
    lo2_i, hi2_i = lo2 + m2, hi2 - m2
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
# Geometry: base connectors
# ---------------------------

def create_cyl_pin(d_mm=5.0, length_mm=10.0, chamfer_mm=0.0, segments=32, name="SnapSplit_Pin"):
    """Create a cylindrical pin mesh object with optional top chamfer."""
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
    """Create a rectangular tenon (elongated cube) with optional bevel modifier for chamfer."""
    mm = unit_mm()
    w = float(w_mm) * mm
    L = float(length_mm) * mm
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    sx = w; sy = w; sz = L
    S = Matrix(((sx, 0, 0, 0), (0, sy, 0, 0), (0, 0, sz, 0), (0, 0, 0, 1)))
    bmesh.ops.transform(bm, matrix=S, verts=bm.verts)
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


def create_uv_sphere(d_mm=2.0, segments=16, rings=8, name="SnapSphere"):
    """Create a UV sphere mesh object with given diameter and segment counts."""
    mm = unit_mm()
    r = max(1e-9, float(d_mm) * 0.5 * mm)

    bm = bmesh.new()
    bmesh.ops.create_uvsphere(
        bm,
        u_segments=max(8, int(segments)),
        v_segments=max(6, int(rings)),
        radius=r,
        calc_uvs=False
    )
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    obj = bpy.data.objects.new(name, me)
    return obj


def create_uv_sphere_preview(d_mm=2.0, segments=12, rings=6, name="SnapSpherePreview"):
    """Create a lightweight wireframe UV sphere for viewport previews."""
    mm = unit_mm()
    r = max(1e-9, float(d_mm) * 0.5 * mm)

    bm = bmesh.new()
    bmesh.ops.create_uvsphere(
        bm,
        u_segments=max(8, int(segments)),
        v_segments=max(6, int(rings)),
        radius=r,
        calc_uvs=False
    )
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    obj = bpy.data.objects.new(name, me)
    obj.display_type = 'WIRE'
    obj.hide_select = True
    return obj


# ---------------------------
# Dovetail geometry (u/v/n relative): new
# ---------------------------

def _safe_mm(v, default):
    """Return a safe float millimeter value with fallback."""
    try:
        return float(v) if v is not None else float(default)
    except Exception:
        return float(default)


def create_dovetail_box_uvn(width_u_mm=10.0, length_v_mm=10.0, depth_n_mm=8.0,
                            signed_taper_pct=0.0, name="SnapSplit_DovetailUVN"):
    """Create a dovetail as a tapered rectangular prism in local (u,v,n):

    - Base face at n=0 (wider in u/v), tip at n=depth_n (narrower/wider per signed taper).
    - Signed taper applies only to in-plane axes (u and v) symmetrically.
      positive -> tip narrower; negative -> tip wider.
    - Depth is not tapered (pure extrusion along n).
    """
    mm = unit_mm()
    wu = max(0.1, _safe_mm(width_u_mm, 10.0)) * mm
    lv = max(0.1, _safe_mm(length_v_mm, 10.0)) * mm
    dn = max(0.1, _safe_mm(depth_n_mm, 8.0)) * mm

    t = max(-90.0, min(90.0, float(signed_taper_pct))) * 0.01
    # Tip scales equally in u and v; clamp to avoid degeneracy
    s_tip = max(0.05, 1.0 - t)

    wb_u = wu; wb_v = lv
    wt_u = max(0.1 * mm, wu * s_tip)
    wt_v = max(0.1 * mm, lv * s_tip)

    bm = bmesh.new()
    # Base (n=0)
    v0 = bm.verts.new((-0.5 * wb_u, -0.5 * wb_v, 0.0))
    v1 = bm.verts.new(( 0.5 * wb_u, -0.5 * wb_v, 0.0))
    v2 = bm.verts.new(( 0.5 * wb_u,  0.5 * wb_v, 0.0))
    v3 = bm.verts.new((-0.5 * wb_u,  0.5 * wb_v, 0.0))
    # Tip (n=depth)
    v4 = bm.verts.new((-0.5 * wt_u, -0.5 * wt_v, dn))
    v5 = bm.verts.new(( 0.5 * wt_u, -0.5 * wt_v, dn))
    v6 = bm.verts.new(( 0.5 * wt_u,  0.5 * wt_v, dn))
    v7 = bm.verts.new((-0.5 * wt_u,  0.5 * wt_v, dn))

    bm.faces.new([v3, v2, v1, v0])  # base
    bm.faces.new([v4, v5, v6, v7])  # tip
    bm.faces.new([v0, v1, v5, v4])
    bm.faces.new([v1, v2, v6, v5])
    bm.faces.new([v2, v3, v7, v6])
    bm.faces.new([v3, v0, v4, v7])

    me = bpy.data.meshes.new(name)
    bm.to_mesh(me); bm.free()
    return bpy.data.objects.new(name, me)


# ---------------------------
# New geometry: flush barbs (unchanged)
# ---------------------------

def _tip_width_from_angle(base_w_mm: float, angle_per_side_deg: float) -> float:
    """Approximate tip width (mm) from base width and taper angle per side (legacy helper, kept)."""
    try:
        a = max(0.0, float(angle_per_side_deg))
        pct = max(0.0, min(0.9, 2.0 * tan(radians(a)) / 10.0))
    except Exception:
        pct = 0.25
    tip = max(0.1, float(base_w_mm) * (1.0 - pct))
    return tip


def _compute_tip_from_signed_taper(base_w_mm: float, signed_taper_pct: float) -> float:
    """Legacy helper for symmetric square-section dovetail; kept for compatibility paths."""
    t = max(-60.0, min(60.0, float(signed_taper_pct))) * 0.01
    wb = max(0.1, float(base_w_mm))
    wt = wb * (1.0 - t)
    return max(0.1, wt)


def create_dovetail_quader(base_w_mm=6.0, depth_mm=8.0, taper_pct=None, angle_per_side_deg=None, name="SnapSplit_Dovetail"):
    """Legacy square dovetail (width=length), retained for backward compatibility."""
    mm = unit_mm()
    wb = float(base_w_mm) * mm
    L = float(depth_mm) * mm

    if angle_per_side_deg is not None:
        wt_mm = _tip_width_from_angle(base_w_mm, angle_per_side_deg)
        wt = float(wt_mm) * mm
    else:
        t = 0.25 if taper_pct is None else max(0.0, min(95.0, float(taper_pct))) * 0.01
        wt = max(1e-9, wb * (1.0 - t))

    bm = bmesh.new()
    half_wb = wb * 0.5
    half_wt = wt * 0.5
    v0 = bm.verts.new((-half_wb, -half_wb, 0.0))
    v1 = bm.verts.new(( half_wb, -half_wb, 0.0))
    v2 = bm.verts.new(( half_wb,  half_wb, 0.0))
    v3 = bm.verts.new((-half_wb,  half_wb, 0.0))
    v4 = bm.verts.new((-half_wt, -half_wt, L))
    v5 = bm.verts.new(( half_wt, -half_wt, L))
    v6 = bm.verts.new(( half_wt,  half_wt, L))
    v7 = bm.verts.new((-half_wt,  half_wt, L))
    bm.faces.new([v3, v2, v1, v0])
    bm.faces.new([v4, v5, v6, v7])
    bm.faces.new([v0, v1, v5, v4])
    bm.faces.new([v1, v2, v6, v5])
    bm.faces.new([v2, v3, v7, v6])
    bm.faces.new([v3, v0, v4, v7])

    me = bpy.data.meshes.new(name)
    bm.to_mesh(me); bm.free()
    obj = bpy.data.objects.new(name, me)
    return obj


def create_dovetail_quader_signed(base_w_mm=6.0, depth_mm=8.0, signed_taper_pct=0.0, name="SnapSplit_DovetailSigned"):
    """Legacy square-section dovetail with signed taper; retained for compatibility."""
    mm = unit_mm()
    wb = float(base_w_mm) * mm
    L = float(depth_mm) * mm
    wt_mm = _compute_tip_from_signed_taper(base_w_mm, signed_taper_pct)
    wt = float(wt_mm) * mm

    bm = bmesh.new()
    half_wb = wb * 0.5
    half_wt = wt * 0.5
    v0 = bm.verts.new((-half_wb, -half_wb, 0.0))
    v1 = bm.verts.new(( half_wb, -half_wb, 0.0))
    v2 = bm.verts.new(( half_wb,  half_wb, 0.0))
    v3 = bm.verts.new((-half_wb,  half_wb, 0.0))
    v4 = bm.verts.new((-half_wt, -half_wt, L))
    v5 = bm.verts.new(( half_wt, -half_wt, L))
    v6 = bm.verts.new(( half_wt,  half_wt, L))
    v7 = bm.verts.new((-half_wt,  half_wt, L))
    bm.faces.new([v3, v2, v1, v0])
    bm.faces.new([v4, v5, v6, v7])
    bm.faces.new([v0, v1, v5, v4])
    bm.faces.new([v1, v2, v6, v5])
    bm.faces.new([v2, v3, v7, v6])
    bm.faces.new([v3, v0, v4, v7])

    me = bpy.data.meshes.new(name)
    bm.to_mesh(me); bm.free()
    obj = bpy.data.objects.new(name, me)
    return obj


def create_flush_barb_cylinder(d_mm=5.0, length_mm=8.0, barb_height_mm=0.6, barb_lip_mm=0.25, segments=32, name="SnapSplit_FlushBarb_Pin"):
    """Create a cylindrical pin with a shallow barb near the seam plane for flush snap-fit."""
    mm = unit_mm()
    d = float(d_mm) * mm
    L = float(length_mm) * mm
    r = max(1e-9, 0.5 * d)
    lip = max(0.0, float(barb_lip_mm) * mm)
    h = max(0.05 * mm, float(barb_height_mm) * mm)

    base = create_cyl_pin(d_mm, length_mm, chamfer_mm=0.0, segments=segments, name=name)
    bm = bmesh.new()
    bm.from_mesh(base.data)
    for v in bm.verts:
        if 0.0 <= v.co.z <= h:
            if r > 1e-9:
                s = (r + lip) / r
                v.co.x *= s
                v.co.y *= s
    bm.to_mesh(base.data); bm.free()
    base.data.update()
    return base


def create_flush_barb_rect(w_mm=6.0, length_mm=8.0, barb_height_mm=0.6, barb_lip_mm=0.25, name="SnapSplit_FlushBarb_Tenon"):
    """Create a rectangular tenon with a shallow barb (slight XY flare) near the seam plane."""
    mm = unit_mm()
    w = float(w_mm) * mm
    L = float(length_mm) * mm
    lip = max(0.0, float(barb_lip_mm) * mm)
    h = max(0.05 * mm, float(barb_height_mm) * mm)

    ten = create_rect_tenon_quader(w_mm, length_mm, chamfer_mm=0.0, name=name)
    bm = bmesh.new()
    bm.from_mesh(ten.data)
    for v in bm.verts:
        if 0.0 <= v.co.z <= h:
            half = max(1e-9, 0.5 * w)
            s = 1.0 + (lip / half)
            v.co.x *= s
            v.co.y *= s
    bm.to_mesh(ten.data); bm.free()
    ten.data.update()
    return ten


# ---------------------------
# Boolean helpers and transform robustness
# ---------------------------

def _apply_object_scale_if_needed(obj):
    """Apply object scale if it's not uniform 1.0 to avoid Boolean instabilities."""
    try:
        sx, sy, sz = obj.scale
        if not (abs(sx - 1.0) < 1e-6 and abs(sy - 1.0) < 1e-6 and abs(sz - 1.0) < 1e-6):
            bpy.context.view_layer.objects.active = obj
            obj.select_set(True)
            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
            obj.select_set(False)
    except Exception:
        pass


def _set_boolean_solver_with_fallback(mod):
    """Try to set solver EXACT, fallback to FAST/FLOAT if unavailable or apply fails upstream."""
    try:
        items = {i.identifier for i in mod.bl_rna.properties['solver'].enum_items}
        if 'EXACT' in items:
            mod.solver = 'EXACT'
        elif 'FAST' in items:
            mod.solver = 'FAST'
        elif 'FLOAT' in items:
            mod.solver = 'FLOAT'
    except Exception:
        try:
            mod.solver = 'EXACT'
        except Exception:
            pass


def boolean_apply(target_obj, mod):
    """Apply a Boolean (or any) modifier on target_obj with validation and error handling."""
    bpy.context.view_layer.objects.active = target_obj
    target_obj.select_set(True)
    try:
        bpy.ops.object.modifier_apply(modifier=mod.name)
    except Exception as e:
        report_user(None, 'WARNING',
                    tr("op.common.warn.mod_apply_fail", f"Modifier apply failed ({mod.name}): {e}"))
    target_obj.select_set(False)
    try:
        target_obj.data.validate(verbose=False)
        target_obj.data.update()
    except Exception:
        pass


def cut_socket_with_cutter(target_obj, cutter_obj):
    """Apply a DIFFERENCE Boolean using cutter_obj on target_obj to create a socket."""
    _apply_object_scale_if_needed(cutter_obj)
    mod = target_obj.modifiers.new("SnapSplit_Socket", 'BOOLEAN')
    mod.operation = 'DIFFERENCE'
    _set_boolean_solver_with_fallback(mod)
    mod.object = cutter_obj
    boolean_apply(target_obj, mod)


# ---------------------------
# TEMP helpers: dispose temporary objects
# ---------------------------

def _dispose_object(obj, remove_data=True):
    """Unlink and remove an object; optionally remove and clear its data if orphaned."""
    if not obj:
        return
    try:
        for coll in list(obj.users_collection):
            try:
                coll.objects.unlink(obj)
            except Exception:
                pass
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
    """Apply DIFFERENCE Boolean and dispose the cutter object afterwards."""
    _apply_object_scale_if_needed(cutter_obj)
    mod = target_obj.modifiers.new("SnapSplit_Socket", 'BOOLEAN')
    mod.operation = 'DIFFERENCE'
    _set_boolean_solver_with_fallback(mod)
    mod.object = cutter_obj
    boolean_apply(target_obj, mod)
    _dispose_object(cutter_obj, remove_data=True)


def union_and_dispose(target_obj, union_obj, name="SnapSplit_Union"):
    """Apply UNION Boolean and dispose the helper object afterwards."""
    _apply_object_scale_if_needed(union_obj)
    mod = target_obj.modifiers.new(name, 'BOOLEAN')
    mod.operation = 'UNION'
    _set_boolean_solver_with_fallback(mod)
    mod.object = union_obj
    boolean_apply(target_obj, mod)
    _dispose_object(union_obj, remove_data=True)


# ---------------------------
# Snap spheres helpers (for cylindrical Pins)
# ---------------------------

def _ring_height_for_visible_half(length_scene, embed_pct):
    """Return the center Z of the protruding half (part B side) along the frame Z-axis."""
    L_free = max(0.0, (1.0 - embed_pct) * length_scene)
    return embed_pct * length_scene + 0.5 * L_free


def _choose_visible_half_robust(base_matrix, zA, zB):
    """Choose which local Z (A or B) protrudes in world coordinates using the frame Z-axis."""
    try:
        z_axis_world = Vector((base_matrix[0][2], base_matrix[1][2], base_matrix[2][2])).normalized()
        p0_w = Vector((base_matrix[0][3], base_matrix[1][3], base_matrix[2][3]))
        pA_w = base_matrix @ Vector((0.0, 0.0, zA, 1.0))
        pB_w = base_matrix @ Vector((0.0, 0.0, zB, 1.0))
        dA = (Vector((pA_w.x, pA_w.y, pA_w.z)) - p0_w).dot(z_axis_world)
        dB = (Vector((pB_w.x, pB_w.y, pB_w.z)) - p0_w).dot(z_axis_world)
        return zB if dB >= dA else zA
    except Exception:
        return zB


def add_snap_spheres_for_cyl_pin(base_matrix, pin_radius_scene, length_scene, props, name_prefix, part_a, part_b, cutters_coll):
    """Add a ring of snap spheres around a cylindrical pin; union to B, socket to A, and dispose helpers."""
    mm = unit_mm()
    n_per_side = max(1, int(getattr(props, "snap_spheres_per_side", 2)))
    d_sph_mm = float(getattr(props, "snap_sphere_diameter_mm", 2.0))
    protrude_scene = float(getattr(props, "snap_sphere_protrusion_mm", 1.0)) * mm

    embed_pct = max(0.0, min(1.0, float(getattr(props, "pin_embed_pct", 50.0)) * 0.01))
    zA = 0.5 * embed_pct * length_scene
    zB = _ring_height_for_visible_half(length_scene, embed_pct)
    ring_z = _choose_visible_half_robust(base_matrix, zA, zB)

    import math
    created = []
    sph_r_scene = 0.5 * float(d_sph_mm) * mm
    r_center = pin_radius_scene + protrude_scene - sph_r_scene

    for i in range(n_per_side):
        ang = (2.0 * math.pi) * (i / n_per_side)
        nx = math.cos(ang); ny = math.sin(ang)

        local_pos = Vector((r_center * nx, r_center * ny, ring_z))
        world_pos = base_matrix @ Vector((local_pos.x, local_pos.y, local_pos.z, 1.0))
        world_pos = Vector((world_pos.x, world_pos.y, world_pos.z))

        sphere = create_uv_sphere(d_mm=d_sph_mm, segments=24, rings=12, name=f"{name_prefix}_Snap_{i}")
        M = Matrix.Translation(world_pos)
        sphere.matrix_world = M
        cutters_coll.objects.link(sphere)

        tol = float(props.effective_tolerance())
        scale = 1.0 + (tol * mm) / max(sph_r_scene, 1e-9)

        sph_cut = sphere.copy()
        sph_cut.data = sphere.data.copy()
        sph_cut.name = f"{name_prefix}_SnapC_{i}"
        cutters_coll.objects.link(sph_cut)
        sph_cut.matrix_world = M @ Matrix.Diagonal(Vector((scale, scale, scale, 1.0)))

        union_and_dispose(part_b, sphere, name=f"{name_prefix}_SnapU_{i}")
        cut_socket_with_cutter_and_dispose(part_a, sph_cut)

        created.append(None)
    return created


# ---------------------------
# Sphere-placement helpers (for rectangular Tenon-as-Quader; ring like pin)
# ---------------------------

def add_snap_spheres_for_rect_tenon_ring(base_matrix, half_w_scene, length_scene, props, name_prefix, part_a, part_b, cutters_coll):
    """Add a ring of snap spheres around a square-section tenon; union to B, socket to A, and dispose helpers."""
    mm = unit_mm()
    n_per_side = max(1, int(getattr(props, "snap_spheres_per_side", 2)))
    d_sph_mm = float(getattr(props, "snap_sphere_diameter_mm", 2.0))
    protrude_scene = float(getattr(props, "snap_sphere_protrusion_mm", 1.0)) * mm

    embed_pct = max(0.0, min(1.0, float(getattr(props, "pin_embed_pct", 50.0)) * 0.01))
    zA = 0.5 * embed_pct * length_scene
    zB = _ring_height_for_visible_half(length_scene, embed_pct)
    ring_z = _choose_visible_half_robust(base_matrix, zA, zB)

    import math
    created = []
    sph_r_scene = 0.5 * float(d_sph_mm) * mm
    r_center = half_w_scene + protrude_scene - sph_r_scene

    for i in range(n_per_side):
        ang = (2.0 * math.pi) * (i / n_per_side)
        nx = math.cos(ang); ny = math.sin(ang)

        local_pos = Vector((r_center * nx, r_center * ny, ring_z))
        world_pos = base_matrix @ Vector((local_pos.x, local_pos.y, local_pos.z, 1.0))
        world_pos = Vector((world_pos.x, world_pos.y, world_pos.z))

        sphere = create_uv_sphere(d_mm=d_sph_mm, segments=24, rings=12, name=f"{name_prefix}_Snap_{i}")
        M = Matrix.Translation(world_pos)
        sphere.matrix_world = M
        cutters_coll.objects.link(sphere)

        tol = float(props.effective_tolerance())
        scale = 1.0 + (tol * mm) / max(sph_r_scene, 1e-9)

        sph_cut = sphere.copy()
        sph_cut.data = sphere.data.copy()
        sph_cut.name = f"{name_prefix}_SnapC_{i}"
        cutters_coll.objects.link(sph_cut)
        sph_cut.matrix_world = M @ Matrix.Diagonal(Vector((scale, scale, scale, 1.0)))

        union_and_dispose(part_b, sphere, name=f"{name_prefix}_SnapU_{i}")
        cut_socket_with_cutter_and_dispose(part_a, sph_cut)

        created.append(None)
    return created


# ---------------------------
# Flush barb helper placement (new): no spheres, shallow ring near seam
# ---------------------------

def add_flush_barb_for_cyl(base_matrix, d_mm, length_mm, props, name_prefix, part_a, part_b, cutters_coll):
    """Create flush barb cylinder, union to B and tolerant socket in A."""
    seg = int(getattr(props, "pin_segments", 32))
    pin = create_flush_barb_cylinder(d_mm=d_mm,
                                     length_mm=length_mm,
                                     barb_height_mm=getattr(props, "flush_barb_height_mm", 0.6),
                                     barb_lip_mm=getattr(props, "flush_barb_lip_mm", 0.25),
                                     segments=seg,
                                     name=f"{name_prefix}_FlushPin")
    pin.matrix_world = base_matrix
    cutters_coll.objects.link(pin)
    union_and_dispose(part_b, pin, name=f"{name_prefix}_FlushPinUnion")

    mm = unit_mm()
    tol = float(props.effective_tolerance())
    socket_d = float(d_mm) + 2.0 * tol
    socket = create_flush_barb_cylinder(d_mm=socket_d,
                                        length_mm=length_mm,
                                        barb_height_mm=getattr(props, "flush_barb_height_mm", 0.6),
                                        barb_lip_mm=getattr(props, "flush_barb_lip_mm", 0.25),
                                        segments=seg,
                                        name=f"{name_prefix}_FlushPinSocketCutter")
    socket.matrix_world = base_matrix
    cutters_coll.objects.link(socket)
    cut_socket_with_cutter_and_dispose(part_a, socket)
    return None


def add_flush_barb_for_rect(base_matrix, w_mm, length_mm, props, name_prefix, part_a, part_b, cutters_coll):
    """Create flush barb rectangular tenon, union to B and tolerant socket in A."""
    ten = create_flush_barb_rect(w_mm=w_mm,
                                 length_mm=length_mm,
                                 barb_height_mm=getattr(props, "flush_barb_height_mm", 0.6),
                                 barb_lip_mm=getattr(props, "flush_barb_lip_mm", 0.25),
                                 name=f"{name_prefix}_FlushTenon")
    ten.matrix_world = base_matrix
    cutters_coll.objects.link(ten)
    # Apply possible bevel modifier prior to boolean
    for mod in list(ten.modifiers):
        if mod.type == 'BEVEL':
            bpy.context.view_layer.objects.active = ten
            ten.select_set(True)
            try:
                bpy.ops.object.modifier_apply(modifier=mod.name)
            except Exception as e:
                report_user(None, 'WARNING', tr("op.common.warn.bevel_apply", f"Bevel apply failure: {e}"))
            ten.select_set(False)
    union_and_dispose(part_b, ten, name=f"{name_prefix}_FlushTenonUnion")

    mm = unit_mm()
    tol = float(props.effective_tolerance())
    half_w = max(0.5 * float(w_mm) * mm, 1e-9)
    sx = 1.0 + (tol * mm) / half_w
    sy = sx
    sz = 1.0
    socket = create_flush_barb_rect(w_mm=w_mm,
                                    length_mm=length_mm,
                                    barb_height_mm=getattr(props, "flush_barb_height_mm", 0.6),
                                    barb_lip_mm=getattr(props, "flush_barb_lip_mm", 0.25),
                                    name=f"{name_prefix}_FlushTenonSocketCutter")
    socket.matrix_world = base_matrix @ Matrix.Diagonal(Vector((sx, sy, sz, 1.0)))
    cutters_coll.objects.link(socket)
    cut_socket_with_cutter_and_dispose(part_a, socket)
    return None


# ---------------------------
# Dovetail helpers: span width, frame ops, side-cut
# ---------------------------

def _orthonormal_frame_from_z(z: Vector):
    """Build a stable orthonormal frame (x,y,z) from a given z-axis."""
    z = z.normalized()
    x = Vector((1, 0, 0))
    if abs(z.dot(x)) > 0.99:
        x = Vector((0, 1, 0))
    y = z.cross(x); y.normalize()
    x = y.cross(z); x.normalize()
    return x, y, z


def _apply_inplane_offset_and_rotation(M: Matrix, offset_mm: float, rotation_deg: float):
    """Apply an in-plane translation along local X (major axis) and a rotation around local Z."""
    mm = unit_mm()
    off = float(offset_mm) * mm
    ang = radians(float(rotation_deg))
    # Local transforms: T_x(off) then R_z(ang)
    T = Matrix.Translation((off, 0.0, 0.0))
    R = Matrix.Rotation(ang, 4, 'Z')
    return M @ T @ R


def _compute_edge_to_edge_span_width(a, b, axis, seam_pos, margin_pct=5.0):
    """Return the span length along the longer in-plane overlap axis on the seam plane (scene units)."""
    n_axis, t1, t2 = _axis_vectors(axis)
    bb_a = _bb_world(a); bb_b = _bb_world(b)

    ca = sum(bb_a, Vector()) / 8.0
    cb = sum(bb_b, Vector()) / 8.0
    origin = (ca + cb) * 0.5
    oi = _axis_index(axis)
    origin = Vector((origin.x, origin.y, origin.z))
    origin[oi] = seam_pos

    t1_min_a, t1_max_a = _proj_interval(bb_a, t1, origin)
    t1_min_b, t1_max_b = _proj_interval(bb_b, t1, origin)
    t2_min_a, t2_max_a = _proj_interval(bb_a, t2, origin)
    t2_min_b, t2_max_b = _proj_interval(bb_b, t2, origin)

    ol1 = max(0.0, min(t1_max_a, t1_max_b) - max(t1_min_a, t1_min_b))
    ol2 = max(0.0, min(t2_max_a, t2_max_b) - max(t2_min_a, t2_min_b))
    span = max(ol1, ol2)

    m = max(0.0, float(margin_pct)) * 0.01 * span
    effective = max(0.0, span - 2.0 * m)
    return effective


def _compute_edge_to_edge_span_along_dir(a, b, measure_dir: Vector, axis: str, seam_pos, margin_pct=5.0):
    """Return the span length along a chosen in-plane direction on the seam plane (scene units)."""
    n_axis, t1, t2 = _axis_vectors(axis)
    dirn = measure_dir.normalized()
    bb_a = _bb_world(a); bb_b = _bb_world(b)
    ca = sum(bb_a, Vector()) / 8.0
    cb = sum(bb_b, Vector()) / 8.0
    origin = (ca + cb) * 0.5
    oi = _axis_index(axis)
    origin = Vector((origin.x, origin.y, origin.z))
    origin[oi] = seam_pos

    min_a, max_a = _proj_interval(bb_a, dirn, origin)
    min_b, max_b = _proj_interval(bb_b, dirn, origin)
    lo = max(min_a, min_b)
    hi = min(max_a, max_b)
    span = max(0.0, hi - lo)

    m = max(0.0, float(margin_pct)) * 0.01 * span
    effective = max(0.0, span - 2.0 * m)
    return effective


def _combined_world_bounds(objects):
    """Return combined world AABB (min, max) as 3D vectors for a list of objects."""
    if not objects:
        z = Vector((0, 0, 0))
        return z.copy(), z.copy()
    mins = Vector((float('inf'), float('inf'), float('inf')))
    maxs = Vector((-float('inf'), -float('inf'), -float('inf')))
    for o in objects:
        for c in _bb_world(o):
            mins.x = min(mins.x, c.x)
            mins.y = min(mins.y, c.y)
            mins.z = min(mins.z, c.z)
            maxs.x = max(maxs.x, c.x)
            maxs.y = max(maxs.y, c.y)
            maxs.z = max(maxs.z, c.z)
    return mins, maxs


def _make_infinite_slab_cutter_along_span_axis(span_axis: str, bounds_min: Vector, bounds_max: Vector, thickness_scale=4.0, name="SnapSplit_DovetailSideSlab"):
    """Create two large slab cutters that trim anything outside [min,max] along span_axis, centered on seam plane."""
    slabs = []
    idx = _axis_index(span_axis)
    U = Vector((1, 0, 0)); V = Vector((0, 1, 0)); W = Vector((0, 0, 1))
    axes = [U, V, W]

    other = [0, 1, 2]
    other.remove(idx)
    o1, o2 = other[0], other[1]

    size_o1 = (bounds_max[o1] - bounds_min[o1]) * thickness_scale + 1.0
    size_o2 = (bounds_max[o2] - bounds_min[o2]) * thickness_scale + 1.0

    for side in ("LOW", "HIGH"):
        bm = bmesh.new()
        bmesh.ops.create_cube(bm, size=1.0)
        me = bpy.data.meshes.new(f"{name}_{side}")
        bm.to_mesh(me); bm.free()
        slab = bpy.data.objects.new(f"{name}_{side}", me)

        scale_vec = [size_o1 if i == o1 else (size_o2 if i == o2 else 1.0) for i in range(3)]
        S = Matrix.Diagonal(Vector((scale_vec[0], scale_vec[1], scale_vec[2], 1.0)))

        center = (bounds_min + bounds_max) * 0.5
        pos = Vector((center.x, center.y, center.z))
        if side == "LOW":
            pos[idx] = bounds_min[idx] - 0.5
        else:
            pos[idx] = bounds_max[idx] + 0.5
        T = Matrix.Translation(pos)

        slab.matrix_world = T @ S
        slabs.append(slab)

    return slabs


def _intersect_keep_within_bounds(helper_obj, span_axis: str, bounds_min: Vector, bounds_max: Vector, cutters_coll):
    """Trim helper_obj so that only the portion within [min,max] along span_axis survives."""
    slabs = _make_infinite_slab_cutter_along_span_axis(span_axis, bounds_min, bounds_max, name="SnapSplit_DVT_SideSlab")
    for s in slabs:
        cutters_coll.objects.link(s)

    for s in slabs:
        _apply_object_scale_if_needed(s)
        mod = helper_obj.modifiers.new("SnapSplit_DVT_SideTrim", 'BOOLEAN')
        mod.operation = 'DIFFERENCE'
        _set_boolean_solver_with_fallback(mod)
        mod.object = s
        boolean_apply(helper_obj, mod)
        _dispose_object(s, remove_data=True)


# ---------------------------
# Single-placement helpers (click)
# ---------------------------

def place_one_cyl_pin_at(a, b, axis, point_world, frame_z=None, props=None, name_prefix="Pin_Click"):
    """Place one cylindrical pin at a world point; union into B and cut socket into A."""
    if props is None:
        props = bpy.context.scene.snapsplit
    z = {
        "X": Vector((1, 0, 0)),
        "Y": Vector((0, 1, 0)),
        "Z": Vector((0, 0, 1)),
    }.get(axis, Vector((0, 0, 1))).normalized()
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
    union_and_dispose(b, pin, name=f"{name_prefix}_Union")

    mm = unit_mm()
    tol = float(props.effective_tolerance())
    socket_d = float(props.pin_diameter_mm) + 2.0 * tol
    socket = create_cyl_pin(socket_d, props.pin_length_mm, 0.0, segments=seg, name=f"{name_prefix}_SocketCutter")
    socket.matrix_world = M
    cutters_coll.objects.link(socket)
    cut_socket_with_cutter_and_dispose(a, socket)
    return None, None


def place_one_rect_tenon_at(a, b, axis, point_world, frame_z=None, props=None, name_prefix="Tenon_Click"):
    """Place one rectangular tenon at a world point; union into B and cut socket into A."""
    if props is None:
        props = bpy.context.scene.snapsplit
    z = {
        "X": Vector((1, 0, 0)),
        "Y": Vector((0, 1, 0)),
        "Z": Vector((0, 0, 1)),
    }.get(axis, Vector((0, 0, 1))).normalized()
    if frame_z is not None:
        z = frame_z.normalized()
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

    tenon = create_rect_tenon_quader(props.tenon_width_mm, props.tenon_depth_mm, props.add_chamfer_mm, name=f"{name_prefix}")
    tenon.matrix_world = M
    cutters_coll.objects.link(tenon)
    for mod in list(tenon.modifiers):
        if mod.type == 'BEVEL':
            bpy.context.view_layer.objects.active = tenon
            tenon.select_set(True)
            try:
                bpy.ops.object.modifier_apply(modifier=mod.name)
            except Exception as e:
                report_user(None, 'WARNING', tr("op.common.warn.bevel_apply", f"Bevel apply failure: {e}"))
            tenon.select_set(False)
    union_and_dispose(b, tenon, name=f"{name_prefix}_Union")

    mm = unit_mm()
    tol = float(props.effective_tolerance())
    half_w = max(0.5 * float(props.tenon_width_mm) * mm, 1e-9)
    sx = 1.0 + (tol * mm) / half_w
    sy = sx
    sz = 1.0

    socket = create_rect_tenon_quader(props.tenon_width_mm, props.tenon_depth_mm, 0.0, name=f"{name_prefix}_SocketCutter")
    socket.matrix_world = M @ Matrix.Diagonal(Vector((sx, sy, sz, 1.0)))
    cutters_coll.objects.link(socket)
    cut_socket_with_cutter_and_dispose(a, socket)
    return None, None


def place_one_dovetail_at(a, b, axis, point_world, frame_z=None, props=None, name_prefix="Dovetail_Click"):
    """Place one dovetail wedge at a world point; union into B and cut socket into A.

    Updated behavior (only for Dovetail):
    - Axis-relative sizing tied to seam plane (u, v, n):
      Width -> along u, Length -> along v, Depth -> along n.
    - Signed Taper applies in-plane (u/v) only; Depth is not tapered.
    - AUTO span per in-plane axis (optional): width_u/length_v can be derived from overlap extents.
    - Preview == final: same transforms including in-plane offset/rotation.
    """
    if props is None:
        props = bpy.context.scene.snapsplit

    # Build local UVN from seam normal
    z = {
        "X": Vector((1, 0, 0)),
        "Y": Vector((0, 1, 0)),
        "Z": Vector((0, 0, 1)),
    }.get(axis, Vector((0, 0, 1))).normalized()
    if frame_z is not None:
        z = frame_z.normalized()
    x, y, z = _orthonormal_frame_from_z(z)  # x->u, y->v, z->n

    # Seam plane world coordinate
    try:
        seam_pos = _pair_seam_plane_pos(a, b, axis, props)
    except Exception:
        seam_pos = 0.0

    # Resolve in-plane auto span if requested; otherwise use manual values
    auto_span = bool(getattr(props, "dovetail_auto_span", False))
    margin_pct = float(getattr(props, "dovetail_span_margin_pct", 10.0))

    width_u_mm = float(getattr(props, "dovetail_width_mm", 10.0))
    length_v_mm = float(getattr(props, "dovetail_length_mm", width_u_mm))  # fallback to width if length not defined
    depth_n_mm = float(getattr(props, "dovetail_depth_mm", 8.0))

    if auto_span:
        # Measure span along u and v separately on the seam plane
        span_u = _compute_edge_to_edge_span_along_dir(a, b, x, axis, seam_pos, margin_pct=margin_pct)
        span_v = _compute_edge_to_edge_span_along_dir(a, b, y, axis, seam_pos, margin_pct=margin_pct)
        width_u_mm = max(span_u / unit_mm(), 0.1)
        length_v_mm = max(span_v / unit_mm(), 0.1)

    # Build placement frame at click with embed percentage along n
    L_scene = float(depth_n_mm) * unit_mm()
    embed_pct = float(getattr(props, "pin_embed_pct", 50.0)) * 0.01
    p_embed = point_world - z * (embed_pct * L_scene)

    M = Matrix((
        (x.x, y.x, z.x, p_embed.x),
        (x.y, y.y, z.y, p_embed.y),
        (x.z, y.z, z.z, p_embed.z),
        (0,   0,   0,   1.0),
    ))
    # Apply in-plane controls (offset along u, rotation around n)
    M = _apply_inplane_offset_and_rotation(
        M,
        offset_mm=float(getattr(props, "dovetail_inplane_offset_mm", 0.0)),
        rotation_deg=float(getattr(props, "dovetail_inplane_rotation_deg", 0.0))
    )

    cutters_coll = ensure_collection("_SnapSplit_Cutters")

    # Create dovetail with axis-relative dimensions and signed in-plane taper
    signed_taper = float(getattr(props, "dovetail_signed_taper_pct", 0.0))
    ten = create_dovetail_box_uvn(width_u_mm=width_u_mm,
                                  length_v_mm=length_v_mm,
                                  depth_n_mm=depth_n_mm,
                                  signed_taper_pct=signed_taper,
                                  name=f"{name_prefix}")
    ten.matrix_world = M
    cutters_coll.objects.link(ten)

    # Optional hard side trimming against combined bounds (keeps only within span along chosen axis)
    if bool(getattr(props, "dovetail_hard_side_cut", False)):
        bmin, bmax = _combined_world_bounds([a, b])
        trim_axis = getattr(props, "dovetail_span_axis", None)
        if trim_axis not in {"X", "Y", "Z"}:
            # Derive a best-effort global axis to trim along the larger in-plane projection
            idxn = _axis_index(axis)
            ext = bmax - bmin
            ext_list = [ext.x, ext.y, ext.z]
            ext_list[idxn] = -1.0
            order = ["X", "Y", "Z"]
            trim_axis = order[max(range(3), key=lambda ii: ext_list[ii])]
        _intersect_keep_within_bounds(ten, trim_axis, bmin, bmax, cutters_coll)

    # UNION into B
    union_and_dispose(b, ten, name=f"{name_prefix}_Union")

    # DIFFERENCE socket in A with XY (u/v) tolerance scaling
    mm = unit_mm()
    # Tolerance uses half of the smaller in-plane size to build a uniform scale in u/v
    half_min_plane = max(0.5 * min(width_u_mm, length_v_mm) * mm, 1e-9)
    s_inplane = 1.0 + (float(props.effective_tolerance()) * mm) / half_min_plane
    sx = s_inplane; sy = s_inplane; sz = 1.0

    socket = create_dovetail_box_uvn(width_u_mm=width_u_mm,
                                     length_v_mm=length_v_mm,
                                     depth_n_mm=depth_n_mm,
                                     signed_taper_pct=signed_taper,
                                     name=f"{name_prefix}_SocketCutter")
    socket.matrix_world = M @ Matrix.Diagonal(Vector((sx, sy, sz, 1.0)))
    cutters_coll.objects.link(socket)

    if bool(getattr(props, "dovetail_hard_side_cut", False)):
        bmin, bmax = _combined_world_bounds([a, b])
        trim_axis = getattr(props, "dovetail_span_axis", None)
        if trim_axis not in {"X", "Y", "Z"}:
            idxn = _axis_index(axis)
            ext = bmax - bmin
            ext_list = [ext.x, ext.y, ext.z]
            ext_list[idxn] = -1.0
            order = ["X", "Y", "Z"]
            trim_axis = order[max(range(3), key=lambda ii: ext_list[ii])]
        _intersect_keep_within_bounds(socket, trim_axis, bmin, bmax, cutters_coll)

    cut_socket_with_cutter_and_dispose(a, socket)
    return None, None


def place_one_flush_pin_at(a, b, axis, point_world, frame_z=None, props=None, name_prefix="FlushPin_Click"):
    """Place one flush snap-fit cylindrical connector at click position."""
    if props is None:
        props = bpy.context.scene.snapsplit
    z = {
        "X": Vector((1, 0, 0)),
        "Y": Vector((0, 1, 0)),
        "Z": Vector((0, 0, 1)),
    }.get(axis, Vector((0, 0, 1))).normalized()
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

    cutters_coll = ensure_collection("_SnapSplit_Cutters")
    add_flush_barb_for_cyl(
        base_matrix=M,
        d_mm=float(getattr(props, "pin_diameter_mm", 5.0)),
        length_mm=float(getattr(props, "pin_length_mm", 8.0)),
        props=props,
        name_prefix=name_prefix,
        part_a=a,
        part_b=b,
        cutters_coll=cutters_coll
    )
    return None, None


def place_one_flush_tenon_at(a, b, axis, point_world, frame_z=None, props=None, name_prefix="FlushTenon_Click"):
    """Place one flush snap-fit rectangular connector at click position."""
    if props is None:
        props = bpy.context.scene.snapsplit
    z = {
        "X": Vector((1, 0, 0)),
        "Y": Vector((0, 1, 0)),
        "Z": Vector((0, 0, 1)),
    }.get(axis, Vector((0, 0, 1))).normalized()
    if frame_z is not None:
        z = frame_z.normalized()
    x, y, z = _orthonormal_frame_from_z(z)

    L_scene = float(getattr(props, "tenon_depth_mm", 8.0)) * unit_mm()
    embed_pct = float(getattr(props, "pin_embed_pct", 50.0)) * 0.01
    p_embed = point_world - z * (embed_pct * L_scene)

    M = Matrix((
        (x.x, y.x, z.x, p_embed.x),
        (x.y, y.y, z.y, p_embed.y),
        (x.z, y.z, z.z, p_embed.z),
        (0,   0,   0,   1.0),
    ))

    cutters_coll = ensure_collection("_SnapSplit_Cutters")
    add_flush_barb_for_rect(
        base_matrix=M,
        w_mm=float(getattr(props, "tenon_width_mm", 6.0)),
        length_mm=float(getattr(props, "tenon_depth_mm", 8.0)),
        props=props,
        name_prefix=name_prefix,
        part_a=a,
        part_b=b,
        cutters_coll=cutters_coll
    )
    return None, None


# ---------------------------
# Placement & connect (pairwise seam plane)
# ---------------------------

def place_connectors_between(parts, axis, count, ctype, props):
    """Place connectors between adjacent parts along axis using LINE or GRID distribution."""
    if not parts:
        return []

    idx = _axis_index(axis)
    ordered = sorted(parts, key=lambda o: o.location[idx])
    pairs = [(ordered[i], ordered[i + 1]) for i in range(len(ordered) - 1)]
    if not pairs:
        return []

    created = []
    cutters_coll = ensure_collection("_SnapSplit_Cutters")

    # Robust axis unit vector with fallback to Z
    axis_map = {"X": Vector((1, 0, 0)), "Y": Vector((0, 1, 0)), "Z": Vector((0, 0, 1))}
    naxis = axis_map.get(axis, Vector((0, 0, 1)))

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

            ctype_cur = getattr(props, "connector_type", "CYL_PIN")
            if ctype_cur in {"CYL_PIN", "SNAP_PIN", "SNAP_FLUSH_PIN"}:
                L_scene = float(props.pin_length_mm) * unit_mm()
            elif ctype_cur in {"RECT_TENON", "SNAP_TENON", "SNAP_FLUSH_TENON", "DOVETAIL"}:
                # For dovetail in batch we will override depth_n via dovetail_depth_mm later
                L_scene = float(getattr(props, "tenon_depth_mm", 8.0)) * unit_mm()
            else:
                L_scene = float(props.tenon_depth_mm) * unit_mm()

            p_embed = p - z * (embed_pct * L_scene)

            M = Matrix((
                (x.x, y.x, z.x, p_embed.x),
                (x.y, y.y, z.y, p_embed.y),
                (x.z, y.z, z.z, p_embed.z),
                (0,   0,   0,   1.0),
            ))

            if ctype_cur in {"CYL_PIN", "SNAP_PIN"}:
                seg = int(getattr(props, "pin_segments", 32))
                pin = create_cyl_pin(props.pin_diameter_mm, props.pin_length_mm, props.add_chamfer_mm,
                                     segments=seg, name=f"Pin_{i}")
                pin.matrix_world = M
                cutters_coll.objects.link(pin)
                union_and_dispose(b, pin, name=f"PinUnion_{i}")

                mm = unit_mm()
                socket_d = float(props.pin_diameter_mm) + 2.0 * tol
                socket = create_cyl_pin(socket_d, props.pin_length_mm, 0.0, segments=seg, name=f"SocketCutter_{i}")
                socket.matrix_world = M
                cutters_coll.objects.link(socket)
                cut_socket_with_cutter_and_dispose(a, socket)
                created.append(None)

                if ctype_cur == "SNAP_PIN":
                    pin_radius_scene = 0.5 * float(props.pin_diameter_mm) * mm
                    length_scene = float(props.pin_length_mm) * mm
                    add_snap_spheres_for_cyl_pin(
                        base_matrix=M,
                        pin_radius_scene=pin_radius_scene,
                        length_scene=length_scene,
                        props=props,
                        name_prefix=f"Pin_{i}",
                        part_a=a,  # A = DIFFERENCE
                        part_b=b,  # B = UNION
                        cutters_coll=cutters_coll
                    )

            elif ctype_cur in {"RECT_TENON", "SNAP_TENON"}:
                tenon = create_rect_tenon_quader(props.tenon_width_mm, props.tenon_depth_mm, props.add_chamfer_mm,
                                                 name=f"Tenon_{i}")
                tenon.matrix_world = M
                cutters_coll.objects.link(tenon)
                for mod in list(tenon.modifiers):
                    if mod.type == 'BEVEL':
                        bpy.context.view_layer.objects.active = tenon
                        tenon.select_set(True)
                        try:
                            bpy.ops.object.modifier_apply(modifier=mod.name)
                        except Exception as e:
                            report_user(None, 'WARNING', tr("op.common.warn.bevel_apply", f"Bevel apply failure: {e}"))
                        tenon.select_set(False)

                union_and_dispose(b, tenon, name=f"TenonUnion_{i}")

                mm = unit_mm()
                half_w = max(0.5 * float(props.tenon_width_mm) * mm, 1e-9)
                sx = 1.0 + (tol * mm) / half_w
                sy = sx
                sz = 1.0
                socket = create_rect_tenon_quader(props.tenon_width_mm, props.tenon_depth_mm, 0.0,
                                                  name=f"TenonSocketCutter_{i}")
                socket.matrix_world = M @ Matrix.Diagonal(Vector((sx, sy, sz, 1.0)))
                cutters_coll.objects.link(socket)
                cut_socket_with_cutter_and_dispose(a, socket)
                created.append(None)

                if ctype_cur == "SNAP_TENON":
                    half_w_scene = max(0.5 * float(props.tenon_width_mm) * mm, 1e-9)
                    length_scene = float(props.tenon_depth_mm) * mm
                    add_snap_spheres_for_rect_tenon_ring(
                        base_matrix=M,
                        half_w_scene=half_w_scene,
                        length_scene=length_scene,
                        props=props,
                        name_prefix=f"Tenon_{i}",
                        part_a=a,  # A = DIFFERENCE
                        part_b=b,  # B = UNION
                        cutters_coll=cutters_coll
                    )

            elif ctype_cur == "DOVETAIL":
                # Build local u/v/n frame for dovetail specifically
                z_d = naxis.normalized()
                x_d = Vector((1, 0, 0))
                if abs(z_d.dot(x_d)) > 0.99:
                    x_d = Vector((0, 1, 0))
                y_d = z_d.cross(x_d); y_d.normalize()
                x_d = y_d.cross(z_d); x_d.normalize()

                # Frame at p with embed along depth_n
                depth_n_mm = float(getattr(props, "dovetail_depth_mm", 8.0))
                L_scene_dv = depth_n_mm * unit_mm()
                p_embed_dv = p - z_d * (embed_pct * L_scene_dv)

                M_base = Matrix((
                    (x_d.x, y_d.x, z_d.x, p_embed_dv.x),
                    (x_d.y, y_d.y, z_d.y, p_embed_dv.y),
                    (x_d.z, y_d.z, z_d.z, p_embed_dv.z),
                    (0,     0,     0,     1.0),
                ))
                # Apply in-plane controls
                M2 = _apply_inplane_offset_and_rotation(
                    M_base,
                    offset_mm=float(getattr(props, "dovetail_inplane_offset_mm", 0.0)),
                    rotation_deg=float(getattr(props, "dovetail_inplane_rotation_deg", 0.0))
                )

                # Compute per-axis in-plane spans if AUTO
                auto_span = bool(getattr(props, "dovetail_auto_span", False))
                margin_pct_dv = float(getattr(props, "dovetail_span_margin_pct", 10.0))

                width_u_mm = float(getattr(props, "dovetail_width_mm", 10.0))
                length_v_mm = float(getattr(props, "dovetail_length_mm", width_u_mm))  # fallback to width
                if auto_span:
                    span_u = _compute_edge_to_edge_span_along_dir(a, b, x_d, axis, seam_pos, margin_pct=margin_pct_dv)
                    span_v = _compute_edge_to_edge_span_along_dir(a, b, y_d, axis, seam_pos, margin_pct=margin_pct_dv)
                    width_u_mm = max(span_u / unit_mm(), 0.1)
                    length_v_mm = max(span_v / unit_mm(), 0.1)

                signed_taper = float(getattr(props, "dovetail_signed_taper_pct", 0.0))
                ten = create_dovetail_box_uvn(width_u_mm=width_u_mm,
                                              length_v_mm=length_v_mm,
                                              depth_n_mm=depth_n_mm,
                                              signed_taper_pct=signed_taper,
                                              name=f"Dovetail_{i}")
                ten.matrix_world = M2
                cutters_coll.objects.link(ten)

                # Hard side cut if enabled
                if bool(getattr(props, "dovetail_hard_side_cut", False)):
                    bmin, bmax = _combined_world_bounds([a, b])
                    trim_axis = getattr(props, "dovetail_span_axis", None)
                    if trim_axis not in {"X", "Y", "Z"}:
                        idxn = _axis_index(axis)
                        ext = bmax - bmin
                        ext_list = [ext.x, ext.y, ext.z]
                        ext_list[idxn] = -1.0
                        order = ["X", "Y", "Z"]
                        trim_axis = order[max(range(3), key=lambda ii: ext_list[ii])]
                    _intersect_keep_within_bounds(ten, trim_axis, bmin, bmax, cutters_coll)

                union_and_dispose(b, ten, name=f"DovetailUnion_{i}")

                # Socket with in-plane tolerance
                mm = unit_mm()
                half_min_plane = max(0.5 * min(width_u_mm, length_v_mm) * mm, 1e-9)
                s_inplane = 1.0 + (float(props.effective_tolerance()) * mm) / half_min_plane
                sx = s_inplane; sy = s_inplane; sz = 1.0

                socket = create_dovetail_box_uvn(width_u_mm=width_u_mm,
                                                 length_v_mm=length_v_mm,
                                                 depth_n_mm=depth_n_mm,
                                                 signed_taper_pct=signed_taper,
                                                 name=f"DovetailSocketCutter_{i}")
                socket.matrix_world = M2 @ Matrix.Diagonal(Vector((sx, sy, sz, 1.0)))
                cutters_coll.objects.link(socket)

                if bool(getattr(props, "dovetail_hard_side_cut", False)):
                    bmin, bmax = _combined_world_bounds([a, b])
                    trim_axis = getattr(props, "dovetail_span_axis", None)
                    if trim_axis not in {"X", "Y", "Z"}:
                        idxn = _axis_index(axis)
                        ext = bmax - bmin
                        ext_list = [ext.x, ext.y, ext.z]
                        ext_list[idxn] = -1.0
                        order = ["X", "Y", "Z"]
                        trim_axis = order[max(range(3), key=lambda ii: ext_list[ii])]
                    _intersect_keep_within_bounds(socket, trim_axis, bmin, bmax, cutters_coll)

                cut_socket_with_cutter_and_dispose(a, socket)
                created.append(None)

            elif ctype_cur == "SNAP_FLUSH_PIN":
                add_flush_barb_for_cyl(
                    base_matrix=M,
                    d_mm=float(getattr(props, "pin_diameter_mm", 5.0)),
                    length_mm=float(getattr(props, "pin_length_mm", 8.0)),
                    props=props,
                    name_prefix=f"FlushPin_{i}",
                    part_a=a,
                    part_b=b,
                    cutters_coll=cutters_coll
                )
                created.append(None)

            elif ctype_cur == "SNAP_FLUSH_TENON":
                add_flush_barb_for_rect(
                    base_matrix=M,
                    w_mm=float(getattr(props, "tenon_width_mm", 6.0)),
                    length_mm=float(getattr(props, "tenon_depth_mm", 8.0)),
                    props=props,
                    name_prefix=f"FlushTenon_{i}",
                    part_a=a,
                    part_b=b,
                    cutters_coll=cutters_coll
                )
                created.append(None)

            else:
                # Fallback -> behave like tenon
                tenon = create_rect_tenon_quader(props.tenon_width_mm, props.tenon_depth_mm, props.add_chamfer_mm,
                                                 name=f"Tenon_{i}")
                tenon.matrix_world = M
                cutters_coll.objects.link(tenon)
                union_and_dispose(b, tenon, name=f"TenonUnion_{i}")

                mm = unit_mm()
                half_w = max(0.5 * float(props.tenon_width_mm) * mm, 1e-9)
                sx = 1.0 + (tol * mm) / half_w
                sy = sx
                sz = 1.0
                socket = create_rect_tenon_quader(props.tenon_width_mm, props.tenon_depth_mm, 0.0,
                                                  name=f"TenonSocketCutter_{i}")
                socket.matrix_world = M @ Matrix.Diagonal(Vector((sx, sy, sz, 1.0)))
                cutters_coll.objects.link(socket)
                cut_socket_with_cutter_and_dispose(a, socket)
                created.append(None)

    return created


# ---------------------------
# Modal operator: place by click (pins or tenons or dovetail)
# ---------------------------

class SNAP_OT_place_connectors_click(Operator):
    """Interactively place a connector (pin/tenon/dovetail) by clicking on the seam plane between two parts."""
    bl_idname = "snapsplit.place_connectors_click"
    bl_label = "Place connectors (click)"
    bl_options = {'REGISTER', 'UNDO', 'BLOCKING'}

    def invoke(self, context, event):
        """Start modal placement with live preview for two selected mesh parts."""
        props = context.scene.snapsplit
        sel = [o for o in context.selected_objects if o.type == 'MESH']
        if len(sel) != 2:
            report_user(self, 'ERROR',
                        tr("op.connect.click.err.need2", "Select exactly 2 adjacent split parts."))
            return {'CANCELLED'}

        self.a, self.b = sel
        self.axis = props.split_axis
        self.props = props

        try:
            self.seam_pos = _pair_seam_plane_pos(self.a, self.b, self.axis, props)
        except Exception:
            report_user(self, 'ERROR', tr("op.connect.click.err.seam", "Could not compute seam plane."))
            return {'CANCELLED'}

        try:
            ctype_cur = getattr(props, "connector_type", "CYL_PIN")
            prev_coll = ensure_collection("_SnapSplit_Preview")

            self.preview_objs = []
            self.preview_obj = None

            if ctype_cur in {"CYL_PIN", "SNAP_PIN", "SNAP_FLUSH_PIN"}:
                seg = int(getattr(props, "pin_segments", 32))
                if ctype_cur == "SNAP_FLUSH_PIN":
                    pin_prev = create_flush_barb_cylinder(props.pin_diameter_mm, props.pin_length_mm,
                                                          getattr(props, "flush_barb_height_mm", 0.6),
                                                          getattr(props, "flush_barb_lip_mm", 0.25),
                                                          segments=seg,
                                                          name="SnapSplit_Preview_FlushPin")
                else:
                    pin_prev = create_cyl_pin(props.pin_diameter_mm, props.pin_length_mm, props.add_chamfer_mm,
                                              segments=seg, name="SnapSplit_Preview_Conn")
                pin_prev.display_type = 'WIRE'
                pin_prev.hide_select = True
                prev_coll.objects.link(pin_prev)
                self.preview_obj = pin_prev
                self.preview_objs.append(pin_prev)

                if ctype_cur == "SNAP_PIN":
                    # Show sphere ring preview
                    mm = unit_mm()
                    n_per_side = max(1, int(getattr(props, "snap_spheres_per_side", 2)))
                    d_sph_mm = float(getattr(props, "snap_sphere_diameter_mm", 2.0))
                    protr_scene = float(getattr(props, "snap_sphere_protrusion_mm", 1.0)) * mm
                    pin_radius_scene = 0.5 * float(props.pin_diameter_mm) * mm
                    length_scene = float(props.pin_length_mm) * mm

                    embed_pct = max(0.0, min(1.0, float(getattr(props, "pin_embed_pct", 50.0)) * 0.01))
                    L_free = max(0.0, (1.0 - embed_pct) * length_scene)
                    zA = 0.5 * embed_pct * length_scene
                    zB = embed_pct * length_scene + 0.5 * L_free

                    sph_r_scene = 0.5 * d_sph_mm * mm
                    r_center = pin_radius_scene + protr_scene - sph_r_scene

                    import math
                    for i in range(n_per_side):
                        ang = (2.0 * math.pi) * (i / n_per_side)
                        nx = math.cos(ang); ny = math.sin(ang)
                        local_A = (r_center * nx, r_center * ny, zA)
                        local_B = (r_center * nx, r_center * ny, zB)
                        sph_prev = create_uv_sphere_preview(d_mm=d_sph_mm, segments=12, rings=6,
                                                            name=f"SnapSplit_Preview_Snap_{i}")
                        sph_prev["_snapsplit_local_offset_A"] = local_A
                        sph_prev["_snapsplit_local_offset_B"] = local_B
                        prev_coll.objects.link(sph_prev)
                        self.preview_objs.append(sph_prev)

            elif ctype_cur in {"RECT_TENON", "SNAP_TENON", "SNAP_FLUSH_TENON", "DOVETAIL"}:
                if ctype_cur == "DOVETAIL":
                    # Dovetail preview uses axis-relative dimensions and signed in-plane taper
                    width_u_mm = float(getattr(props, "dovetail_width_mm", 10.0))
                    length_v_mm = float(getattr(props, "dovetail_length_mm", width_u_mm))
                    depth_n_mm = float(getattr(props, "dovetail_depth_mm", 8.0))
                    signed_taper = float(getattr(props, "dovetail_signed_taper_pct", 0.0))
                    ten_prev = create_dovetail_box_uvn(width_u_mm=width_u_mm,
                                                       length_v_mm=length_v_mm,
                                                       depth_n_mm=depth_n_mm,
                                                       signed_taper_pct=signed_taper,
                                                       name="SnapSplit_Preview_Dovetail")
                elif ctype_cur == "SNAP_FLUSH_TENON":
                    ten_prev = create_flush_barb_rect(
                        w_mm=getattr(props, "tenon_width_mm", 6.0),
                        length_mm=getattr(props, "tenon_depth_mm", 8.0),
                        barb_height_mm=getattr(props, "flush_barb_height_mm", 0.6),
                        barb_lip_mm=getattr(props, "flush_barb_lip_mm", 0.25),
                        name="SnapSplit_Preview_FlushTenon"
                    )
                else:
                    ten_prev = create_rect_tenon_quader(props.tenon_width_mm, props.tenon_depth_mm, props.add_chamfer_mm,
                                                        name="SnapSplit_Preview_Conn")
                ten_prev.display_type = 'WIRE'
                ten_prev.hide_select = True
                prev_coll.objects.link(ten_prev)
                self.preview_obj = ten_prev
                self.preview_objs.append(ten_prev)

                if ctype_cur == "SNAP_TENON":
                    mm = unit_mm()
                    n_per_side = max(1, int(getattr(props, "snap_spheres_per_side", 2)))
                    d_sph_mm = float(getattr(props, "snap_sphere_diameter_mm", 2.0))
                    protr_scene = float(getattr(props, "snap_sphere_protrusion_mm", 1.0)) * mm
                    half_w_scene = 0.5 * float(props.tenon_width_mm) * mm
                    length_scene = float(props.tenon_depth_mm) * mm

                    embed_pct = max(0.0, min(1.0, float(getattr(props, "pin_embed_pct", 50.0)) * 0.01))
                    L_free = max(0.0, (1.0 - embed_pct) * length_scene)
                    zA = 0.5 * embed_pct * length_scene
                    zB = embed_pct * length_scene + 0.5 * L_free

                    sph_r_scene = 0.5 * d_sph_mm * mm
                    r_center = half_w_scene + protr_scene - sph_r_scene

                    import math
                    for i in range(n_per_side):
                        ang = (2.0 * math.pi) * (i / n_per_side)
                        nx = math.cos(ang); ny = math.sin(ang)
                        local_A = (r_center * nx, r_center * ny, zA)
                        local_B = (r_center * nx, r_center * ny, zB)
                        sph_prev = create_uv_sphere_preview(d_mm=d_sph_mm, segments=12, rings=6,
                                                            name=f"SnapSplit_Preview_SnapTen_{i}")
                        sph_prev["_snapsplit_local_offset_A"] = local_A
                        sph_prev["_snapsplit_local_offset_B"] = local_B
                        prev_coll.objects.link(sph_prev)
                        self.preview_objs.append(sph_prev)

        except Exception:
            self.preview_obj = None
            self.preview_objs = []

        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def finish(self, context, cancelled=False):
        """Tear down preview objects and collections; also remove cutters collection on cancel or end."""
        try:
            to_purge = set()

            if getattr(self, "preview_obj", None) and self.preview_obj.name in bpy.data.objects:
                to_purge.add(bpy.data.objects.get(self.preview_obj.name))
            if getattr(self, "preview_objs", None):
                for o in list(self.preview_objs):
                    if o and o.name in bpy.data.objects:
                        to_purge.add(bpy.data.objects.get(o.name))

            prev_coll = bpy.data.collections.get("_SnapSplit_Preview")
            name_prefixes = (
                "SnapSplit_Preview_",
                "SnapSplit_Preview_Snap_",
                "SnapSplit_Preview_SnapTen_",
                "SnapSplit_Preview_Conn",
                "SnapSplit_Preview_FlushPin",
                "SnapSplit_Preview_FlushTenon",
                "SnapSplit_Preview_Dovetail",
            )
            if prev_coll:
                for o in list(prev_coll.objects):
                    try:
                        if (o.name.startswith(name_prefixes)) or bool(o.get("_snapsplit_preview")):
                            to_purge.add(o)
                    except Exception:
                        pass

            for o in list(bpy.data.objects):
                try:
                    if (o.name.startswith(name_prefixes)) or bool(o.get("_snapsplit_preview")):
                        to_purge.add(o)
                except Exception:
                    pass

            for obj in list(to_purge):
                if not obj:
                    continue
                try:
                    for coll in list(obj.users_collection):
                        try:
                            coll.objects.unlink(obj)
                        except Exception:
                            pass
                except Exception:
                    pass

                mesh_data = getattr(obj, "data", None)

                try:
                    bpy.data.objects.remove(obj)
                except Exception:
                    try:
                        _dispose_object(obj, remove_data=False)
                    except Exception:
                        pass

                try:
                    if mesh_data and hasattr(mesh_data, "users") and mesh_data.users == 0:
                        if mesh_data.__class__.__name__ == "Mesh":
                            bpy.data.meshes.remove(mesh_data)
                        else:
                            bpy.data.batch_remove((mesh_data,))
                except Exception:
                    pass

            try:
                if prev_coll:
                    for parent in list(bpy.data.collections):
                        try:
                            if prev_coll.name in [c.name for c in getattr(parent, "children", [])]:
                                parent.children.unlink(prev_coll)
                        except Exception:
                            pass
                    try:
                        scene_root = bpy.context.view_layer.layer_collection.collection
                        if prev_coll.name in [c.name for c in scene_root.children]:
                            scene_root.children.unlink(prev_coll)
                    except Exception:
                        pass
                    try:
                        bpy.data.collections.remove(prev_coll)
                    except Exception:
                        pass
            except Exception:
                pass

            try:
                if getattr(self, "preview_objs", None) is not None:
                    self.preview_objs.clear()
            except Exception:
                pass
            self.preview_obj = None

            try:
                context.view_layer.update()
            except Exception:
                pass

        except Exception:
            pass

        try:
            remove_cutters_collection()
        except Exception:
            pass

        if cancelled:
            report_user(self, 'INFO', tr("op.connect.click.cancelled", "Placement cancelled."))

    def modal(self, context, event):
        """Handle mouse movement for preview updates and left-click for placement."""
        try:
            if event.type in {'ESC', 'RIGHTMOUSE'} and event.value == 'PRESS':
                self.finish(context, cancelled=True)
                return {'CANCELLED'}

            if event.type == 'MOUSEMOVE':
                try:
                    hit = self._intersect_mouse_with_seam_plane(context, event)
                    if hit is not None:
                        M = self._build_frame_at(hit)
                        if self.preview_obj:
                            ctype_cur = getattr(self.props, "connector_type", "CYL_PIN")
                            # For dovetail previews, apply in-plane offset+rotation so preview == result
                            if ctype_cur in {"DOVETAIL"}:
                                M = _apply_inplane_offset_and_rotation(
                                    M,
                                    offset_mm=float(getattr(self.props, "dovetail_inplane_offset_mm", 0.0)),
                                    rotation_deg=float(getattr(self.props, "dovetail_inplane_rotation_deg", 0.0))
                                )
                            self.preview_obj.matrix_world = M

                        if getattr(self, "preview_objs", None) and len(self.preview_objs) > 1:
                            try:
                                z_axis_world = Vector((M[0][2], M[1][2], M[2][2])).normalized()
                            except Exception:
                                z_axis_world = None
                            for o in self.preview_objs:
                                if o is self.preview_obj:
                                    continue
                                try:
                                    if "_snapsplit_local_offset_B" in o:
                                        oxA, oyA, ozA = o.get("_snapsplit_local_offset_A", (0.0, 0.0, 0.0))
                                        oxB, oyB, ozB = o.get("_snapsplit_local_offset_B", (0.0, 0.0, 0.0))
                                        if z_axis_world is not None:
                                            pA_w_v = (M @ Vector((oxA, oyA, ozA, 1.0)))
                                            pB_w_v = (M @ Vector((oxB, oyB, ozB, 1.0)))
                                            dA = Vector((pA_w_v.x, pA_w_v.y, pA_w_v.z)).dot(z_axis_world)
                                            dB = Vector((pB_w_v.x, pB_w_v.y, pB_w_v.z)).dot(z_axis_world)
                                            use_B = dB >= dA
                                        else:
                                            use_B = True
                                        o.matrix_world = M @ Matrix.Translation((oxB, oyB, ozB)) if use_B else M @ Matrix.Translation((oxA, oyA, ozA))
                                except Exception:
                                    pass
                except Exception:
                    pass
                return {'RUNNING_MODAL'}

            if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
                try:
                    hit = self._intersect_mouse_with_seam_plane(context, event)
                    if hit is not None:
                        ctype_cur = getattr(self.props, "connector_type", "CYL_PIN")
                        if ctype_cur == "CYL_PIN":
                            place_one_cyl_pin_at(self.a, self.b, self.axis, hit, props=self.props, name_prefix="Pin_Click")
                        elif ctype_cur == "RECT_TENON":
                            place_one_rect_tenon_at(self.a, self.b, self.axis, hit, props=self.props, name_prefix="Tenon_Click")
                        elif ctype_cur == "SNAP_PIN":
                            place_one_cyl_pin_at(self.a, self.b, self.axis, hit, props=self.props, name_prefix="Pin_Click")
                            M = self._build_frame_at(hit)
                            mm = unit_mm()
                            pin_radius_scene = 0.5 * float(self.props.pin_diameter_mm) * mm
                            length_scene = float(self.props.pin_length_mm) * mm
                            cutters_coll = ensure_collection("_SnapSplit_Cutters")
                            add_snap_spheres_for_cyl_pin(
                                base_matrix=M,
                                pin_radius_scene=pin_radius_scene,
                                length_scene=length_scene,
                                props=self.props,
                                name_prefix="Pin_Click",
                                part_a=self.a,  # A = DIFFERENCE
                                part_b=self.b,  # B = UNION
                                cutters_coll=cutters_coll
                            )
                        elif ctype_cur == "SNAP_TENON":
                            place_one_rect_tenon_at(self.a, self.b, self.axis, hit, props=self.props, name_prefix="Tenon_Click")
                            M = self._build_frame_at(hit)
                            mm = unit_mm()
                            half_w_scene = 0.5 * float(self.props.tenon_width_mm) * mm
                            length_scene = float(self.props.tenon_depth_mm) * mm
                            cutters_coll = ensure_collection("_SnapSplit_Cutters")
                            add_snap_spheres_for_rect_tenon_ring(
                                base_matrix=M,
                                half_w_scene=half_w_scene,
                                length_scene=length_scene,
                                props=self.props,
                                name_prefix="Tenon_Click",
                                part_a=self.a,  # A = DIFFERENCE
                                part_b=self.b,  # B = UNION
                                cutters_coll=cutters_coll
                            )
                        elif ctype_cur == "DOVETAIL":
                            place_one_dovetail_at(self.a, self.b, self.axis, hit, props=self.props, name_prefix="Dovetail_Click")
                        elif ctype_cur == "SNAP_FLUSH_PIN":
                            place_one_flush_pin_at(self.a, self.b, self.axis, hit, props=self.props, name_prefix="FlushPin_Click")
                        elif ctype_cur == "SNAP_FLUSH_TENON":
                            place_one_flush_tenon_at(self.a, self.b, self.axis, hit, props=self.props, name_prefix="FlushTenon_Click")

                        try:
                            remove_cutters_collection()
                        except Exception:
                            pass

                except Exception as e:
                    report_user(self, 'ERROR',
                                tr("op.connect.click.err.place", f"Placement failed: {e}"))
                return {'RUNNING_MODAL'}

            return {'RUNNING_MODAL'}

        except Exception as e:
            report_user(self, 'ERROR', tr("op.connect.click.err.modal", f"Modal error: {e}"))
            return {'RUNNING_MODAL'}

    def _intersect_mouse_with_seam_plane(self, context, event):
        """Raycast from mouse into the seam plane and return the hit point in world space."""
        n = {
            "X": Vector((1, 0, 0)),
            "Y": Vector((0, 1, 0)),
            "Z": Vector((0, 0, 1)),
        }.get(self.axis, Vector((0, 0, 1))).normalized()

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
        """Build a local placement frame (Matrix) at a world point based on axis and embed depth.

        Note: For preview, we use tenon_depth_mm by legacy for non-dovetail types.
        Dovetail placement later overrides depth with dovetail_depth_mm.
        """
        z = {
            "X": Vector((1, 0, 0)),
            "Y": Vector((0, 1, 0)),
            "Z": Vector((0, 0, 1)),
        }.get(self.axis, Vector((0, 0, 1))).normalized()
        x = Vector((1, 0, 0))
        if abs(z.dot(x)) > 0.99:
            x = Vector((0, 1, 0))
        y = z.cross(x); y.normalize()
        x = y.cross(z); x.normalize()

        ctype_cur = getattr(self.props, "connector_type", "CYL_PIN")
        if ctype_cur in {"CYL_PIN", "SNAP_PIN", "SNAP_FLUSH_PIN"}:
            L_scene = float(self.props.pin_length_mm) * unit_mm()
        elif ctype_cur in {"DOVETAIL"}:
            # For dovetail previews, use its own depth
            L_scene = float(getattr(self.props, "dovetail_depth_mm", 8.0)) * unit_mm()
        else:
            L_scene = float(getattr(self.props, "tenon_depth_mm", 8.0)) * unit_mm()

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
    """Batch-place connectors between all adjacent selected parts using current settings."""
    bl_idname = "snapsplit.add_connectors"
    bl_label = "Add connectors"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        """Execute batch placement for selected mesh parts."""
        props = context.scene.snapsplit
        sel = [o for o in context.selected_objects if o.type == 'MESH']
        if len(sel) < 2:
            report_user(self, 'ERROR',
                        tr("op.connect.batch.err.need2", "Select at least 2 cut mesh-pieces."))
            return {'CANCELLED'}

        created = place_connectors_between(
            parts=sel,
            axis=props.split_axis,
            count=props.connectors_per_seam,
            ctype=props.connector_type,
            props=props
        )

        try:
            remove_cutters_collection()
        except Exception:
            pass

        report_user(self, 'INFO',
                    tr("op.connect.batch.info.done", f"{len(created)} connectors created.").format(n=len(created)))
        return {'FINISHED'}


# ---------------------------
# Registration
# ---------------------------

classes = (SNAP_OT_add_connectors, SNAP_OT_place_connectors_click)

def register():
    """Register operators for connector placement."""
    # UI strings via translations
    SNAP_OT_place_connectors_click.bl_label = tr("op.connect.click.label", "Place connectors (click)")
    SNAP_OT_place_connectors_click.__doc__ = tr("op.connect.click.doc", "Interactively place a connector (pin/tenon/dovetail) by clicking on the seam plane between two parts.")

    SNAP_OT_add_connectors.bl_label = tr("op.connect.batch.label", "Add connectors")
    SNAP_OT_add_connectors.__doc__ = tr("op.connect.batch.doc", "Batch-place connectors between all adjacent selected parts using current settings.")

    for c in classes:
        bpy.utils.register_class(c)

def unregister():
    """Unregister operators for connector placement."""
    for c in reversed(classes):
        bpy.utils.unregister_class(c)
