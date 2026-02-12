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
from mathutils import Vector, Matrix
from bpy.types import Operator

from .utils import (
    ensure_collection,
    mm_to_scene,
    unit_mm,                 # legacy factor; adapts to scene (1.0 in mm scenes, 0.001 in meter scenes)
    report_user,
    apply_scale_if_needed,
    validate_mesh,
    is_lang_de,
)

# ---------------------------
# BBox and projection helpers
# ---------------------------

def _bb_world(obj):
    """World-space 8 BB corners."""
    return [obj.matrix_world @ Vector(c) for c in obj.bound_box]

def _proj_interval(points, axis_dir, origin):
    """Project points onto axis_dir (around origin), return scalar (min,max)."""
    a = axis_dir.normalized()
    return (min((p - origin).dot(a) for p in points),
            max((p - origin).dot(a) for p in points))

def _bb_center(points):
    """Average of 8 BB corners."""
    return sum(points, Vector()) / 8.0

# ---------------------------
# Seam-axis detection per pair
# ---------------------------

def detect_seam_axis(obj_a, obj_b):
    """
    Decide likely seam axis (X/Y/Z) via centers delta and orient a normal from A -> B.
    Returns (axis_key, normal_vec).
    """
    ca = _bb_center(_bb_world(obj_a))
    cb = _bb_center(_bb_world(obj_b))
    delta = cb - ca

    if delta.length < 1e-12:
        dims = (abs(obj_a.dimensions.x - obj_b.dimensions.x),
                abs(obj_a.dimensions.y - obj_b.dimensions.y),
                abs(obj_a.dimensions.z - obj_b.dimensions.z))
        idx = max(range(3), key=lambda i: dims[i])
    else:
        abs_d = (abs(delta.x), abs(delta.y), abs(delta.z))
        idx = max(range(3), key=lambda i: abs_d[i])

    axis_key = ('X', 'Y', 'Z')[idx]
    n = Vector((1,0,0)) if axis_key == 'X' else (Vector((0,1,0)) if axis_key == 'Y' else Vector((0,0,1)))
    if delta.length > 0 and delta.dot(n) < 0:
        n = -n
    return axis_key, n

def axis_frame_from_axis(axis_key):
    """Return (normal, t1, t2) for the given axis key."""
    if axis_key == 'X':
        return Vector((1,0,0)), Vector((0,1,0)), Vector((0,0,1))
    if axis_key == 'Y':
        return Vector((0,1,0)), Vector((1,0,0)), Vector((0,0,1))
    return Vector((0,0,1)), Vector((1,0,0)), Vector((0,1,0))  # 'Z'

# ---------------------------
# Distribution: line
# ---------------------------

def distribute_points_line(obj_a, obj_b, count, axis_key, margin_pct=10.0):
    """
    Distribute 'count' points along the longer in-plane tangent of the common seam area,
    constrained to the overlap interval of both parts, with percentage edge margin.
    """
    n_axis, t1, t2 = axis_frame_from_axis(axis_key)

    bb_a = _bb_world(obj_a)
    bb_b = _bb_world(obj_b)

    ca = _bb_center(bb_a)
    cb = _bb_center(bb_b)
    origin = (ca + cb) * 0.5

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
        c = origin
        return [c for _ in range(max(1, count))]

    m = max(0.0, float(margin_pct)) * 0.01 * span
    lo_i = lo + m
    hi_i = hi - m
    if hi_i < lo_i:
        mid = (lo + hi) * 0.5
        return [(origin + t * mid) for _ in range(max(1, count))]

    if count <= 1:
        mid = (lo_i + hi_i) * 0.5
        return [origin + t * mid]

    pts = []
    for i in range(count):
        f = i / (count - 1)  # 0..1
        s = lo_i * (1.0 - f) + hi_i * f
        pts.append(origin + t * s)
    return pts

# ---------------------------
# Distribution: grid (area)
# ---------------------------

