import bpy
import bmesh
from mathutils import Vector, Matrix
from bpy.types import Operator
from .utils import ensure_collection, unit_mm, report_user

# ---------------------------
# Placement entlang der Naht
# ---------------------------

def _bb_world(obj):
    return [obj.matrix_world @ Vector(c) for c in obj.bound_box]

def _proj_interval(points, axis_dir, origin):
    # projiziere Punkte auf 1D entlang axis_dir (normiert), Rückgabe min,max (Skalar)
    a = axis_dir.normalized()
    return (min((p - origin).dot(a) for p in points),
            max((p - origin).dot(a) for p in points))

def distribute_points_along_bbox_edge(obj_a, obj_b, count, axis, margin_pct=10.0):
    """
    Liefert count Positionen entlang der Naht-Tangente, innerhalb der überlappenden Spanne
    beider Teile, mit Randabstand = margin_pct% der Spannenlänge.
    """
    # Naht-Normale und zwei mögliche Tangenten
    axes = {
        "X": (Vector((1,0,0)), Vector((0,1,0)), Vector((0,0,1))),
        "Y": (Vector((0,1,0)), Vector((1,0,0)), Vector((0,0,1))),
        "Z": (Vector((0,0,1)), Vector((1,0,0)), Vector((0,1,0))),
    }
    n_axis, t1, t2 = axes[axis]

    bb_a = _bb_world(obj_a)
    bb_b = _bb_world(obj_b)

    # Ursprung für Projektion: Mittel der BB-Zentren
    ca = sum(bb_a, Vector()) / 8.0
    cb = sum(bb_b, Vector()) / 8.0
    origin = (ca + cb) * 0.5

    # Wähle die Tangente mit der größeren Überlappung
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
        # Fallback: platziere alle an der Mitte
        c = origin
        return [c for _ in range(max(1, count))]

    # Randabstand in Prozent
    m = max(0.0, float(margin_pct)) * 0.01 * span
    lo_i = lo + m
    hi_i = hi - m
    if hi_i < lo_i:
        # zu großer Randabstand → zusammenziehen auf Mitte
        mid = (lo + hi) * 0.5
        return [(origin + t * mid) for _ in range(max(1, count))]

    if count <= 1:
        mid = (lo_i + hi_i) * 0.5
        return [origin + t * mid]

    # Gleichmäßige Verteilung innerhalb [lo_i, hi_i]
    pts = []
    for i in range(count):
        f = i / (count - 1)  # 0..1
        s = lo_i * (1.0 - f) + hi_i * f
        pts.append(origin + t * s)
    return pts

# ---------------------------
# Geometrie: Pins / Tenons
# ---------------------------

