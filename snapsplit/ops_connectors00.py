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
from math import cos, sin, pi, radians
from mathutils import Vector, Matrix
from bpy.types import Operator
from bpy_extras import view3d_utils

from .utils import ensure_collection, unit_mm, report_user
from .profiles import MATERIAL_PROFILES

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
    if axis == "X":
        return Vector((1,0,0)), Vector((0,1,0)), Vector((0,0,1))
    if axis == "Y":
        return Vector((0,1,0)), Vector((1,0,0)), Vector((0,0,1))
    return Vector((0,0,1)), Vector((1,0,0)), Vector((0,1,0))

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
# Distribution with margin% and edge_margin_mm
# ---------------------------

def _edge_margins_scene(props):
    """Return (pct_margin, edge_margin_scene_mm) with sane defaults."""
    mm = unit_mm()
    pct = max(0.0, float(getattr(props, "connector_margin_pct", 10.0)))
    edge_mm = max(0.0, float(getattr(props, "edge_margin_mm", 0.0))) * mm
    return pct, edge_mm

def distribute_points_line_on_seam(obj_a, obj_b, count, axis, seam_pos, margin_pct=10.0, edge_margin_scene=0.0):
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

    # Percentage margin in param space
    m_pct = max(0.0, float(margin_pct)) * 0.01 * span

    # Absolute edge margin (shrink both ends additionally)
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

def distribute_points_grid_on_seam(obj_a, obj_b, cols, rows, axis, seam_pos, margin_pct=10.0, edge_margin_scene=0.0):
    """Distribute cols*rows points over the 2D overlap of (A,B) on the given seam plane."""
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
        return distribute_points_line_on_seam(obj_a, obj_b, cols, axis, seam_pos, margin_pct, edge_margin_scene)

    m1 = max(0.0, float(margin_pct)) * 0.01 * span1
    m2 = max(0.0, float(margin_pct)) * 0.01 * span2

    # Absolute margins on both axes
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
# Geometry: base primitives (existing)
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

def create_rect_tenon_quader(w_mm=6.0, length_mm=10.0, chamfer_mm=0.0, name="SnapSplit_Tenon"):
    """Create a rectangular tenon (elongated cube) with optional bevel modifier for chamfer."""
    mm = unit_mm()
    w = float(w_mm) * mm
    L = float(length_mm) * mm
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.transform(bm, matrix=Matrix.Diagonal(Vector((w, w, L, 1.0))), verts=bm.verts)
    # Base at z=0, tip at z=L (analogous to pin)
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
# Boolean helpers
# ---------------------------

def boolean_apply(target_obj, mod):
    """Apply a Boolean (or any) modifier on target_obj with validation and error handling."""
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
        report_user(None, 'WARNING', f"Modifier apply failed ({mod.name}): {e}",
                    "Modifier-Anwenden fehlgeschlagen.")
    target_obj.select_set(False)
    try:
        target_obj.data.validate(verbose=False)
        target_obj.data.update()
    except:
        pass

def cut_socket_with_cutter(target_obj, cutter_obj):
    """Apply a DIFFERENCE Boolean using cutter_obj on target_obj to create a socket."""
    mod = target_obj.modifiers.new("SnapSplit_Socket", 'BOOLEAN')
    mod.operation = 'DIFFERENCE'
    mod.solver = 'EXACT'
    mod.object = cutter_obj
    boolean_apply(target_obj, mod)

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
    mod = target_obj.modifiers.new("SnapSplit_Socket", 'BOOLEAN')
    mod.operation = 'DIFFERENCE'
    mod.solver = 'EXACT'
    mod.object = cutter_obj
    boolean_apply(target_obj, mod)
    _dispose_object(cutter_obj, remove_data=True)

def union_and_dispose(target_obj, union_obj, name="SnapSplit_Union"):
    """Apply UNION Boolean and dispose the helper object afterwards."""
    mod = target_obj.modifiers.new(name, 'BOOLEAN')
    mod.operation = 'UNION'
    mod.solver = 'EXACT'
    mod.object = union_obj
    boolean_apply(target_obj, mod)
    _dispose_object(union_obj, remove_data=True)

