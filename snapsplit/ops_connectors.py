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

def create_rect_tenon_quader(w_mm=6.0, length_mm=10.0, chamfer_mm=0.0, name="SnapSplit_Tenon"):
    """
    Länglicher Quader: X=Breite, Y=Breite (quadratischer Querschnitt), Z=Länge (Steckrichtung).
    Chamfer optional über Modifier (einfach, nicht destruktiv hier).
    """
    mm = unit_mm()
    w = float(w_mm) * mm
    L = float(length_mm) * mm
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    # Skaliere auf w x w x L
    bmesh.ops.transform(bm, matrix=Matrix.Diagonal(Vector((w, w, L, 1.0))), verts=bm.verts)
    # Verschiebe, so dass Boden z=0, Spitze z=L (wie Pin)
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
# Snap spheres (shared helpers)
# ---------------------------

def _ring_height_for_visible_half(length_scene, embed_pct):
    """Mitte der herausstehenden Hälfte (B-seitig)."""
    L_free = max(0.0, (1.0 - embed_pct) * length_scene)
    return embed_pct * length_scene + 0.5 * L_free

def _choose_visible_half_robust(base_matrix, zA, zB):
    """Wähle robust die wirklich herausstehende Hälfte anhand der Frame-Z-Richtung."""
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

# ---------------------------
# Sphere-placement (for cylindrical Pins)
# ---------------------------

def add_snap_spheres_for_cyl_pin(base_matrix, pin_radius_scene, length_scene, props, name_prefix, part_a, part_b, cutters_coll):
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

        # UNION in Teil B
        um = part_b.modifiers.new(f"{name_prefix}_SnapU_{i}", 'BOOLEAN')
        um.operation = 'UNION'; um.solver = 'EXACT'; um.object = sphere
        boolean_apply(part_b, um)

        # Cutter (mit Toleranz) für Teil A
        tol = float(props.effective_tolerance())
        scale = 1.0 + (tol * mm) / max(sph_r_scene, 1e-9)
        sph_cut = sphere.copy()
        sph_cut.data = sphere.data.copy()
        sph_cut.name = f"{name_prefix}_SnapC_{i}"
        cutters_coll.objects.link(sph_cut)
        sph_cut.matrix_world = M @ Matrix.Diagonal(Vector((scale, scale, scale, 1.0)))
        cut_socket_with_cutter(part_a, sph_cut)

        created.append(sphere)
    return created

# ---------------------------
# Sphere-placement (for rectangular Tenon-as-Quader)
# ---------------------------

def add_snap_spheres_for_rect_tenon_ring(base_matrix, half_w_scene, length_scene, props, name_prefix, part_a, part_b, cutters_coll):
    """
    Ringförmige Sphären um Quader-Querschnitt (quadratisch w x w), analog zu zylindrischem Pin.
    Wir approximieren den Radius mit half_w_scene.
    """
    mm = unit_mm()
    n_per_side = max(1, int(getattr(props, "snap_spheres_per_side", 2)))
    d_sph_mm = float(getattr(props, "snap_sphere_diameter_mm", 2.0))
    protrude_scene = float(getattr(props, "snap_sphere_protrusion_mm", 1.0)) * mm

    embed_pct = max(0.0, min(1.0, float(getattr(props, "pin_embed_pct", 50.0)) * 0.01))
    zA = 0.5 * embed_pct * length_scene
    zB = _ring_height_for_visible_half(length_scene, embed_pct)
    ring_z = _choose_visible_half_robust(base_matrix, zA, zB)

    sph_r_scene = 0.5 * float(d_sph_mm) * mm
    # Abstand vom Zentrum: half_w_scene + Überstand - Sphärenradius (radialisiert)
    r_center = half_w_scene + protrude_scene - sph_r_scene

    import math
    created = []
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

        # UNION in B
        um = part_b.modifiers.new(f"{name_prefix}_SnapU_{i}", 'BOOLEAN')
        um.operation = 'UNION'; um.solver = 'EXACT'; um.object = sphere
        boolean_apply(part_b, um)

        # DIFFERENCE in A (mit Toleranz)
        tol = float(props.effective_tolerance())
        scale = 1.0 + (tol * mm) / max(sph_r_scene, 1e-9)
        sph_cut = sphere.copy()
        sph_cut.data = sphere.data.copy()
        sph_cut.name = f"{name_prefix}_SnapC_{i}"
        cutters_coll.objects.link(sph_cut)
        sph_cut.matrix_world = M @ Matrix.Diagonal(Vector((scale, scale, scale, 1.0)))
        cut_socket_with_cutter(part_a, sph_cut)

        created.append(sphere)

    return created

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
    Boolean-Policy: UNION in B (sichtbar), DIFFERENCE (Socket) in A.
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

    # UNION in B
    um = b.modifiers.new(f"{name_prefix}_Union", 'BOOLEAN')
    um.operation = 'UNION'; um.solver = 'EXACT'; um.object = pin
    boolean_apply(b, um)

    # DIFFERENCE (Socket) in A
    tol = float(props.effective_tolerance())
    socket_d = float(props.pin_diameter_mm) + 2.0 * tol
    socket = create_cyl_pin(socket_d, props.pin_length_mm, 0.0, segments=seg, name=f"{name_prefix}_SocketCutter")
    socket.matrix_world = M
    cutters_coll.objects.link(socket)
    cut_socket_with_cutter(a, socket)

    return pin, socket

