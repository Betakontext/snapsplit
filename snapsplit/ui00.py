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

# ui.py

import bpy
from bpy.types import Panel
from .utils import is_lang_de  # kept import (may be used elsewhere)
from .profiles import MATERIAL_PROFILES  # keep if you show tolerance section
from .languages import tr  # language switch based on Blender UI language


class SNAP_PT_panel(Panel):
    """Main SnapSplit UI panel in the 3D Viewport N-Panel."""
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "SnapSplit"
    bl_label = "SnapSplit"

    @classmethod
    def poll(cls, context):
        # Do not change behavior; only UI text is localized via tr()
        return context is not None and context.scene is not None

    def draw(self, context):
        # Keep structure; only replace texts with tr()
        layout = self.layout
        props = getattr(context.scene, "snapsplit", None)

        if props is None:
            layout.label(text=tr("ui.msg.props_missing", "SnapSplit properties not available."), icon="ERROR")
            layout.label(text=tr("ui.msg.please_reenable", "Please re-enable the Add-on."))
            return

        # =========================
        # SEGMENTATION
        # =========================

        box = layout.box()
        header = box.row(align=True)
        header.label(text=tr("ui.segmentation_title", "Segmentation"), icon='MOD_BOOLEAN')
        more_txt = tr("ui.less", "Less...") if props.ui_more_seg else tr("ui.more_less_more", "More...")
        header.prop(props, "ui_more_seg", text=more_txt, toggle=True)

        col = box.column(align=True)
        col.prop(props, "split_axis", text=tr("ui.split_axis", "Split Axis"))

        row = col.row(align=True)
        row.prop(props, "show_split_preview", text=tr("ui.show_split_preview", "Show split preview"))
        row.operator("snapsplit.adjust_split_axis",
                     icon="EMPTY_AXIS",
                     text=tr("ui.adjust", "Adjust"))

        if props.ui_more_seg:
            adv = box.column(align=True)
            adv.prop(props, "parts_count",
                     text=tr("ui.parts_count", "Number of Parts"))
            try:
                if int(props.parts_count) >= 12:
                    adv.label(icon='INFO',
                              text=tr("ui.high_part_count_slow", "High part count may be slow"))
            except Exception:
                pass
            adv.prop(props, "split_offset_mm",
                     text=tr("ui.split_offset_mm", "Split Offset (mm)"))
            adv.prop(props, "cap_seams_during_split",
                     text=tr("ui.cap_seams_during_split_short", "Cap seams during split (slower)"))

            if not props.cap_seams_during_split:
                sub = adv.column(align=True)
                sub.operator("snapsplit.cap_open_seams_now",
                             icon="OUTLINER_OB_SURFACE",
                             text=tr("op.cap_now.label", "Cap seams now"))
                sub.label(text=tr("ui.cap_seams_hint",
                                  "To close existing seams, run 'Cap seams now'."), icon='INFO')

        col_bottom = box.column(align=True)
        col_bottom.operator("snapsplit.planar_split",
                            icon="MOD_BOOLEAN",
                            text=tr("op.split.label", "Planar Split"))

        layout.separator()

        # =========================
        # CONNECTIONS
        # =========================

        box = layout.box()
        header = box.row(align=True)
        header.label(text=tr("ui.connections_title", "Connections"), icon='SNAP_FACE')
        more_txt = tr("ui.less", "Less...") if props.ui_more_conn else tr("ui.more_less_more", "More...")
        header.prop(props, "ui_more_conn", text=more_txt, toggle=True)

        col = box.column(align=True)
        col.prop(props, "connector_type", text=tr("ui.connector_type", "Connector Type"))
        col.prop(props, "connector_distribution", text=tr("ui.distribution", "Distribution"))

        col = layout.column(align=True)
        col.operator("snapsplit.add_connectors",
                     icon="SNAP_FACE",
                     text=tr("ui.add_connectors", "Add connectors"))
        col.operator("snapsplit.place_connectors_click",
                     icon="CURSOR",
                     text=tr("ui.place_connectors_click", "Place connectors (click)"))

        if props.ui_more_conn:
            adv = box.column(align=True)
            if props.connector_distribution == "LINE":
                adv.prop(props, "connectors_per_seam",
                         text=tr("ui.connectors_per_seam", "Connectors per Seam"))
            else:
                r = adv.row(align=True)
                r.prop(props, "connectors_per_seam",
                       text=tr("ui.columns", "Columns"))
                r.prop(props, "connectors_rows",
                       text=tr("ui.rows", "Rows"))

            adv.prop(props, "connector_margin_pct",
                     text=tr("ui.margin_pct", "Margin (%)"))

            gbox = box.box()

            if props.connector_type in {"CYL_PIN", "SNAP_PIN"}:
                gbox.prop(props, "pin_diameter_mm",
                          text=tr("ui.pin_diameter_mm", "Pin Diameter (mm)"))
                gbox.prop(props, "pin_length_mm",
                          text=tr("ui.pin_length_mm", "Pin Length (mm)"))
                gbox.prop(props, "pin_embed_pct",
                          text=tr("ui.insert_depth_pct", "Insert Depth (%)"))

                rr = gbox.row(align=True)
                rr.prop(props, "pin_segments",
                        text=tr("ui.segments", "Segments"))
                try:
                    from .profiles import _suggest_pin_segments_from_diameter
                    suggested = _suggest_pin_segments_from_diameter(float(getattr(props, "pin_diameter_mm", 5.0)))
                    hint = tr("ui.suggested", "Suggested: ") + f"{suggested}"
                    sub = rr.row(align=True)
                    sub.alignment = 'RIGHT'
                    sub.label(text=hint, icon='INFO')
                except Exception:
                    pass

            elif props.connector_type in {"RECT_TENON", "SNAP_TENON"}:
                gbox.prop(props, "tenon_width_mm",
                          text=tr("ui.tenon_width_mm", "Tenon Width (mm)"))
                gbox.prop(props, "tenon_depth_mm",
                          text=tr("ui.tenon_depth_mm", "Tenon Depth (mm)"))
                gbox.prop(props, "pin_embed_pct",
                          text=tr("ui.insert_depth_pct", "Insert Depth (%)"))
            else:
                gbox.label(text=tr("ui.unsupported_connector_type", "Unsupported connector type"), icon='INFO')

            gbox.prop(props, "add_chamfer_mm",
                      text=tr("ui.chamfer_mm", "Chamfer (mm)"))

            if props.connector_type in {"SNAP_PIN", "SNAP_TENON"}:
                sbox = box.box()
                sbox.label(text=tr("ui.snap_spheres", "Snap spheres"), icon='SPHERE')
                sbox.prop(props, "snap_spheres_per_side",
                          text=tr("ui.spheres_per_side", "Spheres per side"))
                sbox.prop(props, "snap_sphere_diameter_mm",
                          text=tr("ui.sphere_diameter_mm", "Sphere  (mm)"))
                sbox.prop(props, "snap_sphere_protrusion_mm",
                          text=tr("ui.protrusion_mm", "Protrusion (mm)"))

        layout.separator()

        # =========================
        # TOLERANCE
        # =========================

        box = layout.box()
        header = box.row(align=True)
        header.label(text=tr("ui.section.tolerance", "Tolerance"), icon='MOD_SOLIDIFY')
        more_txt = tr("ui.less", "Less...") if props.ui_more_tol else tr("ui.more_less_more", "More...")
        header.prop(props, "ui_more_tol", text=more_txt, toggle=True)

        col = box.column(align=True)
        col.prop(props, "material_profile",
                 text=tr("ui.material_profiles", "Material Profiles"))

        if props.ui_more_tol:
            adv = box.column(align=True)
            row = adv.row(align=True)
            row.prop(props, "tol_override",
                     text=tr("ui.tol_per_face_mm", "Tolerance per Face (mm)"))

            prof_val = MATERIAL_PROFILES.get(props.material_profile, 0.2)
            row = adv.row(align=True)
            row.label(text=tr("ui.profile_value_mm", "Profile: ") + f"{prof_val:.2f} mm")
            try:
                eff_tol = float(props.effective_tolerance())
                row2 = adv.row(align=True)
                row2.label(text=tr("ui.effective_value_mm", "Effective: ") + f"{eff_tol:.2f} mm")
            except Exception:
                pass

        # =========================
        # ALIGNMENT (Object Mode)  collapsible
        # =========================

        box = layout.box()
        header = box.row(align=True)
        header.label(text=tr("ui.section.alignment", "Alignment"), icon='SNAP_ON')

        more_txt = tr("ui.less", "Less...") if props.ui_more_align else tr("ui.more_less_more", "More...")
        header.prop(props, "ui_more_align", text=more_txt, toggle=True)

        if props.ui_more_align:
            col = box.column(align=True)
            col.label(text=tr("ui.pick_faces_hint",
                              "Pick faces in Object Mode (A = target, B = moving)"))

            # Status line for stored picks
            wm = context.window_manager
            nameA = getattr(wm, "snapsplit_face_a_obj", "")
            idxA = getattr(wm, "snapsplit_face_a_index", -1)
            nameB = getattr(wm, "snapsplit_face_b_obj", "")
            idxB = getattr(wm, "snapsplit_face_b_index", -1)

            status_a = (f"{tr('ui.face_a', 'A')}: {nameA} [#{idxA}]" if nameA and idxA >= 0
                        else tr("ui.face_a_none", "A: none"))
            status_b = (f"{tr('ui.face_b', 'B')}: {nameB} [#{idxB}]" if nameB and idxB >= 0
                        else tr("ui.face_b_none", "B: none"))

            stat = box.row(align=True)
            stat.label(text=status_a, icon='INFO')
            stat.label(text=status_b, icon='INFO')
            stat.operator("snapsplit.clear_picks", text="", icon='X')

            row = box.row(align=True)
            row.operator("snapsplit.pick_face_a",
                         text=tr("ui.pick_face_a", "Pick Face A"),
                         icon='MOUSE_LMB')
            row.operator("snapsplit.pick_face_b",
                         text=tr("ui.pick_face_b", "Pick Face B"),
                         icon='MOUSE_LMB')

            # Disable Align until both picks are valid
            can_align = (bool(nameA) and idxA >= 0 and bool(nameB) and idxB >= 0)
            row_align = box.row(align=True)
            row_align.enabled = can_align
            row_align.operator("snapsplit.align_faces",
                               text=tr("ui.align_faces", "Align Faces"),
                               icon='SNAP_ON')

        # =========================
        # Donate
        # =========================

        col = layout.column(align=True)
        col.separator()
        col.operator(
            "wm.url_open",
            text=tr("ui.buy_me_coffee", "Buy me a coffee "),
            icon='FUND').url="https://buymeacoffee.com/betakontext"

        layout.separator()


def register():
    bpy.utils.register_class(SNAP_PT_panel)


def unregister():
    bpy.utils.unregister_class(SNAP_PT_panel)
