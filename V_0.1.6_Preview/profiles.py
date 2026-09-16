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

# profiles.py

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

# Only use the translation helper; remove any custom language branches
from .languages import tr


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
        # Fail silently to not break UI interactions if preview operator is unavailable
        pass


def _snapsplit_update_connector_preview(self, context):
    """Property update callback to refresh or clear the connector placement live preview.

    This is fully independent from the split-plane preview above. The called
    function itself checks the 'connector_live_preview' toggle and the current
    selection/distribution mode, and performs cleanup when preview is not
    applicable. Kept in a try/except so UI interactions never break, even if
    the preview builder raises under unusual context states (e.g. during
    file load or when running from a background context).
    """
    try:
        from . import ops_connectors
        ops_connectors.update_connector_placement_preview(context)
    except Exception:
        # Fail silently to not break UI interactions if the preview function is unavailable
        pass


def _suggest_pin_segments_from_diameter(d_mm: float) -> int:
    """
    Return a heuristic segment count for cylindrical pins from diameter in mm.
    Aims for visually round pins suitable for 3D printing without heavy meshes.
    """
    if d_mm <= 0:
        return 16
    base = int(round(math.pi * d_mm / 1.8))
    lo, hi = 12, 64
    if d_mm < 3.0:
        lo = 16
    return max(lo, min(hi, base))


def _mat_item_desc(key: str, val: float) -> str:
    """
    Build a localized tooltip text for a material profile entry.

    Uses languages.py template key "profiles.mat.tooltip" and formats it
    with {val} = tolerance value in mm, rounded to 2 decimals.
    """
    templ = tr("profiles.mat.tooltip", "Recommended tolerance per side: {val} mm")
    try:
        return templ.format(val=f"{val:.2f}")
    except Exception:
        return f"Recommended tolerance per side: {val:.2f} mm"


def _material_items():
    """Return EnumProperty items for material profiles with localized tooltips."""
    return [(k, k, _mat_item_desc(k, v)) for k, v in MATERIAL_PROFILES.items()]

def _poll_custom_connector_object(self, obj):
    """Restrict the Custom Connector object picker to mesh objects only."""
    return obj.type == 'MESH'

# ---------------------------
# Property group
# ---------------------------

