import bpy
from bpy.props import EnumProperty, FloatProperty, PointerProperty
from bpy.types import PropertyGroup

MATERIAL_PROFILES = {
    "PLA": 0.20,   # mm per side
    "PETG": 0.30,
    "ABS": 0.25,
    "ASA": 0.25,
    "TPU": 0.35,
    "SLA": 0.10,
}

# Statische Items-Liste, damit default ein String sein darf
MATERIAL_ITEMS = [(k, k, f"Empf. Toleranz pro Seite: {v:.2f} mm") for k, v in MATERIAL_PROFILES.items()]

class SnapSplitProps(PropertyGroup):
    parts_count: bpy.props.IntProperty(
        name="Teileanzahl",
        default=2,
        min=2,
        max=12,
        description="Anzahl der gewünschten Segmente",
    )
    split_axis: bpy.props.EnumProperty(
        name="Schnittachse",
        items=[
            ("X", "X", "Entlang X teilen"),
            ("Y", "Y", "Entlang Y teilen"),
            ("Z", "Z", "Entlang Z teilen"),
        ],
        default="Z",
    )
    connector_type: bpy.props.EnumProperty(
        name="Verbindungsart",
        items=[
            ("CYL_PIN", "Zylinder-Pin", "Rundstift + Buchse"),
            ("RECT_TENON", "Rechteck-Zapfen", "Anti-Verdreh-Verbindung"),
        ],
        default="CYL_PIN",
    )
    material_profile: bpy.props.EnumProperty(
        name="Materialprofil",
        items=MATERIAL_ITEMS,   # statisch
        default="PLA",          # String ist jetzt erlaubt
    )
    tol_override: FloatProperty(
        name="Toleranz pro Seite (mm)",
        description="Übersteuert das Materialprofil (0 = Profilwert verwenden)",
        default=0.0,
        min=0.0,
        soft_max=0.6,
    )
    pin_diameter_mm: FloatProperty(
        name="Pin Ø (mm)",
        default=5.0,
        min=1.0,
        soft_max=20.0,
    )
    pin_length_mm: FloatProperty(
        name="Pin Länge (mm)",
        default=8.0,
        min=2.0,
        soft_max=60.0,
    )
    tenon_width_mm: FloatProperty(
        name="Zapfen Breite (mm)",
        default=6.0,
        min=1.0,
        soft_max=30.0,
    )
    connector_margin_pct: FloatProperty(
        name="Randabstand (%)",
        description="Randabstand entlang der Naht in Prozent der Teil-Länge (0–40 % empfohlen)",
        default=10.0,
        min=0.0,
        soft_max=40.0,
        subtype='PERCENTAGE'
    )
    tenon_depth_mm: FloatProperty(
        name="Zapfen Tiefe (mm)",
        default=8.0,
        min=2.0,
        soft_max=60.0,
    )
    connectors_per_seam: bpy.props.IntProperty(
        name="Verbinder je Naht",
        default=3,
        min=1,
        max=12,
    )
    add_chamfer_mm: FloatProperty(
        name="Fase (mm)",
        default=0.3,
        min=0.0,
        soft_max=1.0,
    )

    def effective_tolerance(self):
        prof = MATERIAL_PROFILES.get(self.material_profile, 0.2)
        return prof if self.tol_override <= 0.0 else self.tol_override

classes = (SnapSplitProps,)

def register():
    for c in classes:
        bpy.utils.register_class(c)
    bpy.types.Scene.snapsplit = bpy.props.PointerProperty(type=SnapSplitProps)

def unregister():
    if hasattr(bpy.types.Scene, "snapsplit"):
        del bpy.types.Scene.snapsplit
    for c in reversed(classes):
        bpy.utils.unregister_class(c)
