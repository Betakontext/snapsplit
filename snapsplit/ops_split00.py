import bpy
from bpy.types import Operator
from mathutils import Vector
from .utils import ensure_collection, obj_world_bb, report_user

def create_cut_planes(obj, axis, parts_count):
    # Create (parts_count - 1) planes positioned within object bounds
    min_v, max_v = obj_world_bb(obj)
    axis_index = {"X":0, "Y":1, "Z":2}[axis]
    length = max_v[axis_index] - min_v[axis_index]
    if length <= 0.0:
        return []

    planes = []
    for i in range(1, parts_count):
        t = i / parts_count
        pos = min_v[axis_index] + t * length

        # Create a large plane oriented to axis
        bpy.ops.mesh.primitive_plane_add(size=1.0, enter_editmode=False)
        plane = bpy.context.active_object
        plane.name = f"SnapSplit_Plane_{axis}_{i}"

        # Scale plane large to ensure full cut coverage
        plane.scale = (length * 2.0, length * 2.0, 1.0)

        # Orient plane normal along axis and move to pos
        if axis == "X":
            plane.rotation_euler = (0.0, 1.5708, 0.0)  # 90deg around Y
            plane.location.x = pos
        elif axis == "Y":
            plane.rotation_euler = (1.5708, 0.0, 0.0)  # 90deg around X
            plane.location.y = pos
        else:  # Z
            # Default plane lies on XY, normal along +Z; move along Z
            plane.location.z = pos

        planes.append(plane)

    return planes

def boolean_slice(obj, planes):
    # Returns list of new part objects created from boolean slices
    # Strategy: iterative cutting using cube half-spaces, using Exact solver.
    parts = [obj]
    for plane in planes:
        new_parts = []
        # Build two cut volumes: positive and negative half-space from plane
        # Using a very large cube and boolean intersect/difference

        # Create large cube
        bpy.ops.mesh.primitive_cube_add(size=2.0, enter_editmode=False)
        cutter_pos = bpy.context.active_object
        cutter_pos.name = plane.name + "_POS"
        # Create negative (opposite) cutter
        cutter_neg = cutter_pos.copy()
        cutter_neg.data = cutter_pos.data.copy()
        bpy.context.collection.objects.link(cutter_neg)

        # Align cutters to plane orientation/location
        for c in (cutter_pos, cutter_neg):
            c.matrix_world = plane.matrix_world.copy()
            c.scale = (1000.0, 1000.0, 0.001)  # very thin along plane normal, wide across

        # Offset along plane normal tiny amounts to define half-spaces
        n = plane.matrix_world.to_3x3() @ Vector((0, 0, 1))
        cutter_pos.location += n * 0.05
        cutter_neg.location -= n * 0.05

        for p in parts:
            # Positive half
            a = p.copy()
            a.data = p.data.copy()
            a.name = p.name + "_A"
            bpy.context.collection.objects.link(a)
            bm1 = a.modifiers.new("Slice_POS", 'BOOLEAN')
            bm1.operation = 'INTERSECT'
            bm1.solver = 'EXACT'
            bm1.object = cutter_pos

            # Negative half
            b = p.copy()
            b.data = p.data.copy()
            b.name = p.name + "_B"
            bpy.context.collection.objects.link(b)
            bm2 = b.modifiers.new("Slice_NEG", 'BOOLEAN')
            bm2.operation = 'INTERSECT'
            bm2.solver = 'EXACT'
            bm2.object = cutter_neg

            new_parts.extend([a, b])

            # Hide old part
            p.hide_set(True)

        parts = new_parts

        # Housekeeping: place cutters in dedicated collection
        cutters_coll = ensure_collection("_SnapSplit_Cutters")
        for c in (cutter_pos, cutter_neg, plane):
            try:
                for col in c.users_collection:
                    col.objects.unlink(c)
            except:
                pass
            cutters_coll.objects.link(c)

    # Apply modifiers to finalize geometry
    for p in parts:
        for m in list(p.modifiers):
            try:
                bpy.context.view_layer.objects.active = p
                bpy.ops.object.modifier_apply(modifier=m.name)
            except Exception:
                pass

    # Filter invalid/empty meshes
    valid = []
    for p in parts:
        if p.data and len(p.data.polygons) > 0:
            valid.append(p)
        else:
            bpy.data.objects.remove(p, do_unlink=True)

    return valid

class SNAP_OT_planar_split(Operator):
    bl_idname = "snapsplit.planar_split"
    bl_label = "Planar Split"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.active_object
        if not obj or obj.type != 'MESH':
            report_user(self, 'ERROR', "Bitte ein Mesh-Objekt auswählen.")
            return {'CANCELLED'}

        props = context.scene.snapsplit
        planes = create_cut_planes(obj, props.split_axis, props.parts_count)
        if not planes:
            report_user(self, 'ERROR', "Konnte keine Schnittflächen erzeugen.")
            return {'CANCELLED'}

        parts = boolean_slice(obj, planes)
        if len(parts) < props.parts_count:
            report_user(self, 'WARNING', "Weniger Teile als erwartet erzeugt. Geometrie prüfen.")
        else:
            report_user(self, 'INFO', f"{len(parts)} Teile erzeugt.")

        # Pack parts into collection
        parts_coll = ensure_collection("_SnapSplit_Parts")
        for p in parts:
            # Keep existing links but ensure visible in parts coll
            if parts_coll not in p.users_collection:
                parts_coll.objects.link(p)

        return {'FINISHED'}

classes = (SNAP_OT_planar_split,)

def register():
    for c in classes:
        bpy.utils.register_class(c)

def unregister():
    for c in reversed(classes):
        bpy.utils.unregister_class(c)

