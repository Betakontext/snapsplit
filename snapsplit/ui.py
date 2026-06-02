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
from .profiles import MATERIAL_PROFILES  # for tolerance info badge

class SNAP_PT_panel(Panel):
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
            layout.label(text=("SnapSplit properties not available." if not _DE else "SnapSplit-Eigenschaften nicht verfügbar."), icon="ERROR")
            layout.label(text=("Please re-enable the Add-on." if not _DE else "Bitte das Add-on erneut aktivieren."))
            return

        # =========================
        # SEGMENTATION
        # =========================
        seg_box = layout.box()
        seg_header = seg_box.row(align=True)
        seg_header.label(text=("Segmentation" if not _DE else "Segmentierung"), icon='MOD_BOOLEAN')
        seg_header.prop(props, "ui_more_seg", text=("Less..." if props.ui_more_seg else "More...") if not _DE else ("Weniger..." if props.ui_more_seg else "Mehr..."), toggle=True)

        col = seg_box.column(align=True)
        col.prop(props, "split_axis", text=("Split Axis" if not _DE else "Schnittachse"))

        row = col.row(align=True)
        row.prop(props, "show_split_preview", text=("Show split preview" if not _DE else "Schnittvorschau anzeigen"))
        row.operator("snapsplit.adjust_split_axis", icon="EMPTY_AXIS", text=("Adjust" if not _DE else "Anpassen"))

        if props.ui_more_seg:
            adv = seg_box.column(align=True)
            adv.prop(props, "parts_count", text=("Number of Parts" if not _DE else "Anzahl Teile"))
            try:
                if int(props.parts_count) >= 12:
                    adv.label(icon='INFO', text=("High part count may be slow" if not _DE else "Hohe Teilzahl kann langsam sein"))
            except Exception:
                pass
            adv.prop(props, "split_offset_mm", text=("Split Offset (mm)" if not _DE else "Schnitt-Offset (mm)"))
            adv.prop(props, "cap_seams_during_split", text=("Cap seams during split (slower)" if not _DE else "Nähte beim Schnitt schließen (langsamer)"))
            if not props.cap_seams_during_split:
                sub = adv.column(align=True)
                sub.operator("snapsplit.cap_open_seams_now", icon="OUTLINER_OB_SURFACE", text=("Cap seams now" if not _DE else "Nähte jetzt schließen"))
                sub.label(text=("To close existing seams, run 'Cap seams now'." if not _DE else "Bestehende Nähte mit 'Nähte jetzt schließen' füllen."), icon='INFO')

        seg_box.operator("snapsplit.planar_split", icon="MOD_BOOLEAN", text=("Planar Split" if not _DE else "Planarer Schnitt"))

        layout.separator()

        # =========================
        # CONNECTIONS
        # =========================
        con_box = layout.box()
        con_header = con_box.row(align=True)
        con_header.label(text=("Connections" if not _DE else "Verbindungen"), icon='SNAP_FACE')
        con_header.prop(props, "ui_more_conn", text=("Less..." if props.ui_more_conn else "More...") if not _DE else ("Weniger..." if props.ui_more_conn else "Mehr..."), toggle=True)

        col = con_box.column(align=True)
        col.prop(props, "connector_type", text=("Connector Type" if not _DE else "Verbinder-Typ"))
        col.prop(props, "connector_distribution", text=("Distribution" if not _DE else "Verteilung"))

        btns = layout.column(align=True)
        btns.operator("snapsplit.add_connectors", icon="SNAP_FACE", text=("Add connectors" if not _DE else "Verbinder hinzufügen"))
        btns.operator("snapsplit.place_connectors_click", icon="CURSOR", text=("Place connectors (click)" if not _DE else "Verbinder per Klick"))

        if props.ui_more_conn:
            adv = con_box.column(align=True)
            if props.connector_distribution == "LINE":
                adv.prop(props, "connectors_per_seam", text=("Connectors per Seam" if not _DE else "Verbinder pro Naht"))
            else:
                r = adv.row(align=True)
                r.prop(props, "connectors_per_seam", text=("Columns" if not _DE else "Spalten"))
                r.prop(props, "connectors_rows", text=("Rows" if not _DE else "Reihen"))

            adv.prop(props, "connector_margin_pct", text=("Margin (%)" if not _DE else "Randabstand (%)"))
            adv.prop(props, "edge_margin_mm", text=("Edge margin (mm)" if not _DE else "Randabstand (mm)"))

            gbox = con_box.box()

            # CYL_PIN / SNAP_PIN
            if props.connector_type in {"CYL_PIN", "SNAP_PIN"}:
                gbox.prop(props, "pin_prop_enabled", text=("Proportional scaling (Pins)" if not _DE else "Proportionale Skalierung (Pins)"))
                gbox.prop(props, "pin_diameter_mm", text=("Pin Diameter (mm)" if not _DE else "Pin-Durchmesser (mm)"))
                gbox.prop(props, "pin_length_mm", text=("Pin Length (mm)" if not _DE else "Pin-Länge (mm)"))
                gbox.prop(props, "pin_embed_pct", text=("Insert Depth (%)" if not _DE else "Einstecktiefe (%)"))

                rr = gbox.row(align=True)
                rr.prop(props, "pin_segments", text=("Segments" if not _DE else "Segmente"))
                try:
                    from .profiles import _suggest_pin_segments_from_diameter
                    suggested = _suggest_pin_segments_from_diameter(float(getattr(props, "pin_diameter_mm", 5.0)))
                    sub = rr.row(align=True); sub.alignment = 'RIGHT'
                    sub.label(text=(f"Suggested: {suggested}" if not _DE else f"Vorschlag: {suggested}"), icon='INFO')
                except Exception:
                    pass

                sbox = gbox.box()
                sbox.label(text=("Snap spheres" if not _DE else "Schnapp-Sphären"), icon='SPHERE')
                sbox.prop(props, "snap_spheres_per_side", text=("Spheres per side" if not _DE else "Sphären je Seite"))
                sbox.prop(props, "snap_sphere_diameter_mm", text=("Sphere Ø (mm)" if not _DE else "Sphären-Ø (mm)"))
                sbox.prop(props, "snap_sphere_protrusion_mm", text=("Protrusion (mm)" if not _DE else "Überstand (mm)"))
                sbox.label(text=("Auto-updated by Tolerance → Friction/Material" if not _DE else "Automatisch aus Toleranz → Reibung/Material"), icon='INFO')

            # RECT_TENON / SNAP_TENON
            elif props.connector_type in {"RECT_TENON", "SNAP_TENON"}:
                gbox.prop(props, "tenon_prop_enabled", text=("Proportional scaling (Tenon)" if not _DE else "Proportionale Skalierung (Zapfen)"))
                gbox.prop(props, "tenon_width_mm", text=("Tenon Width (mm)" if not _DE else "Zapfen-Breite (mm)"))
                gbox.prop(props, "tenon_depth_mm", text=("Tenon Depth (mm)" if not _DE else "Zapfen-Tiefe (mm)"))
                gbox.prop(props, "pin_embed_pct", text=("Insert Depth (%)" if not _DE else "Einstecktiefe (%)"))

                if props.connector_type == "SNAP_TENON":
                    sbox = gbox.box()
                    sbox.label(text=("Snap spheres" if not _DE else "Schnapp-Sphären"), icon='SPHERE')
                    sbox.prop(props, "snap_spheres_per_side", text=("Spheres per side" if not _DE else "Sphären je Seite"))
                    sbox.prop(props, "snap_sphere_diameter_mm", text=("Sphere Ø (mm)" if not _DE else "Sphären-Ø (mm)"))
                    sbox.prop(props, "snap_sphere_protrusion_mm", text=("Protrusion (mm)" if not _DE else "Überstand (mm)"))
                    sbox.label(text=("Auto-updated by Tolerance → Friction/Material" if not _DE else "Automatisch aus Toleranz → Reibung/Material"), icon='INFO')

            # PIN_HOLE
            if props.connector_type == "PIN_HOLE":
                pbox = con_box.box()
                pbox.prop(props, "pin_prop_enabled", text=("Proportional scaling (Pins)" if not _DE else "Proportionale Skalierung (Pins)"))
                pbox.label(text=("Pin & Hole (fit modes)" if not _DE else "Pin & Bohrung (Passungen)"), icon='MESH_CYLINDER')
                pbox.prop(props, "pin_diameter_mm", text=("Pin Diameter (mm)" if not _DE else "Pin-Durchmesser (mm)"))
                pbox.prop(props, "pin_length_mm", text=("Pin Length (mm)" if not _DE else "Pin-Länge (mm)"))
                pbox.prop(props, "pin_embed_pct", text=("Insert Depth (%)" if not _DE else "Einstecktiefe (%)"))
                pbox.prop(props, "pin_segments", text=("Segments" if not _DE else "Segmente"))
                pbox.prop(props, "add_chamfer_mm", text=("Chamfer (mm)" if not _DE else "Fase (mm)"))
                pbox.prop(props, "pin_fit_mode", text=("Fit mode" if not _DE else "Passung"))
                pbox.prop(props, "pin_hole_only", text=("Hole only (for metal pins)" if not _DE else "Nur Bohrung (für Metallstifte)"))
                pbox.label(text=("Chamfer helps compensate elephant's foot" if not _DE else "Fase kompensiert Elephant's Foot"), icon='INFO')

            # DOVETAIL_TAPER (Tenon-based with angled side walls)
            if props.connector_type == "DOVETAIL_TAPER":
                dbox = con_box.box()
                dbox.label(text=("Dovetail (angled)" if not _DE else "Schwalbenschwanz (Winkel)"), icon='MOD_SIMPLEDEFORM')

                # Proportional wie bei Snap Pin: liefert Defaults, UI bleibt editierbar
                dbox.prop(props, "dovetail_prop_enabled", text=("Proportional scaling (Dovetail)" if not _DE else "Proportionale Skalierung (Dovetail)"))
                dbox.label(
                    text=("Proportional sets defaults; manual Dim X/Y/Z always editable."
                        if not _DE else "Proportional liefert Standardwerte; Dim X/Y/Z sind immer editierbar."),
                    icon='INFO'
                )

                # Immer editierbar
                dims = dbox.column(align=True)
                dims.prop(props, "dovetail_dim_x_mm", text=("Dim X (mm)" if not _DE else "Maß X (mm)"))
                dims.prop(props, "dovetail_dim_y_mm", text=("Dim Y (mm)" if not _DE else "Maß Y (mm)"))
                dims.prop(props, "dovetail_dim_z_mm", text=("Dim Z (mm)" if not _DE else "Maß Z (mm)"))

                # Full span + Stretch axis
                row_fs = dbox.row(align=True)
                row_fs.prop(props, "dovetail_use_full_span", text=("Use full seam span" if not _DE else "Volle Nahtspanne"))
                row_fs.prop(props, "dovetail_stretch_axis", text=("Stretch axis" if not _DE else "Streckachse"))

                # Prozentsteuerung nur wenn Full Span aus; bezieht sich auf Stretch-Achse
                pbox = dbox.box()
                pbox.enabled = not props.dovetail_use_full_span
                pbox.label(text=("Percent of seam span (applies to stretch axis)" if not _DE else "Prozent der Nahtspanne (gilt für Streckachse)"), icon='ARROW_LEFTRIGHT')
                pbox.prop(props, "dovetail_fit_pct", text=("Span %" if not _DE else "Spanne %"))
                pbox.prop(props, "dovetail_clip_to_edge", text=("Clip to edge" if not _DE else "Am Rand ausrichten"))

                # End inset wirkt auf die aktuelle Längsprojektion der Streckachse
                dbox.prop(props, "dovetail_end_inset_mm", text=("End inset (mm)" if not _DE else "Randabzug (mm)"))

                dbox.separator()
                # Winkel gelten auf die zwei Seiten, die zur Streckachse orthogonal sind
                dbox.prop(props, "dovetail_side_angle_a_deg", text=("Side angle A (°)" if not _DE else "Seitenwinkel A (°)"))
                dbox.prop(props, "dovetail_side_angle_b_deg", text=("Side angle B (°)" if not _DE else "Seitenwinkel B (°)"))
                dbox.prop(props, "dovetail_leadin_chamfer_mm", text=("Lead-in chamfer (mm)" if not _DE else "Einführfase (mm)"))
                dbox.prop(props, "dovetail_clearance_scale", text=("Clearance scale" if not _DE else "Spiel-Skalierung"))


            # SNAP_CANTILEVER
            if props.connector_type == "SNAP_CANTILEVER":
                sbox = con_box.box()
                sbox.label(text=("Snap-Fit (Cantilever)" if not _DE else "Schnapphaken (Kragarm)"), icon='MOD_BUILD')
                sbox.prop(props, "snapcant_prop_enabled", text=("Proportional scaling (Cantilever)" if not _DE else "Proportionale Skalierung (Kragarm)"))
                sbox.prop(props, "snap_cant_arm_w_mm", text=("Arm width (mm)" if not _DE else "Armbreite (mm)"))
                sbox.prop(props, "snap_cant_arm_len_mm", text=("Arm length (mm)" if not _DE else "Armlänge (mm)"))
                sbox.prop(props, "snap_cant_arm_thk_mm", text=("Arm thickness (mm)" if not _DE else "Armdicke (mm)"))
                sbox.prop(props, "snap_cant_hook_undercut_mm", text=("Hook undercut (mm)" if not _DE else "Hinterschneidung (mm)"))
                sbox.prop(props, "snap_cant_fillet_mm", text=("Base fillet (mm)" if not _DE else "Grundradius (mm)"))
                smore = sbox.column(align=True)
                smore.prop(props, "snap_cant_leadin_chamfer_mm", text=("Lead-in chamfer (mm)" if not _DE else "Einführfase (mm)"))
                smore.prop(props, "snap_cant_stop_offset_mm", text=("Stop offset (mm)" if not _DE else "Anschlag (mm)"))
                smore.prop(props, "snap_cant_clearance_scale", text=("Clearance scale" if not _DE else "Spiel-Skalierung"))
                if props.material_profile == "PLA":
                    sbox.label(text=("PLA is brittle for snap-fits; prefer PETG or tough resin." if not _DE else "PLA ist spröde für Schnapphaken; PETG oder zähe Harze bevorzugen."), icon='INFO')

            # BALL_SOCKET
            if props.connector_type == "BALL_SOCKET":
                bsb = con_box.box()
                bsb.label(text=("Ball & Socket" if not _DE else "Kugel & Schale"), icon='SPHERE')
                bsb.prop(props, "ballsocket_prop_enabled", text=("Proportional scaling (Ball&Socket)" if not _DE else "Proportionale Skalierung (Kugel&Schale)"))
                bsb.prop(props, "ball_diameter_mm", text=("Ball Ø (mm)" if not _DE else "Kugel-Ø (mm)"))
                bsb.prop(props, "ball_friction_target", text=("Friction" if not _DE else "Reibung"))
                bmore = bsb.column(align=True)
                bmore.prop(props, "ball_socket_clearance_mm", text=("Socket clearance (mm)" if not _DE else "Buchsen-Spiel (mm)"))
                bmore.prop(props, "ball_lip_thickness_mm", text=("Retention lip (mm)" if not _DE else "Halte-Lippe (mm)"))
                bmore.prop(props, "ball_socket_open_angle_deg", text=("Open angle (°)" if not _DE else "Öffnungswinkel (°)"))
                bmore.prop(props, "ball_leadin_fillet_mm", text=("Lead-in fillet (mm)" if not _DE else "Einführ-Radius (mm)"))
                bsb.label(text=("Use wear-resistant materials (PETG, tough resin)." if not _DE else "Verschleißfeste Materialien verwenden (PETG, zähes Harz)."), icon='INFO')

            # PIP_HINGE
            if props.connector_type == "PIP_HINGE":
                hib = con_box.box()
                hib.label(text=("Print-in-Place Hinge" if not _DE else "Druckbares Scharnier (PiP)"), icon='MOD_SKIN')
                hib.prop(props, "pip_prop_enabled", text=("Proportional scaling (PiP)" if not _DE else "Proportionale Skalierung (PiP)"))
                hib.prop(props, "pip_hinge_width_mm", text=("Hinge width (mm)" if not _DE else "Scharnier-Breite (mm)"))
                hib.prop(props, "pip_gap_mm", text=("PIP gap (mm)" if not _DE else "PIP-Spalt (mm)"))
                hmore = hib.column(align=True)
                hmore.prop(props, "pip_hinge_thickness_mm", text=("Thickness (mm)" if not _DE else "Dicke (mm)"))
                hmore.prop(props, "pip_segments_count", text=("Segments" if not _DE else "Segmente"))
                hmore.prop(props, "pip_relief_fillet_mm", text=("Relief fillet (mm)" if not _DE else "Entlastungs-Radius (mm)"))
                hib.label(text=("Print-in-place requires excellent calibration; test a small sample first." if not _DE else "PiP erfordert sehr gute Kalibrierung; zuerst ein kleines Muster testen."), icon='INFO')
                if props.material_profile == "PLA" and props.pip_hinge_type == "living_web":
                    hib.label(text=("PLA prone to fatigue/breakage in living hinges." if not _DE else "PLA neigt bei Living Hinges zu Ermüdung/Bruch."), icon='INFO')

            # Global chamfer
            gbox.prop(props, "add_chamfer_mm", text=("Chamfer (mm)" if not _DE else "Fase (mm)"))

        layout.separator()

        # =========================
        # TOLERANCE
        # =========================
        tol_box = layout.box()
        tol_header = tol_box.row(align=True)
        tol_header.label(text=("Tolerance" if not _DE else "Toleranz"), icon='MOD_SOLIDIFY')
        tol_header.prop(props, "ui_more_tol", text=("Less..." if props.ui_more_tol else "More...") if not _DE else ("Weniger..." if props.ui_more_tol else "Mehr..."), toggle=True)

        col = tol_box.column(align=True)
        col.prop(props, "material_profile", text=("Material Profiles" if not _DE else "Material-Profile"))
        col.prop(props, "snap_friction_target", text=("Friction" if not _DE else "Reibung"))

        info = f"Spheres preset: Ø {props.snap_sphere_diameter_mm:.2f} mm, protr {props.snap_sphere_protrusion_mm:.2f} mm" if not _DE else f"Sphären-Preset: Ø {props.snap_sphere_diameter_mm:.2f} mm, Überstand {props.snap_sphere_protrusion_mm:.2f} mm"
        col.label(text=info, icon='INFO')

        if props.ui_more_tol:
            adv = tol_box.column(align=True)
            row = adv.row(align=True)
            row.prop(props, "tol_override", text=("Tolerance per Face (mm)" if not _DE else "Toleranz pro Fläche (mm)"))
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
        # ALIGNMENT
        # =========================
        align_box = layout.box()
        align_header = align_box.row(align=True)
        align_header.label(text=("Alignment" if not _DE else "Ausrichtung"), icon='SNAP_ON')
        align_header.prop(props, "ui_more_align", text=("Less..." if props.ui_more_align else "More...") if not _DE else ("Weniger..." if props.ui_more_align else "Mehr..."), toggle=True)

        if props.ui_more_align:
            col = align_box.column(align=True)
            col.label(text=("Pick faces in Object Mode (A = target, B = moving)" if not _DE else "Flächen im Objektmodus wählen (A = Ziel, B = bewegt)"))

            wm = context.window_manager
            nameA = getattr(wm, "snapsplit_face_a_obj", ""); idxA = getattr(wm, "snapsplit_face_a_index", -1)
            nameB = getattr(wm, "snapsplit_face_b_obj", ""); idxB = getattr(wm, "snapsplit_face_b_index", -1)

            status_a = (f"A: {nameA} [#{idxA}]" if nameA and idxA >= 0 else ("A: none" if not _DE else "A: keine"))
            status_b = (f"B: {nameB} [#{idxB}]" if nameB and idxB >= 0 else ("B: none" if not _DE else "B: keine"))

            stat = align_box.row(align=True)
            stat.label(text=status_a, icon='INFO')
            stat.label(text=status_b, icon='INFO')
            stat.operator("snapsplit.clear_picks", text="", icon='X')

            row = align_box.row(align=True)
            row.operator("snapsplit.pick_face_a", text=("Pick Face A" if not _DE else "Fläche A wählen"), icon='MOUSE_LMB')
            row.operator("snapsplit.pick_face_b", text=("Pick Face B" if not _DE else "Fläche B wählen"), icon='MOUSE_LMB')

            can_align = (bool(nameA) and idxA >= 0 and bool(nameB) and idxB >= 0)
            row_align = align_box.row(align=True); row_align.enabled = can_align
            row_align.operator("snapsplit.align_faces", text=("Align Faces" if not _DE else "Flächen ausrichten"), icon='SNAP_ON')

        layout.separator()
        cta = layout.column(align=True)
        cta.operator("wm.url_open", text=("Buy me a coffee ❤️"), icon='FUND').url = "https://buymeacoffee.com/betakontext"


def register():
    bpy.utils.register_class(SNAP_PT_panel)


def unregister():
    bpy.utils.unregister_class(SNAP_PT_panel)