# ---------------------------
# Snap spheres helpers (existing)
# ---------------------------

def _ring_height_for_visible_half(length_scene, embed_pct):
    L_free = max(0.0, (1.0 - embed_pct) * length_scene)
    return embed_pct * length_scene + 0.5 * L_free

def _choose_visible_half_robust(base_matrix, zA, zB):
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

    created = []
    sph_r_scene = 0.5 * float(d_sph_mm) * mm
    r_center = pin_radius_scene + protrude_scene - sph_r_scene

    for i in range(n_per_side):
        ang = (2.0 * pi) * (i / n_per_side)
        nx = cos(ang); ny = sin(ang)

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

    sph_r_scene = 0.5 * float(d_sph_mm) * mm
    r_center = half_w_scene + protrude_scene - sph_r_scene

    created = []
    for i in range(n_per_side):
        ang = (2.0 * pi) * (i / n_per_side)
        nx = cos(ang); ny = sin(ang)

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
# New geometry helpers (Phase 1)
# ---------------------------

def create_dovetail_tongue(width_mm, depth_mm, length_mm, draft_deg, leadin_chamfer_mm=0.0, name="SnapSplit_DovetailTongue"):
    """
    Create a tapered dovetail 'tongue' prism aligned along +Z (length), with XY cross-section trapezoid.
    - width_mm: nominal top width at entry
    - draft_deg: linear taper along +Z; widens or narrows by tan(angle)*Z on each side
    Geometry baseline: centered on XY, base at z=0, tip at z=length.
    """
    mm = unit_mm()
    w0 = float(width_mm) * mm
    D = float(depth_mm) * mm
    L = float(length_mm) * mm
    draft = radians(float(draft_deg))
    # For robustness, keep a symmetric trapezoid: base width w0, end width w1 = w0 + 2*tan(draft)*L
    dw = 2.0 * (L * (0.5 * (abs(draft) / max(1e-9, (pi/180.0))) if False else (abs(draft))))  # direct tan approximated small-angle
    # Use exact tan
    dw = 2.0 * L * abs((0.0 if draft == 0.0 else (abs(sin(draft)/cos(draft)))))  # tan = sin/cos

    w1 = max(1e-6, w0 + dw)  # progressive widening
    # Build a prism via bmesh: rectangle at z=0 with width w0 and depth D in Y, rectangle at z=L with width w1 and depth D
    # We'll align D along Y (half depth each side), and width along X (half width each side)

    bm = bmesh.new()

    def add_rect_layer(z, w, d):
        hx = 0.5 * w
        hy = 0.5 * d
        verts = [
            bm.verts.new(Vector((-hx, -hy, z))),
            bm.verts.new(Vector(( hx, -hy, z))),
            bm.verts.new(Vector(( hx,  hy, z))),
            bm.verts.new(Vector((-hx,  hy, z))),
        ]
        return verts

    v0 = add_rect_layer(0.0, w0, D)
    v1 = add_rect_layer(L,   w1, D)
    bm.verts.index_update(); bm.verts.ensure_lookup_table()

    # Create sides (quads)
    def face_quad(a, b, c, d):
        try:
            bm.faces.new([a, b, c, d])
        except ValueError:
            pass

    # Create faces between corresponding edges
    for i in range(4):
        a = v0[i]
        b = v0[(i + 1) % 4]
        c = v1[(i + 1) % 4]
        d = v1[i]
        face_quad(a, b, c, d)

    # Caps
    try:
        bm.faces.new(v0)
    except ValueError:
        pass
    try:
        bm.faces.new(v1[::-1])
    except ValueError:
        pass

    bm.normal_update()
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me); bm.free()
    obj = bpy.data.objects.new(name, me)

    # Optional lead-in chamfer: approximate by bevel modifier on entry rim (z=0), small value
    if leadin_chamfer_mm and leadin_chamfer_mm > 0.0:
        bev = obj.modifiers.new("Bevel", 'BEVEL')
        bev.width = float(leadin_chamfer_mm) * mm
        bev.segments = 1
        bev.limit_method = 'ANGLE'
        bev.angle_limit = radians(0.1)  # nearly all sharp edges

    return obj

