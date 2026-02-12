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
from bpy.props import (
    EnumProperty,
    FloatProperty,
    PointerProperty,
    IntProperty,
)
from bpy.types import PropertyGroup

from .utils import current_language, is_lang_de

# ---------------------------
# Material profiles (tolerance per side, in mm)
# ---------------------------

MATERIAL_PROFILES = {
    "PLA": 0.20,
    "PETG": 0.30,
    "ABS": 0.25,
    "ASA": 0.25,
    "TPU": 0.35,
    "SLA": 0.10,
}

def _mat_item_desc(key: str, val: float) -> str:
    """Localized tooltip for material items."""
    if is_lang_de():
        return f"Empfohlene Toleranz pro Seite: {val:.2f} mm"
    return f"Recommended tolerance per side: {val:.2f} mm"

# Build items list dynamically so the tooltip localizes at runtime
def _material_items():
    return [(k, k, _mat_item_desc(k, v)) for k, v in MATERIAL_PROFILES.items()]

# ---------------------------
# Property group
# ---------------------------

class SnapSplitProps(PropertyGroup):
    # Segmentation
    parts_count: IntProperty(
        name="Number of Parts" if not is_lang_de() else "Anzahl Teile",
        default=2,
        min=2,
        max=12,
        description=("Number of desired segments"
                     if not is_lang_de() else "Anzahl gewünschter Segmente"),
    )
    split_axis: EnumProperty(
        name="Split Axis" if not is_lang_de() else "Schnittachse",
        items=[
            ("X", "X", "Split along X" if not is_lang_de() else "Entlang X schneiden"),
            ("Y", "Y", "Split along Y" if not is_lang_de() else "Entlang Y schneiden"),
            ("Z", "Z", "Split along Z" if not is_lang_de() else "Entlang Z schneiden"),
        ],
        default="Z",
    )

    # Connector type and distribution
    connector_type: EnumProperty(
        name="Connector Type" if not is_lang_de() else "Verbinder-Typ",
        items=[
            ("CYL_PIN",
             "Cylinder Pin" if not is_lang_de() else "Zylinder-Pin",
             "Dowel pin + socket" if not is_lang_de() else "Holzdübel + Buchse"),
            ("RECT_TENON",
             "Rectangular Tenon" if not is_lang_de() else "Rechteck-Zapfen",
             "Anti-rotation joint" if not is_lang_de() else "Verdrehsicherer Zapfen"),
        ],
        default="CYL_PIN",
    )
    connector_distribution: EnumProperty(
        name="Distribution" if not is_lang_de() else "Verteilung",
        description=("Distribute connectors along a line or grid across the seam face"
                     if not is_lang_de() else "Verbinder entlang einer Linie oder als Raster über die Nahtfläche verteilen"),
        items=[
            ("LINE",
             "Line" if not is_lang_de() else "Linie",
             "Place connectors along a line in the seam face"
             if not is_lang_de() else "Verbinder entlang einer Linie in der Nahtfläche platzieren"),
            ("GRID",
             "Grid" if not is_lang_de() else "Raster",
             "Distribute connectors in a grid over the seam face"
             if not is_lang_de() else "Verbinder als Raster über die Nahtfläche verteilen"),
        ],
        default="LINE",
    )
    connectors_per_seam: IntProperty(
        name="Connectors per Seam" if not is_lang_de() else "Verbinder pro Naht",
        default=3,
        min=1,
        max=64,
    )
    connectors_rows: IntProperty(
        name="Rows (GRID)" if not is_lang_de() else "Reihen (RASTER)",
        description=("Number of rows in grid distribution"
                     if not is_lang_de() else "Anzahl der Reihen bei Raster-Verteilung"),
        default=2,
        min=1,
        max=64,
    )

    # Pin / Tenon dimensions (mm)
    pin_diameter_mm: FloatProperty(
        name="Pin Diameter (mm)" if not is_lang_de() else "Pin-Durchmesser (mm)",
        default=5.0,
        min=0.5,
        soft_max=50.0,
    )
    pin_length_mm: FloatProperty(
        name="Pin Length (mm)" if not is_lang_de() else "Pin-Länge (mm)",
        default=8.0,
        min=1.0,
        soft_max=200.0,
    )
    tenon_width_mm: FloatProperty(
        name="Tenon Width (mm)" if not is_lang_de() else "Zapfen-Breite (mm)",
        default=6.0,
        min=1.0,
        soft_max=100.0,
    )
    tenon_depth_mm: FloatProperty(
        name="Tenon Depth (mm)" if not is_lang_de() else "Zapfen-Tiefe (mm)",
        default=8.0,
        min=1.0,
        soft_max=200.0,
    )
    add_chamfer_mm: FloatProperty(
        name="Chamfer (mm)" if not is_lang_de() else "Fase (mm)",
        default=0.3,
        min=0.0,
        soft_max=2.0,
    )

    # Insert depth
    pin_embed_pct: FloatProperty(
        name="Insert Depth (%)" if not is_lang_de() else "Einstecktiefe (%)",
        description=("Percentage of connector length recessed into part A"
                     if not is_lang_de() else "Prozentualer Anteil der Verbinderlänge, die in Teil A steckt"),
        default=50.0,
        min=0.0,
        max=100.0,
        subtype='PERCENTAGE'
    )

    # Distribution margin
    connector_margin_pct: FloatProperty(
        name="Margin (%)" if not is_lang_de() else "Randabstand (%)",
        description=("Edge margin along the seam (and perpendicular in GRID) as percentage of part length (0–40% recommended)"
                     if not is_lang_de() else "Randabstand entlang der Naht (und senkrecht im Raster) als Prozent der Bauteillänge (0–40% empfohlen)"),
        default=10.0,
        min=0.0,
        soft_max=40.0,
        subtype='PERCENTAGE'
    )

    # Tolerances / material profile
    material_profile: EnumProperty(
        name="Material Profiles" if not is_lang_de() else "Material-Profile",
        items=_material_items(),   # localized tooltips
        default="PLA",
        description=("Select a material profile to auto-fill tolerance per side"
                     if not is_lang_de() else "Materialprofil wählen, um die Toleranz pro Seite zu setzen"),
    )
    tol_override: FloatProperty(
        name="Tolerance per Face (mm)" if not is_lang_de() else "Toleranz pro Fläche (mm)",
        description=("Overrides material profile (0 = use profile value)"
                     if not is_lang_de() else "Überschreibt das Materialprofil (0 = Profilwert verwenden)"),
        default=0.0,
        min=0.0,
        soft_max=0.6,
    )

    # Effective tolerance (mm, per side)
    def effective_tolerance(self) -> float:
        prof = MATERIAL_PROFILES.get(self.material_profile, 0.2)
        return prof if self.tol_override <= 0.0 else self.tol_override

# ---------------------------
# Registration
# ---------------------------

classes = (SnapSplitProps,)

def register():
    for c in classes:
        bpy.utils.register_class(c)
    bpy.types.Scene.snapsplit = PointerProperty(type=SnapSplitProps)

def unregister():
    if hasattr(bpy.types.Scene, "snapsplit"):
        del bpy.types.Scene.snapsplit
    for c in reversed(classes):
        bpy.utils.unregister_class(c)
