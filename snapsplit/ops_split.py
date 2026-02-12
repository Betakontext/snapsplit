import bpy
import bmesh
from bpy.types import Operator
from mathutils import Vector
from .utils import ensure_collection, obj_world_bb, report_user

# ---------------------------
# BMesh-basierter Kernsplit
# ---------------------------

def split_mesh_bmesh_into_two(obj, plane_co_obj, plane_no_obj, name_suffix=""):
    """
    Teilt obj entlang einer Ebene (im Objektraum von obj).
    Erzeugt zwei neue Meshes: POS (behält Seite in Normalenrichtung) und NEG (Gegenseite).
    Gibt zwei neue Objekte zurück. Original wird ausgeblendet.
    """
    # Objekt aktivieren und Transforms anwenden (wichtig für stabile Maße)
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    try:
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    except Exception:
        pass

    def make_half(keep_positive: bool):
        bm = bmesh.new()
        bm.from_mesh(obj.data)
        geom = bm.verts[:] + bm.edges[:] + bm.faces[:]

        # Mesh entlang Ebene schneiden und je nach Hälfte Seite löschen
        bmesh.ops.bisect_plane(
            bm,
            geom=geom,
            plane_co=plane_co_obj,
            plane_no=plane_no_obj,
            use_snap_center=False,
            clear_outer=not keep_positive,   # löscht "negative" Seite relativ zur Normalen
            clear_inner=keep_positive        # löscht "positive" Seite
        )

        # Offene Schnittkanten schließen (Caps), damit Teile manifold sind
        boundary_edges = [e for e in bm.edges if e.is_boundary]
        if boundary_edges:
            try:
                bmesh.ops.holes_fill(bm, edges=boundary_edges, sides=0)
            except Exception:
                # Falls Füllen irgendwo scheitert, Mesh bleibt dennoch teilbar
                pass

        bm.normal_update()

        me = bpy.data.meshes.new(f"{obj.name}_{'POS' if keep_positive else 'NEG'}{name_suffix}")
        bm.to_mesh(me)
        bm.free()
        return me

    me_pos = make_half(True)
    me_neg = make_half(False)

    # Neue Objekte verlinken
    col = obj.users_collection[0] if obj.users_collection else bpy.context.scene.collection
    o1 = bpy.data.objects.new(f"{obj.name}_A{name_suffix}", me_pos)
    o2 = bpy.data.objects.new(f"{obj.name}_B{name_suffix}", me_neg)
    col.objects.link(o1)
    col.objects.link(o2)

    # Original ausblenden zur klaren Sicht
    obj.hide_set(True)

    # Daten validieren/aktualisieren
    for o in (o1, o2):
        try:
            o.data.validate(verbose=False)
            o.data.update()
        except Exception:
            pass

    return o1, o2

# ---------------------------
# Ebenendaten direkt aus BB
# ---------------------------

def create_cut_data(obj, axis, parts_count):
    """
    Liefert eine Liste von (co_world, no_world) Ebenen für gleichmäßige Schnitte
    entlang der Bounding-Box-Achse in Weltkoordinaten.
    """
    min_v, max_v = obj_world_bb(obj)
    axis_index = {"X": 0, "Y": 1, "Z": 2}[axis]
    length = max_v[axis_index] - min_v[axis_index]
    if length <= 0.0 or parts_count < 2:
        return []

    cuts = []
    for i in range(1, parts_count):
        t = i / parts_count
        pos_world = min_v[axis_index] + t * length
        if axis == "X":
            no_world = Vector((1, 0, 0))
            co_world = Vector((pos_world, 0, 0))
        elif axis == "Y":
            no_world = Vector((0, 1, 0))
            co_world = Vector((0, pos_world, 0))
        else:
            no_world = Vector((0, 0, 1))
            co_world = Vector((0, 0, pos_world))
        cuts.append((co_world, no_world))
    return cuts

def apply_bmesh_split_sequence(obj, axis, parts_count):
    """
    Führt nacheinander BMesh-basierte Splits anhand der Ebenen durch.
    Nach jedem Schnitt werden alle aktuell vorhandenen Teile weiter geschnitten.
    """
    cuts = create_cut_data(obj, axis, parts_count)
    if not cuts:
        return [obj]

    current_parts = [obj]

    for idx, (co_world, no_world) in enumerate(cuts, start=1):
        next_parts = []
        for p in current_parts:
            # Welt -> Objektraum dieses Teils
            M = p.matrix_world
            M_inv = M.inverted()
            co_obj = M_inv @ co_world
            no_obj = (M_inv.to_3x3().transposed() @ no_world).normalized()

            a, b = split_mesh_bmesh_into_two(p, co_obj, no_obj, name_suffix=f"_S{idx}")
            next_parts.extend([a, b])
        current_parts = next_parts

    # Valide Meshes zurückgeben
    valid = [o for o in current_parts if o.type == 'MESH' and o.data and len(o.data.polygons) > 0]
    return valid

# ---------------------------
# Operator
# ---------------------------

class SNAP_OT_planar_split(Operator):
    bl_idname = "snapsplit.planar_split"
    bl_label = "Planar Split"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = context.active_object
        if not obj or obj.type != 'MESH':
            report_user(self, 'ERROR', "Please select a Mesh-Objekt.")
            return {'CANCELLED'}

        props = context.scene.snapsplit
        axis = props.split_axis
        count = max(2, int(props.parts_count))

        parts = apply_bmesh_split_sequence(obj, axis, count)

        if len(parts) < count:
            report_user(self, 'WARNING', f"Less parts created as expected ({len(parts)} < {count}).")
        else:
            report_user(self, 'INFO', f"{len(parts)} parts created.")

        # In _SnapSplit_Parts sammeln und selektieren
        parts_coll = ensure_collection("_SnapSplit_Parts")
        bpy.ops.object.select_all(action='DESELECT')
        for p in parts:
            if parts_coll not in p.users_collection:
                parts_coll.objects.link(p)
            p.select_set(True)
        if parts:
            bpy.context.view_layer.objects.active = parts[0]

        return {'FINISHED'}

classes = (SNAP_OT_planar_split,)

def register():
    for c in classes:
        bpy.utils.register_class(c)

def unregister():
    for c in reversed(classes):
        bpy.utils.unregister_class(c)