def create_dovetail_socket_cutter(width_mm, depth_mm, length_mm, clearance_per_side_mm, draft_deg, name="SnapSplit_DovetailSocketCutter"):
    """
    Create a slightly larger 'socket' cutter for the dovetail tongue:
    - widens by clearance on X (both sides), same D on Y, same L on Z, same draft.
    """
    mm = unit_mm()
    w = float(width_mm) + 2.0 * float(clearance_per_side_mm)
    D = float(depth_mm)
    L = float(length_mm)
    obj = create_dovetail_tongue(w, D, L, draft_deg, leadin_chamfer_mm=0.0, name=name)
    return obj

# ---------------------------
# Single-placement helpers (click) — existing + new types
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

def _resolve_preview_density_segments():
    """Return a dict with suggested preview segments based on addon prefs."""
    # Safe defaults
    seg = {"cyl": 24, "sph_u": 24, "sph_v": 12}
    try:
        prefs = bpy.context.preferences.addons[__package__].preferences
        d = getattr(prefs, "preview_density", "medium")
        if d == "low":
            seg = {"cyl": 12, "sph_u": 12, "sph_v": 6}
        elif d == "high":
            seg = {"cyl": 36, "sph_u": 36, "sph_v": 18}
    except Exception:
        pass
    return seg

def _rotate_frame_for_slide_dir(M, slide_dir):
    """Rotate local frame so that +X aligns with requested slide direction (+/-X, +/-Y) in frame space."""
    if slide_dir not in {"+X", "-X", "+Y", "-Y"}:
        return M
    # Current axes from M
    x = Vector((M[0][0], M[1][0], M[2][0]))
    y = Vector((M[0][1], M[1][1], M[2][1]))
    z = Vector((M[0][2], M[1][2], M[2][2]))
    # Target axis
    tgt = {"+X": x, "-X": -x, "+Y": y, "-Y": -y}[slide_dir].normalized()
    # We want local +X to become 'tgt'. Build new ortho basis:
    new_x = tgt
    new_y = z.cross(new_x)
    if new_y.length_squared < 1e-12:
        # fallback
        new_y = y
    new_y.normalize()
    new_x = new_y.cross(z).normalized()  # re-orthogonalize
    R = Matrix(((new_x.x, new_y.x, z.x, 0.0),
                (new_x.y, new_y.y, z.y, 0.0),
                (new_x.z, new_y.z, z.z, 0.0),
                (0.0,     0.0,     0.0, 1.0)))
    T = Matrix.Translation(Vector((M[0][3], M[1][3], M[2][3])))
    return T @ R

def _pin_fit_mode_clearance_mm(props):
    """Map pin_fit_mode and material_profile to per-side clearance in mm."""
    mat = getattr(props, "material_profile", "PETG")
    mode = getattr(props, "pin_fit_mode", "snug")
    # If tol_override is set, prefer the explicit mapping values below
    # FDM mapping
    fdm = {"snug": 0.25, "sliding": 0.45, "glue_ready": 0.60}
    sla = {"snug": 0.08, "sliding": 0.12, "glue_ready": 0.18}
    if mat == "SLA":
        return sla.get(mode, 0.08)
    return fdm.get(mode, 0.25)

def place_one_cyl_pin_at(a, b, axis, point_world, frame_z=None, props=None, name_prefix="Pin_Click", override_fit_mode=False):
    """Place one cylindrical pin at a world point; union into B and cut socket into A. If override_fit_mode True, use PIN_HOLE mapping."""
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

    # Create pin only if not hole-only
    hole_only = bool(getattr(props, "pin_hole_only", False)) if override_fit_mode else False
    if not hole_only:
        pin = create_cyl_pin(props.pin_diameter_mm, props.pin_length_mm, props.add_chamfer_mm,
                             segments=seg, name=f"{name_prefix}")
        pin.matrix_world = M
        cutters_coll.objects.link(pin)
        union_and_dispose(b, pin, name=f"{name_prefix}_Union")

    # DIFFERENCE (socket) into A
    mm = unit_mm()
    if override_fit_mode:
        c_mm = _pin_fit_mode_clearance_mm(props)
        socket_d = float(props.pin_diameter_mm) + 2.0 * c_mm
    else:
        tol = float(props.effective_tolerance())
        socket_d = float(props.pin_diameter_mm) + 2.0 * tol
    socket = create_cyl_pin(socket_d, props.pin_length_mm, 0.0, segments=seg, name=f"{name_prefix}_SocketCutter")
    socket.matrix_world = M
    cutters_coll.objects.link(socket)
    cut_socket_with_cutter_and_dispose(a, socket)
    return None, None

