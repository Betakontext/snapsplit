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
from .utils import is_lang_de

class SNAP_PT_panel(Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "SnapSplit"
    bl_label = "SnapSplit"

    @classmethod
    def poll(cls, context):
        return (context is not None) and (context.scene is not None)

    def draw(self, context):
        layout = self.layout
        props = getattr(context.scene, "snapsplit", None)

        if props is None:
            layout.label(text=("SnapSplit properties not available." if not is_lang_de()
                               else "SnapSplit-Eigenschaften nicht verfügbar."),
                         icon="ERROR")
            layout.label(text=("Please re-enable the add-on." if not is_lang_de()
                               else "Bitte das Add-on erneut aktivieren."))
            return

        # Segmentation
        col = layout.column(align=True)
        col.label(text=("Segmentation" if not is_lang_de() else "Segmentierung"))
        col.prop(props, "parts_count")
        col.prop(props, "split_axis")
        col.operator("snapsplit.planar_split",
                     icon="MOD_BOOLEAN",
                     text=("Planar Split" if not is_lang_de() else "Planarer Schnitt"))

        layout.separator()

        # Connections
        col = layout.column(align=True)
        col.label(text=("Connections" if not is_lang_de() else "Verbindungen"))
        col.prop(props, "connector_type",
                 text=("Connector Type" if not is_lang_de() else "Verbinder-Typ"))
        col.prop(props, "connector_distribution",
                 text=("Distribution" if not is_lang_de() else "Verteilung"))

        if props.connector_distribution == "LINE":
            col.prop(props, "connectors_per_seam",
                     text=("Connectors per Seam" if not is_lang_de() else "Verbinder pro Naht"))
        else:
            row = col.row(align=True)
            row.prop(props, "connectors_per_seam",
                     text=("Columns" if not is_lang_de() else "Spalten"))
            row.prop(props, "connectors_rows",
                     text=("Rows" if not is_lang_de() else "Reihen"))

        col.prop(props, "connector_margin_pct",
                 text=("Margin (%)" if not is_lang_de() else "Randabstand (%)"))

        box = col.box()
        if props.connector_type == "CYL_PIN":
            box.prop(props, "pin_diameter_mm",
                     text=("Pin Diameter (mm)" if not is_lang_de() else "Pin-Durchmesser (mm)"))
            box.prop(props, "pin_length_mm",
                     text=("Pin Length (mm)" if not is_lang_de() else "Pin-Länge (mm)"))
            box.prop(props, "pin_embed_pct",
                     text=("Insert Depth (%)" if not is_lang_de() else "Einstecktiefe (%)"))
        else:
            box.prop(props, "tenon_width_mm",
                     text=("Tenon Width (mm)" if not is_lang_de() else "Zapfen-Breite (mm)"))
            box.prop(props, "tenon_depth_mm",
                     text=("Tenon Depth (mm)" if not is_lang_de() else "Zapfen-Tiefe (mm)"))
            # Reuse insert depth setting for tenons (optional feature)
            box.prop(props, "pin_embed_pct",
                     text=("Insert Depth (%)" if not is_lang_de() else "Einstecktiefe (%)"))

        box.prop(props, "add_chamfer_mm",
                 text=("Chamfer (mm)" if not is_lang_de() else "Fase (mm)"))

        layout.separator()

        # Tolerance
        col = layout.column(align=True)
        col.label(text=("Tolerance" if not is_lang_de() else "Toleranz"))
        col.prop(props, "material_profile",
                 text=("Material Profiles" if not is_lang_de() else "Material-Profile"))

        row = col.row(align=True)
        row.prop(props, "tol_override",
                 text=("Tolerance per Face (mm)" if not is_lang_de() else "Toleranz pro Fläche (mm)"))

        prof_val = MATERIAL_PROFILES.get(props.material_profile, 0.2)
        row = col.row(align=True)
        row.label(text=(f"Profile: {prof_val:.2f} mm" if not is_lang_de()
                        else f"Profil: {prof_val:.2f} mm"))

        layout.separator()

        # Action
        col = layout.column(align=True)
        col.operator("snapsplit.add_connectors",
                     icon="SNAP_FACE",
                     text=("Add connectors" if not is_lang_de() else "Verbinder hinzufügen"))

def register():
    bpy.utils.register_class(SNAP_PT_panel)

def unregister():
    bpy.utils.unregister_class(SNAP_PT_panel)
