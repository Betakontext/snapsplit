'''
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
    along with this program; if not, see <https://www.gnu.org
/licenses>.
'''

import bpy
import bmesh
from mathutils import Vector, Matrix
from bpy.types import Operator
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

# ---------------------------
# Distribution: line
# ---------------------------

def distribute_points_line(obj_a, obj_b, count, axis, margin_pct=10.0):
    """
    Distribute 'count' points along the longer in-plane tangent of the common seam area,
    constrained to the overlap span of both parts, with percentage edge margin.
    """
    axes = {
        "X": (Vector((1,0,0)), Vector((0,1,0)), Vector((0,0,1))),
        "Y": (Vector((0,1,0)), Vector((1,0,0)), Vector((0,0,1))),
        "Z": (Vector((0,0,1)), Vector((1,0,0)), Vector((0,1,0))),
    }
    n_axis, t1, t2 = axes[axis]

    bb_a = _bb_world(obj_a)
    bb_b = _bb_world(obj_b)

    ca = sum(bb_a, Vector()) / 8.0
    cb = sum(bb_b, Vector()) / 8.0
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

def distribute_points_grid(obj_a, obj_b, cols, rows, axis, margin_pct=10.0):
    """
    Distribute points in a grid within the overlapping rectangular span of the seam area.
    cols = columns along primary tangent, rows = along secondary tangent.
    """
    axes = {
        "X": (Vector((1,0,0)), Vector((0,1,0)), Vector((0,0,1))),
        "Y": (Vector((0,1,0)), Vector((1,0,0)), Vector((0,0,1))),
        "Z": (Vector((0,0,1)), Vector((1,0,0)), Vector((0,1,0))),
    }
    n_axis, t1, t2 = axes[axis]

    bb_a = _bb_world(obj_a)
    bb_b = _bb_world(obj_b)

    ca = sum(bb_a, Vector()) / 8.0
    cb = sum(bb_b, Vector()) / 8.0
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
        # No rectangular overlap -> fallback to line on the larger span
        return distribute_points_line(obj_a, obj_b, cols, axis, margin_pct)

    m1 = max(0.0, float(margin_pct)) * 0.01 * span1
    m2 = max(0.0, float(margin_pct)) * 0.01 * span2
    lo1_i, hi1_i = lo1 + m1, hi1 - m1
    lo2_i, hi2_i = lo2 + m2, lo2 + (span2 - m2)
    if hi1_i < lo1_i or hi2_i < lo2_i:
        # Margin too large -> place in the middle
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
    Create a cylindrical pin object (not linked). Dimensions are millimeters converted to scene units.
    """
    mm = unit_mm()
    d = float(d_mm) * mm
    L = float(length_mm) * mm
    r = max(1e-9, d * 0.5)

    # Debug
    print(f"[SnapSplit] create_cyl_pin: d_mm={d_mm}, L_mm={length_mm} -> d_scene={d:.6f}, L_scene={L:.6f}")

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
    # Bottom at z=0, top at z=L
    bmesh.ops.transform(bm, matrix=Matrix.Translation((0, 0, L * 0.5)), verts=bm.verts)

    # Optional top chamfer (simple approx)
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
    obj = bpy.data.objects.new(name, me)
    return obj

def create_rect_tenon(w_mm, depth_mm, chamfer_mm, name="RectTenon"):
    """
    Rectangular tenon (W×W×Depth) with optional chamfer (Bevel modifier). Returns an unlinked object.
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
# Placement & connect
# ---------------------------