def place_one_dovetail_at(a, b, axis, point_world, frame_z=None, props=None, name_prefix="Dovetail_Click"):
    """Place a tapered dovetail tongue at world point; union into B and cut socket into A."""
    if props is None:
        props = bpy.context.scene.snapsplit
    z = {"X": Vector((1,0,0)), "Y": Vector((0,1,0)), "Z": Vector((0,0,1))}[axis].normalized()
    if frame_z is not None:
        z = frame_z.normalized()
    x, y, z = _orthonormal_frame_from_z(z)

    # Use dovetail length for embed
    L_scene = float(props.dovetail_length_mm) * unit_mm()
    embed_pct = float(getattr(props, "pin_embed_pct", 50.0)) * 0.01  # reuse as "embed" control
    p_embed = point_world - z * (embed_pct * L_scene)

    M = Matrix((
        (x.x, y.x, z.x, p_embed.x),
        (x.y, y.y, z.y, p_embed.y),
        (x.z, y.z, z.z, p_embed.z),
        (0,   0,   0,   1.0),
    ))
    # Rotate frame so +X is the requested slide direction
    M = _rotate_frame_for_slide_dir(M, getattr(props, "dovetail_slide_dir", "+X"))

    cutters_coll = ensure_collection("_SnapSplit_Cutters")
    # Build tongue
    tong = create_dovetail_tongue(
        width_mm=props.dovetail_width_mm,
        depth_mm=props.dovetail_depth_mm,
        length_mm=props.dovetail_length_mm,
        draft_deg=props.dovetail_draft_deg,
        leadin_chamfer_mm=props.dovetail_leadin_chamfer_mm,
        name=f"{name_prefix}_Tongue"
    )
    tong.matrix_world = M
    cutters_coll.objects.link(tong)

    # Apply bevel if present (lead-in)
    for mod in list(tong.modifiers):
        if mod.type == 'BEVEL':
            bpy.context.view_layer.objects.active = tong
            tong.select_set(True)
            try:
                bpy.ops.object.modifier_apply(modifier=mod.name)
            except Exception as e:
                report_user(None, 'WARNING', f"Bevel apply failure: {e}", "Bevel anwenden fehlgeschlagen.")
            tong.select_set(False)

    # UNION into B
    union_and_dispose(b, tong, name=f"{name_prefix}_Union")

    # Socket cutter with clearance
    base_tol = float(props.effective_tolerance())
    clr_scale = float(getattr(props, "dovetail_clearance_scale", 1.0))
    c_mm = base_tol * clr_scale
    sock = create_dovetail_socket_cutter(
        width_mm=props.dovetail_width_mm,
        depth_mm=props.dovetail_depth_mm,
        length_mm=props.dovetail_length_mm,
        clearance_per_side_mm=c_mm,
        draft_deg=props.dovetail_draft_deg,
        name=f"{name_prefix}_SocketCutter"
    )
    sock.matrix_world = M
    cutters_coll.objects.link(sock)
    cut_socket_with_cutter_and_dispose(a, sock)
    return None, None