def place_one_rect_tenon_at(a, b, axis, point_world, frame_z=None, props=None, name_prefix="Tenon_Click"):
    """
    Place one rectangular tenon-as-quader at point_world (same logic as pins).
    Boolean-Policy: UNION in B (sichtbar), DIFFERENCE (Socket) in A.
    Returns (tenon, socket_cutter).
    """
    if props is None:
        props = bpy.context.scene.snapsplit
    z = {"X": Vector((1,0,0)), "Y": Vector((0,1,0)), "Z": Vector((0,0,1))}[axis].normalized()
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

    # Bevel ggf. anwenden
    for mod in list(tenon.modifiers):
        if mod.type == 'BEVEL':
            bpy.context.view_layer.objects.active = tenon
            tenon.select_set(True)
            try:
                bpy.ops.object.modifier_apply(modifier=mod.name)
            except Exception as e:
                report_user(None, 'WARNING', f"Bevel apply failure: {e}")
            tenon.select_set(False)

    # UNION in B
    um = b.modifiers.new(f"{name_prefix}_Union", 'BOOLEAN')
    um.operation = 'UNION'; um.solver = 'EXACT'; um.object = tenon
    boolean_apply(b, um)

    # DIFFERENCE (Socket) in A (skaliert mit Toleranz auf X/Y, volle Länge Z)
    mm = unit_mm()
    tol = float(props.effective_tolerance())
    # Half-Extents des Tenon-Quaders
    half_w = max(tenon.dimensions.x * 0.5, 1e-9)  # = y ebenfalls, da quadratisch
    half_L = max(tenon.dimensions.z * 0.5, 1e-9)
    sx = 1.0 + (tol * mm) / half_w
    sy = 1.0 + (tol * mm) / half_w
    sz = 1.0  # keine Toleranz in Längsrichtung nötig

    socket = tenon.copy()
    socket.data = tenon.data.copy()
    socket.name = f"{name_prefix}_SocketCutter"
    cutters_coll.objects.link(socket)
    socket.matrix_world = M @ Matrix.Diagonal(Vector((sx, sy, sz, 1.0)))
    cut_socket_with_cutter(a, socket)

    return tenon, socket

# ---------------------------
# Placement & connect (pairwise seam plane)
# ---------------------------