def create_cyl_pin(d_mm=5.0, length_mm=10.0, chamfer_mm=0.0, segments=32, name="SnapSplit_Pin"):
    """
    Erzeugt einen zylindrischen Pin als Objekt (NICHT verlinkt).
    Maße in Millimetern, konvertiert zu Blender-Einheiten (Meter).
    """
    mm = unit_mm()
    d = d_mm * mm
    L = length_mm * mm
    r = max(1e-9, d * 0.5)

    bm = bmesh.new()
    # WICHTIG: radius1/radius2 statt diameter*
    bmesh.ops.create_cone(
        bm,
        cap_ends=True,
        cap_tris=False,
        segments=max(8, int(segments)),
        radius1=r,     # unten
        radius2=r,     # oben
        depth=L
    )
    # Unterkante auf z=0, Oberkante auf z=L verschieben
    bmesh.ops.transform(bm, matrix=Matrix.Translation((0, 0, L * 0.5)), verts=bm.verts)

    # Optionale Fase an Oberkante (einfacher Approx)
    if chamfer_mm and chamfer_mm > 0.0:
        chamfer = chamfer_mm * mm
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
    Rechteckiger Zapfen (W×W×Depth) mit optionaler Fase (Bevel-Modifier).
    Gibt ein nicht-verlinktes Objekt zurück.
    """
    mm = unit_mm()
    w = w_mm * mm
    d = depth_mm * mm
    ch = max(0.0, min(chamfer_mm, min(w_mm, depth_mm) * 0.5)) * mm

    # Mesh via BMesh erzeugen (stabiler als Operator-Kette)
    bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    # skaliere zu W×W×Depth
    bmesh.ops.transform(bm, matrix=Matrix.Diagonal(Vector((w, w, d, 1.0))))
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    bm.free()
    obj = bpy.data.objects.new(name, me)

    if ch > 0.0:
        # Für einfache Fase: Bevel-Modifier später anwenden (nachdem verlinkt)
        mod = obj.modifiers.new("Bevel", 'BEVEL')
        mod.width = ch
        mod.segments = 1
        mod.limit_method = 'NONE'
    return obj

# ---------------------------
# Boolean Helpers
# ---------------------------

def boolean_apply(target_obj, mod):
    bpy.context.view_layer.objects.active = target_obj
    target_obj.select_set(True)
    try:
        bpy.ops.object.modifier_apply(modifier=mod.name)
    except Exception as e:
        report_user(None, 'WARNING', f"Modifier Apply fehlgeschlagen ({mod.name}): {e}")
    target_obj.select_set(False)

def cut_socket_with_cutter(target_obj, cutter_obj):
    mod = target_obj.modifiers.new("SnapSplit_Socket", 'BOOLEAN')
    mod.operation = 'DIFFERENCE'
    mod.solver = 'EXACT'
    mod.object = cutter_obj
    boolean_apply(target_obj, mod)

# ---------------------------
# Platzieren & Verbinden
# ---------------------------

def place_connectors_between(parts, axis, count, ctype, props):
    """
    Verbindet benachbarte Teile entlang 'axis' mit 'count' Verbindern.
    - Zylinder-Pin: UNION in Teil A, DIFFERENCE (mit Toleranz) in Teil B
    - Rechteck-Zapfen: analog; Socket per skaliertem Cutter
    """
    idx = {"X": 0, "Y": 1, "Z": 2}[axis]
    ordered = sorted(parts, key=lambda o: o.location[idx])
    pairs = [(ordered[i], ordered[i + 1]) for i in range(len(ordered) - 1)]
    if not pairs:
        return []

    created = []
    cutters_coll = ensure_collection("_SnapSplit_Cutters")

    # Naht-Normale (A -> B)
    naxis = {"X": Vector((1, 0, 0)), "Y": Vector((0, 1, 0)), "Z": Vector((0, 0, 1))}[axis]
    tol = float(props.effective_tolerance())  # mm pro Seite

    for a, b in pairs:
        points = distribute_points_along_bbox_edge(a, b, count, axis, margin_pct=getattr(props, "connector_margin_pct", 10.0))

        for i, p in enumerate(points):
            # Orthonormalbasis, Z entlang Naht
            z = naxis.normalized()
            x = Vector((1, 0, 0))
            if abs(z.dot(x)) > 0.99:
                x = Vector((0, 1, 0))
            y = z.cross(x).normalized()
            x = y.cross(z).normalized()
            M = Matrix((
                (x.x, y.x, z.x, p.x),
                (x.y, y.y, z.y, p.y),
                (x.z, y.z, z.z, p.z),
                (0,   0,   0,   1  ),
            ))

            if ctype == "CYL_PIN":
                # Pin erzeugen und link nur in Cutter-Collection
                pin = create_cyl_pin(props.pin_diameter_mm, props.pin_length_mm, props.add_chamfer_mm, segments=32, name=f"Pin_{i}")
                pin.matrix_world = M
                cutters_coll.objects.link(pin)

                # UNION in A
                um = a.modifiers.new(f"PinUnion_{i}", 'BOOLEAN')
                um.operation = 'UNION'
                um.solver = 'EXACT'
                um.object = pin
                boolean_apply(a, um)

                # Socket-Cutter (separates Objekt) mit Durchmesser = Pin + 2*Tol
                socket_d = props.pin_diameter_mm + 2.0 * tol
                socket = create_cyl_pin(socket_d, props.pin_length_mm, 0.0, segments=32, name=f"SocketCutter_{i}")
                socket.matrix_world = M
                cutters_coll.objects.link(socket)

                # DIFFERENCE in B
                cut_socket_with_cutter(b, socket)

                created.append(pin)

            elif ctype == "RECT_TENON":
                # Tenon erzeugen
                tenon = create_rect_tenon(props.tenon_width_mm, props.tenon_depth_mm, props.add_chamfer_mm)
                tenon.matrix_world = M
                cutters_coll.objects.link(tenon)

                # Bevel ggf. anwenden, falls vorhanden
                for mod in list(tenon.modifiers):
                    if mod.type == 'BEVEL':
                        bpy.context.view_layer.objects.active = tenon
                        tenon.select_set(True)
                        try:
                            bpy.ops.object.modifier_apply(modifier=mod.name)
                        except Exception as e:
                            report_user(None, 'WARNING', f"Bevel Apply fehlgeschlagen: {e}")
                        tenon.select_set(False)

                # UNION in A
                um = a.modifiers.new(f"TenonUnion_{i}", 'BOOLEAN')
                um.operation = 'UNION'
                um.solver = 'EXACT'
                um.object = tenon
                boolean_apply(a, um)

                # Socket via skaliertem Cutter (uniforme Skalierung um ~Tol je Achse)
                mm = unit_mm()
                # Halbe Ausdehnungen im lokalen Raum grob aus den aktuellen Dimensionen
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
                report_user(None, 'WARNING', f"Unbekannter Connector-Typ: {ctype}")

    return created

# ---------------------------
# Operator
# ---------------------------

class SNAP_OT_add_connectors(Operator):
    bl_idname = "snapsplit.add_connectors"
    bl_label = "Verbinder hinzufügen"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        props = context.scene.snapsplit
        sel = [o for o in context.selected_objects if o.type == 'MESH']
        if len(sel) < 2:
            report_user(self, 'ERROR', "Mindestens zwei geschnittene Mesh-Teile auswählen.")
            return {'CANCELLED'}

        created = place_connectors_between(
            parts=sel,
            axis=props.split_axis,
            count=props.connectors_per_seam,
            ctype=props.connector_type,
            props=props
        )
        report_user(self, 'INFO', f"{len(created)} Verbinder erzeugt.")
        return {'FINISHED'}

classes = (SNAP_OT_add_connectors,)

def register():
    for c in classes:
        bpy.utils.register_class(c)

def unregister():
    for c in reversed(classes):
        bpy.utils.unregister_class(c)