# ---------------------------
# Batch placement
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

    naxis = {"X": Vector((1, 0, 0)), "Y": Vector((0, 1, 0)), "Z": Vector((0, 0, 1))}[axis]
    embed_pct = float(getattr(props, "pin_embed_pct", 50.0)) * 0.01
    margin_pct = float(getattr(props, "connector_margin_pct", 10.0))
    cols = max(1, int(getattr(props, "connectors_per_seam", count)))
    pct, edge_abs = _edge_margins_scene(props)

    for a, b in pairs:
        seam_pos = _pair_seam_plane_pos(a, b, axis, props)

        if getattr(props, "connector_distribution", "LINE") == "GRID":
            rows = max(1, int(getattr(props, "connectors_rows", 2)))
            points = distribute_points_grid_on_seam(a, b, cols, rows, axis, seam_pos,
                                                    margin_pct=pct, edge_margin_scene=edge_abs)
        else:
            points = distribute_points_line_on_seam(a, b, cols, axis, seam_pos,
                                                    margin_pct=pct, edge_margin_scene=edge_abs)

        for i, p in enumerate(points):
            z = naxis.normalized()
            x = Vector((1, 0, 0))
            if abs(z.dot(x)) > 0.99:
                x = Vector((0, 1, 0))
            y = z.cross(x); y.normalize()
            x = y.cross(z); x.normalize()

            ctype_cur = getattr(props, "connector_type", "CYL_PIN")
            # Determine length for embed calculation
            if ctype_cur in {"CYL_PIN", "SNAP_PIN", "PIN_HOLE"}:
                L_scene = float(props.pin_length_mm) * unit_mm()
            elif ctype_cur == "DOVETAIL_TAPER":
                L_scene = float(props.dovetail_length_mm) * unit_mm()
            else:
                L_scene = float(getattr(props, "tenon_depth_mm", 8.0)) * unit_mm()

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

                # DIFFERENCE (socket) into A and dispose
                mm = unit_mm()
                tol = float(props.effective_tolerance())
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

                # Apply bevel if present
                for mod in list(tenon.modifiers):
                    if mod.type == 'BEVEL':
                        bpy.context.view_layer.objects.active = tenon
                        tenon.select_set(True)
                        try:
                            bpy.ops.object.modifier_apply(modifier=mod.name)
                        except Exception as e:
                            report_user(None, 'WARNING', f"Bevel apply failure: {e}",
                                        "Bevel anwenden fehlgeschlagen.")
                        tenon.select_set(False)

                union_and_dispose(b, tenon, name=f"TenonUnion_{i}")

                mm = unit_mm()
                tol = float(props.effective_tolerance())
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

            elif ctype_cur == "PIN_HOLE":
                # Fit-mode socket. Respect pin_hole_only
                hole_only = bool(getattr(props, "pin_hole_only", False))
                if hole_only:
                    # Place only socket at location (no union)
                    seg = int(getattr(props, "pin_segments", 32))
                    c_mm = _pin_fit_mode_clearance_mm(props)
                    socket_d = float(props.pin_diameter_mm) + 2.0 * c_mm
                    socket = create_cyl_pin(socket_d, props.pin_length_mm, 0.0, segments=seg, name=f"PinHole_Socket_{i}")
                    socket.matrix_world = M
                    cutters_coll.objects.link(socket)
                    cut_socket_with_cutter_and_dispose(a, socket)
                    created.append(None)
                else:
                    # Standard pin + fit-mode socket
                    place_one_cyl_pin_at(a, b, axis, p, props=props, name_prefix=f"PinHole_{i}", override_fit_mode=True)
                    created.append(None)

            elif ctype_cur == "DOVETAIL_TAPER":
                # Dovetail tongue + socket using slide_dir
                # Rotate local frame so +X is slide_dir
                M2 = _rotate_frame_for_slide_dir(M, getattr(props, "dovetail_slide_dir", "+X"))
                # Union tongue, cut socket
                place_one_dovetail_at(a, b, axis, p, props=props, name_prefix=f"Dovetail_{i}")
                created.append(None)

            else:
                # Unknown future types fallback -> rectangular tenon as safe default
                tenon = create_rect_tenon_quader(props.tenon_width_mm, props.tenon_depth_mm, props.add_chamfer_mm,
                                                 name=f"Tenon_{i}")
                tenon.matrix_world = M
                cutters_coll.objects.link(tenon)
                union_and_dispose(b, tenon, name=f"TenonUnion_{i}")

                mm = unit_mm()
                tol = float(props.effective_tolerance())
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
# Modal operator: place by click (extended)
# ---------------------------

