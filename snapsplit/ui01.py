# ui.py
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

import bpy
from bpy.types import Panel
from .utils import is_lang_de
from .profiles import MATERIAL_PROFILES  # used for tolerance display

class SNAP_PT_panel(Panel):
    """Main SnapSplit UI panel in the 3D Viewport N-Panel."""
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "SnapSplit"
    bl_label = "SnapSplit"

    @classmethod
    def poll(cls, context):
        return context is not None and context.scene is not None

    def draw(self, context):
        _DE = is_lang_de()
        layout = self.layout
        props = getattr(context.scene, "snapsplit", None)

        if props is None:
            layout.label(text=("SnapSplit properties not available." if not _DE
                               else "SnapSplit-Eigenschaften nicht verfügbar."),
                         icon="ERROR")
            layout.label(text=("Please re-enable the Add-on." if not _DE
                               else "Bitte das Add-on erneut aktivieren."))
            return

        # =========================
        # SEGMENTATION
        # =========================

        box = layout.box()
        header = box.row(align=True)
        header.label(text=("Segmentation" if not _DE else "Segmentierung"), icon='MOD_BOOLEAN')
        more_txt = ("Less..." if props.ui_more_seg else "More...") if not _DE else ("Weniger..." if props.ui_more_seg else "Mehr...")
        header.prop(props, "ui_more_seg", text=more_txt, toggle=True)

        col = box.column(align=True)
        col.prop(props, "split_axis", text=("Split Axis" if not _DE else "Schnittachse"))

        row = col.row(align=True)
        row.prop(props, "show_split_preview", text=("Show split preview" if not _DE else "Schnittvorschau anzeigen"))
        row.operator("snapsplit.adjust_split_axis",
                     icon="EMPTY_AXIS",
                     text=("Adjust" if not _DE else "Anpassen"))

        if props.ui_more_seg:
            adv = box.column(align=True)
            adv.prop(props, "parts_count",
                     text=("Number of Parts" if not _DE else "Anzahl Teile"))
            try:
                if int(props.parts_count) >= 12:
                    adv.label(icon='INFO',
                              text=("High part count may be slow" if not _DE else "Hohe Teilzahl kann langsam sein"))
            except Exception:
                pass
            adv.prop(props, "split_offset_mm",
                     text=("Split Offset (mm)" if not _DE else "Schnitt-Offset (mm)"))
            adv.prop(props, "cap_seams_during_split",
                     text=("Cap seams during split (slower)" if not _DE else "Nähte beim Schnitt schließen (langsamer)"))

            if not props.cap_seams_during_split:
                sub = adv.column(align=True)
                sub.operator("snapsplit.cap_open_seams_now",
                             icon="OUTLINER_OB_SURFACE",
                             text=("Cap seams now" if not _DE else "Nähte jetzt schließen"))
                sub.label(text=("To close existing seams, run 'Cap seams now'."
                                if not _DE else "Bestehende Nähte mit 'Nähte jetzt schließen' füllen."),
                          icon='INFO')

        col_bottom = box.column(align=True)
        col_bottom.operator("snapsplit.planar_split",
                            icon="MOD_BOOLEAN",
                            text=("Planar Split" if not _DE else "Planarer Schnitt"))

        layout.separator()

        # =========================
        # CONNECTIONS
        # =========================

        box = layout.box()
        header = box.row(align=True)
        header.label(text=("Connections" if not _DE else "Verbindungen"), icon='SNAP_FACE')
        more_txt = ("Less..." if props.ui_more_conn else "More...") if not _DE else ("Weniger..." if props.ui_more_conn else "Mehr...")
        header.prop(props, "ui_more_conn", text=more_txt, toggle=True)

        col = box.column(align=True)
        col.prop(props, "connector_type", text=("Connector Type" if not _DE else "Verbinder-Typ"))
        col.prop(props, "connector_distribution", text=("Distribution" if not _DE else "Verteilung"))

        col = layout.column(align=True)
        col.operator("snapsplit.add_connectors",
                     icon="SNAP_FACE",
                     text=("Add connectors" if not _DE else "Verbinder hinzufügen"))
        col.operator("snapsplit.place_connectors_click",
                     icon="CURSOR",
                     text=("Place connectors (click)" if not _DE else "Verbinder per Klick"))

        if props.ui_more_conn:
            adv = box.column(align=True)
            if props.connector_distribution == "LINE":
                adv.prop(props, "connectors_per_seam",
                         text=("Connectors per Seam" if not _DE else "Verbinder pro Naht"))
            else:
                r = adv.row(align=True)
                r.prop(props, "connectors_per_seam",
                       text=("Columns" if not _DE else "Spalten"))
                r.prop(props, "connectors_rows",
                       text=("Rows" if not _DE else "Reihen"))

            adv.prop(props, "connector_margin_pct",
                     text=("Margin (%)" if not _DE else "Randabstand (%)"))
            adv.prop(props, "edge_margin_mm",
                     text=("Edge margin (mm)" if not _DE else "Randabstand (mm)"))

            gbox = box.box()

            # Existing families (CYL_PIN / SNAP_PIN / RECT_TENON / SNAP_TENON)
            if props.connector_type in {"CYL_PIN", "SNAP_PIN"}:
                gbox.prop(props, "pin_diameter_mm",
                          text=("Pin Diameter (mm)" if not _DE else "Pin-Durchmesser (mm)"))
                gbox.prop(props, "pin_length_mm",
                          text=("Pin Length (mm)" if not _DE else "Pin-Länge (mm)"))
                gbox.prop(props, "pin_embed_pct",
                          text=("Insert Depth (%)" if not _DE else "Einstecktiefe (%)"))

                rr = gbox.row(align=True)
                rr.prop(props, "pin_segments",
                        text=("Segments" if not _DE else "Segmente"))
                try:
                    from .profiles import _suggest_pin_segments_from_diameter
                    suggested = _suggest_pin_segments_from_diameter(float(getattr(props, "pin_diameter_mm", 5.0)))
                    hint = f"Suggested: {suggested}" if not _DE else f"Vorschlag: {suggested}"
                    sub = rr.row(align=True)
                    sub.alignment = 'RIGHT'
                    sub.label(text=hint, icon='INFO')
                except Exception:
                    pass

            elif props.connector_type in {"RECT_TENON", "SNAP_TENON"}:
                gbox.prop(props, "tenon_width_mm",
                          text=("Tenon Width (mm)" if not _DE else "Zapfen-Breite (mm)"))
                gbox.prop(props, "tenon_depth_mm",
                          text=("Tenon Depth (mm)" if not _DE else "Zapfen-Tiefe (mm)"))
                gbox.prop(props, "pin_embed_pct",
                          text=("Insert Depth (%)" if not _DE else "Einstecktiefe (%)"))

            # New families UI
            if props.connector_type == "PIN_HOLE":
                pbox = box.box()
                pbox.label(text=("Pin & Hole (fit modes)" if not _DE else "Pin & Bohrung (Passungen)"), icon='MESH_CYLINDER')
                pbox.prop(props, "pin_diameter_mm",
                          text=("Pin Diameter (mm)" if not _DE else "Pin-Durchmesser (mm)"))
                pbox.prop(props, "pin_length_mm",
                          text=("Pin Length (mm)" if not _DE else "Pin-Länge (mm)"))
                pbox.prop(props, "pin_embed_pct",
                          text=("Insert Depth (%)" if not _DE else "Einstecktiefe (%)"))
                pbox.prop(props, "pin_segments",
                          text=("Segments" if not _DE else "Segmente"))
                pbox.prop(props, "add_chamfer_mm",
                          text=("Chamfer (mm)" if not _DE else "Fase (mm)"))
                pbox.prop(props, "pin_fit_mode",
                          text=("Fit mode" if not _DE else "Passung"))
                pbox.prop(props, "pin_hole_only",
                          text=("Hole only (for metal pins)" if not _DE else "Nur Bohrung (für Metallstifte)"))
                tip = "Chamfer helps compensate elephant's foot" if not _DE else "Fase kompensiert Elephant's Foot"
                pbox.label(text=tip, icon='INFO')

            if props.connector_type == "DOVETAIL_TAPER":
                dbox = box.box()
                dbox.label(text=("Dovetail (tapered)" if not _DE else "Schwalbenschwanz (mit Schräge)"), icon='MOD_SIMPLEDEFORM')

                # Core fields (Length/Depth/Width/Draft)

                core_row1 = dbox.row(align=True)
                en_len = not (props.dovetail_use_full_span or props.dovetail_auto_fit == "FIT_LENGTH")
                sub_len = core_row1.row(align=True)
                sub_len.enabled = en_len
                sub_len.prop(props, "dovetail_length_mm", text=("Length (mm)" if not _DE else "Länge (mm)"))
                core_row1.prop(props, "dovetail_depth_mm", text=("Depth (mm)" if not _DE else "Tiefe (mm)"))
                core_row2 = dbox.row(align=True)
                en_wid = not (props.dovetail_auto_fit == "FIT_WIDTH")
                sub_wid = core_row2.row(align=True)
                sub_wid.enabled = en_wid
                sub_wid.prop(props, "dovetail_width_mm", text=("Width (mm)" if not _DE else "Breite (mm)"))
                dbox.prop(props, "dovetail_draft_deg", text=("Draft (°)" if not _DE else "Schräge (°)"))

                # Advanced
                dmore = dbox.column(align=True)
                dmore.prop(props, "dovetail_proportional_enabled", text=("Proportional scaling" if not _DE else "Proportionale Skalierung"))
                dmore.prop(props, "dovetail_master_dim", text=("Master dimension" if not _DE else "Leitmaß"))
                dmore.prop(props, "dovetail_auto_fit", text=("Auto-fit" if not _DE else "Auto-Anpassung"))
                dmore.prop(props, "dovetail_use_full_span", text=("Use full edge length" if not _DE else "Über gesamte Kantenlänge"))
                if props.dovetail_use_full_span or props.dovetail_auto_fit in {"FIT_LENGTH","FIT_WIDTH"}:
                    dmore.prop(props, "dovetail_end_inset_mm", text=("End inset (mm)" if not _DE else "Randabzug (mm)"))
                    dmore.prop(props, "dovetail_span_orientation", text=("Span orientation" if not _DE else "Spanausrichtung"))

                # Width/Depth fit modes (20%-Schalter)
                wbox = dbox.box()
                wbox.label(text=("Width/Depth auto-sizing" if not _DE else "Breite/Tiefe automatisch"), icon='ARROW_LEFTRIGHT')
                wrow = wbox.row(align=True)
                wrow.prop(props, "dovetail_fit_width_mode", text=("Width mode" if not _DE else "Breitenmodus"))
                if props.dovetail_fit_width_mode == "PERCENT_SHORT":
                    wrow2 = wbox.row(align=True)
                    wrow2.prop(props, "dovetail_fit_width_pct", text=("Width %" if not _DE else "Breite %"))
                drow = wbox.row(align=True)
                drow.prop(props, "dovetail_fit_depth_mode", text=("Depth mode" if not _DE else "Tiefenmodus"))
                if props.dovetail_fit_depth_mode == "PERCENT_SHORT":
                    drow2 = wbox.row(align=True)
                    drow2.prop(props, "dovetail_fit_depth_pct", text=("Depth %" if not _DE else "Tiefe %"))

                dmore.prop(props, "dovetail_leadin_chamfer_mm", text=("Lead-in chamfer (mm)" if not _DE else "Einführfase (mm)"))
                dmore.prop(props, "dovetail_clearance_scale", text=("Clearance scale" if not _DE else "Spiel-Skalierung"))
                dmore.prop(props, "dovetail_slide_dir", text=("Slide direction" if not _DE else "Schieberichtung"))

                tip = "Use 1–2° taper for progressive friction." if not _DE else "1–2° Schräge für progressiven Sitz."
                dbox.label(text=tip, icon='INFO')
                if props.dovetail_use_full_span:
                    dbox.label(text=("Length uses full seam span minus margins and inset."
                                     if not _DE else "Länge nutzt volle Nahtlaufweite abzüglich Ränder und Randabzug."), icon='INFO')

            if props.connector_type == "SNAP_CANTILEVER":
                sbox = box.box()
                sbox.label(text=("Snap-Fit (Cantilever)" if not _DE else "Schnapphaken (Kragarm)"), icon='MOD_BUILD')
                sbox.prop(props, "snap_cant_arm_len_mm", text=("Arm length (mm)" if not _DE else "Armlänge (mm)"))
                sbox.prop(props, "snap_cant_arm_thk_mm", text=("Arm thickness (mm)" if not _DE else "Armdicke (mm)"))
                sbox.prop(props, "snap_cant_hook_undercut_mm", text=("Hook undercut (mm)" if not _DE else "Hinterschneidung (mm)"))
                sbox.prop(props, "snap_cant_fillet_mm", text=("Base fillet (mm)" if not _DE else "Grundradius (mm)"))
                smore = sbox.column(align=True)
                smore.prop(props, "snap_cant_arm_w_mm", text=("Arm width (mm)" if not _DE else "Armbreite (mm)"))
                smore.prop(props, "snap_cant_stop_offset_mm", text=("Stop offset (mm)" if not _DE else "Anschlag (mm)"))
                smore.prop(props, "snap_cant_leadin_chamfer_mm", text=("Lead-in chamfer (mm)" if not _DE else "Einführfase (mm)"))
                smore.prop(props, "snap_cant_clearance_scale", text=("Clearance scale" if not _DE else "Spiel-Skalierung"))
                if props.material_profile == "PLA":
                    warn = "PLA is brittle for snap-fits; prefer PETG or tough resin." if not _DE else "PLA ist spröde für Schnapphaken; PETG oder zähe Harze bevorzugen."
                    sbox.label(text=warn, icon='INFO')

            if props.connector_type == "BALL_SOCKET":
                bsb = box.box()
                bsb.label(text=("Ball & Socket" if not _DE else "Kugel & Schale"), icon='SPHERE')
                bsb.prop(props, "ball_diameter_mm", text=("Ball Ø (mm)" if not _DE else "Kugel-Ø (mm)"))
                bsb.prop(props, "ball_friction_target", text=("Friction" if not _DE else "Reibung"))
                bmore = bsb.column(align=True)
                bmore.prop(props, "ball_socket_clearance_mm", text=("Socket clearance (mm)" if not _DE else "Buchsen-Spiel (mm)"))
                bmore.prop(props, "ball_lip_thickness_mm", text=("Retention lip (mm)" if not _DE else "Halte-Lippe (mm)"))
                bmore.prop(props, "ball_socket_open_angle_deg", text=("Open angle (°)" if not _DE else "Öffnungswinkel (°)"))
                bmore.prop(props, "ball_leadin_fillet_mm", text=("Lead-in fillet (mm)" if not _DE else "Einführ-Radius (mm)"))
                tip = "Use wear-resistant materials (PETG, tough resin)." if not _DE else "Verschleißfeste Materialien verwenden (PETG, zähes Harz)."
                bsb.label(text=tip, icon='INFO')

            if props.connector_type == "PIP_HINGE":
                hib = box.box()
                hib.label(text=("Print-in-Place Hinge" if not _DE else "Druckbares Scharnier (PiP)"), icon='MOD_SKIN')
                hib.prop(props, "pip_hinge_type", text=("Hinge type" if not _DE else "Scharnier-Typ"))
                hib.prop(props, "pip_gap_mm", text=("PIP gap (mm)" if not _DE else "PIP-Spalt (mm)"))
                hib.prop(props, "pip_hinge_width_mm", text=("Hinge width (mm)" if not _DE else "Scharnier-Breite (mm)"))
                hmore = hib.column(align=True)
                hmore.prop(props, "pip_hinge_thickness_mm", text=("Thickness (mm)" if not _DE else "Dicke (mm)"))
                hmore.prop(props, "pip_segments_count", text=("Segments" if not _DE else "Segmente"))
                hmore.prop(props, "pip_relief_fillet_mm", text=("Relief fillet (mm)" if not _DE else "Entlastungs-Radius (mm)"))
                tip = "Print-in-place requires excellent calibration; test a small sample first." if not _DE else "PiP erfordert sehr gute Kalibrierung; zuerst ein kleines Muster testen."
                hib.label(text=tip, icon='INFO')
                if props.material_profile == "PLA" and props.pip_hinge_type == "living_web":
                    warn = "PLA prone to fatigue/breakage in living hinges." if not _DE else "PLA neigt bei Living Hinges zu Ermüdung/Bruch."
                    hib.label(text=warn, icon='INFO')

            # Global chamfer
            gbox.prop(props, "add_chamfer_mm",
                      text=("Chamfer (mm)" if not _DE else "Fase (mm)"))

            # Snap spheres block
            if props.connector_type in {"SNAP_PIN", "SNAP_TENON"}:
                sbox = box.box()
                sbox.label(text=("Snap spheres" if not _DE else "Schnapp-Sphären"), icon='SPHERE')
                sbox.prop(props, "snap_spheres_per_side",
                          text=("Spheres per side" if not _DE else "Sphären je Seite"))
                sbox.prop(props, "snap_sphere_diameter_mm",
                          text=("Sphere Ø (mm)" if not _DE else "Sphären-Ø (mm)"))
                sbox.prop(props, "snap_sphere_protrusion_mm",
                          text=("Protrusion (mm)" if not _DE else "Überstand (mm)"))

        layout.separator()

        # =========================
        # TOLERANCE
        # =========================

        box = layout.box()
        header = box.row(align=True)
        header.label(text=("Tolerance" if not _DE else "Toleranz"), icon='MOD_SOLIDIFY')
        more_txt = ("Less..." if props.ui_more_tol else "More...") if not _DE else ("Weniger..." if props.ui_more_tol else "Mehr...")
        header.prop(props, "ui_more_tol", text=more_txt, toggle=True)

        col = box.column(align=True)
        col.prop(props, "material_profile",
                 text=("Material Profiles" if not _DE else "Material-Profile"))

        if props.ui_more_tol:
            adv = box.column(align=True)
            row = adv.row(align=True)
            row.prop(props, "tol_override",
                     text=("Tolerance per Face (mm)" if not _DE else "Toleranz pro Fläche (mm)"))

            prof_val = MATERIAL_PROFILES.get(props.material_profile, 0.3)
            row = adv.row(align=True)
            row.label(text=(f"Profile: {prof_val:.2f} mm" if not _DE else f"Profil: {prof_val:.2f} mm"))
            try:
                eff_tol = float(props.effective_tolerance())
                row2 = adv.row(align=True)
                row2.label(text=(f"Effective: {eff_tol:.2f} mm" if not _DE else f"Effektiv: {eff_tol:.2f} mm"))
            except Exception:
                pass

        # =========================
        # ALIGNMENT (Object Mode)
        # =========================

        box = layout.box()
        header = box.row(align=True)
        header.label(text=("Alignment" if not _DE else "Ausrichtung"), icon='SNAP_ON')

        more_txt = ("Less..." if props.ui_more_align else "More...") if not _DE else ("Weniger..." if props.ui_more_align else "Mehr...")
        header.prop(props, "ui_more_align", text=more_txt, toggle=True)

        if props.ui_more_align:
            col = box.column(align=True)
            col.label(text=("Pick faces in Object Mode (A = target, B = moving)" if not _DE
                            else "Flächen im Objektmodus wählen (A = Ziel, B = bewegt)"))

            wm = context.window_manager
            nameA = getattr(wm, "snapsplit_face_a_obj", "")
            idxA = getattr(wm, "snapsplit_face_a_index", -1)
            nameB = getattr(wm, "snapsplit_face_b_obj", "")
            idxB = getattr(wm, "snapsplit_face_b_index", -1)

            status_a = (f"A: {nameA} [#{idxA}]" if nameA and idxA >= 0
                        else ("A: none" if not _DE else "A: keine"))
            status_b = (f"B: {nameB} [#{idxB}]" if nameB and idxB >= 0
                        else ("B: none" if not _DE else "B: keine"))

            stat = box.row(align=True)
            stat.label(text=status_a, icon='INFO')
            stat.label(text=status_b, icon='INFO')
            stat.operator("snapsplit.clear_picks", text="", icon='X')

            row = box.row(align=True)
            row.operator("snapsplit.pick_face_a",
                         text=("Pick Face A" if not _DE else "Fläche A wählen"),
                         icon='MOUSE_LMB')
            row.operator("snapsplit.pick_face_b",
                         text=("Pick Face B" if not _DE else "Fläche B wählen"),
                         icon='MOUSE_LMB')

            can_align = (bool(nameA) and idxA >= 0 and bool(nameB) and idxB >= 0)
            row_align = box.row(align=True)
            row_align.enabled = can_align
            row_align.operator("snapsplit.align_faces",
                            text=("Align Faces" if not _DE else "Flächen ausrichten"),
                            icon='SNAP_ON')

        # =========================
        # Donate
        # =========================

        col = layout.column(align=True)
        col.separator()
        col.operator(
            "wm.url_open",
            text=("Buy me a coffee ❤️"),
            icon='FUND'
        ).url = "https://buymeacoffee.com/betakontext"

        layout.separator()


def register():
    bpy.utils.register_class(SNAP_PT_panel)


def unregister():
    bpy.utils.unregister_class(SNAP_PT_panel)
