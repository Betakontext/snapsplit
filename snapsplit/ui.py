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
            layout.label(text="SnapSplit properties not available.", icon="ERROR")
            layout.label(text="Please reactivate the Add-on.")
            return

        col = layout.column(align=True)
        col.label(text="Segmentation")
        col.prop(props, "parts_count")
        col.prop(props, "split_axis")
        col.operator("snapsplit.planar_split", icon="MOD_BOOLEAN")

        layout.separator()

        col = layout.column(align=True)
        col.label(text="Connections")
        col.prop(props, "connector_type")
        col.prop(props, "connector_distribution")
        if props.connector_distribution == "LINE":
            col.prop(props, "connectors_per_seam")
        else:
            row = col.row(align=True)
            row.prop(props, "connectors_per_seam", text="Columns")
            row.prop(props, "connectors_rows", text="Rows")
        col.prop(props, "connector_margin_pct")  # Randabstand %

        box = col.box()
        if props.connector_type == "CYL_PIN":
            box.prop(props, "pin_diameter_mm")
            box.prop(props, "pin_length_mm")
            box.prop(props, "pin_embed_pct")
        else:
            box.prop(props, "tenon_width_mm")
            box.prop(props, "tenon_depth_mm")
            box.prop(props, "pin_embed_pct")
        box.prop(props, "add_chamfer_mm")

        layout.separator()
        col = layout.column(align=True)
        col.label(text="Tolerance")
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
