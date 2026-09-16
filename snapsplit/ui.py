# -*- coding: utf-8 -*-
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
from .profiles import MATERIAL_PROFILES  # used for tolerance preview
from .languages import tr  # language switch based on Blender UI language


def _exists(obj, attr):
    """Small helper to guard missing properties in early integration phases."""
    try:
        getattr(obj, attr)
        return True
    except Exception:
        return False


class SNAP_PT_panel(Panel):
    """Main SnapSplit UI panel in the 3D Viewport N-Panel."""
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "SnapSplit"
    bl_label = "SnapSplit"

    @classmethod
    def poll(cls, context):
        # Keep enabled as long as a scene exists.
        return context is not None and context.scene is not None

    def draw(self, context):
        # Draw localized UI using tr(); do not alter underlying behavior.
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
        more_txt = tr("ui.less", "Less...") if getattr(props, "ui_more_seg", False) else tr("ui.more_less_more", "More...")
        if _exists(props, "ui_more_seg"):
            header.prop(props, "ui_more_seg", text=more_txt, toggle=True)

        col = box.column(align=True)
        if _exists(props, "split_axis"):
            col.prop(props, "split_axis", text=tr("ui.split_axis", "Split Axis"))

        row = col.row(align=True)
        if _exists(props, "show_split_preview"):
            row.prop(props, "show_split_preview", text=tr("ui.show_split_preview", "Show split preview"))
        row.operator("snapsplit.adjust_split_axis",
                     icon="EMPTY_AXIS",
                     text=tr("ui.adjust", "Adjust"))

        if getattr(props, "ui_more_seg", False):
            adv = box.column(align=True)
            if _exists(props, "parts_count"):
                adv.prop(props, "parts_count", text=tr("ui.parts_count", "Number of Parts"))
                try:
                    if int(getattr(props, "parts_count")) >= 12:
                        adv.label(icon='INFO', text=tr("ui.high_part_count_slow", "High part count may be slow"))
                except Exception:
                    pass
            if _exists(props, "split_offset_mm"):
                adv.prop(props, "split_offset_mm", text=tr("ui.split_offset_mm", "Split Offset (mm)"))
            if _exists(props, "cap_seams_during_split"):
                adv.prop(props, "cap_seams_during_split",
                         text=tr("ui.cap_seams_during_split_short", "Cap seams during split (slower)"))
                if not getattr(props, "cap_seams_during_split", False):
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
        more_txt = tr("ui.less", "Less...") if getattr(props, "ui_more_conn", False) else tr("ui.more_less_more", "More...")
        if _exists(props, "ui_more_conn"):
            header.prop(props, "ui_more_conn", text=more_txt, toggle=True)

        col = box.column(align=True)
        if _exists(props, "connector_type"):
            col.prop(props, "connector_type", text=tr("ui.connector_type", "Connector Type"))
        if _exists(props, "connector_distribution"):
            col.prop(props, "connector_distribution", text=tr("ui.distribution", "Distribution"))

        # Action buttons
        col = layout.column(align=True)
        col.operator("snapsplit.add_connectors", icon="SNAP_FACE", text=tr("ui.add_connectors", "Add connectors"))
        col.operator("snapsplit.place_connectors_click", icon="CURSOR", text=tr("ui.place_connectors_click", "Place connectors (click)"))

        if getattr(props, "ui_more_conn", False):
            adv = box.column(align=True)
            dist = getattr(props, "connector_distribution", "LINE")
            if dist == "LINE":
                if _exists(props, "connectors_per_seam"):
                    adv.prop(props, "connectors_per_seam", text=tr("ui.connectors_per_seam", "Connectors per Seam"))
            else:
                r = adv.row(align=True)
                if _exists(props, "connectors_per_seam"):
                    r.prop(props, "connectors_per_seam", text=tr("ui.columns", "Columns"))
                if _exists(props, "connectors_rows"):
                    r.prop(props, "connectors_rows", text=tr("ui.rows", "Rows"))

            if _exists(props, "connector_margin_pct"):
                adv.prop(props, "connector_margin_pct", text=tr("ui.margin_pct", "Margin (%)"))

            # Connector-specific geometry/settings
            gbox = box.box()
            ctype = getattr(props, "connector_type", "CYL_PIN")

            # --- Pin-like connectors ---
            if ctype in {"CYL_PIN", "SNAP_PIN", "SNAP_FLUSH_PIN"}:
                if _exists(props, "pin_diameter_mm"):
                    gbox.prop(props, "pin_diameter_mm", text=tr("ui.pin_diameter_mm", "Pin Diameter (mm)"))
                if _exists(props, "pin_length_mm"):
                    gbox.prop(props, "pin_length_mm", text=tr("ui.pin_length_mm", "Pin Length (mm)"))
                if _exists(props, "pin_embed_pct"):
                    gbox.prop(props, "pin_embed_pct", text=tr("ui.insert_depth_pct", "Insert Depth (%)"))

                rr = gbox.row(align=True)
                if _exists(props, "pin_segments"):
                    rr.prop(props, "pin_segments", text=tr("ui.segments", "Segments"))
                try:
                    from .profiles import _suggest_pin_segments_from_diameter
                    diameter = float(getattr(props, "pin_diameter_mm", 5.0))
                    suggested = _suggest_pin_segments_from_diameter(diameter)
                    hint = tr("ui.suggested", "Suggested: ") + f"{suggested}"
                    sub = rr.row(align=True)
                    sub.alignment = 'RIGHT'
                    sub.label(text=hint, icon='INFO')
                except Exception:
                    pass

                if ctype in {"CYL_PIN", "SNAP_PIN"} and _exists(props, "add_chamfer_mm"):
                    gbox.prop(props, "add_chamfer_mm", text=tr("ui.chamfer_mm", "Chamfer (mm)"))


                if ctype == "SNAP_PIN" and _exists(props, "snap_spheres_per_side"):
                    s = gbox.column(align=True)
                    s.label(text=tr("ui.snap_group", "Snap spheres:"), icon='MESH_ICOSPHERE')
                    s.prop(props, "snap_spheres_per_side", text=tr("ui.snap_spheres_per_side", "Spheres per side"))
                    if _exists(props, "snap_sphere_diameter_mm"):
                        s.prop(props, "snap_sphere_diameter_mm", text=tr("ui.snap_sphere_diameter_mm", "Sphere Diameter (mm)"))
                    if _exists(props, "snap_sphere_protrusion_mm"):
                        s.prop(props, "snap_sphere_protrusion_mm", text=tr("ui.snap_sphere_protrusion_mm", "Protrusion (mm)"))

                if ctype == "SNAP_FLUSH_PIN":
                    s = gbox.column(align=True)
                    s.label(text=tr("ui.flush_group", "Flush snap (barb near seam):"), icon='MOD_SOLIDIFY')
                    if _exists(props, "flush_barb_height_mm"):
                        s.prop(props, "flush_barb_height_mm", text=tr("ui.flush_barb_height_mm", "Barb Height (mm)"))
                    if _exists(props, "flush_barb_lip_mm"):
                        s.prop(props, "flush_barb_lip_mm", text=tr("ui.flush_barb_lip_mm", "Barb Lip (mm)"))

            # --- Tenon-like connectors ---
            elif ctype in {"RECT_TENON", "SNAP_TENON", "SNAP_FLUSH_TENON"}:
                if _exists(props, "tenon_width_mm"):
                    gbox.prop(props, "tenon_width_mm", text=tr("ui.tenon_width_mm", "Tenon Width (mm)"))
                if _exists(props, "tenon_depth_mm"):
                    gbox.prop(props, "tenon_depth_mm", text=tr("ui.tenon_depth_mm", "Tenon Depth (mm)"))
                if _exists(props, "pin_embed_pct"):
                    gbox.prop(props, "pin_embed_pct", text=tr("ui.insert_depth_pct", "Insert Depth (%)"))

                if ctype in {"RECT_TENON", "SNAP_TENON"} and _exists(props, "add_chamfer_mm"):
                    gbox.prop(props, "add_chamfer_mm", text=tr("ui.chamfer_mm", "Chamfer (mm)"))


                if ctype == "SNAP_TENON" and _exists(props, "snap_spheres_per_side"):
                    s = gbox.column(align=True)
                    s.label(text=tr("ui.snap_group", "Snap spheres:"), icon='MESH_ICOSPHERE')
                    s.prop(props, "snap_spheres_per_side", text=tr("ui.snap_spheres_per_side", "Spheres per side"))
                    if _exists(props, "snap_sphere_diameter_mm"):
                        s.prop(props, "snap_sphere_diameter_mm", text=tr("ui.snap_sphere_diameter_mm", "Sphere Diameter (mm)"))
                    if _exists(props, "snap_sphere_protrusion_mm"):
                        s.prop(props, "snap_sphere_protrusion_mm", text=tr("ui.snap_sphere_protrusion_mm", "Protrusion (mm)"))

                if ctype == "SNAP_FLUSH_TENON":
                    s = gbox.column(align=True)
                    s.label(text=tr("ui.flush_group", "Flush snap (barb near seam):"), icon='MOD_SOLIDIFY')
                    if _exists(props, "flush_barb_height_mm"):
                        s.prop(props, "flush_barb_height_mm", text=tr("ui.flush_barb_height_mm", "Barb Height (mm)"))
                    if _exists(props, "flush_barb_lip_mm"):
                        s.prop(props, "flush_barb_lip_mm", text=tr("ui.flush_barb_lip_mm", "Barb Lip (mm)"))

            # --- Dovetail connector ---
            # NOTE: extended from "ctype == \"DOVETAIL\"" to also cover the new
            # Snap Dovetail connector, which shares the exact same wedge geometry
            # (Base size, Signed Taper, Span Axis, Hard-side Cut, Placement).
            elif ctype in {"DOVETAIL", "SNAP_DOVETAIL"}:
                # Base size group  ordered: Width  Length  Depth
                base_box = gbox.box()
                base_box.label(text=tr("ui.dovetail_base", "Base size"), icon='MESH_CUBE')
                if _exists(props, "dovetail_width_mm"):
                    base_box.prop(props, "dovetail_width_mm", text=tr("ui.dovetail_width_mm", "Dovetail Width (mm)"))
                # CRITICAL: Explicit Dovetail Length in UI
                if _exists(props, "dovetail_length_mm"):
                    base_box.prop(props, "dovetail_length_mm", text=tr("ui.dovetail_length_mm", "Dovetail Length (mm)"))
                if _exists(props, "dovetail_depth_mm"):
                    base_box.prop(props, "dovetail_depth_mm", text=tr("ui.dovetail_depth_mm", "Dovetail Depth (mm)"))
                if _exists(props, "add_chamfer_mm"):
                    base_box.prop(props, "add_chamfer_mm", text=tr("ui.chamfer_mm", "Chamfer (mm)"))

                # Taper (signed) comes next

                if _exists(props, "dovetail_signed_taper_pct"):
                    base_box.prop(props, "dovetail_signed_taper_pct", text=tr("ui.dovetail_signed_taper_pct", "Signed Taper (%)"))

                if _exists(props, "dovetail_span_axis"):
                    base_box.prop(props, "dovetail_span_axis", text=tr("ui.dovetail_span_axis", "Span Axis"))
                    if str(getattr(props, "dovetail_span_axis", "NONE")) != "NONE":
                        base_box.label(text=tr("ui.span_axis_hint", "Forces hard-side cut along this axis."), icon='INFO')


                 # Hard-side Cut
                if _exists(props, "dovetail_hard_side_cut"):
                    base_box.prop(props, "dovetail_hard_side_cut", text=tr("ui.dovetail_hard_side_cut", "Hard-side Cut"))

                # NEW: Snap Options box, only shown for the Snap Dovetail variant.
                # Same label/prop pattern as SNAP_PIN / SNAP_TENON so the panel
                # stays visually consistent across all snap-capable connectors.
                if ctype == "SNAP_DOVETAIL" and _exists(props, "snap_spheres_per_side"):
                    s = gbox.box()
                    s.label(text=tr("ui.snap_group", "Snap spheres:"), icon='MESH_ICOSPHERE')
                    s.prop(props, "snap_spheres_per_side", text=tr("ui.snap_spheres_per_side", "Spheres per side"))
                    if _exists(props, "snap_sphere_diameter_mm"):
                        s.prop(props, "snap_sphere_diameter_mm", text=tr("ui.snap_sphere_diameter_mm", "Sphere Diameter (mm)"))
                    if _exists(props, "snap_sphere_protrusion_mm"):
                        s.prop(props, "snap_sphere_protrusion_mm", text=tr("ui.snap_sphere_protrusion_mm", "Protrusion (mm)"))

                # Span options after taper
                # span_box = gbox.box()
                # span_box.label(text=tr("ui.dovetail_span", "Span along seam"), icon='ORIENTATION_GLOBAL')
                # if _exists(props, "dovetail_span_mode"):
                #     span_box.prop(props, "dovetail_span_mode", text=tr("ui.dovetail_span_mode", "Span Mode"))
                # if _exists(props, "dovetail_margin_pct"):
                #     span_box.prop(props, "dovetail_margin_pct", text=tr("ui.dovetail_margin_pct", "Margin (%)"))
                # if _exists(props, "dovetail_auto_span"):
                #     span_box.prop(props, "dovetail_auto_span", text=tr("ui.dovetail_auto_span", "Auto span along seam"))
                # if _exists(props, "dovetail_span_margin_pct"):
                #     span_box.prop(props, "dovetail_span_margin_pct", text=tr("ui.dovetail_span_margin_pct", "Auto-span End Margin (%)"))
                # span_box.label(text=tr("ui.auto_span_hint", "AUTO span = edge-to-edge along seam; # margin trims ends."), icon='INFO')

                # Placement
                extra = gbox.box()
                # extra.label(text=tr("ui.dovetail_extra", "Placement & Sides"),  icon='ORIENTATION_GIMBAL')
                # In-plane placement controls (offsets along width/length + rotation)
                # Ensures "Rotation in plane" is visible; ops already apply it in placement and preview.
                extra.label(text=tr("ui.dovetail_extra", "Placement"), icon='ORIENTATION_GLOBAL')
                if _exists(props, "dovetail_inplane_offset_u_mm") or _exists(props, "dovetail_inplane_offset_v_mm") or _exists(props, "dovetail_inplane_rotation_deg"):
                    s = gbox.box()
                    if _exists(props, "dovetail_inplane_offset_u_mm"):
                        s.prop(props, "dovetail_inplane_offset_u_mm", text=tr("ui.inplane_offset_u_mm", "Offset along Width (mm)"))
                    if _exists(props, "dovetail_inplane_offset_v_mm"):
                        s.prop(props, "dovetail_inplane_offset_v_mm", text=tr("ui.inplane_offset_v_mm", "Offset along Length (mm)"))
                    if _exists(props, "dovetail_inplane_rotation_deg"):
                        s.prop(props, "dovetail_inplane_rotation_deg", text=tr("ui.inplane_rotation_deg", "Rotation in plane (deg)"))

            # --- Custom connector ---
            elif ctype == "CUSTOM":
                if _exists(props, "custom_connector_object"):
                    gbox.prop(props, "custom_connector_object", text=tr("ui.custom_connector_object", "Select connector object"))
                if _exists(props, "custom_connector_width_mm"):
                    gbox.prop(props, "custom_connector_width_mm", text=tr("ui.custom_connector_width_mm", "Custom Width (mm)"))
                if _exists(props, "custom_connector_length_mm"):
                    gbox.prop(props, "custom_connector_length_mm", text=tr("ui.custom_connector_length_mm", "Custom Length (mm)"))
                if _exists(props, "custom_connector_depth_mm"):
                    gbox.prop(props, "custom_connector_depth_mm", text=tr("ui.custom_connector_depth_mm", "Custom Depth (mm)"))
                if _exists(props, "pin_embed_pct"):
                    gbox.prop(props, "pin_embed_pct", text=tr("ui.insert_depth_pct", "Insert Depth (%)"))

            else:
                gbox.label(text=tr("ui.unsupported_connector_type", "Unsupported connector type"), icon='INFO')

        layout.separator()

        # =========================
        # TOLERANCE
        # =========================

        box = layout.box()
        header = box.row(align=True)
        header.label(text=tr("ui.section.tolerance", "Tolerance"), icon='MOD_SOLIDIFY')
        more_txt = tr("ui.less", "Less...") if getattr(props, "ui_more_tol", False) else tr("ui.more_less_more", "More...")
        if _exists(props, "ui_more_tol"):
            header.prop(props, "ui_more_tol", text=more_txt, toggle=True)

        col = box.column(align=True)
        if _exists(props, "material_profile"):
            col.prop(props, "material_profile", text=tr("ui.material_profiles", "Material Profiles"))

        if getattr(props, "ui_more_tol", False):
            adv = box.column(align=True)
            if _exists(props, "tol_override"):
                row = adv.row(align=True)
                row.prop(props, "tol_override", text=tr("ui.tol_per_face_mm", "Tolerance per Face (mm)"))

            # Profile numeric hint
            try:
                prof_key = getattr(props, "material_profile", None)
                prof_val = MATERIAL_PROFILES.get(prof_key, 0.2)
                row = adv.row(align=True)
                row.label(text=tr("ui.profile_value_mm", "Profile: ") + f"{prof_val:.2f} mm")
            except Exception:
                pass

            # Effective tolerance
            try:
                if hasattr(props, "effective_tolerance") and callable(props.effective_tolerance):
                    eff_tol = float(props.effective_tolerance())
                    row2 = adv.row(align=True)
                    row2.label(text=tr("ui.effective_value_mm", "Effective: ") + f"{eff_tol:.2f} mm")
            except Exception:
                pass

            # Short print-fit hint
            adv.label(text=tr("ui.tolerance_hint",
                              "For tight fit, reduce tolerance; for easy assembly, increase."), icon='INFO')

        # =========================
        # ALIGNMENT (Object Mode)
        # =========================

        box = layout.box()
        header = box.row(align=True)
        header.label(text=tr("ui.section.alignment", "Alignment"), icon='SNAP_ON')

        more_txt = tr("ui.less", "Less...") if getattr(props, "ui_more_align", False) else tr("ui.more_less_more", "More...")
        if _exists(props, "ui_more_align"):
            header.prop(props, "ui_more_align", text=more_txt, toggle=True)

        if getattr(props, "ui_more_align", False):
            col = box.column(align=True)
            col.label(text=tr("ui.pick_faces_hint", "Pick faces in Object Mode (A = target, B = moving)"))

            wm = context.window_manager
            nameA = getattr(wm, "snapsplit_face_a_obj", "")
            idxA = getattr(wm, "snapsplit_face_a_index", -1)
            nameB = getattr(wm, "snapsplit_face_b_obj", "")
            idxB = getattr(wm, "snapsplit_face_b_index", -1)

            status_a = (f"{tr('ui.face_a', 'A')}: {nameA} [#{idxA}]" if nameA and idxA >= 0 else tr("ui.face_a_none", "A: none"))
            status_b = (f"{tr('ui.face_b', 'B')}: {nameB} [#{idxB}]" if nameB and idxB >= 0 else tr("ui.face_b_none", "B: none"))

            stat = box.row(align=True)
            stat.label(text=status_a, icon='INFO')
            stat.label(text=status_b, icon='INFO')
            stat.operator("snapsplit.clear_picks", text="", icon='X')

            row = box.row(align=True)
            row.operator("snapsplit.pick_face_a", text=tr("ui.pick_face_a", "Pick Face A"), icon='MOUSE_LMB')
            row.operator("snapsplit.pick_face_b", text=tr("ui.pick_face_b", "Pick Face B"), icon='MOUSE_LMB')

            can_align = (bool(nameA) and idxA >= 0 and bool(nameB) and idxB >= 0)
            row_align = box.row(align=True)
            row_align.enabled = can_align
            row_align.operator("snapsplit.align_faces", text=tr("ui.align_faces", "Align Faces"), icon='SNAP_ON')

        # =========================
        # Donate
        # =========================

        col = layout.column(align=True)
        col.separator()
        op = col.operator("wm.url_open", text=tr("ui.buy_me_coffee", "Buy me a coffee "), icon='FUND')
        op.url = "https://buymeacoffee.com/betakontext"
        layout.separator()


def register():
    """Register panel class with Blender."""
    bpy.utils.register_class(SNAP_PT_panel)


def unregister():
    """Unregister panel class from Blender."""
    bpy.utils.unregister_class(SNAP_PT_panel)

