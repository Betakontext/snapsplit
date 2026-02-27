"""
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
along with this program; if not, see <https://www.gnu.org/licenses>.
"""

import math
import bpy
from bpy.props import (
    EnumProperty,
    FloatProperty,
    PointerProperty,
    IntProperty,
    BoolProperty,
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

def _snapsplit_update_preview(self, context):
    """Property update callback to refresh or clear split preview planes."""
    try:
        from . import ops_split
        ops_split.update_split_preview_plane(context)
    except Exception:
        pass

def _is_de():
    """Return True if current UI language is German (best-effort)."""
    try:
        return current_language().lower().startswith("de")
    except Exception:
        return is_lang_de()

def _suggest_pin_segments_from_diameter(d_mm: float) -> int:
    """
    Return a heuristic segment count for cylindrical pins from diameter in mm.
    Aims for visually round pins suitable for 3D printing without heavy meshes.
    """
    if d_mm <= 0:
        return 16
    # Proportional to circumference; adjust divisor to taste
    base = int(round(math.pi * d_mm / 1.8))
    # Practical clamps
    lo, hi = 12, 64
    if d_mm < 3.0:
        lo = 16  # very small pins still need enough segments to avoid visible flats
    return max(lo, min(hi, base))

def _mat_item_desc(key: str, val: float) -> str:
    """Build a localized tooltip text for a material profile entry."""
    if _is_de():
        return f"Recommended tolerance per side: {val:.2f} mm"
    return f"Recommended tolerance per side: {val:.2f} mm"

def _material_items():
    """Return EnumProperty items for material profiles with localized tooltips."""
    return [(k, k, _mat_item_desc(k, v)) for k, v in MATERIAL_PROFILES.items()]

# ---------------------------
# Property group
# ---------------------------

class SnapSplitProps(PropertyGroup):
    """Scene-level settings for segmentation, preview, connectors, and tolerances."""
    _DE = _is_de()

    # Split / Preview
    split_offset_mm: FloatProperty(
        name="Split Offset (mm)" if not _DE else "Schnitt-Offset (mm)",
        description=("Offset of the cutting plane along the split axis (positive in axis direction)"
                     if not _DE else "Verschiebung der Schnittebene entlang der Achse (positiv in Achsrichtung)"),
        default=0.0,
        soft_min=-100000.0,
        soft_max=100000.0,
        update=_snapsplit_update_preview,
    )

    split_axis: EnumProperty(
        name="Split Axis" if not _DE else "Schnittachse",
        items=[
            ("X", "X", "Split along X" if not _DE else "Entlang X schneiden"),
            ("Y", "Y", "Split along Y" if not _DE else "Entlang Y schneiden"),
            ("Z", "Z", "Split along Z" if not _DE else "Entlang Z schneiden"),
        ],
        default="Z",
        update=_snapsplit_update_preview,
    )

    show_split_preview: BoolProperty(
        name="Show split preview" if not _DE else "Schnittvorschau anzeigen",
        description=("Show temporary orange planes at planned cut positions"
                     if not _DE else "Temporäre orange Ebenen als geplante Schnittpositionen anzeigen"),
        default=False,
        update=_snapsplit_update_preview,
    )

    parts_count: IntProperty(
        name="Number of Parts" if not _DE else "Anzahl Teile",
        default=2,
        min=2,
        max=64,
        description=("Number of desired segments (cut planes = parts - 1)"
                     if not _DE else "Anzahl gewünschter Segmente (Schnittebenen = Teile - 1)"),
        update=_snapsplit_update_preview,
    )

    # Performance/Workflow: Cap seams automatically during split
    cap_seams_during_split: BoolProperty(
        name="Cap seams during split" if not _DE else "Nähte beim Schnitt schließen",
        description=("Automatically close seams after splitting. With hollow/inner shell: precise outer/inner loop fill; without hollow: simple fill. May increase runtime."
                     if not _DE else "Wendet nach dem Schnitt automatisch den Randverschluss an. Mit Hollow/Innenhülle: präzise Außen/Innen-Loop-Füllung; ohne Hollow: einfache Füllung. Kann die Laufzeit erhöhen."),
        default=True,
    )

    # Connectors
    connector_type: EnumProperty(
        name="Connector Type" if not _DE else "Verbinder-Typ",
        items=[
            ("CYL_PIN",
             "Cylinder Pin" if not _DE else "Zylinder-Pin",
             "Dowel pin + socket" if not _DE else "Holzdübel + Buchse"),
            ("RECT_TENON",
             "Rectangular Tenon" if not _DE else "Rechteck-Zapfen",
             "Anti-rotation joint" if not _DE else "Verdrehsicherer Zapfen"),
            ("SNAP_PIN",
             "Snap Pin" if not _DE else "Snap-Pin",
             "Connector with snap spheres" if not _DE else "Zylinder-/Zapfen-Verbinder mit Schnappnoppen"),
            ("SNAP_TENON",
             "Snap Tenon" if not _DE else "Snap-Zapfen",
             "Rectangular tenon with snap spheres" if not _DE else "Rechteckiger Zapfen mit Schnapp-Sphären"),
        ],
        default="CYL_PIN",
    )

    # Placement distribution
    connector_distribution: EnumProperty(
        name="Distribution" if not _DE else "Verteilung",
        description=("Distribute connectors along a line or a grid across the seam face"
                     if not _DE else "Verbinder entlang einer Linie oder als Raster über die Nahtfläche verteilen"),
        items=[
            ("LINE",
             "Line" if not _DE else "Linie",
             "Place connectors along a line in the seam face"
             if not _DE else "Verbinder entlang einer Linie in der Nahtfläche platzieren"),
            ("GRID",
             "Grid" if not _DE else "Raster",
             "Distribute connectors in a grid over the seam face"
             if not _DE else "Verbinder als Raster über die Nahtfläche verteilen"),
        ],
        default="LINE",
    )

    connectors_per_seam: IntProperty(
        name="Connectors per Seam" if not _DE else "Verbinder pro Naht",
        default=3,
        min=1,
        max=128,
    )

    connectors_rows: IntProperty(
        name="Rows (GRID)" if not _DE else "Reihen (RASTER)",
        description=("Number of rows for grid distribution"
                     if not _DE else "Anzahl der Reihen bei Raster-Verteilung"),
        default=2,
        min=1,
        max=128,
    )

    connector_margin_pct: FloatProperty(
        name="Margin (%)" if not _DE else "Randabstand (%)",
        description=("Edge margin along the seam (and perpendicular in GRID) as percentage of part length (0–40% recommended)"
                     if not _DE else "Randabstand entlang der Naht (und senkrecht im Raster) als Prozent der Bauteillänge (0–40% empfohlen)"),
        default=10.0,
        min=0.0,
        soft_max=40.0,
        subtype='PERCENTAGE'
    )

    # Snap options (active when connector_type == 'SNAP_PIN')
    snap_spheres_per_side: IntProperty(
        name="Spheres per side" if not _DE else "Sphären je Seite",
        description=("Number of snap spheres per side/around"
                     if not _DE else "Anzahl der Schnapp-Sphären je Seitenfläche/Umfang"),
        default=2,
        min=1,
        max=32,
    )

    snap_sphere_diameter_mm: FloatProperty(
        name="Sphere Ø (mm)" if not _DE else "Sphären-Ø (mm)",
        description=("Diameter of snap spheres"
                     if not _DE else "Durchmesser der Schnapp-Sphären"),
        default=2.0,
        min=0.5,
        soft_max=10.0,
    )

    snap_sphere_protrusion_mm: FloatProperty(
        name="Protrusion (mm)" if not _DE else "Überstand (mm)",
        description=("How far spheres protrude from side surface"
                     if not _DE else "Wie weit die Sphären aus der Seitenfläche herausstehen"),
        default=1.0,
        min=0.0,
        soft_max=5.0,
    )

    # Pin / Tenon dimensions (mm)
    pin_diameter_mm: FloatProperty(
        name="Pin Diameter (mm)" if not _DE else "Pin-Durchmesser (mm)",
        default=5.0,
        min=0.5,
        soft_max=50.0,
    )

    pin_length_mm: FloatProperty(
        name="Pin Length (mm)" if not _DE else "Pin-Länge (mm)",
        default=8.0,
        min=1.0,
        soft_max=200.0,
    )

    pin_segments: IntProperty(
        name="Segments" if not _DE else "Segmente",
        description=("Cylinder pin radial segments (visual smoothness)"
                     if not _DE else "Kreissegmente des Pins (nur Optik/Glätte)"),
        default=32,
        min=8,
        max=128,
    )

    tenon_width_mm: FloatProperty(
        name="Tenon Width (mm)" if not _DE else "Zapfen-Breite (mm)",
        default=6.0,
        min=1.0,
        soft_max=100.0,
    )

    tenon_depth_mm: FloatProperty(
        name="Tenon Depth (mm)" if not _DE else "Zapfen-Tiefe (mm)",
        default=8.0,
        min=1.0,
        soft_max=200.0,
    )

    add_chamfer_mm: FloatProperty(
        name="Chamfer (mm)" if not _DE else "Fase (mm)",
        default=0.3,
        min=0.0,
        soft_max=2.0,
    )

    # Insert depth
    pin_embed_pct: FloatProperty(
        name="Insert Depth (%)" if not _DE else "Einstecktiefe (%)",
        description=("Percentage of connector length recessed into part A"
                     if not _DE else "Prozentualer Anteil der Verbinderlänge, die in Teil A steckt"),
        default=50.0,
        min=0.0,
        max=100.0,
        subtype='PERCENTAGE'
    )

    # Distribution margin (duplicate kept if intentionally needed elsewhere)
    connector_margin_pct: FloatProperty(
        name="Margin (%)" if not _DE else "Randabstand (%)",
        description=("Edge margin along the seam (and perpendicular in GRID) as percentage of part length (0–40% recommended)"
                     if not _DE else "Randabstand entlang der Naht (und senkrecht im Raster) als Prozent der Bauteillänge (0–40% empfohlen)"),
        default=10.0,
        min=0.0,
        soft_max=40.0,
        subtype='PERCENTAGE'
    )

    # Tolerances / material profile
    material_profile: EnumProperty(
        name="Material Profiles" if not _DE else "Material-Profile",
        items=_material_items(),
        default="PLA",
        description=("Select a material profile to auto-fill tolerance per side"
                     if not _DE else "Materialprofil wählen, um die Toleranz pro Seite zu setzen"),
    )

    tol_override: FloatProperty(
        name="Tolerance per Face (mm)" if not _DE else "Toleranz pro Fläche (mm)",
        description=("Overrides material profile (0 = use profile value)"
                     if not _DE else "Überschreibt das Materialprofil (0 = Profilwert verwenden)"),
        default=0.0,
        min=0.0,
        soft_max=0.6,
    )

    def effective_tolerance(self) -> float:
        """Return the active tolerance per side, considering the override if set."""
        prof = MATERIAL_PROFILES.get(self.material_profile, 0.2)
        return prof if self.tol_override <= 0.0 else self.tol_override

    # UI foldouts
    ui_more_seg: BoolProperty(
        name="More segmentation settings",
        description="Show advanced segmentation options",
        default=False
    )

    ui_more_conn: BoolProperty(
        name="More connection settings",
        description="Show advanced connection/geometry options",
        default=False
    )

    ui_more_tol: BoolProperty(
        name="More tolerance settings",
        description="Show advanced tolerance options",
        default=False
    )

# ---------------------------
# Registration
# ---------------------------

classes = (SnapSplitProps,)

def register():
    """Register property classes and attach to bpy.types.Scene."""
    for c in classes:
        bpy.utils.register_class(c)
    bpy.types.Scene.snapsplit = PointerProperty(type=SnapSplitProps)

def unregister():
    """Unregister property classes and detach from bpy.types.Scene."""
    if hasattr(bpy.types.Scene, "snapsplit"):
        del bpy.types.Scene.snapsplit
    for c in reversed(classes):
        bpy.utils.unregister_class(c)