def place_connectors_between(parts, axis, count, ctype, props):
    """
    Connect adjacent parts along 'axis' with distribution per props.connector_distribution.
    Boolean-Policy: Geometrie (Pin/Tenon + Snap-Spheres) UNION in B, Socket/Cutter DIFFERENCE in A.
    Tenon ist länglicher Quader analog zu Pin-Logik.
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

            ctype_cur = getattr(props, "connector_type", "CYL_PIN")

            if ctype_cur in {"CYL_PIN", "SNAP_PIN"}:
                L_scene = float(props.pin_length_mm) * unit_mm()
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
                # Pin
                seg = int(getattr(props, "pin_segments", 32))
                pin = create_cyl_pin(props.pin_diameter_mm, props.pin_length_mm, props.add_chamfer_mm,
                                     segments=seg, name=f"Pin_{i}")
                pin.matrix_world = M
                cutters_coll.objects.link(pin)

                # UNION in B
                um = b.modifiers.new(f"PinUnion_{i}", 'BOOLEAN')
                um.operation = 'UNION'; um.solver = 'EXACT'; um.object = pin
                boolean_apply(b, um)

                # DIFFERENCE (Socket) in A
                mm = unit_mm()
                socket_d = float(props.pin_diameter_mm) + 2.0 * tol
                socket = create_cyl_pin(socket_d, props.pin_length_mm, 0.0, segments=seg, name=f"SocketCutter_{i}")
                socket.matrix_world = M
                cutters_coll.objects.link(socket)
                cut_socket_with_cutter(a, socket)

                created.append(pin)

                # Snap spheres für Pin
                if ctype_cur == "SNAP_PIN":
                    pin_radius_scene = 0.5 * float(props.pin_diameter_mm) * mm
                    length_scene = float(props.pin_length_mm) * mm
                    add_snap_spheres_for_cyl_pin(
                        base_matrix=M,
                        pin_radius_scene=pin_radius_scene,
                        length_scene=length_scene,
                        props=props,
                        name_prefix=f"Pin_{i}",
                        part_a=a,
                        part_b=b,
                        cutters_coll=cutters_coll
                    )

            elif ctype_cur in {"RECT_TENON", "SNAP_TENON"}:
                # Tenon als Quader (analog zu Pin)
                tenon = create_rect_tenon_quader(props.tenon_width_mm, props.tenon_depth_mm, props.add_chamfer_mm,
                                                 name=f"Tenon_{i}")
                tenon.matrix_world = M
                cutters_coll.objects.link(tenon)

                # Bevel ggf. anwenden
                for mod in list(tenon.modifiers):
                    if mod.type == 'BEVEL':
                        bpy.context.view_layer.objects.active = tenon
                        tenon.select_set(True)
                        try:
                            bpy.ops.object.modifier_apply(modifier=mod.name)
                        except Exception as e:
                            report_user(None, 'WARNING', f"Bevel apply failure: {e}")
                        tenon.select_set(False)

                # UNION in B
                um = b.modifiers.new(f"TenonUnion_{i}", 'BOOLEAN')
                um.operation = 'UNION'; um.solver = 'EXACT'; um.object = tenon
                boolean_apply(b, um)

                # DIFFERENCE (Socket) in A (X/Y aufgeweitet, Z unverändert)
                mm = unit_mm()
                half_w = max(tenon.dimensions.x * 0.5, 1e-9)
                sx = 1.0 + (tol * mm) / half_w
                sy = sx
                sz = 1.0

                socket = tenon.copy()
                socket.data = tenon.data.copy()
                socket.name = f"TenonSocketCutter_{i}"
                cutters_coll.objects.link(socket)
                socket.matrix_world = M @ Matrix.Diagonal(Vector((sx, sy, sz, 1.0)))
                cut_socket_with_cutter(a, socket)

                created.append(tenon)

                # Snap spheres für Snap-Tenon: ringförmig um Querschnitt (wie Pin)
                if ctype_cur == "SNAP_TENON":
                    half_w_scene = max(tenon.dimensions.x * 0.5, 1e-9)
                    length_scene = float(props.tenon_depth_mm) * unit_mm()
                    add_snap_spheres_for_rect_tenon_ring(
                        base_matrix=M,
                        half_w_scene=half_w_scene,
                        length_scene=length_scene,
                        props=props,
                        name_prefix=f"Tenon_{i}",
                        part_a=a,
                        part_b=b,
                        cutters_coll=cutters_coll
                    )

            else:
                # Fallback: behandle wie Tenon-Quader
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
                            report_user(None, 'WARNING', f"Bevel apply failure: {e}")
                        tenon.select_set(False)

                # UNION in B
                um = b.modifiers.new(f"TenonUnion_{i}", 'BOOLEAN')
                um.operation = 'UNION'; um.solver = 'EXACT'; um.object = tenon
                boolean_apply(b, um)

                # DIFFERENCE (Socket) in A
                mm = unit_mm()
                half_w = max(tenon.dimensions.x * 0.5, 1e-9)
                sx = 1.0 + (tol * mm) / half_w
                sy = sx
                sz = 1.0

                socket = tenon.copy()
                socket.data = tenon.data.copy()
                socket.name = f"TenonSocketCutter_{i}"
                cutters_coll.objects.link(socket)
                socket.matrix_world = M @ Matrix.Diagonal(Vector((sx, sy, sz, 1.0)))
                cut_socket_with_cutter(a, socket)

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
            ctype_cur = getattr(props, "connector_type", "CYL_PIN")
            prev_coll = ensure_collection("_SnapSplit_Preview")

            self.preview_objs = []  # mehrere Objekte bei SNAP_PIN/SNAP_TENON
            self.preview_obj = None

            if ctype_cur in {"CYL_PIN", "SNAP_PIN"}:
                seg = int(getattr(props, "pin_segments", 32))
                pin_prev = create_cyl_pin(props.pin_diameter_mm, props.pin_length_mm, props.add_chamfer_mm,
                                          segments=seg, name="SnapSplit_Preview_Conn")
                pin_prev.display_type = 'WIRE'
                pin_prev.hide_select = True
                prev_coll.objects.link(pin_prev)
                self.preview_obj = pin_prev
                self.preview_objs.append(pin_prev)

                if ctype_cur == "SNAP_PIN":
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
            else:
                # Tenon-Quader
                ten_prev = create_rect_tenon_quader(props.tenon_width_mm, props.tenon_depth_mm, props.add_chamfer_mm,
                                                    name="SnapSplit_Preview_Conn")
                ten_prev.display_type = 'WIRE'
                ten_prev.hide_select = True
                prev_coll.objects.link(ten_prev)
                self.preview_obj = ten_prev
                self.preview_objs.append(ten_prev)

                if ctype_cur == "SNAP_TENON":
                    # Vorschau-Sphären als Ring um Querschnitt, analog zu Pin
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
                            self.preview_obj.matrix_world = M
                        # SNAP_PIN / SNAP_TENON previews
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
                                        # A/B-Offsets vorhanden -> robust wählen
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
                                    else:
                                        # einfacher Offset
                                        ox, oy, oz = o.get("_snapsplit_local_offset", (0.0, 0.0, 0.0))
                                        o.matrix_world = M @ Matrix.Translation((ox, oy, oz))
                                except Exception:
                                    pass
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
                            place_one_rect_tenon_at(self.a, self.b, self.axis, hit, props=self.props, name_prefix="Tenon_Click")
                        elif ctype_cur == "SNAP_PIN":
                            pin, socket = place_one_cyl_pin_at(self.a, self.b, self.axis, hit, props=self.props, name_prefix="Pin_Click")
                            M = pin.matrix_world.copy()
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
                            tenon, socket = place_one_rect_tenon_at(self.a, self.b, self.axis, hit, props=self.props, name_prefix="Tenon_Click")
                            M = tenon.matrix_world.copy()
                            half_w_scene = max(tenon.dimensions.x * 0.5, 1e-9)
                            length_scene = float(self.props.tenon_depth_mm) * unit_mm()
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
                except Exception as e:
                    report_user(self, 'ERROR', f"Placement failed: {e}",
                                "Platzierung fehlgeschlagen.")
                return {'RUNNING_MODAL'}

            # Fallback
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

    def _build_frame_at(self, point_world):
        z = {"X": Vector((1,0,0)), "Y": Vector((0,1,0)), "Z": Vector((0,0,1))}[self.axis].normalized()
        x = Vector((1,0,0))
        if abs(z.dot(x)) > 0.99:
            x = Vector((0,1,0))
        y = z.cross(x); y.normalize()
        x = y.cross(z); x.normalize()

        ctype_cur = getattr(self.props, "connector_type", "CYL_PIN")
        if ctype_cur in {"CYL_PIN", "SNAP_PIN"}:
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