def distribute_points_grid(obj_a, obj_b, cols, rows, axis_key, margin_pct=10.0):
    """
    Distribute points in a grid within the overlapping rectangle of the seam area.
    cols = columns along primary tangent, rows = along secondary tangent.
    """
    n_axis, t1, t2 = axis_frame_from_axis(axis_key)

    bb_a = _bb_world(obj_a)
    bb_b = _bb_world(obj_b)

    ca = _bb_center(bb_a)
    cb = _bb_center(bb_b)
    origin = (ca + cb) * 0.5

    def interval_overlap(a_min, a_max, b_min, b_max):
        lo = max(a_min, b_min)
        hi = min(a_max, b_max)
        return lo, hi, max(0.0, hi - lo)

    t1_min_a, t1_max_a = _proj_interval(bb_a, t1, origin)
    t1_min_b, t1_max_b = _proj_interval(bb_b, t1, origin)
    t2_min_a, t2_max_a = _proj_interval(bb_a, t2, origin)
    t2_min_b, t2_max_b = _proj_interval(bb_b, t2, origin)

    lo1, hi1, span1 = interval_overlap(t1_min_a, t1_max_a, t1_min_b, t1_max_b)
    lo2, hi2, span2 = interval_overlap(t2_min_a, t2_max_a, t2_min_b, t2_max_b)

    if span1 <= 0.0 or span2 <= 0.0:
        # No rectangular overlap -> fallback to line distribution on the larger span
        return distribute_points_line(obj_a, obj_b, cols, axis_key, margin_pct)

    m1 = max(0.0, float(margin_pct)) * 0.01 * span1
    m2 = max(0.0, float(margin_pct)) * 0.01 * span2
    lo1_i, hi1_i = lo1 + m1, hi1 - m1
    lo2_i, hi2_i = lo2 + m2, hi2 - m2
    if hi1_i < lo1_i or hi2_i < lo2_i:
        # Margin too large -> place in the center
        c = origin + t1.normalized() * ((lo1 + hi1) * 0.5) + t2.normalized() * ((lo2 + hi2) * 0.5)
        return [c for _ in range(max(1, cols * rows))]

    # Even grid
    t1n = t1.normalized()
    t2n = t2.normalized()

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
    """
    Create a cylindrical pin object (unlinked).
    Dimensions in mm converted to scene units via unit_mm().
    """
    mm = unit_mm()
    d = float(d_mm) * mm
    L = float(length_mm) * mm
    r = max(1e-9, d * 0.5)

    bm = bmesh.new()
    bmesh.ops.create_cone(
        bm,
        cap_ends=True,
        cap_tris=False,
        segments=max(8, int(segments)),
        radius1=r,
        radius2=r,
        depth=L
    )
    # Place bottom at z=0, top at z=L
    bmesh.ops.transform(bm, matrix=Matrix.Translation((0, 0, L * 0.5)), verts=bm.verts)

    # Optional top chamfer (simple approximation)
    if chamfer_mm and chamfer_mm > 0.0:
        chamfer = float(chamfer_mm) * mm
        top_z = max(v.co.z for v in bm.verts)
        top_verts = [v for v in bm.verts if abs(v.co.z - top_z) < 1e-7]
        scale = max(0.0, (r - chamfer) / r)
        for v in top_verts:
            v.co.x *= scale
            v.co.y *= scale
            v.co.z -= chamfer

    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    return bpy.data.objects.new(name, me)

def create_rect_tenon(w_mm, depth_mm, chamfer_mm, name="RectTenon"):
    """
    Create a rectangular tenon object (W×W×Depth) with optional chamfer (via bevel modifier). Unlinked.
    """
    mm = unit_mm()
    w = float(w_mm) * mm
    d = float(depth_mm) * mm
    ch = max(0.0, min(float(chamfer_mm), min(float(w_mm), float(depth_mm)) * 0.5)) * mm

    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    bmesh.ops.transform(bm, matrix=Matrix.Diagonal(Vector((w, w, d, 1.0))), verts=bm.verts)
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    obj = bpy.data.objects.new(name, me)

    if ch > 0.0:
        mod = obj.modifiers.new("Bevel", 'BEVEL')
        mod.width = ch
        mod.segments = 1
        mod.limit_method = 'NONE'
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
        report_user(None, 'WARNING',
                    f"Modifier apply failed ({mod.name}): {e}",
                    f"Modifier anwenden fehlgeschlagen ({mod.name}): {e}")
    target_obj.select_set(False)
    validate_mesh(target_obj)

def cut_socket_with_cutter(target_obj, cutter_obj):
    mod = target_obj.modifiers.new("SnapSplit_Socket", 'BOOLEAN')
    mod.operation = 'DIFFERENCE'
    mod.solver = 'EXACT'
    mod.object = cutter_obj
    boolean_apply(target_obj, mod)

# ---------------------------
# Placement & connect
# ---------------------------

