"""
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
along with this program; if not, see <https://www.gnu.org/licenses>.
"""

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

def _is_de():
    # Use current_language() explicitly; fall back to is_lang_de()
    try:
        return current_language().lower().startswith("de")
    except Exception:
        return is_lang_de()

def _mat_item_desc(key: str, val: float) -> str:
    """Localized tooltip for material items."""
    if _is_de():
        return f"Empfohlene Toleranz pro Seite: {val:.2f} mm"
    return f"Recommended tolerance per side: {val:.2f} mm"

# Build items list dynamically so the tooltip localizes at runtime
def _material_items():
    return [(k, k, _mat_item_desc(k, v)) for k, v in MATERIAL_PROFILES.items()]

# ---------------------------
# Property group
# ---------------------------

class SnapSplitProps(PropertyGroup):
    # Cache the language decision once at class creation time
    _DE = _is_de()

    # Segmentation
    parts_count: IntProperty(
        name="Anzahl Teile" if _DE else "Number of Parts",
        default=2,
        min=2,
        max=12,
        description=("Anzahl gewünschter Segmente" if _DE else "Number of desired segments"),
    )
    split_axis: EnumProperty(
        name="Schnittachse" if _DE else "Split Axis",
        items=[
            ("X", "X", "Entlang X schneiden" if _DE else "Split along X"),
            ("Y", "Y", "Entlang Y schneiden" if _DE else "Split along Y"),
            ("Z", "Z", "Entlang Z schneiden" if _DE else "Split along Z"),
        ],
        default="Z",
    )

    # Connector type and distribution
    connector_type: EnumProperty(
        name="Verbinder-Typ" if _DE else "Connector Type",
        items=[
            ("CYL_PIN",
             "Zylinder-Pin" if _DE else "Cylinder Pin",
             "Holzdübel + Buchse" if _DE else "Dowel pin + socket"),
            ("RECT_TENON",
             "Rechteck-Zapfen" if _DE else "Rectangular Tenon",
             "Verdrehsicherer Zapfen" if _DE else "Anti-rotation joint"),
        ],
        default="CYL_PIN",
    )
    connector_distribution: EnumProperty(
        name="Verteilung" if _DE else "Distribution",
        description=("Verbinder entlang einer Linie oder als Raster über die Nahtfläche verteilen"
                     if _DE else "Distribute connectors along a line or grid across the seam face"),
        items=[
            ("LINE",
             "Linie" if _DE else "Line",
             "Verbinder entlang einer Linie in der Nahtfläche platzieren"
             if _DE else "Place connectors along a line in the seam face"),
            ("GRID",
             "Raster" if _DE else "Grid",
             "Verbinder als Raster über die Nahtfläche verteilen"
             if _DE else "Distribute connectors in a grid over the seam face"),
        ],
        default="LINE",
    )
    connectors_per_seam: IntProperty(
        name="Verbinder pro Naht" if _DE else "Connectors per Seam",
        default=3,
        min=1,
        max=64,
    )
    connectors_rows: IntProperty(
        name="Reihen (RASTER)" if _DE else "Rows (GRID)",
        description=("Anzahl der Reihen bei Raster-Verteilung"
                     if _DE else "Number of rows in grid distribution"),
        default=2,
        min=1,
        max=64,
    )

    # Pin / Tenon dimensions (mm)
    pin_diameter_mm: FloatProperty(
        name="Pin-Durchmesser (mm)" if _DE else "Pin Diameter (mm)",
        default=5.0,
        min=0.5,
        soft_max=50.0,
    )
    pin_length_mm: FloatProperty(
        name="Pin-Länge (mm)" if _DE else "Pin Length (mm)",
        default=8.0,
        min=1.0,
        soft_max=200.0,
    )
    tenon_width_mm: FloatProperty(
        name="Zapfen-Breite (mm)" if _DE else "Tenon Width (mm)",
        default=6.0,
        min=1.0,
        soft_max=100.0,
    )
    tenon_depth_mm: FloatProperty(
        name="Zapfen-Tiefe (mm)" if _DE else "Tenon Depth (mm)",
        default=8.0,
        min=1.0,
        soft_max=200.0,
    )
    add_chamfer_mm: FloatProperty(
        name="Fase (mm)" if _DE else "Chamfer (mm)",
        default=0.3,
        min=0.0,
        soft_max=2.0,
    )

    # Insert depth
    pin_embed_pct: FloatProperty(
        name="Einstecktiefe (%)" if _DE else "Insert Depth (%)",
        description=("Prozentualer Anteil der Verbinderlänge, die in Teil A steckt"
                     if _DE else "Percentage of connector length recessed into part A"),
        default=50.0,
        min=0.0,
        max=100.0,
        subtype='PERCENTAGE'
    )

    # Distribution margin
    connector_margin_pct: FloatProperty(
        name="Randabstand (%)" if _DE else "Margin (%)",
        description=("Randabstand entlang der Naht (und senkrecht im Raster) als Prozent der Bauteillänge (0–40% empfohlen)"
                     if _DE else "Edge margin along the seam (and perpendicular in GRID) as percentage of part length (0–40% recommended)"),
        default=10.0,
        min=0.0,
        soft_max=40.0,
        subtype='PERCENTAGE'
    )

    # Tolerances / material profile
    material_profile: EnumProperty(
        name="Material-Profile" if _DE else "Material Profiles",
        items=_material_items(),   # localized tooltips
        default="PLA",
        description=("Materialprofil wählen, um die Toleranz pro Seite zu setzen"
                     if _DE else "Select a material profile to auto-fill tolerance per side"),
    )
    tol_override: FloatProperty(
        name="Toleranz pro Fläche (mm)" if _DE else "Tolerance per Face (mm)",
        description=("Überschreibt das Materialprofil (0 = Profilwert verwenden)"
                     if _DE else "Overrides material profile (0 = use profile value)"),
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
