# profiles.py
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
    "PLA": 0.25,
    "PETG": 0.30,
    "ABS": 0.25,
    "ASA": 0.25,
    "TPU": 0.35,
    "SLA": 0.10,
}

# Snap-sphere presets by (material, friction)
SNAP_SPHERE_PRESETS = {
    ("PLA", "tight"):   (2.4, 0.25),
    ("PLA", "medium"):  (2.0, 0.20),
    ("PLA", "loose"):   (1.6, 0.15),

    ("PETG", "tight"):  (2.0, 0.20),
    ("PETG", "medium"): (1.8, 0.18),
    ("PETG", "loose"):  (1.6, 0.15),

    ("ABS", "tight"):   (2.2, 0.22),
    ("ABS", "medium"):  (2.0, 0.20),
    ("ABS", "loose"):   (1.8, 0.17),

    ("ASA", "tight"):   (2.2, 0.22),
    ("ASA", "medium"):  (2.0, 0.20),
    ("ASA", "loose"):   (1.8, 0.17),

    ("TPU", "tight"):   (2.8, 0.30),
    ("TPU", "medium"):  (2.4, 0.25),
    ("TPU", "loose"):   (2.0, 0.20),

    ("SLA", "tight"):   (1.6, 0.12),
    ("SLA", "medium"):  (1.4, 0.10),
    ("SLA", "loose"):   (1.2, 0.08),
}

def _snapsplit_update_preview(self, context):
    """Lightweight: invokes the preview update; do not write back to props here."""
    try:
        from . import ops_split
        ops_split.update_split_preview_plane(context)
    except Exception:
        pass

def _is_de():
    try:
        return current_language().lower().startswith("de")
    except Exception:
        return is_lang_de()

def _suggest_pin_segments_from_diameter(d_mm: float) -> int:
    """Heuristic for cylinder resolution by diameter."""
    if d_mm <= 0:
        return 16
    base = int(round(math.pi * d_mm / 1.8))
    lo, hi = 12, 64
    if d_mm < 3.0:
        lo = 16
    return max(lo, min(hi, base))

def _mat_item_desc(key: str, val: float) -> str:
    return f"Recommended tolerance per side: {val:.2f} mm"

def _material_items():
    return [(k, k, _mat_item_desc(k, v)) for k, v in MATERIAL_PROFILES.items()]

# ---------------------------
# Snap-sphere preset helpers
# ---------------------------

def _get_snap_sphere_preset(self):
    mat = getattr(self, "material_profile", "PETG")
    fr = getattr(self, "snap_friction_target", "medium")
    return SNAP_SPHERE_PRESETS.get((mat, fr), SNAP_SPHERE_PRESETS.get(("PETG","medium")))

def _apply_snap_sphere_preset(self):
    vals = _get_snap_sphere_preset(self)
    if not vals:
        return
    d, p = vals
    try:
        self.snap_sphere_diameter_mm = float(d)
        self.snap_sphere_protrusion_mm = float(p)
    except Exception:
        pass

# ---------------------------
# Property group
# ---------------------------