def place_connectors_between(parts, axis_hint, count, ctype, props):
    """
    Connect adjacent parts with connectors.

    - Auto-detect the seam axis per adjacent pair (A,B).
    - Cylindrical Pin: UNION into A, DIFFERENCE socket (with tolerance) in B.
    - Rectangular Tenon: analogous; socket via locally-inflated cutter.

    Supports line and grid distributions with percentage margin.
    """
    # Sort by hint axis to form adjacent pairs; each pair detects its own seam axis
    idx_hint = {"X": 0, "Y": 1, "Z": 2}[axis_hint]
    ordered = sorted(parts, key=lambda o: o.location[idx_hint])
    pairs = [(ordered[i], ordered[i + 1]) for i in range(len(ordered) - 1)]
    if not pairs:
        return []

    created = []
    cutters_coll = ensure_collection("_SnapSplit_Cutters")

    tol_mm = float(props.effective_tolerance())  # per-side clearance in mm
    embed_pct = float(getattr(props, "pin_embed_pct", 50.0)) * 0.01
    margin_pct = float(getattr(props, "connector_margin_pct", 10.0))
    mode = getattr(props, "connector_distribution", "LINE")

    for a, b in pairs:
        # Optional stability: remove object scale on targets (helps boolean robustness)
        apply_scale_if_needed(a, apply_scale=True)
        apply_scale_if_needed(b, apply_scale=True)

        # Detect seam axis for this pair
        axis_key, naxis = detect_seam_axis(a, b)

        # Compute distribution points in the seam plane
        if mode == "GRID":
            cols = max(1, int(getattr(props, "connectors_per_seam", count)))
            rows = max(1, int(getattr(props, "connectors_rows", 2)))
            points = distribute_points_grid(a, b, cols, rows, axis_key, margin_pct=margin_pct)
        else:
            cols = max(1, int(getattr(props, "connectors_per_seam", count)))
            points = distribute_points_line(a, b, cols, axis_key, margin_pct=margin_pct)

        for i, p in enumerate(points):
            # Build an orthonormal frame with z along seam normal (A -> B)
            z = naxis.normalized()
            x = Vector((1, 0, 0))
            if abs(z.dot(x)) > 0.99:
                x = Vector((0, 1, 0))
            y = z.cross(x); y.normalize()
            x = y.cross(z); x.normalize()

            # Embed/placement: pins honor embed %, tenons are centered across seam
            length_mm = float(props.pin_length_mm if ctype == "CYL_PIN" else props.tenon_depth_mm)
            L_scene = mm_to_scene(length_mm)
            if ctype == "CYL_PIN":
                p_embed = p - z * (embed_pct * L_scene)
            else:
                p_embed = p - z * (0.5 * L_scene)

            M = Matrix((
                (x.x, y.x, z.x, p_embed.x),
                (x.y, y.y, z.y, p_embed.y),
                (x.z, y.z, z.z, p_embed.z),
                (0,   0,   0,   1.0),
            ))

            if ctype == "CYL_PIN":
                # Pin
                pin = create_cyl_pin(props.pin_diameter_mm, props.pin_length_mm, props.add_chamfer_mm,
                                     segments=32, name=f"Pin_{i}")
                pin.matrix_world = M
                cutters_coll.objects.link(pin)

                # UNION into A
                um = a.modifiers.new(f"PinUnion_{i}", 'BOOLEAN')
                um.operation = 'UNION'
                um.solver = 'EXACT'
                um.object = pin
                boolean_apply(a, um)

                # Socket cutter with diameter = pin + 2*tol
                socket_d_mm = float(props.pin_diameter_mm) + 2.0 * tol_mm
                socket = create_cyl_pin(socket_d_mm, props.pin_length_mm, 0.0, segments=32, name=f"SocketCutter_{i}")
                socket.matrix_world = M
                cutters_coll.objects.link(socket)
                cut_socket_with_cutter(b, socket)

                created.append(pin)

            elif ctype == "RECT_TENON":
                # Create tenon and link
                tenon = create_rect_tenon(props.tenon_width_mm, props.tenon_depth_mm, props.add_chamfer_mm)
                tenon.matrix_world = M
                cutters_coll.objects.link(tenon)

                # Apply bevel (if any)
                for mod in list(tenon.modifiers):
                    if mod.type == 'BEVEL':
                        bpy.context.view_layer.objects.active = tenon
                        tenon.select_set(True)
                        try:
                            bpy.ops.object.modifier_apply(modifier=mod.name)
                        except Exception as e:
                            report_user(None, 'WARNING',
                                        f"Tenon bevel apply failed: {e}",
                                        f"Fase am Zapfen konnte nicht angewendet werden: {e}")
                        tenon.select_set(False)

                # Bake rotation+scale for robust boolean
                try:
                    bpy.context.view_layer.objects.active = tenon
                    bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
                except Exception:
                    pass

                # Triangulate + recalc normals
                try:
                    mod_tri = tenon.modifiers.new("TriangulateTmp", 'TRIANGULATE')
                    bpy.ops.object.modifier_apply(modifier=mod_tri.name)
                except Exception:
                    pass
                try:
                    me = tenon.data
                    bm = bmesh.new()
                    bm.from_mesh(me)
                    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
                    bm.to_mesh(me); bm.free(); me.update()
                except Exception:
                    pass

                # UNION into A
                try:
                    um = a.modifiers.new(f"TenonUnion_{i}", 'BOOLEAN')
                    um.operation = 'UNION'
                    um.solver = 'EXACT'
                    um.object = tenon
                    boolean_apply(a, um)
                except Exception as e:
                    report_user(None, 'ERROR',
                                f"Tenon union failed: {e}",
                                f"Vereinigung des Zapfens fehlgeschlagen: {e}")

                # Build socket cutter (deep copy, inflate locally), then slight push into B
                try:
                    socket = tenon.copy()
                    socket.data = tenon.data.copy()
                    socket.name = f"TenonSocketCutter_{i}"
                    cutters_coll.objects.link(socket)

                    # Per-axis inflation derived from tolerance (scene units)
                    tol_scene = mm_to_scene(tol_mm)
                    hx = max(socket.dimensions.x * 0.5, 1e-9)
                    hy = max(socket.dimensions.y * 0.5, 1e-9)
                    hz = max(socket.dimensions.z * 0.5, 1e-9)
                    sx = 1.0 + tol_scene / hx
                    sy = 1.0 + tol_scene / hy
                    sz = 1.0 + tol_scene / hz

                    # Inflate mesh locally via BMesh (avoid object-level scale)
                    bpy.context.view_layer.objects.active = socket
                    socket.select_set(True)
                    bm = bmesh.new()
                    bm.from_mesh(socket.data)
                    S = Matrix.Diagonal((sx, sy, sz, 1.0))
                    bmesh.ops.transform(bm, matrix=S, verts=bm.verts)
                    bm.normal_update()
                    bm.to_mesh(socket.data)
                    bm.free()
                    socket.select_set(False)
                    validate_mesh(socket)

                    # Ensure overlap: small epsilon push along seam normal toward B
                    eps = max(1e-6, mm_to_scene(0.05))  # ~0.05 mm
                    T = Matrix.Translation(z * eps)
                    socket.matrix_world = T @ socket.matrix_world

                    # DIFFERENCE into B
                    cut_socket_with_cutter(b, socket)

                except Exception as e:
                    report_user(None, 'ERROR',
                                f"Tenon socket cutting failed: {e}",
                                f"Zapfen-Buchse konnte nicht geschnitten werden: {e}")

                created.append(tenon)

            else:
                report_user(None, 'WARNING',
                            f"Unknown connector type: {ctype}",
                            f"Unbekannter Verbinder-Typ: {ctype}")

    return created

# ---------------------------
# Operator
# ---------------------------

class SNAP_OT_add_connectors(Operator):
    bl_idname = "snapsplit.add_connectors"
    bl_label = "Add connectors" if not is_lang_de() else "Verbinder hinzufügen"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        props = context.scene.snapsplit
        sel = [o for o in context.selected_objects if o.type == 'MESH']
        if len(sel) < 2:
            report_user(self, 'ERROR',
                        "Select at least two cut mesh parts.",
                        "Mindestens zwei geschnittene Mesh-Teile auswählen.")
            return {'CANCELLED'}

        created = place_connectors_between(
            parts=sel,
            axis_hint=props.split_axis,              # order hint; true axis is detected per pair
            count=props.connectors_per_seam,
            ctype=props.connector_type,
            props=props
        )
        report_user(self, 'INFO',
                    f"{len(created)} connectors created.",
                    f"{len(created)} Verbinder erzeugt.")
        return {'FINISHED'}

classes = (SNAP_OT_add_connectors,)

def register():
    for c in classes:
        bpy.utils.register_class(c)

def unregister():
    for c in reversed(classes):
        bpy.utils.unregister_class(c)

