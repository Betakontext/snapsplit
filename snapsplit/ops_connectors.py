import bpy
import bmesh
from math import pi
from mathutils import Vector, Matrix
from bpy.types import Operator
from .profiles import MATERIAL_PROFILES
from .utils import ensure_collection, unit_mm, report_user

def distribute_points_along_bbox_edge(obj_a, obj_b, count, axis):
    # Simple heuristic: place connectors along the midline between two parts, spaced evenly
    # Axis determines seam normal; we compute centers and spread along longest seam axis.
    bb_a = [obj_a.matrix_world @ Vector(c) for c in obj_a.bound_box]
    bb_b = [obj_b.matrix_world @ Vector(c) for c in obj_b.bound_box]
    center = (sum(bb_a, Vector())/8 + sum(bb_b, Vector())/8) * 0.5

    # Determine tangent axes orthogonal to split axis
    axes = {"X": (Vector((0,1,0)), Vector((0,0,1))),
            "Y": (Vector((1,0,0)), Vector((0,0,1))),
            "Z": (Vector((1,0,0)), Vector((0,1,0)))}
    t1, t2 = axes[axis]
    span = 0.0
    # Estimate span using larger of projected bbox dims
    dims = obj_a.dimensions + obj_b.dimensions
    if axis == "X":
        span = max(dims.y, dims.z)
        primary = t1 if dims.y >= dims.z else t2
    elif axis == "Y":
        span = max(dims.x, dims.z)
        primary = t1 if dims.x >= dims.z else t2
    else:
        span = max(dims.x, dims.y)
        primary = t1 if dims.x >= dims.y else t2

    pts = []
    if count == 1:
        pts = [center]
    else:
        for i in range(count):
            f = (i/(count-1) - 0.5) * 0.7  # keep margin
            pts.append(center + primary * span * 0.25 * f)
    return pts

def create_cyl_pin(d_mm, length_mm, chamfer_mm):
    d = d_mm * unit_mm()
    L = length_mm * unit_mm()
    ch = max(0.0, min(chamfer_mm, d_mm*0.5)) * unit_mm()

    mesh = bpy.data.meshes.new("SnapPinMesh")
    bm = bmesh.new()
    segs = max(24, int(d_mm*6))  # smoother for larger diameters
    bmesh.ops.create_circle(bm, cap_ends=True, segments=segs, diameter=d*0.5)
    ret = bmesh.ops.extrude_face_region(bm, geom=list(bm.faces))
    verts = [e for e in ret["geom"] if isinstance(e, bmesh.types.BMVert)]
    bmesh.ops.translate(bm, verts=verts, vec=Vector((0,0,L)))
    # Simple chamfer via bevel modifier later
    bm.to_mesh(mesh); bm.free()
    obj = bpy.data.objects.new("SnapPin", mesh)

    bev = obj.modifiers.new("Bevel", 'BEVEL')
    bev.width = ch if ch > 0 else 0.0
    bev.segments = 1
    bev.limit_method = 'ANGLE'
    bev.angle_limit = pi/4
    return obj

def create_rect_tenon(w_mm, depth_mm, chamfer_mm):
    w = w_mm * unit_mm()
    d = depth_mm * unit_mm()
    ch = max(0.0, min(chamfer_mm, min(w_mm, depth_mm)*0.5)) * unit_mm()

    bpy.ops.mesh.primitive_cube_add(size=1.0)
    obj = bpy.context.active_object
    obj.name = "RectTenon"
    obj.scale = (w*0.5, w*0.5, d*0.5)

    bev = obj.modifiers.new("Bevel", 'BEVEL')
    bev.width = ch if ch > 0 else 0.0
    bev.segments = 1
    bev.limit_method = 'NONE'
    return obj