def place_connectors_between(parts, axis, count, ctype, props):
    """
    Connect adjacent parts along 'axis' with distribution per props.connector_distribution.
    - Cylinder Pin: UNION into part A, DIFFERENCE (with tolerance) in part B
    - Rectangular Tenon: same; socket via scaled cutter
    """
    idx = {"X": 0, "Y": 1, "Z": 2}[axis]
    ordered = sorted(parts, key=lambda o: o.location[idx])
    pairs = [(ordered[i], ordered[i + 1]) for i in range(len(ordered) - 1)]
    if not pairs:
        return []

    created = []
    cutters_coll = ensure_collection("_SnapSplit_Cutters")

    # Seam normal (A -> B)
    naxis = {"X": Vector((1, 0, 0)), "Y": Vector((0, 1, 0)), "Z": Vector((0, 0, 1))}[axis]
    tol = float(props.effective_tolerance())  # mm per side
    embed_pct = float(getattr(props, "pin_embed_pct", 50.0)) * 0.01
    margin_pct = float(getattr(props, "connector_margin_pct", 10.0))

    for a, b in pairs:
        if getattr(props, "connector_distribution", "LINE") == "GRID":
            cols = max(1, int(getattr(props, "connectors_per_seam", count)))
            rows = max(1, int(getattr(props, "connectors_rows", 2)))
            points = distribute_points_grid(a, b, cols, rows, axis, margin_pct=margin_pct)
        else:
            cols = max(1, int(getattr(props, "connectors_per_seam", count)))
            points = distribute_points_line(a, b, cols, axis, margin_pct=margin_pct)

        for i, p in enumerate(points):
            # Orthonormal frame; Z along seam
            z = naxis.normalized()
            x = Vector((1, 0, 0))
            if abs(z.dot(x)) > 0.99:
                x = Vector((0, 1, 0))
            y = z.cross(x); y.normalize()
            x = y.cross(z); x.normalize()

            # Embed depth: move placement point toward A (against z)
            # so that 'embed_pct' of connector length is in A.
            L_scene = float(props.pin_length_mm if ctype == "CYL_PIN" else props.tenon_depth_mm) * unit_mm()
            p_embed = p - z * (embed_pct * L_scene)

            M = Matrix((
                (x.x, y.x, z.x, p_embed.x),
                (x.y, y.y, z.y, p_embed.y),
                (x.z, y.z, z.z, p_embed.z),
                (0,   0,   0,   1.0),
            ))

            if ctype == "CYL_PIN":
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

                # Socket cutter with d = pin + 2*tol
                socket_d = float(props.pin_diameter_mm) + 2.0 * tol
                socket = create_cyl_pin(socket_d, props.pin_length_mm, 0.0, segments=32, name=f"SocketCutter_{i}")
                socket.matrix_world = M
                cutters_coll.objects.link(socket)
                cut_socket_with_cutter(b, socket)

                created.append(pin)

            elif ctype == "RECT_TENON":
                tenon = create_rect_tenon(props.tenon_width_mm, props.tenon_depth_mm, props.add_chamfer_mm)
                tenon.matrix_world = M
                cutters_coll.objects.link(tenon)

                # Apply bevel if any
                for mod in list(tenon.modifiers):
                    if mod.type == 'BEVEL':
                        bpy.context.view_layer.objects.active = tenon
                        tenon.select_set(True)
                        try:
                            bpy.ops.object.modifier_apply(modifier=mod.name)
                        except Exception as e:
                            report_user(None, 'WARNING', f"Bevel apply failure: {e}")
                        tenon.select_set(False)

                # UNION into A
                um = a.modifiers.new(f"TenonUnion_{i}", 'BOOLEAN')
                um.operation = 'UNION'
                um.solver = 'EXACT'
                um.object = tenon
                boolean_apply(a, um)

                # Socket via scaled cutter (uniform tolerance)
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

            else:
                report_user(None, 'WARNING', f"Unknown connector type: {ctype}")

    return created

# ---------------------------
# Operator
# ---------------------------

class SNAP_OT_add_connectors(Operator):
    bl_idname = "snapsplit.add_connectors"
    bl_label = "Add connectors"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        props = context.scene.snapsplit
        sel = [o for o in context.selected_objects if o.type == 'MESH']
        if len(sel) < 2:
            report_user(self, 'ERROR', "Select at least 2 cut mesh-pieces.")
            return {'CANCELLED'}

        created = place_connectors_between(
            parts=sel,
            axis=props.split_axis,
            count=props.connectors_per_seam,
            ctype=props.connector_type,
            props=props
        )
        report_user(self, 'INFO', f"{len(created)} connectors created.")
        return {'FINISHED'}

classes = (SNAP_OT_add_connectors,)

def register():
    for c in classes:
        bpy.utils.register_class(c)

def unregister():
    for c in reversed(classes):
        bpy.utils.unregister_class(c)

