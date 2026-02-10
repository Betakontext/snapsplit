import bpy
from bpy.types import Operator
from mathutils import Vector, Matrix
from .utils import ensure_collection, obj_world_bb, report_user

def create_cut_planes(obj, axis, parts_count):
    # Create (parts_count - 1) planes positioned within object bounds
    min_v, max_v = obj_world_bb(obj)
    axis_index = {"X": 0, "Y": 1, "Z": 2}[axis]
    length = max_v[axis_index] - min_v[axis_index]
    if length <= 0.0 or parts_count < 2:
        return []

    planes = []
    for i in range(1, parts_count):
        t = i / parts_count
        pos = min_v[axis_index] + t * length

        bpy.ops.mesh.primitive_plane_add(size=1.0, enter_editmode=False)
        plane = bpy.context.active_object
        plane.name = f"SnapSplit_Plane_{axis}_{i}"

        # großzügig skalieren, nur als visueller Marker
        plane.scale = (length * 2.0, length * 2.0, 1.0)

        # Orientierung und Position der Ebene
        if axis == "X":
            plane.rotation_euler = (0.0, 1.5708, 0.0)  # 90° um Y -> Normal entlang +X
            plane.location.x = pos
        elif axis == "Y":
            plane.rotation_euler = (1.5708, 0.0, 0.0)  # 90° um X -> Normal entlang +Y
            plane.location.y = pos
        else:  # Z
            # Standard-Plane liegt in XY, Normal entlang +Z
            plane.location.z = pos

        planes.append(plane)

    return planes

def bisect_separate_on_plane(obj, plane_obj):
    # Zielobjekt aktivieren und Transforms anwenden
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj
    try:
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
    except Exception:
        pass

    # Ebene von Plane (Welt) in Objektraum des Zielobjekts umrechnen
    plane_no_world = (plane_obj.matrix_world.to_3x3() @ Vector((0, 0, 1))).normalized()
    plane_co_world = plane_obj.matrix_world @ Vector((0, 0, 0))
    M = obj.matrix_world
    M_inv = M.inverted()
    plane_co_obj = M_inv @ plane_co_world
    plane_no_obj = (M_inv.to_3x3().transposed() @ plane_no_world).normalized()

    # In Edit Mode wechseln
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')

    # Bisect ausführen: Füllfläche erzeugen, nichts löschen
    res = bpy.ops.mesh.bisect(
        plane_co=(plane_co_obj.x, plane_co_obj.y, plane_co_obj.z),
        plane_no=(plane_no_obj.x, plane_no_obj.y, plane_no_obj.z),
        use_fill=True,
        clear_inner=False,
        clear_outer=False
    )

    # Jetzt in lose Teile separieren
    try:
        bpy.ops.mesh.separate(type='LOOSE')
    except Exception:
        # Falls keine getrennten Inseln vorliegen, kommt hier ggf. ein Fehler
        pass

    # Zurück in Object Mode
    bpy.ops.object.mode_set(mode='OBJECT')

    # Einsammeln: alle aktuellen Auswahlobjekte, die Meshes sind und nicht das Original
    new_parts = [o for o in bpy.context.selected_objects if o.type == 'MESH' and o != obj]

    # Wenn Blender nach Separate nicht automatisch selektiert:
    # Wir prüfen über die Collections, was neu hinzugekommen ist.
    if not new_parts:
        # Heuristik: Finde alle Objekte, die dieselbe Mesh-Daten-Quelle teilen wie obj, aber nicht obj selbst
        # (nach Separate werden neue Mesh-Daten erzeugt; diese Heuristik greift nur schwach)
        pass  # belassen; Rückfall unten

    # Wenn keine neuen Teile entstanden sind, Original zurückgeben
    if not new_parts:
        return [obj]

    # Transforms anwenden und Original optional ausblenden
    for o in new_parts:
        bpy.context.view_layer.objects.active = o
        o.select_set(True)
        try:
            bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
        except Exception:
            pass
        o.select_set(False)

    obj.hide_set(True)
    return new_parts

def planar_split_sequence(obj, planes):
    current_parts = [obj]

    for plane in planes:
        next_parts = []
        for p in current_parts:
            parts = bisect_separate_on_plane(p, plane)
            # Wenn keine echten neuen Teile, p behalten
            if parts and (len(parts) >= 2 or parts[0] is not p):
                next_parts.extend(parts)
            else:
                next_parts.append(p)
        current_parts = next_parts

        # Plane in Cutter-Collection verschieben
        cutters_coll = ensure_collection("_SnapSplit_Cutters")
        try:
            for col in plane.users_collection:
                col.objects.unlink(plane)
        except Exception:
            pass
        cutters_coll.objects.link(plane)

    # Valide Meshes filtern
    valid = []
    for p in current_parts:
        if p and p.type == 'MESH' and p.data and len(p.data.polygons) > 0:
            valid.append(p)
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
        axis = props.split_axis
        count = max(2, int(props.parts_count))

        # Schnittebenen an den gleichmäßigen Positionen der Bounding Box erzeugen
        planes = create_cut_planes(obj, axis, count)
        if not planes:
            report_user(self, 'ERROR', "Konnte keine Schnittflächen erzeugen.")
            return {'CANCELLED'}

        # Sequenzieller Bisect über alle Ebenen/Teile
        parts = planar_split_sequence(obj, planes)

        # Erwartet: mindestens 'count' Teile
        if len(parts) < count:
            report_user(self, 'WARNING', f"Weniger Teile als erwartet erzeugt ({len(parts)} < {count}). Geometrie prüfen.")
        else:
            report_user(self, 'INFO', f"{len(parts)} Teile erzeugt.")

        # Teile in Sammlung
        parts_coll = ensure_collection("_SnapSplit_Parts")
        for p in parts:
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