def cut_socket(target_obj, cutter_obj, clearance_mm):
    # Make an enlarged cutter for socket (clearance per side)
    clr_scale = 1.0
    # Uniform scale approximation: s = 1 + clr / radius for cylinders; for general shapes use Solidify/offset.
    # Here we use a simple Shrink/Fatten on a duplicate mesh for robustness.
    dup = cutter_obj.copy()
    dup.data = cutter_obj.data.copy()
    bpy.context.collection.objects.link(dup)

    # Convert mm to blender units and apply normal offset via Solidify trick
    solid = dup.modifiers.new("Clearance_Offset", 'SOLIDIFY')
    solid.thickness = clearance_mm * unit_mm()
    solid.offset = 1.0
    solid.use_even_offset = True

    # Apply bevel on cutter before boolean for smooth entry
    for mod in list(dup.modifiers):
        try:
            bpy.context.view_layer.objects.active = dup
            bpy.ops.object.modifier_apply(modifier=mod.name)
        except Exception:
            pass

    bm = target_obj.modifiers.new("MakeSocket", 'BOOLEAN')
    bm.operation = 'DIFFERENCE'
    bm.solver = 'EXACT'
    bm.object = dup
    bpy.context.view_layer.objects.active = target_obj
    try:
        bpy.ops.object.modifier_apply(modifier=bm.name)
    except Exception:
        pass

    # Cleanup: move dup to cutters collection
    cutters = ensure_collection("_SnapSplit_Cutters")
    for col in dup.users_collection:
        col.objects.unlink(dup)
    cutters.objects.link(dup)

def place_connectors_between(parts, axis, count, ctype, props):
    # Pair adjacent parts based on bounding-box order along axis
    idx = {"X":0, "Y":1, "Z":2}[axis]
    ordered = sorted(parts, key=lambda o: o.location[idx])
    pairs = [(ordered[i], ordered[i+1]) for i in range(len(ordered)-1)]

    created = []
    cutters_coll = ensure_collection("_SnapSplit_Cutters")

    tol = props.effective_tolerance()  # mm per side
    for a, b in pairs:
        points = distribute_points_along_bbox_edge(a, b, count, axis)

        # Seam normal direction from a to b
        naxis = {"X":Vector((1,0,0)), "Y":Vector((0,1,0)), "Z":Vector((0,0,1))}[axis]
        for i, p in enumerate(points):
            if ctype == "CYL_PIN":
                pin = create_cyl_pin(props.pin_diameter_mm, props.pin_length_mm, props.add_chamfer_mm)
                pin.matrix_world.translation = p
                # Orient pin along seam normal, half in A half in free-space
                # We'll boolean-cut socket in B, keep pin as protrusion on A
                # Move slightly into A so it bonds
                pin_dir = naxis
                # Align Z axis of pin to seam normal
                z = pin_dir.normalized()
                x = Vector((1,0,0))
                if abs(z.dot(x)) > 0.99:
                    x = Vector((0,1,0))
                y = z.cross(x).normalized()
                x = y.cross(z).normalized()
                pin.matrix_world = Matrix((
                    (x.x, y.x, z.x, p.x),
                    (x.y, y.y, z.y, p.y),
                    (x.z, y.z, z.z, p.z),
                    (0,   0,   0,   1  ),
                ))

                bpy.context.collection.objects.link(pin)
                cutters_coll.objects.link(pin)

                # Boolean union pin into A (ensure solid connection)
                um = a.modifiers.new(f"PinUnion_{i}", 'BOOLEAN')
                um.operation = 'UNION'
                um.solver = 'EXACT'
                um.object = pin
                bpy.context.view_layer.objects.active = a
                try:
                    bpy.ops.object.modifier_apply(modifier=um.name)
                except Exception:
                    pass

                # Cut socket in B with clearance
                cut_socket(b, pin, tol)

                created.append(pin)

            elif ctype == "RECT_TENON":
                tenon = create_rect_tenon(props.tenon_width_mm, props.tenon_depth_mm, props.add_chamfer_mm)
                tenon.matrix_world.translation = p

                # Align Z axis of tenon to seam normal
                z = naxis.normalized()
                x = Vector((1,0,0))
                if abs(z.dot(x)) > 0.99:
                    x = Vector((0,1,0))
                y = z.cross(x).normalized()
                x = y.cross(z).normalized()
                tenon.matrix_world = Matrix((
                    (x.x, y.x, z.x, p.x),
                    (x.y, y.y, z.y, p.y),
                    (x.z, y.z, z.z, p.z),
                    (0,   0,   0,   1  ),
                ))

                cutters_coll.objects.link(tenon)

                # Union into A
                um = a.modifiers.new(f"TenonUnion_{i}", 'BOOLEAN')
                um.operation = 'UNION'
                um.solver = 'EXACT'
                um.object = tenon
                bpy.context.view_layer.objects.active = a
                try:
                    bpy.ops.object.modifier_apply(modifier=um.name)
                except Exception:
                    pass

                # Socket in B
                cut_socket(b, tenon, tol)
                created.append(tenon)
    return created

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