class SnapSplitProps(PropertyGroup):
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
        items=[("X","X",""),("Y","Y",""),("Z","Z","")],
        default="Z",
        update=_snapsplit_update_preview,
    )

    show_split_preview: BoolProperty(
        name="Show split preview" if not _DE else "Schnittvorschau anzeigen",
        default=False,
        update=_snapsplit_update_preview,
    )

    parts_count: IntProperty(
        name="Number of Parts" if not _DE else "Anzahl Teile",
        default=2, min=2, max=64,
        update=_snapsplit_update_preview,
    )

    cap_seams_during_split: BoolProperty(
        name="Cap seams during split" if not _DE else "Nähte beim Schnitt schließen",
        default=True,
    )

    # Connections
    connector_type: EnumProperty(
        name="Connector Type" if not _DE else "Verbinder-Typ",
        items=[
            ("CYL_PIN","Cylinder Pin" if not _DE else "Zylinder-Pin",""),
            ("RECT_TENON","Rectangular Tenon" if not _DE else "Rechteck-Zapfen",""),
            ("SNAP_PIN","Snap Pin" if not _DE else "Snap-Pin",""),
            ("SNAP_TENON","Snap Tenon" if not _DE else "Snap-Zapfen",""),
            ("PIN_HOLE","Pin & Hole" if not _DE else "Pin & Bohrung",""),
            ("DOVETAIL_TAPER","Dovetail (Tapered)" if not _DE else "Schwalbenschwanz (mit Schräge)",""),
            ("SNAP_CANTILEVER","Snap-Fit (Cantilever)" if not _DE else "Schnapphaken (Kragarm)",""),
            ("BALL_SOCKET","Ball & Socket" if not _DE else "Kugel & Schale",""),
            ("PIP_HINGE","Print-in-Place Hinge" if not _DE else "Druckbares Scharnier (PiP)",""),
        ],
        default="DOVETAIL_TAPER",
    )

    connector_distribution: EnumProperty(
        name="Distribution" if not _DE else "Verteilung",
        items=[("LINE","Line" if not _DE else "Linie",""),("GRID","Grid" if not _DE else "Raster","")],
        default="LINE",
    )

    connectors_per_seam: IntProperty(
        name="Connectors per Seam" if not _DE else "Verbinder pro Naht",
        default=1, min=1, max=128,
    )

    connectors_rows: IntProperty(
        name="Rows (GRID)" if not _DE else "Reihen (RASTER)",
        default=2, min=1, max=128,
    )

    connector_margin_pct: FloatProperty(
        name="Margin (%)" if not _DE else "Randabstand (%)",
        default=0.0, min=0.0, soft_max=40.0, subtype='PERCENTAGE'
    )
    edge_margin_mm: FloatProperty(
        name="Edge margin (mm)" if not _DE else "Randabstand (mm)",
        default=0.0, min=0.0, soft_max=20.0,
    )

    # Snap spheres (shared for SNAP_PIN & SNAP_TENON) – auto-updated by material+friction
    snap_spheres_per_side: IntProperty(
        name="Spheres per side" if not _DE else "Sphären je Seite",
        default=2, min=1, max=32,
    )
    snap_sphere_diameter_mm: FloatProperty(
        name="Sphere Ø (mm)" if not _DE else "Sphären-Ø (mm)",
        default=2.0, min=0.5, soft_max=10.0,
    )
    snap_sphere_protrusion_mm: FloatProperty(
        name="Protrusion (mm)" if not _DE else "Überstand (mm)",
        default=1.0, min=0.0, soft_max=5.0,
    )

    # Pins / Pin&Hole (Proportional master: pin_diameter_mm)
    pin_prop_enabled: BoolProperty(
        name="Proportional (Pins)" if _DE else "Proportional (Pins)",
        default=True,
    )

    def _update_pin_ratios_from_values(self):
        """Update internal pin ratios from current absolute values (when proportional is OFF)."""
        try:
            d = float(self.pin_diameter_mm)
            if d > 1e-9:
                self.pin_ratio_len = max(0.01, float(self.pin_length_mm) / d)
                self.pin_ratio_chamfer = max(0.0, float(self.add_chamfer_mm) / d)
        except Exception:
            pass

    def _on_pin_diameter_changed(self, context):
        """When proportional is ON, drive dependents from diameter; otherwise, learn ratios."""
        if not getattr(self, "pin_prop_enabled", True):
            self._update_pin_ratios_from_values()
            return
        try:
            d = float(self.pin_diameter_mm)
            self.pin_length_mm = max(0.5, d * float(self.pin_ratio_len))
            self.add_chamfer_mm = max(0.0, d * float(self.pin_ratio_chamfer))
        except Exception:
            pass

    def _on_pin_dependents_changed(self, context):
        """Learn ratios from edited dependents when proportional is OFF."""
        self._update_pin_ratios_from_values()

    pin_diameter_mm: FloatProperty(
        name="Pin Diameter (mm)" if not _DE else "Pin-Durchmesser (mm)",
        default=5.0, min=0.5, soft_max=50.0,
        update=_on_pin_diameter_changed,
    )
    pin_length_mm: FloatProperty(
        name="Pin Length (mm)" if not _DE else "Pin-Länge (mm)",
        default=8.0, min=1.0, soft_max=200.0,
        update=_on_pin_dependents_changed,
    )
    pin_segments: IntProperty(
        name="Segments" if not _DE else "Segmente",
        default=32, min=8, max=128,
    )
    add_chamfer_mm: FloatProperty(
        name="Chamfer (mm)" if not _DE else "Fase (mm)",
        default=0.30, min=0.0, soft_max=2.0,
        update=_on_pin_dependents_changed,
    )

    pin_fit_mode: EnumProperty(
        name="Fit mode" if not _DE else "Passung",
        items=[
            ("snug", "Snug" if not _DE else "Stramm",""),
            ("sliding", "Sliding" if not _DE else "Leichtgängig",""),
            ("glue_ready", "Glue-ready" if not _DE else "Klebe-Bereit",""),
        ],
        default="snug",
    )
    pin_hole_only: BoolProperty(
        name="Hole only (for metal pins)" if not _DE else "Nur Bohrung (für Metallstifte)",
        default=False,
    )

    pin_embed_pct: FloatProperty(
        name="Insert Depth (%)" if not _DE else "Einstecktiefe (%)",
        default=50.0, min=0.0, max=100.0, subtype='PERCENTAGE'
    )

    pin_ratio_len: FloatProperty(name="k_pin_len", default=1.6, min=0.01, soft_max=10.0, options={'HIDDEN'})
    pin_ratio_chamfer: FloatProperty(name="k_pin_ch", default=0.06, min=0.0, soft_max=0.5, options={'HIDDEN'})

    # Tenon (Master: tenon_width_mm)
    tenon_prop_enabled: BoolProperty(
        name="Proportional (Tenon)" if _DE else "Proportional (Tenon)",
        default=True,
    )

    def _update_tenon_ratios_from_values(self):
        try:
            w = float(self.tenon_width_mm)
            if w > 1e-9:
                self.tenon_ratio_depth = max(0.01, float(self.tenon_depth_mm) / w)
                self.tenon_ratio_chamfer = max(0.0, float(self.add_chamfer_mm) / w)
        except Exception:
            pass

    def _on_tenon_width_changed(self, context):
        if not getattr(self, "tenon_prop_enabled", True):
            self._update_tenon_ratios_from_values()
            return
        try:
            w = float(self.tenon_width_mm)
            self.tenon_depth_mm = max(0.5, w * float(self.tenon_ratio_depth))
            self.add_chamfer_mm = max(0.0, w * float(self.tenon_ratio_chamfer))
        except Exception:
            pass

    def _on_tenon_dependents_changed(self, context):
        self._update_tenon_ratios_from_values()

    tenon_width_mm: FloatProperty(
        name="Tenon Width (mm)" if not _DE else "Zapfen-Breite (mm)",
        default=6.0, min=1.0, soft_max=100.0,
        update=_on_tenon_width_changed,
    )
    tenon_depth_mm: FloatProperty(
        name="Tenon Depth (mm)" if not _DE else "Zapfen-Tiefe (mm)",
        default=8.0, min=1.0, soft_max=200.0,
        update=_on_tenon_dependents_changed,
    )
    tenon_ratio_depth: FloatProperty(name="k_ten_depth", default=1.33, min=0.01, soft_max=10.0, options={'HIDDEN'})
    tenon_ratio_chamfer: FloatProperty(name="k_ten_ch", default=0.05, min=0.0, soft_max=0.5, options={'HIDDEN'})

    # --- Dovetail dimensions (X driver when proportional is enabled) ---

    dovetail_dim_x_mm: FloatProperty(
        name="Dim X (mm)",
        description="Dovetail size along local X (depth/thickness)",
        default=12.0, min=0.0,
    )
    dovetail_dim_y_mm: FloatProperty(
        name="Dim Y (mm)",
        description="Dovetail size along local Y (width; tapered faces)",
        default=16.0, min=0.0,
    )
    dovetail_dim_z_mm: FloatProperty(
        name="Dim Z (mm)",
        description="Dovetail size along local Z (length/extrusion)",
        default=20.0, min=0.0,
    )

    dovetail_prop_enabled: BoolProperty(
        name="Proportional scaling (Dovetail)",
        default=True,
        description="If enabled, X drives Y and Z via ratios (Y = X / Ratio X; Z = Y * Ratio Z)"
    )
    dovetail_ratio_x: FloatProperty(
        name="Ratio X",
        default=0.75, min=0.01, soft_max=5.0,
        description="Defines Y = X / Ratio X when proportional is enabled"
    )
    dovetail_ratio_z: FloatProperty(
        name="Ratio Z",
        default=1.25, min=0.01, soft_max=5.0,
        description="Defines Z = (X / Ratio X) * Ratio Z when proportional is enabled"
    )

    def dovetail_effective_dims_x_driver(self):
        """
        Compute effective dovetail (x, y, z) without writing back to properties.
        - When proportional is ON: X is the only editable driver, Y = X/kx, Z = Y*kz.
        - When proportional is OFF: use raw X, Y, Z.
        """
        x = max(0.0, float(getattr(self, "dovetail_dim_x_mm", 12.0)))
        y = max(0.0, float(getattr(self, "dovetail_dim_y_mm", 16.0)))
        z = max(0.0, float(getattr(self, "dovetail_dim_z_mm", 20.0)))
        if bool(getattr(self, "dovetail_prop_enabled", True)):
            kx = max(0.01, float(getattr(self, "dovetail_ratio_x", 0.75)))
            kz = max(0.01, float(getattr(self, "dovetail_ratio_z", 1.25)))
            y_eff = x / kx
            z_eff = y_eff * kz
            return (x, y_eff, z_eff)
        return (x, y, z)

    # Side angles (mirror at read when proportional is enabled)
    dovetail_side_angle_a_deg: FloatProperty(
        name="Side angle A (°)",
        default=7.0, min=0.0, max=85.0,
        description="Side wall angle on one side of the taper axis"
    )
    dovetail_side_angle_b_deg: FloatProperty(
        name="Side angle B (°)",
        default=7.0, min=0.0, max=85.0,
        description="Side wall angle on the opposite side of the taper axis"
    )

    def dovetail_effective_angles(self):
        """
        Return (a, b) side angles.
        - When proportional is ON: B mirrors A.
        - When proportional is OFF: return A, B as set.
        """
        a = float(getattr(self, "dovetail_side_angle_a_deg", 7.0))
        b = float(getattr(self, "dovetail_side_angle_b_deg", 7.0))
        if bool(getattr(self, "dovetail_prop_enabled", True)):
            return (a, a)
        return (a, b)

    # Axis selection for 'fill to edges'
    dovetail_stretch_axis: EnumProperty(
        name="Stretch axis",
        description="Axis that is stretched across the seam's usable span",
        items=[('X', 'X', ''), ('Y', 'Y', ''), ('Z', 'Z', '')],
        default='Z'
    )

    # Full span, percent-of-span, edge snapping and end inset
    dovetail_use_full_span: BoolProperty(
        name="Use full seam span",
        default=True,
        description="Stretch along selected axis to full usable seam overlap (with margins/inset)"
    )
    dovetail_fit_pct: FloatProperty(
        name="Span %",
        default=100.0, min=1.0, max=100.0,
        description="If not full span, use this percentage of the usable span along the stretch axis"
    )
    dovetail_clip_to_edge: BoolProperty(
        name="Clip to edge",
        default=True,
        description="When not full span and <100%, align from nearest edge instead of centered"
    )
    dovetail_end_inset_mm: FloatProperty(
        name="End inset (mm)",
        default=0.0, min=0.0,
        description="Extra inset from seam ends along the stretch axis"
    )

    # Lead-in and clearance scale (optional for ops)
    dovetail_leadin_chamfer_mm: FloatProperty(
        name="Lead-in chamfer (mm)",
        default=0.0, min=0.0
    )
    dovetail_clearance_scale: FloatProperty(
        name="Clearance scale",
        default=1.0, min=0.0, soft_max=3.0,
        description="Scales base tolerance for dovetail socket clearance per side"
    )

    # Dovetail overshoot (in mm, left unit-agnostic; ops multiply by unit_mm())
    dovetail_overshoot_mm: FloatProperty(
        name="Overshoot (mm)" if not _DE else "Überstand (mm)",
        description=("Small extra length along the selected stretch axis to ensure clean booleans (in mm)"
                     if not _DE else "Kleiner Längenzuschlag entlang der Streckachse für saubere Booleans (in mm)"),
        default=0.5, min=0.0, soft_max=2.0, step=0.1, precision=3
    )

    # Snap-Cantilever (Master: arm width)
    snap_cant_arm_len_mm: FloatProperty(
        name="Arm length (mm)" if not _DE else "Armlänge (mm)",
        default=18.0, min=4.0, soft_max=60.0,
    )
    snap_cant_arm_thk_mm: FloatProperty(
        name="Arm thickness (mm)" if not _DE else "Armdicke (mm)",
        default=2.2, min=0.8, soft_max=6.0,
    )
    snap_cant_arm_w_mm: FloatProperty(
        name="Arm width (mm)" if not _DE else "Armbreite (mm)",
        default=6.0, min=2.0, soft_max=40.0,
    )
    snap_cant_hook_undercut_mm: FloatProperty(
        name="Hook undercut (mm)" if not _DE else "Hinterschneidung (mm)",
        default=0.8, min=0.2, soft_max=2.0,
    )
    snap_cant_fillet_mm: FloatProperty(
        name="Base fillet (mm)" if not _DE else "Grundradius (mm)",
        default=1.2, min=0.4, soft_max=4.0,
    )
    snap_cant_leadin_chamfer_mm: FloatProperty(
        name="Lead-in chamfer (mm)" if not _DE else "Einführfase (mm)",
        default=0.6, min=0.0, soft_max=2.0,
    )
    snap_cant_stop_offset_mm: FloatProperty(
        name="Stop offset (mm)" if not _DE else "Anschlag (mm)",
        default=0.2, min=0.0, soft_max=2.0,
    )
    snap_cant_clearance_scale: FloatProperty(
        name="Clearance scale" if not _DE else "Spiel-Skalierung",
        default=1.1, min=0.5, soft_max=2.0,
    )

    snapcant_prop_enabled: BoolProperty(
        name="Proportional (Cantilever)" if _DE else "Proportional (Cantilever)",
        default=True,
    )
    snapcant_ratio_len: FloatProperty(name="k_sc_len", default=3.0, min=0.01, soft_max=10.0, options={'HIDDEN'})
    snapcant_ratio_thk: FloatProperty(name="k_sc_thk", default=0.37, min=0.01, soft_max=5.0, options={'HIDDEN'})
    snapcant_ratio_undercut: FloatProperty(name="k_sc_uc", default=0.13, min=0.0, soft_max=1.0, options={'HIDDEN'})
    snapcant_ratio_fillet: FloatProperty(name="k_sc_fil", default=0.20, min=0.0, soft_max=2.0, options={'HIDDEN'})
    snapcant_ratio_leadin: FloatProperty(name="k_sc_ch", default=0.10, min=0.0, soft_max=2.0, options={'HIDDEN'})

    # Ball & Socket (Master: ball_diameter_mm)
    ball_diameter_mm: FloatProperty(
        name="Ball Ø (mm)" if not _DE else "Kugel-Ø (mm)",
        default=12.0, min=4.0, soft_max=40.0,
    )
    ball_friction_target: EnumProperty(
        name="Friction" if not _DE else "Reibung",
        items=[("tight", "Tight" if not _DE else "Fest", ""),
               ("medium", "Medium" if not _DE else "Mittel", ""),
               ("loose", "Loose" if not _DE else "Locker", "")],
        default="medium",
    )
    ball_socket_clearance_mm: FloatProperty(
        name="Socket clearance (mm)" if not _DE else "Buchsen-Spiel (mm)",
        default=0.0, min=0.0, soft_max=0.8,
    )
    ball_lip_thickness_mm: FloatProperty(
        name="Retention lip (mm)" if not _DE else "Halte-Lippe (mm)",
        default=1.2, min=0.0, soft_max=4.0,
    )
    ball_socket_open_angle_deg: FloatProperty(
        name="Open angle (°)" if not _DE else "Öffnungswinkel (°)",
        default=230.0, min=160.0, soft_max=300.0,
    )
    ball_leadin_fillet_mm: FloatProperty(
        name="Lead-in fillet (mm)" if not _DE else "Einführ-Radius (mm)",
        default=0.6, min=0.0, soft_max=2.0,
    )

    ballsocket_prop_enabled: BoolProperty(
        name="Proportional (Ball&Socket)" if _DE else "Proportional (Ball&Socket)",
        default=True,
    )
    ballsocket_ratio_clear: FloatProperty(name="k_bs_clr", default=0.03, min=0.0, soft_max=0.5, options={'HIDDEN'})
    ballsocket_ratio_lip: FloatProperty(name="k_bs_lip", default=0.10, min=0.0, soft_max=1.0, options={'HIDDEN'})
    ballsocket_ratio_leadin: FloatProperty(name="k_bs_ch", default=0.05, min=0.0, soft_max=1.0, options={'HIDDEN'})

    # PiP Hinge (Master: pip_hinge_width_mm)
    pip_hinge_type: EnumProperty(
        name="Hinge type" if not _DE else "Scharnier-Typ",
        items=[("knuckle_pin", "Knuckle (pin)" if not _DE else "Laschen (Bolzen)", ""),
               ("living_web", "Living web" if not _DE else "Living Hinge", "")],
        default="knuckle_pin",
    )
    pip_gap_mm: FloatProperty(
        name="PIP gap (mm)" if not _DE else "PIP-Spalt (mm)",
        default=0.30, min=0.05, soft_max=1.0,
    )
    pip_hinge_width_mm: FloatProperty(
        name="Hinge width (mm)" if not _DE else "Scharnier-Breite (mm)",
        default=8.0, min=2.0, soft_max=60.0,
    )
    pip_hinge_thickness_mm: FloatProperty(
        name="Thickness (mm)" if not _DE else "Dicke (mm)",
        default=2.0, min=0.3, soft_max=6.0,
    )
    pip_segments_count: IntProperty(
        name="Segments" if not _DE else "Segmente",
        default=3, min=1, max=21,
    )
    pip_relief_fillet_mm: FloatProperty(
        name="Relief fillet (mm)" if not _DE else "Entlastungs-Radius (mm)",
        default=0.6, min=0.0, soft_max=2.0,
    )

    pip_prop_enabled: BoolProperty(
        name="Proportional (PiP)" if not _DE else "Proportional (PiP)",
        default=True,
    )
    pip_ratio_gap: FloatProperty(name="k_pip_gap", default=0.04, min=0.0, soft_max=0.2, options={'HIDDEN'})
    pip_ratio_thk: FloatProperty(name="k_pip_thk", default=0.25, min=0.05, soft_max=1.0, options={'HIDDEN'})
    pip_ratio_relief: FloatProperty(name="k_pip_rel", default=0.075, min=0.0, soft_max=0.5, options={'HIDDEN'})

    # Tolerance + friction (auto-applies snap-sphere presets)
    def _on_material_changed(self, context):
        _apply_snap_sphere_preset(self)

    material_profile: EnumProperty(
        name="Material Profiles" if not _DE else "Material-Profile",
        items=_material_items(),
        default="PETG",
        update=_on_material_changed,
    )

    def _on_snap_friction_changed(self, context):
        _apply_snap_sphere_preset(self)

    snap_friction_target: EnumProperty(
        name="Friction" if not _DE else "Reibung",
        description=("Auto-applies snap-sphere diameter and protrusion"
                     if not _DE else "Setzt Sphären-Ø und -Überstand automatisch"),
        items=[("tight","Tight" if not _DE else "Fest",""),
               ("medium","Medium" if not _DE else "Mittel",""),
               ("loose","Loose" if not _DE else "Locker","")],
        default="medium",
        update=_on_snap_friction_changed,
    )

    tol_override: FloatProperty(
        name="Tolerance per Face (mm)" if not _DE else "Toleranz pro Fläche (mm)",
        default=0.0, min=0.0, soft_max=0.8,
    )

    def effective_tolerance(self) -> float:
        prof = MATERIAL_PROFILES.get(self.material_profile, 0.3)
        return prof if self.tol_override <= 0.0 else self.tol_override

    # UI foldouts
    ui_more_seg: BoolProperty(default=False)
    ui_more_conn: BoolProperty(default=False)
    ui_more_tol: BoolProperty(default=False)
    ui_more_align: BoolProperty(default=False)


# ---------------------------
# Registration
# ---------------------------

classes = (SnapSplitProps,)

def register():
    for c in classes:
        bpy.utils.register_class(c)
    bpy.types.Scene.snapsplit = PointerProperty(type=SnapSplitProps)

    # Initial apply of snap-sphere presets (optional, good UX)
    try:
        sc = bpy.context.scene
        if hasattr(sc, "snapsplit") and sc.snapsplit:
            _apply_snap_sphere_preset(sc.snapsplit)
    except Exception:
        pass

def unregister():
    if hasattr(bpy.types.Scene, "snapsplit"):
        del bpy.types.Scene.snapsplit
    for c in reversed(classes):
        bpy.utils.unregister_class(c)
