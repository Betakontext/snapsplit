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
from .profiles import MATERIAL_PROFILES
from .utils import is_lang_de


class SNAP_PT_panel(Panel):
    """Main SnapSplit UI panel in the 3D Viewport sidebar."""
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "SnapSplit"
    bl_label = "SnapSplit"

    @classmethod
    def poll(cls, context):
        """Show panel when a scene is available."""
        return context is not None and context.scene is not None

    def draw(self, context):
        """Build the SnapSplit UI with sections for Segmentation, Connections, and Tolerance."""
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

        # One row: Show split preview + Adjust
        row = col.row(align=True)
        row.prop(props, "show_split_preview", text=("Show split preview" if not _DE else "Schnittvorschau anzeigen"))
        row.operator("snapsplit.adjust_split_axis",
                    icon="EMPTY_AXIS",
                    text=("Adjust" if not _DE else "Anpassen"))

        # Advanced segmentation controls (layout only; no logic changes)
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

            # Only when auto-cap is OFF, show manual cap button and hint
            if not props.cap_seams_during_split:
                sub = adv.column(align=True)
                sub.operator("snapsplit.cap_open_seams_now",
                            icon="OUTLINER_OB_SURFACE",
                            text=("Cap seams now" if not _DE else "Nähte jetzt schließen"))
                sub.label(text=("To close existing seams, run 'Cap seams now'."
                                if not _DE else "Bestehende Nähte mit 'Nähte jetzt schließen' füllen."),
                        icon='INFO')

        # Planar Split at the bottom of the section
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

        # Actions
        col = layout.column(align=True)
        col.operator("snapsplit.add_connectors",
                     icon="SNAP_FACE",
                     text=("Add connectors" if not _DE else "Verbinder hinzufügen"))
        col.operator("snapsplit.place_connectors_click",
                     icon="CURSOR",
                     text=("Place connectors (click)" if not _DE else "Verbinder per Klick"))

        if props.ui_more_conn:
            # Advanced connection placement
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

            # SNAP-specific (for SNAP_PIN and SNAP_TENON)
            if props.connector_type in {"SNAP_PIN", "SNAP_TENON"}:
                sbox = box.box()
                sbox.label(text=("Snap spheres" if not _DE else "Schnapp-Sphären"), icon='SPHERE')
                sbox.prop(props, "snap_spheres_per_side",
                          text=("Spheres per side" if not _DE else "Sphären je Seite"))
                sbox.prop(props, "snap_sphere_diameter_mm",
                          text=("Sphere Ø (mm)" if not _DE else "Sphären-Ø (mm)"))
                sbox.prop(props, "snap_sphere_protrusion_mm",
                          text=("Protrusion (mm)" if not _DE else "Überstand (mm)"))

            # Geometry settings
            gbox = box.box()

            # Pin parameters for CYL_PIN and SNAP_PIN
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

            # Tenon parameters for RECT_TENON and SNAP_TENON
            elif props.connector_type in {"RECT_TENON", "SNAP_TENON"}:
                gbox.prop(props, "tenon_width_mm",
                          text=("Tenon Width (mm)" if not _DE else "Zapfen-Breite (mm)"))
                gbox.prop(props, "tenon_depth_mm",
                          text=("Tenon Depth (mm)" if not _DE else "Zapfen-Tiefe (mm)"))
                gbox.prop(props, "pin_embed_pct",
                          text=("Insert Depth (%)" if not _DE else "Einstecktiefe (%)"))

            else:
                gbox.label(text=("Unsupported connector type" if not _DE else "Nicht unterstützter Verbinder-Typ"), icon='INFO')

            gbox.prop(props, "add_chamfer_mm",
                      text=("Chamfer (mm)" if not _DE else "Fase (mm)"))

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

            # Profile and effective readout
            prof_val = MATERIAL_PROFILES.get(props.material_profile, 0.2)
            row = adv.row(align=True)
            row.label(text=(f"Profile: {prof_val:.2f} mm" if not _DE else f"Profil: {prof_val:.2f} mm"))
            try:
                eff_tol = float(props.effective_tolerance())
                row2 = adv.row(align=True)
                row2.label(text=(f"Effective: {eff_tol:.2f} mm" if not _DE else f"Effektiv: {eff_tol:.2f} mm"))
            except Exception:
                pass

        layout.separator()


def register():
    """Register the SnapSplit UI panel."""
    bpy.utils.register_class(SNAP_PT_panel)


def unregister():
    """Unregister the SnapSplit UI panel."""
    bpy.utils.unregister_class(SNAP_PT_panel)
