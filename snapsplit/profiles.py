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

MATERIAL_PROFILES = {
    "PLA": 0.20,   # mm per side
    "PETG": 0.30,
    "ABS": 0.25,
    "ASA": 0.25,
    "TPU": 0.35,
    "SLA": 0.10,
}

# Static items list to allow string default
MATERIAL_ITEMS = [(k, k, f"Recommended tolerance per side: {v:.2f} mm") for k, v in MATERIAL_PROFILES.items()]

class SnapSplitProps(PropertyGroup):
    # Segmentation
    parts_count: bpy.props.IntProperty(
        name="Number of Parts",
        default=2,
        min=2,
        max=12,
        description="Number of desired segments",
    )
    split_axis: bpy.props.EnumProperty(
        name="Split Axis",
        items=[
            ("X", "X", "Split along X"),
            ("Y", "Y", "Split along Y"),
            ("Z", "Z", "Split along Z"),
        ],
        default="Z",
    )

    # Connector Type and Distribution
    connector_type: bpy.props.EnumProperty(
        name="Connector Type",
        items=[
            ("CYL_PIN", "Cylinder Pin", "Dowel pin + socket"),
            ("RECT_TENON", "Rectangular Tenon", "Anti-rotation joint"),
        ],
        default="CYL_PIN",
    )
    connector_distribution: EnumProperty(
        name="Distribution",
        description="Distribute connectors along a line or grid across the seam face",
        items=[
            ("LINE", "Line", "Place connectors along a line in the seam face"),
            ("GRID", "Grid", "Distribute connectors in a grid over the seam face"),
        ],
        default="LINE",
    )
    connectors_per_seam: bpy.props.IntProperty(
        name="Connectors per Seam",
        default=3,
        min=1,
        max=64,
    )
    connectors_rows: IntProperty(
        name="Rows (GRID)",
        description="Number of rows in grid distribution",
        default=2,
        min=1,
        max=64,
    )

    # Pin / Tenon Dimensions
    pin_diameter_mm: FloatProperty(
        name="Pin Diameter (mm)",
        default=5.0,
        min=0.5,
        soft_max=50.0,
    )
    pin_length_mm: FloatProperty(
        name="Pin Length (mm)",
        default=8.0,
        min=1.0,
        soft_max=200.0,
    )
    tenon_width_mm: FloatProperty(
        name="Tenon Width (mm)",
        default=6.0,
        min=1.0,
        soft_max=100.0,
    )
    tenon_depth_mm: FloatProperty(
        name="Tenon Depth (mm)",
        default=8.0,
        min=1.0,
        soft_max=200.0,
    )
    add_chamfer_mm: FloatProperty(
        name="Chamfer (mm)",
        default=0.3,
        min=0.0,
        soft_max=2.0,
    )

    # Insert Depth
    pin_embed_pct: FloatProperty(
        name="Insert Depth (%)",
        description="Percentage of connector length recessed into part A",
        default=50.0,
        min=0.0,
        max=100.0,
        subtype='PERCENTAGE'
    )

    # Margin for Distribution
    connector_margin_pct: FloatProperty(
        name="Margin (%)",
        description="Edge margin along the seam (and perpendicular in GRID) as percentage of part length (0–40% recommended)",
        default=10.0,
        min=0.0,
        soft_max=40.0,
        subtype='PERCENTAGE'
    )

    # Tolerances / Material Profile
    material_profile: bpy.props.EnumProperty(
        name="Material Profiles",
        items=MATERIAL_ITEMS,   # static
        default="PLA",
    )
    tol_override: FloatProperty(
        name="Tolerance per Face (mm)",
        description="Overrides material profile (0 = use profile value)",
        default=0.0,
        min=0.0,
        soft_max=0.6,
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