class SNAP_OT_place_connectors_click(Operator):
    """Interactively place a connector (pin/tenon/fit/dovetail) by clicking on the seam plane between two parts."""
    bl_idname = "snapsplit.place_connectors_click"
    bl_label = "Place connectors (click)"
    bl_options = {'REGISTER', 'UNDO', 'BLOCKING'}

    def invoke(self, context, event):
        """Start modal placement with live preview for two selected mesh parts."""
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

        # Preview object(s)
        try:
            ctype_cur = getattr(props, "connector_type", "CYL_PIN")
            prev_coll = ensure_collection("_SnapSplit_Preview")

            self.preview_objs = []  # may be multiple for complex previews
            self.preview_obj = None

            segmap = _resolve_preview_density_segments()

            if ctype_cur in {"CYL_PIN", "SNAP_PIN", "PIN_HOLE"}:
                # reuse pin preview
                seg = int(getattr(props, "pin_segments", segmap["cyl"]))
                pin_prev = create_cyl_pin(props.pin_diameter_mm, props.pin_length_mm, getattr(props, "add_chamfer_mm", 0.0),
                                          segments=seg, name="SnapSplit_Preview_Conn")
                pin_prev.display_type = 'WIRE'
                pin_prev.hide_select = True
                prev_coll.objects.link(pin_prev)
                self.preview_obj = pin_prev
                self.preview_objs.append(pin_prev)

            elif ctype_cur in {"RECT_TENON", "SNAP_TENON"}:
                ten_prev = create_rect_tenon_quader(props.tenon_width_mm, props.tenon_depth_mm, getattr(props, "add_chamfer_mm", 0.0),
                                                    name="SnapSplit_Preview_Conn")
                ten_prev.display_type = 'WIRE'
                ten_prev.hide_select = True
                prev_coll.objects.link(ten_prev)
                self.preview_obj = ten_prev
                self.preview_objs.append(ten_prev)

            elif ctype_cur == "DOVETAIL_TAPER":
                dov_prev = create_dovetail_tongue(
                    width_mm=props.dovetail_width_mm,
                    depth_mm=props.dovetail_depth_mm,
                    length_mm=props.dovetail_length_mm,
                    draft_deg=props.dovetail_draft_deg,
                    leadin_chamfer_mm=0.0,
                    name="SnapSplit_Preview_Dovetail"
                )
                dov_prev.display_type = 'WIRE'
                dov_prev.hide_select = True
                prev_coll.objects.link(dov_prev)
                self.preview_obj = dov_prev
                self.preview_objs.append(dov_prev)

            else:
                # fallback preview: a small cube
                ten_prev = create_rect_tenon_quader(4.0, 6.0, 0.0, name="SnapSplit_Preview_Generic")
                ten_prev.display_type = 'WIRE'
                ten_prev.hide_select = True
                prev_coll.objects.link(ten_prev)
                self.preview_obj = ten_prev
                self.preview_objs.append(ten_prev)

        except Exception:
            self.preview_obj = None
            self.preview_objs = []

        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def finish(self, context, cancelled=False):
        """Tear down preview objects and optionally report cancellation."""
        try:
            if getattr(self, "preview_obj", None) and self.preview_obj.name in bpy.data.objects:
                for coll in list(self.preview_obj.users_collection):
                    coll.objects.unlink(self.preview_obj)
                bpy.data.objects.remove(self.preview_obj)

            if getattr(self, "preview_objs", None):
                for o in list(self.preview_objs):
                    if o and o.name in bpy.data.objects:
                        for coll in list(o.users_collection):
                            try: coll.objects.unlink(o)
                            except Exception: pass
                        try: bpy.data.objects.remove(o)
                        except Exception: pass
                self.preview_objs.clear()
        except Exception:
            pass

        if cancelled:
            report_user(self, 'INFO', "Placement cancelled.", "Platzierung abgebrochen.")

    def modal(self, context, event):
        """Handle mouse movement for preview updates and left-click for placement."""
        try:
            # Cancel
            if event.type in {'ESC', 'RIGHTMOUSE'} and event.value == 'PRESS':
                self.finish(context, cancelled=True)
                return {'CANCELLED'}

            # Mouse move: Update preview transforms
            if event.type == 'MOUSEMOVE':
                try:
                    hit = self._intersect_mouse_with_seam_plane(context, event)
                    if hit is not None:
                        M = self._build_frame_at(hit)
                        if self.preview_obj:
                            # Apply slide-dir adjustment for dovetail preview
                            if getattr(self.props, "connector_type", "") == "DOVETAIL_TAPER":
                                M = _rotate_frame_for_slide_dir(M, getattr(self.props, "dovetail_slide_dir", "+X"))
                            self.preview_obj.matrix_world = M
                except Exception:
                    pass
                return {'RUNNING_MODAL'}

            # Left click: place connector
            if event.type == 'LEFTMOUSE' and event.value == 'PRESS':
                try:
                    hit = self._intersect_mouse_with_seam_plane(context, event)
                    if hit is not None:
                        ctype_cur = getattr(self.props, "connector_type", "CYL_PIN")
                        if ctype_cur == "CYL_PIN":
                            place_one_cyl_pin_at(self.a, self.b, self.axis, hit, props=self.props, name_prefix="Pin_Click")
                        elif ctype_cur == "RECT_TENON":
                            # Reuse existing tenon placement by converting via batch code fallback
                            # Minimal: create and union + socket similar to batch (omitted here for brevity)
                            place_one_rect_tenon_at = None  # not redefining existing; keep batch flow primary
                            report_user(self, 'INFO', "Use batch add for tenons currently.", "Für Zapfen derzeit Batch verwenden.")
                        elif ctype_cur == "SNAP_PIN":
                            place_one_cyl_pin_at(self.a, self.b, self.axis, hit, props=self.props, name_prefix="Pin_Click")
                            # Note: snap spheres added only in batch flow for now to keep click flow lightweight
                        elif ctype_cur == "SNAP_TENON":
                            report_user(self, 'INFO', "Use batch add for snap tenons currently.", "Für Snap-Zapfen derzeit Batch verwenden.")
                        elif ctype_cur == "PIN_HOLE":
                            place_one_cyl_pin_at(self.a, self.b, self.axis, hit, props=self.props, name_prefix="PinHole_Click", override_fit_mode=True)
                        elif ctype_cur == "DOVETAIL_TAPER":
                            place_one_dovetail_at(self.a, self.b, self.axis, hit, props=self.props, name_prefix="Dovetail_Click")
                        else:
                            report_user(self, 'INFO', "Use batch add for this connector.", "Für diesen Verbinder Batch verwenden.")
                except Exception as e:
                    report_user(self, 'ERROR', f"Placement failed: {e}",
                                "Platzierung fehlgeschlagen.")
                return {'RUNNING_MODAL'}

            return {'RUNNING_MODAL'}

        except Exception as e:
            report_user(self, 'ERROR', f"Modal error: {e}", "Modal-Fehler.")
            return {'RUNNING_MODAL'}

    def _intersect_mouse_with_seam_plane(self, context, event):
        """Raycast from mouse into the seam plane and return the hit point in world space."""
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
        """Build a local placement frame (Matrix) at a world point based on axis and embed depth."""
        z = {"X": Vector((1,0,0)), "Y": Vector((0,1,0)), "Z": Vector((0,0,1))}[self.axis].normalized()
        x = Vector((1,0,0))
        if abs(z.dot(x)) > 0.99:
            x = Vector((0,1,0))
        y = z.cross(x); y.normalize()
        x = y.cross(z); x.normalize()

        ctype_cur = getattr(self.props, "connector_type", "CYL_PIN")
        if ctype_cur in {"CYL_PIN", "SNAP_PIN", "PIN_HOLE"}:
            L_scene = float(self.props.pin_length_mm) * unit_mm()
        elif ctype_cur == "DOVETAIL_TAPER":
            L_scene = float(self.props.dovetail_length_mm) * unit_mm()
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
# Batch placement operator (existing name, extended)
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
    """Register operators for connector placement."""
    for c in classes:
        bpy.utils.register_class(c)

def unregister():
    """Unregister operators for connector placement."""
    for c in reversed(classes):
        bpy.utils.unregister_class(c)