class SnapSplitProps(PropertyGroup):
    """Scene-level settings for segmentation, preview, connectors, tolerances, and alignment."""

    # Split / Preview
    split_offset_mm: FloatProperty(
        name=tr("ui.split_offset_mm", "Split Offset (mm)"),
        description=tr(
            "ui.split_offset_desc",
            "Offset of the cutting plane along the split axis (positive in axis direction)"
        ),
        default=0.0,
        soft_min=-100000.0,
        soft_max=100000.0,
        update=_snapsplit_update_preview,
    )

    split_axis: EnumProperty(
        name=tr("ui.split_axis", "Split Axis"),
        items=[
            ("X", "X", tr("ui.split_along_x", "Split along X")),
            ("Y", "Y", tr("ui.split_along_y", "Split along Y")),
            ("Z", "Z", tr("ui.split_along_z", "Split along Z")),
        ],
        default="Z",
        update=_snapsplit_update_preview,
    )

    show_split_preview: BoolProperty(
        name=tr("ui.show_split_preview", "Show split preview"),
        description=tr(
            "ui.show_split_preview_desc",
            "Show temporary orange planes at planned cut positions"
        ),
        default=False,
        update=_snapsplit_update_preview,
    )

    parts_count: IntProperty(
        name=tr("ui.parts_count", "Number of Parts"),
        default=2,
        min=2,
        max=64,
        description=tr(
            "ui.parts_count_desc",
            "Number of desired segments (cut planes = parts - 1)"
        ),
        update=_snapsplit_update_preview,
    )

    # Performance/Workflow: Cap seams automatically during split
    cap_seams_during_split: BoolProperty(
        name=tr("ui.cap_seams_during_split_short", "Cap seams during split"),
        description=tr(
            "ui.cap_seams_during_split_desc",
            "Automatically close seams after splitting. With hollow/inner shell: precise outer/inner loop fill; without hollow: simple fill. May increase runtime."
        ),
        default=True,
    )

    # Connections
    connector_type: EnumProperty(
        name=tr("ui.connector_type", "Connector Type"),
        items=[
            ("CYL_PIN", tr("ui.cyl_pin", "Cylinder Pin"), tr("ui.cyl_pin_desc", "Dowel pin + socket")),
            ("RECT_TENON", tr("ui.rect_tenon", "Rectangular Tenon"), tr("ui.rect_tenon_desc", "Anti-rotation joint")),
            ("DOVETAIL", tr("ui.dovetail", "Dovetail"), tr("ui.dovetail_desc", "Tapered wedge connector")),
            ("SNAP_PIN", tr("ui.snap_pin", "Snap Pin"), tr("ui.snap_pin_desc", "Connector with snap spheres")),
            ("SNAP_TENON", tr("ui.snap_tenon", "Snap Tenon"), tr("ui.snap_tenon_desc", "Rectangular tenon with snap spheres")),
            ("SNAP_DOVETAIL", tr("ui.snap_dovetail", "Snap Dovetail"), tr("ui.snap_dovetail_desc", "Tapered wedge connector with snap spheres")),
            ("CUSTOM", tr("ui.custom_connector", "Custom Connector"), tr("ui.custom_connector_desc", "Use another mesh object from the scene as connector shape")),
            # ("SNAP_FLUSH_PIN", tr("ui.snap_flush_pin", "Snap Flush Pin"), tr("ui.snap_flush_pin_desc", "Flush snap-fit cylindrical mortise/tenon")),
            # ("SNAP_FLUSH_TENON", tr("ui.snap_flush_tenon", "Snap Flush Tenon"), tr("ui.snap_flush_tenon_desc", "Flush snap-fit rectangular mortise/tenon")),
        ],
        default="CYL_PIN",
        update=_snapsplit_update_connector_preview,
    )

    # Placement distribution
    connector_distribution: EnumProperty(
        name=tr("ui.distribution", "Distribution"),
        description=tr(
            "ui.distribution_desc",
            "Distribute connectors along a line or a grid across the seam face"
        ),
        items=[
            ("LINE", tr("ui.line", "Line"), tr("ui.line_desc", "Place connectors along a line in the seam face")),
            ("GRID", tr("ui.grid", "Grid"), tr("ui.grid_desc", "Distribute connectors in a grid over the seam face")),
        ],
        default="LINE",
        update=_snapsplit_update_connector_preview,
    )

    connectors_per_seam: IntProperty(
        name=tr("ui.connectors_per_seam", "Connectors per Seam"),
        default=3,
        min=1,
        max=128,
        update=_snapsplit_update_connector_preview,
    )

    connectors_rows: IntProperty(
        name=tr("ui.rows_grid", "Rows (GRID)"),
        description=tr("ui.rows_grid_desc", "Number of rows for grid distribution"),
        default=2,
        min=1,
        max=128,
        update=_snapsplit_update_connector_preview,
    )

    connector_margin_pct: FloatProperty(
        name=tr("ui.margin_pct", "Margin (%)"),
        description=tr(
            "ui.margin_pct_desc",
            "Edge margin along the seam (and perpendicular in GRID) as percentage of part length (0–40% recommended)"
        ),
        default=10.0,
        min=0.0,
        soft_max=40.0,
        subtype='PERCENTAGE',
        update=_snapsplit_update_connector_preview,
    )

    # Live preview toggle for the LINE/GRID connector distribution.
    # When enabled, non-boolean wireframe placeholders are drawn in the
    # viewport for the currently selected parts, refreshed whenever the
    # selection or any relevant connector property changes.
    connector_live_preview: BoolProperty(
        name=tr("ui.connector_live_preview", "Live Preview"),
        description=tr(
            "ui.connector_live_preview_desc",
            "Show a live wireframe preview of connector placement (LINE/GRID) for the current selection. Capped at 200 preview objects for performance."
        ),
        default=False,
        update=_snapsplit_update_connector_preview,
    )

    # Snap options (sphere ring; used by SNAP_PIN / SNAP_TENON)
    snap_spheres_per_side: IntProperty(
        name=tr("ui.spheres_per_side", "Spheres per side"),
        description=tr("ui.spheres_per_side_desc", "Number of snap spheres per side/around"),
        default=2,
        min=1,
        max=32,
        update=_snapsplit_update_connector_preview,
    )

    snap_sphere_diameter_mm: FloatProperty(
        name=tr("ui.sphere_diameter_mm", "Sphere  (mm)"),
        description=tr("ui.sphere_diameter_mm_desc", "Diameter of snap spheres"),
        default=2.0,
        min=0.5,
        soft_max=10.0,
        update=_snapsplit_update_connector_preview,
    )

    snap_sphere_protrusion_mm: FloatProperty(
        name=tr("ui.protrusion_mm", "Protrusion (mm)"),
        description=tr("ui.protrusion_mm_desc", "How far spheres protrude from side surface"),
        default=1.0,
        min=0.0,
        soft_max=5.0,
        update=_snapsplit_update_connector_preview,
    )

    # Pin / Tenon dimensions (mm)
    pin_diameter_mm: FloatProperty(
        name=tr("ui.pin_diameter_mm", "Pin Diameter (mm)"),
        default=5.0,
        min=0.5,
        soft_max=50.0,
        update=_snapsplit_update_connector_preview,
    )

    pin_length_mm: FloatProperty(
        name=tr("ui.pin_length_mm", "Pin Length (mm)"),
        default=8.0,
        min=1.0,
        soft_max=200.0,
        update=_snapsplit_update_connector_preview,
    )

    pin_segments: IntProperty(
        name=tr("ui.segments", "Segments"),
        description=tr("ui.segments_desc", "Cylinder pin radial segments (visual smoothness)"),
        default=32,
        min=8,
        max=128,
        update=_snapsplit_update_connector_preview,
    )

    tenon_width_mm: FloatProperty(
        name=tr("ui.tenon_width_mm", "Tenon Width (mm)"),
        default=6.0,
        min=1.0,
        soft_max=100.0,
        update=_snapsplit_update_connector_preview,
    )

    tenon_depth_mm: FloatProperty(
        name=tr("ui.tenon_depth_mm", "Tenon Depth (mm)"),
        default=8.0,
        min=1.0,
        soft_max=200.0,
        update=_snapsplit_update_connector_preview,
    )

    add_chamfer_mm: FloatProperty(
        name=tr("ui.chamfer_mm", "Chamfer (mm)"),
        default=0.3,
        min=0.0,
        soft_max=2.0,
        update=_snapsplit_update_connector_preview,
    )

    # Custom connector (arbitrary mesh object, rescaled to target dimensions)
    custom_connector_object: PointerProperty(
        type=bpy.types.Object,
        name=tr("ui.custom_connector_object", "Select connector object"),
        description=tr(
            "ui.custom_connector_object_desc",
            "Mesh object from this scene used as connector shape. Its local Z axis "
            "is treated as the insertion direction; it will be rescaled to the "
            "Width/Length/Depth values below."
        ),
        poll=_poll_custom_connector_object,
        update=_snapsplit_update_connector_preview,
    )

    custom_connector_width_mm: FloatProperty(
        name=tr("ui.custom_connector_width_mm", "Custom Width (mm)"),
        description=tr("ui.custom_connector_width_desc", "Target size along the object's local X axis"),
        default=6.0,
        min=0.1,
        soft_max=100.0,
        update=_snapsplit_update_connector_preview,
    )

    custom_connector_length_mm: FloatProperty(
        name=tr("ui.custom_connector_length_mm", "Custom Length (mm)"),
        description=tr("ui.custom_connector_length_desc", "Target size along the object's local Y axis"),
        default=6.0,
        min=0.1,
        soft_max=100.0,
        update=_snapsplit_update_connector_preview,
    )

    custom_connector_depth_mm: FloatProperty(
        name=tr("ui.custom_connector_depth_mm", "Custom Depth (mm)"),
        description=tr("ui.custom_connector_depth_desc", "Target size along the object's local Z axis (insertion depth)"),
        default=8.0,
        min=0.1,
        soft_max=200.0,
        update=_snapsplit_update_connector_preview,
    )


    # Insert depth
    pin_embed_pct: FloatProperty(
        name=tr("ui.insert_depth_pct", "Insert Depth (%)"),
        description=tr("ui.insert_depth_pct_desc", "Percentage of connector length recessed into part A"),
        default=50.0,
        min=0.0,
        max=100.0,
        subtype='PERCENTAGE',
        update=_snapsplit_update_connector_preview,
    )

    # Dovetail basics
    dovetail_width_mm: FloatProperty(
        name=tr("ui.dovetail_width_mm", "Dovetail Width (mm)"),
        default=6.0,
        min=2.0,
        soft_max=60.0,
        update=_snapsplit_update_connector_preview,
    )

    dovetail_length_mm: FloatProperty(
        name=tr("ui.dovetail_length_mm", "Dovetail Length (mm)"),
        description=tr("ui.dovetail_length_mm_desc", "Length along seam plane (local v)"),
        default=6.0,
        min=2.0,
        soft_max=200.0,
        update=_snapsplit_update_connector_preview,
    )

    dovetail_depth_mm: FloatProperty(
        name=tr("ui.dovetail_depth_mm", "Dovetail Depth (mm)"),
        default=8.0,
        min=2.0,
        soft_max=120.0,
        update=_snapsplit_update_connector_preview,
    )

    dovetail_taper_pct: FloatProperty(
        name=tr("ui.dovetail_taper_pct", "Taper (%)"),
        description=tr("ui.dovetail_taper_pct_desc", "Percentage by which the tip is narrower than the base"),
        default=25.0,
        min=5.0,
        max=60.0,
        subtype='PERCENTAGE',
        update=_snapsplit_update_connector_preview,
    )

    # Flush snap barb parameters (shared for pin/tenon)
    flush_barb_height_mm: FloatProperty(
        name=tr("ui.flush_barb_height_mm", "Barb Height (mm)"),
        description=tr("ui.flush_barb_height_desc", "Axial height of the shallow barb near the seam"),
        default=0.6,
        min=0.2,
        soft_max=1.2,
        update=_snapsplit_update_connector_preview,
    )

    flush_barb_lip_mm: FloatProperty(
        name=tr("ui.flush_barb_lip_mm", "Barb Lip (mm)"),
        description=tr("ui.flush_barb_lip_desc", "Radial/XY lip amount for the barb at the seam"),
        default=0.25,
        min=0.1,
        soft_max=0.6,
        update=_snapsplit_update_connector_preview,
    )

    # Tolerances / material profile
    material_profile: EnumProperty(
        name=tr("ui.material_profiles", "Material Profiles"),
        items=_material_items(),
        default="PLA",
        description=tr(
            "ui.material_profile_desc",
            "Select a material profile to auto-fill tolerance per side"
        ),
    )

    tol_override: FloatProperty(
        name=tr("ui.tol_per_face_mm", "Tolerance per Face (mm)"),
        description=tr("ui.tol_override_desc", "Overrides material profile (0 = use profile value)"),
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
        name=tr("ui.foldout.more_seg", "More segmentation settings"),
        description=tr("ui.foldout.more_seg_desc", "Show advanced segmentation options"),
        default=False
    )

    ui_more_conn: BoolProperty(
        name=tr("ui.foldout.more_conn", "More connection settings"),
        description=tr("ui.foldout.more_conn_desc", "Show advanced connection/geometry options"),
        default=False
    )

    ui_more_tol: BoolProperty(
        name=tr("ui.foldout.more_tol", "More tolerance settings"),
        description=tr("ui.foldout.more_tol_desc", "Show advanced tolerance options"),
        default=False
    )

    # Alignment foldout
    ui_more_align: BoolProperty(
        name=tr("ui.foldout.more_align", "More alignment settings"),
        description=tr("ui.foldout.more_align_desc", "Show advanced alignment options"),
        default=False
    )

    # ------------------------------------------------------------
    # NEW: Advanced Dovetail controls
    # ------------------------------------------------------------


    # Signed taper override in percent — if non-zero, overrides plain taper in ops.
    dovetail_signed_taper_pct: FloatProperty(
        name=tr("ui.dovetail_signed_taper_pct", "Signed Taper (%)"),
        description=tr("ui.dovetail_signed_taper_desc", "Signed taper along insertion. Positive widens, negative narrows. If non-zero, overrides plain taper."),
        default=0.0,
        soft_min=-60.0,
        soft_max=60.0,
        min=-90.0,
        max=90.0,
        update=_snapsplit_update_connector_preview,
    )

    # Span mode across the seam; UI already supports this.
    dovetail_span_mode: EnumProperty(
        name=tr("ui.dovetail_span_mode", "Span Mode"),
        description=tr("ui.dovetail_span_mode_desc", "How the dovetail spans along the seam"),
        items=[
            ("AUTO", tr("ui.auto", "Auto"), tr("ui.auto_span_tip", "Use full edge-to-edge span of the seam")),
            ("FIXED", tr("ui.fixed", "Fixed"), tr("ui.fixed_span_tip", "Use a fixed repeating spacing")),
            ("CENTERED", tr("ui.centered", "Centered"), tr("ui.centered_span_tip", "Center block(s) with margins")),
        ],
        default="AUTO",
        update=_snapsplit_update_connector_preview,
    )

    # Margin already present as connector_margin_pct; keep dovetail-specific too if UI expects it.
    dovetail_margin_pct: FloatProperty(
        name=tr("ui.dovetail_margin_pct", "Margin (%)"),
        description=tr("ui.dovetail_margin_pct_desc", "Trim percentage at both ends of seam span"),
        default=10.0,
        min=0.0,
        soft_max=40.0,
        subtype='PERCENTAGE',
        update=_snapsplit_update_connector_preview,
    )

    # Force a fixed span axis for the dovetail so it always overshoots the
    # object's outer sides along that axis (for automatic hard-side trimming).
    # NONE keeps the normal margin-based sizing; edges are only trimmed if the
    # separate Hard-side Cut option is enabled manually.
    dovetail_span_axis: EnumProperty(
        name=tr("ui.dovetail_span_axis", "Span Axis"),
        description=tr("ui.dovetail_span_axis_desc",
                        "Auto stretches along the Dovetail Width axis and trims to the outer sides; "
                        "X/Y/Z force overshoot along that world axis if it lies in the seam plane; "
                        "None uses the manually configured Dovetail Length"),
        items=[
            ("NONE", tr("ui.none", "None"), tr("ui.span_axis_none", "Use the manually configured Dovetail Length; only trim edges if Hard-side Cut is enabled")),
            ("AUTO", tr("ui.auto", "Auto"), tr("ui.span_axis_auto", "Automatically stretch along the Dovetail Width axis and trim to the outer sides")),
            ("X", "X", tr("ui.span_axis_x", "Force overshoot along world X, if it lies in the seam plane")),
            ("Y", "Y", tr("ui.span_axis_y", "Force overshoot along world Y, if it lies in the seam plane")),
            ("Z", "Z", tr("ui.span_axis_z", "Force overshoot along world Z, if it lies in the seam plane")),
        ],
        default="AUTO",
        update=_snapsplit_update_connector_preview,
    )



    # Prefer a sharp side cut for socket/slot walls.
    # NOTE: intentionally has no live-preview update callback, since the
    # wireframe live preview never performs the boolean hard-side cut
    # (identical behavior to the existing click-placement preview).
    dovetail_hard_side_cut: BoolProperty(
        name=tr("ui.dovetail_hard_side_cut", "Hard-side Cut"),
        description=tr("ui.dovetail_hard_side_cut_desc", "Prefer sharp side cut for dovetail socket/slot"),
        default=False,
    )

    # In-plane placement: offsets (mm) along both seam-plane axes (u = width, v = length)
    # and rotation (deg) within the cut plane.
    dovetail_inplane_offset_u_mm: FloatProperty(
        name=tr("ui.inplane_offset_u_mm", "Offset along Width (mm)"),
        description=tr("ui.inplane_offset_u_mm_desc", "Offset within the cut plane along the width (u) axis to shift the dovetail pattern"),
        default=0.0,
        soft_min=-100000.0,
        soft_max=100000.0,
        update=_snapsplit_update_connector_preview,
    )

    dovetail_inplane_offset_v_mm: FloatProperty(
        name=tr("ui.inplane_offset_v_mm", "Offset along Length (mm)"),
        description=tr("ui.inplane_offset_v_mm_desc", "Offset within the cut plane along the length (v) axis to shift the dovetail pattern"),
        default=0.0,
        soft_min=-100000.0,
        soft_max=100000.0,
        update=_snapsplit_update_connector_preview,
    )


    dovetail_inplane_rotation_deg: FloatProperty(
        name=tr("ui.inplane_rotation_deg", "Rotation in plane (deg)"),
        description=tr("ui.inplane_rotation_deg_desc", "Rotation within the cut plane to orient the dovetail pattern"),
        default=0.0,
        soft_min=-180.0,
        soft_max=180.0,
        update=_snapsplit_update_connector_preview,
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
