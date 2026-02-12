import bpy
from bpy.types import Panel
from .profiles import MATERIAL_PROFILES

class SNAP_PT_panel(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "SnapSplit"
    bl_label = "SnapSplit"

    @classmethod
    def poll(cls, context):
        return context is not None and context.scene is not None

    def draw(self, context):
        layout = self.layout
        props = getattr(context.scene, "snapsplit", None)
        if props is None:
            layout.label(text="SnapSplit Properties nicht verfügbar.", icon="ERROR")
            layout.label(text="Bitte Add-on neu aktivieren.")
            return

        col = layout.column(align=True)
        col.label(text="Segmentierung")
        col.prop(props, "parts_count")
        col.prop(props, "split_axis")
        col.operator("snapsplit.planar_split", icon="MOD_BOOLEAN")

        layout.separator()

        col = layout.column(align=True)
        col.label(text="Verbindungen")
        col.prop(props, "connector_type")
        col.prop(props, "connectors_per_seam")
        col.prop(props, "connector_margin_pct")  # NEU: Randabstand in %

        box = col.box()
        if props.connector_type == "CYL_PIN":
            box.prop(props, "pin_diameter_mm")
            box.prop(props, "pin_length_mm")
        else:
            box.prop(props, "tenon_width_mm")
            box.prop(props, "tenon_depth_mm")
        box.prop(props, "add_chamfer_mm")

        layout.separator()
        col = layout.column(align=True)
        col.label(text="Toleranzen")
        col.prop(props, "material_profile")
        row = col.row(align=True)
        row.prop(props, "tol_override")
        row.label(text=f"Profil: {MATERIAL_PROFILES.get(props.material_profile, 0.2):.2f} mm")

        layout.separator()
        col = layout.column(align=True)
        col.operator("snapsplit.add_connectors", icon="SNAP_FACE")

def register():
    bpy.utils.register_class(SNAP_PT_panel)

def unregister():
    bpy.utils.unregister_class(SNAP_PT_panel)
