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

from __future__ import annotations

from typing import Dict, Optional

try:
    import bpy
except Exception:
    bpy = None  # Allow limited import outside Blender (e.g., linters/tests)


# ---------------------------
# Language cache helpers
# ---------------------------

_CACHED_LANG: Optional[str] = None

def set_cached_lang(lang: str) -> None:
    """Cache last-known language (optional external use)."""
    global _CACHED_LANG
    _CACHED_LANG = lang

def get_cached_lang() -> Optional[str]:
    """Return cached language or None."""
    return _CACHED_LANG


# ---------------------------
# Language detection and normalization
# ---------------------------

def get_current_language() -> str:
    """Return Blender UI language locale, or 'en_US' outside Blender or when DEFAULT."""
    if bpy is None:
        return "en_US"
    prefs = getattr(bpy.context, "preferences", None)
    if prefs and getattr(prefs, "view", None):
        lang = getattr(prefs.view, "language", "") or ""
        if lang and lang != "DEFAULT":
            return lang
    return "en_US"

def lang_base(lang: str) -> str:
    """Extract base language code (e.g., 'de_DE' -> 'de')."""
    if not lang:
        return "en"
    return lang.split("_", 1)[0] if "_" in lang else lang

# Preferred locale per base; include all requested languages
_BASE_TO_DEFAULT_LOCALE = {
    "en": "en_US",
    "de": "de_DE",
    "fr": "fr_FR",
    "es": "es_ES",
    "it": "it_IT",
    "pt": "pt_BR",  # prefer Brazilian Portuguese as default; pt_PT covered too
    "nl": "nl_NL",
    "pl": "pl_PL",
    "ja": "ja_JP",
    "zh": "zh_CN",  # prefer Simplified Chinese; zh_TW covered too
    "ru": "ru_RU",
    "uk": "uk_UA",
    "tr": "tr_TR",
}

def normalize_lang(lang: Optional[str]) -> str:
    """Normalize language to a known full locale key in translations."""
    if not lang:
        return "en_US"
    lang = lang.strip()
    if lang in translations:
        return lang
    base = lang_base(lang)
    # Map well-known alternates (e.g., en_GB) to preferred default locales
    mapped = _BASE_TO_DEFAULT_LOCALE.get(base, "en_US")
    return mapped if mapped in translations else "en_US"

def _lookup(lang: str, key: str) -> Optional[str]:
    """Look up translation with fallback: exact-locale -> base-bucket -> en_US."""
    exact = translations.get(lang, {})
    if key in exact:
        return exact[key]
    base = lang_base(lang)
    base_dict = translations.get(base, {})
    if key in base_dict:
        return base_dict[key]
    en = translations.get("en_US", {})
    return en.get(key)

def tr(key: str, default: str = "") -> str:
    """Translate key to current Blender language, falling back to English and finally default/key."""
    lang = normalize_lang(get_current_language())
    value = _lookup(lang, key)
    if value is not None:
        return value
    return default or key


# ---------------------------
# Translation keys used across SnapSplit
# Keep English (en_US) complete. Other locales should cover all keys here.
# ---------------------------

# Note: This tuple is informative for devs; en_US below is authoritative.
_ALL_KEYS = (
    # Generic/UI
    "ui.panel.title",
    "ui.reload_language",
    "ui.reload_language_desc",
    "ui.section.profiles",
    "ui.section.tools",
    "ui.button.apply",
    "ui.button.cancel",
    "ui.button.ok",
    "ui.section.export",
    "ui.section.settings",
    "ui.label.collection",
    "ui.tooltip.collection",

    # Preferences
    "prefs.title",
    "prefs.default_profile",
    "prefs.create_export_collection",
    "prefs.language_note",
    "prefs.reload_language",
    "prefs.reload_language_desc",

    # Profiles (generic)
    "profiles.name",
    "profiles.description",
    "profiles.enum.material",
    "profiles.enum.material_desc",
    "profiles.enum.method",
    "profiles.enum.method_desc",

    # Operators and descriptions
    "op.adjust_axis.label",
    "op.adjust_axis.done",
    "op.adjust_axis.cancelled",

    "op.split.label",
    "op.split.desc",
    "op.split.many_parts_hint",
    "op.split.autocap.none",
    "op.split.autocap.count",
    "op.split.fewer_parts",
    "op.split.parts_created",

    "op.cap_now.label",
    "op.cap_now.desc",
    "op.cap_now.only_selected.name",
    "op.cap_now.max_planes.name",
    "op.cap_now.max_planes.desc",
    "op.cap_now.select_only.name",
    "op.cap_now.require_two_seeds.name",
    "op.cap_now.require_two_seeds.desc",
    "op.cap_now.no_targets",
    "op.cap_now.failed_one",
    "op.cap_now.none_selected",
    "op.cap_now.none_capped",
    "op.cap_now.selected_count",
    "op.cap_now.capped_count",

    # Common operator messages
    "op.common.select_mesh",

    # Warnings/Infos
    "warn.unapplied_transforms",
    "warn.apply_transforms_hint",

    # Generic reports
    "msg.no_active_object",
    "msg.not_mesh",
    "msg.operation_done",
    "msg.operation_failed",
    "msg.unapplied_transforms",

    # profiles.py specific UI (added)
    # Segmentation / Preview
    "ui.split_offset_mm",
    "ui.split_offset_desc",
    "ui.split_axis",
    "ui.split_along_x",
    "ui.split_along_y",
    "ui.split_along_z",
    "ui.show_split_preview",
    "ui.show_split_preview_desc",
    "ui.parts_count",
    "ui.parts_count_desc",

    # Auto-cap option
    "ui.cap_seams_during_split_short",
    "ui.cap_seams_during_split_desc",

    # Connectors
    "ui.connector_type",
    "ui.cyl_pin",
    "ui.cyl_pin_desc",
    "ui.rect_tenon",
    "ui.rect_tenon_desc",
    "ui.snap_pin",
    "ui.snap_pin_desc",
    "ui.snap_tenon",
    "ui.snap_tenon_desc",

    # Distribution
    "ui.distribution",
    "ui.distribution_desc",
    "ui.line",
    "ui.line_desc",
    "ui.grid",
    "ui.grid_desc",
    "ui.connectors_per_seam",
    "ui.rows_grid",
    "ui.rows_grid_desc",
    "ui.margin_pct",
    "ui.margin_pct_desc",

    # Snap options
    "ui.spheres_per_side",
    "ui.spheres_per_side_desc",
    "ui.sphere_diameter_mm",
    "ui.sphere_diameter_mm_desc",
    "ui.protrusion_mm",
    "ui.protrusion_mm_desc",

    # Pin / Tenon
    "ui.pin_diameter_mm",
    "ui.pin_length_mm",
    "ui.segments",
    "ui.segments_desc",
    "ui.tenon_width_mm",
    "ui.tenon_depth_mm",
    "ui.chamfer_mm",

    # Insert depth
    "ui.insert_depth_pct",
    "ui.insert_depth_pct_desc",

    # Material / Tolerance
    "ui.material_profiles",
    "ui.material_profile_desc",
    "profiles.mat.tooltip",
    "ui.tol_per_face_mm",
    "ui.tol_override_desc",

    # Foldouts (now localized)
    "ui.foldout.more_seg",
    "ui.foldout.more_seg_desc",
    "ui.foldout.more_conn",
    "ui.foldout.more_conn_desc",
    "ui.foldout.more_tol",
    "ui.foldout.more_tol_desc",
    "ui.foldout.more_align",
    "ui.foldout.more_align_desc",

    # New concise tooltips (hover)
    "tooltip.planar_split",
    "tooltip.adjust",
    "tooltip.show_split_preview",

    # ---------------------------
    # Additional keys to cover all UI you mentioned explicitly
    # ---------------------------
    "ui.segmentation_title",
    "ui.less",
    "ui.adjust",
    "ui.cap_seams_during_split_slow",
    "ui.connections_title",
    "ui.add_connectors",
    "ui.place_connectors_click",
    "ui.pick_faces_hint",
    "ui.face_a_none",
    "ui.face_b_none",
    "ui.pick_face_a",
    "ui.pick_face_b",
    "ui.align_faces",
    "ui.align_faces_desc",
)

# ---------------------------
# Translations dictionary
# ---------------------------

translations: Dict[str, Dict[str, str]] = {
    # Base buckets (optional; can be used for base-only overrides)
    "en": {},
    "de": {},
    "fr": {},
    "es": {},
    "it": {},
    "pt": {},
    "nl": {},
    "pl": {},
    "ja": {},
    "zh": {},
    "ru": {},
    "uk": {},
    "tr": {},

    # English (US) - complete
    "en_US": {
        # Generic/UI
        "ui.panel.title": "SnapSplit",
        "ui.reload_language": "Reload UI Language",
        "ui.reload_language_desc": "Re-register the add-on to apply the current Blender language to static labels.",
        "ui.section.profiles": "Profiles",
        "ui.section.tools": "Tools",
        "ui.button.apply": "Apply",
        "ui.button.cancel": "Cancel",
        "ui.button.ok": "OK",
        "ui.section.export": "Export",
        "ui.section.settings": "Settings",
        "ui.label.collection": "Export Collection",
        "ui.tooltip.collection": "Collection used for export output",

        # Preferences
        "prefs.title": "SnapSplit Preferences",
        "prefs.default_profile": "Default Profile",
        "prefs.create_export_collection": "Create export collection",
        "prefs.language_note": "Language follows Blender’s UI language. Use 'Reload UI Language' after changing Blender language.",
        "prefs.reload_language": "Reload UI Language",
        "prefs.reload_language_desc": "Re-register the add-on to refresh static labels (operators/properties).",

        # Profiles (generic)
        "profiles.name": "Profile",
        "profiles.description": "Active SnapSplit profile",
        "profiles.enum.material": "Material",
        "profiles.enum.material_desc": "Material assignment strategy",
        "profiles.enum.method": "Method",
        "profiles.enum.method_desc": "Splitting method to use",

        # Operators / Adjust axis
        "op.adjust_axis.label": "Adjust split axis",
        "op.adjust_axis.done": "Split axis adjusted.",
        "op.adjust_axis.cancelled": "Adjust split axis cancelled.",

        # Operators / Split
        "op.split.label": "Planar Split",
        "op.split.desc": "Split faces along a fitted plane",
        "op.split.many_parts_hint": "Splitting into many parts can take a while on dense meshes...",
        "op.split.autocap.none": "Auto-cap during split did not find valid loops to fill.",
        "op.split.autocap.count": "Auto-capped seams on {n} part(s).",
        "op.split.fewer_parts": "Fewer parts created than expected ({have} < {want}).",
        "op.split.parts_created": "{n} parts created.",

        # Operators / Cap now
        "op.cap_now.label": "Cap seams now",
        "op.cap_now.desc": "Fill between exactly two split edge loops (outer+inner) per plane. Seeds preferred.",
        "op.cap_now.only_selected.name": "Only selected objects",
        "op.cap_now.max_planes.name": "Max planes",
        "op.cap_now.max_planes.desc": "0 = all planes per object, 1 = only largest",
        "op.cap_now.select_only.name": "Select only (no fill)",
        "op.cap_now.require_two_seeds.name": "Require exactly two seed edges",
        "op.cap_now.require_two_seeds.desc": "If exactly two edges are selected in Edit Mode, use them as seeds only (no auto-detection).",
        "op.cap_now.no_targets": "No mesh objects to cap. Select split parts or use the parts collection.",
        "op.cap_now.failed_one": "Processing failed on '{name}': {err}",
        "op.cap_now.none_selected": "Could not determine split edge loops to select.",
        "op.cap_now.none_capped": "Could not determine and fill split edge loops.",
        "op.cap_now.selected_count": "Selected split edge loops on {n} object(s).",
        "op.cap_now.capped_count": "Capped seams on {n} object(s).",

        # Common
        "op.common.select_mesh": "Please select a mesh object.",

        # Warnings/Infos
        "warn.unapplied_transforms": "Object has unapplied transforms",
        "warn.apply_transforms_hint": "Consider Apply All Transforms (Ctrl+A) for exact and predictable split results.",

        # Generic reports
        "msg.no_active_object": "No active object.",
        "msg.not_mesh": "Active object is not a mesh.",
        "msg.operation_done": "Operation finished.",
        "msg.operation_failed": "Operation failed.",
        "msg.unapplied_transforms": "Object has unapplied transforms",

        # profiles.py specific UI

        # Segmentation / Preview
        "ui.split_offset_mm": "Split Offset (mm)",
        "ui.split_offset_desc": "Offset of the cutting plane along the split axis (positive in axis direction)",
        "ui.split_axis": "Split Axis",
        "ui.split_along_x": "Split along X",
        "ui.split_along_y": "Split along Y",
        "ui.split_along_z": "Split along Z",
        "ui.show_split_preview": "Show split preview",
        "ui.show_split_preview_desc": "Show temporary orange planes at planned cut positions",
        "ui.parts_count": "Number of Parts",
        "ui.parts_count_desc": "Number of desired segments (cut planes = parts - 1)",

        # Auto-cap option
        "ui.cap_seams_during_split_short": "Cap seams during split",
        "ui.cap_seams_during_split_desc": "Automatically close seams after splitting. With hollow/inner shell: precise outer/inner loop fill; without hollow: simple fill. May increase runtime.",

        # Connectors
        "ui.connector_type": "Connector Type",
        "ui.cyl_pin": "Cylinder Pin",
        "ui.cyl_pin_desc": "Dowel pin + socket",
        "ui.rect_tenon": "Rectangular Tenon",
        "ui.rect_tenon_desc": "Anti-rotation joint",
        "ui.snap_pin": "Snap Pin",
        "ui.snap_pin_desc": "Connector with snap spheres",
        "ui.snap_tenon": "Snap Tenon",
        "ui.snap_tenon_desc": "Rectangular tenon with snap spheres",

        # Distribution
        "ui.distribution": "Distribution",
        "ui.distribution_desc": "Distribute connectors along a line or a grid across the seam face",
        "ui.line": "Line",
        "ui.line_desc": "Place connectors along a line in the seam face",
        "ui.grid": "Grid",
        "ui.grid_desc": "Distribute connectors in a grid over the seam face",
        "ui.connectors_per_seam": "Connectors per Seam",
        "ui.rows_grid": "Rows (GRID)",
        "ui.rows_grid_desc": "Number of rows for grid distribution",
        "ui.margin_pct": "Margin (%)",
        "ui.margin_pct_desc": "Edge margin along the seam (and perpendicular in GRID) as percentage of part length (0–40% recommended)",

        # Snap options
        "ui.spheres_per_side": "Spheres per side",
        "ui.spheres_per_side_desc": "Number of snap spheres per side/around",
        "ui.sphere_diameter_mm": "Sphere Diameter (mm)",
        "ui.sphere_diameter_mm_desc": "Diameter of snap spheres",
        "ui.protrusion_mm": "Protrusion (mm)",
        "ui.protrusion_mm_desc": "How far spheres protrude from side surface",

        # Pin / Tenon
        "ui.pin_diameter_mm": "Pin Diameter (mm)",
        "ui.pin_length_mm": "Pin Length (mm)",
        "ui.segments": "Segments",
        "ui.segments_desc": "Cylinder pin radial segments (visual smoothness)",
        "ui.tenon_width_mm": "Tenon Width (mm)",
        "ui.tenon_depth_mm": "Tenon Depth (mm)",
        "ui.chamfer_mm": "Chamfer (mm)",

        # Insert depth
        "ui.insert_depth_pct": "Insert Depth (%)",
        "ui.insert_depth_pct_desc": "Percentage of connector length recessed into part A",

        # Material / Tolerance
        "ui.material_profiles": "Material Profiles",
        "ui.material_profile_desc": "Select a material profile to auto-fill tolerance per side",
        "profiles.mat.tooltip": "Recommended tolerance per side: {val:.2f} mm",
        "ui.tol_per_face_mm": "Tolerance per Face (mm)",
        "ui.tol_override_desc": "Overrides material profile (0 = use profile value)",

        # Foldouts
        "ui.foldout.more_seg": "More segmentation settings",
        "ui.foldout.more_seg_desc": "Show advanced segmentation options",
        "ui.foldout.more_conn": "More connection settings",
        "ui.foldout.more_conn_desc": "Show advanced connection/geometry options",
        "ui.foldout.more_tol": "More tolerance settings",
        "ui.foldout.more_tol_desc": "Show advanced tolerance options",
        "ui.foldout.more_align": "More alignment settings",
        "ui.foldout.more_align_desc": "Show advanced alignment options",

        # New concise tooltips (hover)
        "tooltip.planar_split": "Split selected geometry along a best-fit plane.",
        "tooltip.adjust": "Open fine-tuning options for the current operation.",
        "tooltip.show_split_preview": "Toggle a visual preview of the split before applying.",

        # Additional UI you mentioned
        "ui.segmentation_title": "Segmentation",
        "ui.less": "Less",
        "ui.adjust": "Adjust",
        "ui.cap_seams_during_split_slow": "Cap seams during split (slower)",
        "ui.connections_title": "Connections",
        "ui.add_connectors": "Add connectors",
        "ui.place_connectors_click": "Place connectors (click)",
        "ui.pick_faces_hint": "Pick faces in Object Mode (A = target, B = moving)",
        "ui.face_a_none": "A: none",
        "ui.face_b_none": "B: none",
        "ui.pick_face_a": "Pick Face A",
        "ui.pick_face_b": "Pick Face B",
        "ui.align_faces": "Align Faces",
        "ui.align_faces_desc": "Align face B to face A using local fit and orientation",
    },

    # German (Germany) - complete
    "de_DE": {
        "ui.panel.title": "SnapSplit",
        "ui.reload_language": "UI-Sprache neu laden",
        "ui.reload_language_desc": "Add-on neu registrieren, um statische Bezeichnungen an die aktuelle Blender-Sprache anzupassen.",
        "ui.section.profiles": "Profile",
        "ui.section.tools": "Werkzeuge",
        "ui.button.apply": "Übernehmen",
        "ui.button.cancel": "Abbrechen",
        "ui.button.ok": "OK",
        "ui.section.export": "Export",
        "ui.section.settings": "Einstellungen",
        "ui.label.collection": "Export-Kollektion",
        "ui.tooltip.collection": "Kollektion für Exportausgaben",

        "prefs.title": "SnapSplit Einstellungen",
        "prefs.default_profile": "Standard-Profil",
        "prefs.create_export_collection": "Export-Kollektion erstellen",
        "prefs.language_note": "Die Sprache folgt der Blender-UI-Sprache. Nach Sprachwechsel 'UI-Sprache neu laden' verwenden.",
        "prefs.reload_language": "UI-Sprache neu laden",
        "prefs.reload_language_desc": "Add-on neu registrieren, um statische Bezeichnungen (Operatoren/Properties) zu aktualisieren.",

        "profiles.name": "Profil",
        "profiles.description": "Aktives SnapSplit-Profil",
        "profiles.enum.material": "Material",
        "profiles.enum.material_desc": "Strategie zur Materialzuweisung",
        "profiles.enum.method": "Methode",
        "profiles.enum.method_desc": "Zu verwendende Split-Methode",

        "op.adjust_axis.label": "Schnittachse anpassen",
        "op.adjust_axis.done": "Schnittachse angepasst.",
        "op.adjust_axis.cancelled": "Anpassen der Schnittachse abgebrochen.",

        "op.split.label": "Planarer Schnitt",
        "op.split.desc": "Flächen entlang einer angepassten Ebene trennen",
        "op.split.many_parts_hint": "Das Aufteilen in viele Teile kann bei dichten Meshes eine Weile dauern...",
        "op.split.autocap.none": "Automatisches Verschließen fand keine gültigen Schleifen.",
        "op.split.autocap.count": "Nähte automatisch bei {n} Teil(en) verschlossen.",
        "op.split.fewer_parts": "Weniger Teile erzeugt als erwartet ({have} < {want}).",
        "op.split.parts_created": "{n} Teile erzeugt.",

        "op.cap_now.label": "Nähte jetzt verschließen",
        "op.cap_now.desc": "Zwischen genau zwei Schnittkanten-Schleifen (außen+innen) pro Ebene füllen. Seeds werden bevorzugt.",
        "op.cap_now.only_selected.name": "Nur ausgewählte Objekte",
        "op.cap_now.max_planes.name": "Maximale Ebenen",
        "op.cap_now.max_planes.desc": "0 = alle Ebenen pro Objekt, 1 = nur größte",
        "op.cap_now.select_only.name": "Nur auswählen (nicht füllen)",
        "op.cap_now.require_two_seeds.name": "Genau zwei Seed-Kanten erforderlich",
        "op.cap_now.require_two_seeds.desc": "Wenn genau zwei Kanten im Edit-Modus ausgewählt sind, nur diese als Seeds verwenden (keine Auto-Erkennung).",
        "op.cap_now.no_targets": "Keine Mesh-Objekte zum Verschließen. Teile auswählen oder die Teile-Kollektion verwenden.",
        "op.cap_now.failed_one": "Verarbeitung bei '{name}' fehlgeschlagen: {err}",
        "op.cap_now.none_selected": "Konnte die Schnittkanten-Schleifen nicht zur Auswahl bestimmen.",
        "op.cap_now.none_capped": "Konnte die Schnittkanten-Schleifen nicht bestimmen und füllen.",
        "op.cap_now.selected_count": "Schnittkanten-Schleifen bei {n} Objekt(en) ausgewählt.",
        "op.cap_now.capped_count": "Nähte bei {n} Objekt(en) verschlossen.",

        "op.common.select_mesh": "Bitte ein Mesh-Objekt auswählen.",

        "warn.unapplied_transforms": "Objekt hat nicht angewendete Transformationen",
        "warn.apply_transforms_hint": "Für exakte und vorhersagbare Ergebnisse ggf. 'Alle Transformationen anwenden' (Strg+A).",

        "msg.no_active_object": "Kein aktives Objekt.",
        "msg.not_mesh": "Aktives Objekt ist kein Mesh.",
        "msg.operation_done": "Vorgang abgeschlossen.",
        "msg.operation_failed": "Vorgang fehlgeschlagen.",
        "msg.unapplied_transforms": "Objekt hat nicht angewendete Transformationen",

        # Segmentation / Preview
        "ui.split_offset_mm": "Schnitt-Offset (mm)",
        "ui.split_offset_desc": "Versatz der Schnittebene entlang der Schnittachse (positiv in Achsrichtung)",
        "ui.split_axis": "Schnittachse",
        "ui.split_along_x": "Entlang X schneiden",
        "ui.split_along_y": "Entlang Y schneiden",
        "ui.split_along_z": "Entlang Z schneiden",
        "ui.show_split_preview": "Schnittvorschau anzeigen",
        "ui.show_split_preview_desc": "Temporäre orange Ebenen an geplanten Schnittpositionen anzeigen",
        "ui.parts_count": "Anzahl Teile",
        "ui.parts_count_desc": "Gewünschte Segmentanzahl (Schnittebenen = Teile - 1)",

        # Auto-cap option
        "ui.cap_seams_during_split_short": "Nähte während des Schnitts verschließen",
        "ui.cap_seams_during_split_desc": "Nähte nach dem Schneiden automatisch schließen. Mit Hohlraum/Innenhülle: präzises Füllen äußerer/innerer Schleifen; ohne Hohlraum: einfaches Füllen. Kann die Laufzeit erhöhen.",

        # Connectors
        "ui.connector_type": "Verbinder-Typ",
        "ui.cyl_pin": "Zylinderstift",
        "ui.cyl_pin_desc": "Passstift + Buchse",
        "ui.rect_tenon": "Rechteck-Zapfen",
        "ui.rect_tenon_desc": "Verdrehsicheres Gelenk",
        "ui.snap_pin": "Schnappstift",
        "ui.snap_pin_desc": "Verbinder mit Schnappkugeln",
        "ui.snap_tenon": "Schnapp-Zapfen",
        "ui.snap_tenon_desc": "Rechteck-Zapfen mit Schnappkugeln",

        # Distribution
        "ui.distribution": "Verteilung",
        "ui.distribution_desc": "Verbinder entlang einer Linie oder in einem Raster über die Nahtfläche verteilen",
        "ui.line": "Linie",
        "ui.line_desc": "Verbinder entlang einer Linie in der Nahtfläche platzieren",
        "ui.grid": "Raster",
        "ui.grid_desc": "Verbinder in einem Raster über die Nahtfläche verteilen",
        "ui.connectors_per_seam": "Verbinder pro Naht",
        "ui.rows_grid": "Zeilen (RASTER)",
        "ui.rows_grid_desc": "Anzahl der Zeilen für die Rasterverteilung",
        "ui.margin_pct": "Rand (%)",
        "ui.margin_pct_desc": "Randabstand entlang der Naht (und senkrecht im RASTER) als Prozent der Teil-Länge (0–40 % empfohlen)",

        # Snap options
        "ui.spheres_per_side": "Kugeln pro Seite",
        "ui.spheres_per_side_desc": "Anzahl der Schnappkugeln pro Seite/Umfang",
        "ui.sphere_diameter_mm": "Kugeldurchmesser (mm)",
        "ui.sphere_diameter_mm_desc": "Durchmesser der Schnappkugeln",
        "ui.protrusion_mm": "Überstand (mm)",
        "ui.protrusion_mm_desc": "Wie weit die Kugeln aus der Seitenfläche hervortreten",

        # Pin / Tenon
        "ui.pin_diameter_mm": "Stiftdurchmesser (mm)",
        "ui.pin_length_mm": "Stiftlänge (mm)",
        "ui.segments": "Segmente",
        "ui.segments_desc": "Zylinderstift-Radialsegmente (optische Glätte)",
        "ui.tenon_width_mm": "Zapfenbreite (mm)",
        "ui.tenon_depth_mm": "Zapfentiefe (mm)",
        "ui.chamfer_mm": "Fase (mm)",

        # Insert depth
        "ui.insert_depth_pct": "Einstecktiefe (%)",
        "ui.insert_depth_pct_desc": "Prozentualer Anteil der Verbinderlänge, der in Teil A versenkt wird",

        # Material / Tolerance
        "ui.material_profiles": "Material-Profile",
        "ui.material_profile_desc": "Materialprofil wählen, um Toleranz pro Seite automatisch zu befüllen",
        "profiles.mat.tooltip": "Empfohlene Toleranz pro Seite: {val:.2f} mm",
        "ui.tol_per_face_mm": "Toleranz pro Fläche (mm)",
        "ui.tol_override_desc": "Überschreibt das Materialprofil (0 = Profilwert verwenden)",

        # Foldouts
        "ui.foldout.more_seg": "Weitere Segmentierungs-Einstellungen",
        "ui.foldout.more_seg_desc": "Erweiterte Segmentierungsoptionen anzeigen",
        "ui.foldout.more_conn": "Weitere Verbindungs-Einstellungen",
        "ui.foldout.more_conn_desc": "Erweiterte Verbindungs-/Geometrieoptionen anzeigen",
        "ui.foldout.more_tol": "Weitere Toleranz-Einstellungen",
        "ui.foldout.more_tol_desc": "Erweiterte Toleranzoptionen anzeigen",
        "ui.foldout.more_align": "Weitere Ausrichtungs-Einstellungen",
        "ui.foldout.more_align_desc": "Erweiterte Ausrichtungsoptionen anzeigen",

        # Tooltips
        "tooltip.planar_split": "Teilt die ausgewählte Geometrie entlang einer Best-Fit-Ebene.",
        "tooltip.adjust": "Öffnet Feineinstellungen für den aktuellen Vorgang.",
        "tooltip.show_split_preview": "Schaltet die visuelle Schnittvorschau vor dem Anwenden um.",

        # Additional UI mentioned
        "ui.segmentation_title": "Segmentierung",
        "ui.less": "Weniger",
        "ui.adjust": "Anpassen",
        "ui.cap_seams_during_split_slow": "Nähte während des Schnitts verschließen (langsamer)",
        "ui.connections_title": "Verbindungen",
        "ui.add_connectors": "Verbinder hinzufügen",
        "ui.place_connectors_click": "Verbinder platzieren (Klick)",
        "ui.pick_faces_hint": "Flächen im Objektmodus wählen (A = Ziel, B = beweglich)",
        "ui.face_a_none": "A: keine",
        "ui.face_b_none": "B: keine",
        "ui.pick_face_a": "Fläche A wählen",
        "ui.pick_face_b": "Fläche B wählen",
        "ui.align_faces": "Flächen ausrichten",
        "ui.align_faces_desc": "Richte Fläche B an Fläche A mit lokaler Anpassung und Orientierung aus",
    },

    # French (France) - complete
    "fr_FR": {
        "ui.panel.title": "SnapSplit",
        "ui.reload_language": "Recharger la langue de l’interface",
        "ui.reload_language_desc": "Réenregistrer l’add-on pour appliquer la langue Blender aux libellés statiques.",
        "ui.section.profiles": "Profils",
        "ui.section.tools": "Outils",
        "ui.button.apply": "Appliquer",
        "ui.button.cancel": "Annuler",
        "ui.button.ok": "OK",
        "ui.section.export": "Exporter",
        "ui.section.settings": "Paramètres",
        "ui.label.collection": "Collection d’export",
        "ui.tooltip.collection": "Collection utilisée pour la sortie d’export",

        "prefs.title": "Préférences SnapSplit",
        "prefs.default_profile": "Profil par défaut",
        "prefs.create_export_collection": "Créer une collection d’export",
        "prefs.language_note": "La langue suit celle de l’interface Blender. Après changement, utilisez « Recharger la langue de l’interface ».",
        "prefs.reload_language": "Recharger la langue de l’interface",
        "prefs.reload_language_desc": "Réenregistrer l’add-on pour actualiser les libellés statiques (opérateurs/propriétés).",

        "profiles.name": "Profil",
        "profiles.description": "Profil SnapSplit actif",
        "profiles.enum.material": "Matériau",
        "profiles.enum.material_desc": "Stratégie d’attribution des matériaux",
        "profiles.enum.method": "Méthode",
        "profiles.enum.method_desc": "Méthode de découpe à utiliser",

        "op.adjust_axis.label": "Ajuster l’axe de coupe",
        "op.adjust_axis.done": "Axe de coupe ajusté.",
        "op.adjust_axis.cancelled": "Ajustement de l’axe de coupe annulé.",

        "op.split.label": "Découpe planaire",
        "op.split.desc": "Séparer les faces le long d’un plan ajusté",
        "op.split.many_parts_hint": "Découper en de nombreuses pièces peut prendre du temps sur des maillages denses...",
        "op.split.autocap.none": "Le bouchage automatique n’a trouvé aucune boucle valide.",
        "op.split.autocap.count": "Bouchage automatique des arêtes sur {n} pièce(s).",
        "op.split.fewer_parts": "Moins de pièces créées que prévu ({have} < {want}).",
        "op.split.parts_created": "{n} pièces créées.",

        "op.cap_now.label": "Boucher les arêtes maintenant",
        "op.cap_now.desc": "Remplir entre exactement deux boucles d’arêtes de coupe (externe+interne) per plan. Seeds privilégiés.",
        "op.cap_now.only_selected.name": "Objets sélectionnés uniquement",
        "op.cap_now.max_planes.name": "Plans maximum",
        "op.cap_now.max_planes.desc": "0 = tous les plans per objet, 1 = seulement le plus grand",
        "op.cap_now.select_only.name": "Sélectionner seulement (sans remplissage)",
        "op.cap_now.require_two_seeds.name": "Exiger exactement deux arêtes seed",
        "op.cap_now.require_two_seeds.desc": "Si exactement deux arêtes sont sélectionnées en mode Édition, les utiliser uniquement comme seeds (pas d’auto-détection).",
        "op.cap_now.no_targets": "Aucun objet maillage à boucher. Sélectionnez des pièces découpées ou utilisez la collection des pièces.",
        "op.cap_now.failed_one": "Échec du traitement sur « {name} » : {err}",
        "op.cap_now.none_selected": "Impossible de déterminer les boucles d’arêtes de coupe à sélectionner.",
        "op.cap_now.none_capped": "Impossible de déterminer et de remplir les boucles d’arêtes de coupe.",
        "op.cap_now.selected_count": "Boucles d’arêtes de coupe sélectionnées sur {n} objet(s).",
        "op.cap_now.capped_count": "Arêtes bouchées sur {n} objet(s).",

        "op.common.select_mesh": "Veuillez sélectionner un objet maillage.",

        "warn.unapplied_transforms": "L’objet a des transformations non appliquées",
        "warn.apply_transforms_hint": "Envisagez d’appliquer toutes les transformations (Ctrl+A) pour des résultats précis et prévisibles.",

        "msg.no_active_object": "Aucun objet actif.",
        "msg.not_mesh": "L’objet actif n’est pas un maillage.",
        "msg.operation_done": "Opération terminée.",
        "msg.operation_failed": "Échec de l’opération.",
        "msg.unapplied_transforms": "L’objet a des transformations non appliquées",

        # profiles.py specific UI
        "ui.split_offset_mm": "Décalage de coupe (mm)",
        "ui.split_offset_desc": "Décalage du plan de coupe le long de l’axe (positif dans le sens de l’axe)",
        "ui.split_axis": "Axe de coupe",
        "ui.split_along_x": "Couper selon X",
        "ui.split_along_y": "Couper selon Y",
        "ui.split_along_z": "Couper selon Z",
        "ui.show_split_preview": "Afficher l’aperçu de coupe",
        "ui.show_split_preview_desc": "Afficher des plans orange temporaires aux positions de coupe prévues",
        "ui.parts_count": "Nombre de pièces",
        "ui.parts_count_desc": "Nombre de segments souhaités (plans de coupe = pièces - 1)",

        "ui.cap_seams_during_split_short": "Boucher les arêtes pendant la coupe",
        "ui.cap_seams_during_split_desc": "Fermer automatiquement les arêtes après la coupe. Avec cavité/coque interne : remplissage précis des boucles externe/interne ; sans cavité : remplissage simple. Peut augmenter le temps d’exécution.",

        "ui.connector_type": "Type de connecteur",
        "ui.cyl_pin": "Goujon cylindrique",
        "ui.cyl_pin_desc": "Goujon + douille",
        "ui.rect_tenon": "Tenon rectangulaire",
        "ui.rect_tenon_desc": "Articulation anti-rotation",
        "ui.snap_pin": "Goujon à encliqueter",
        "ui.snap_pin_desc": "Connecteur avec billes d’encliquetage",
        "ui.snap_tenon": "Tenon à encliqueter",
        "ui.snap_tenon_desc": "Tenon rectangulaire avec billes d’encliquetage",

        "ui.distribution": "Répartition",
        "ui.distribution_desc": "Répartir les connecteurs le long d’une ligne ou en grille sur la surface de la couture",
        "ui.line": "Ligne",
        "ui.line_desc": "Placer les connecteurs le long d’une ligne dans la surface de la couture",
        "ui.grid": "Grille",
        "ui.grid_desc": "Répartir les connecteurs en grille sur la surface de la couture",
        "ui.connectors_per_seam": "Connecteurs par couture",
        "ui.rows_grid": "Rangées (GRILLE)",
        "ui.rows_grid_desc": "Nombre de rangées pour la répartition en grille",
        "ui.margin_pct": "Marge (%)",
        "ui.margin_pct_desc": "Marge de bord le long de la couture (et perpendiculaire en GRILLE) en pourcentage de la longueur de la pièce (0–40 % recommandé)",

        "ui.spheres_per_side": "Billes par côté",
        "ui.spheres_per_side_desc": "Nombre de billes d’encliquetage par côté/pourtour",
        "ui.sphere_diameter_mm": "Diamètre bille (mm)",
        "ui.sphere_diameter_mm_desc": "Diamètre des billes d’encliquetage",
        "ui.protrusion_mm": "Saillie (mm)",
        "ui.protrusion_mm_desc": "De combien les billes dépassent de la surface latérale",

        "ui.pin_diameter_mm": "Diamètre du goujon (mm)",
        "ui.pin_length_mm": "Longueur du goujon (mm)",
        "ui.segments": "Segments",
        "ui.segments_desc": "Segments radiaux du goujon cylindrique (lissage visuel)",
        "ui.tenon_width_mm": "Largeur du tenon (mm)",
        "ui.tenon_depth_mm": "Profondeur du tenon (mm)",
        "ui.chamfer_mm": "Chanfrein (mm)",

        "ui.insert_depth_pct": "Profondeur d’insertion (%)",
        "ui.insert_depth_pct_desc": "Pourcentage de la longueur du connecteur encastré dans la pièce A",

        "ui.material_profiles": "Profils de matériau",
        "ui.material_profile_desc": "Sélectionner un profil matériau pour préremplir la tolérance par côté",
        "profiles.mat.tooltip": "Tolérance recommandée par côté : {val:.2f} mm",
        "ui.tol_per_face_mm": "Tolérance par face (mm)",
        "ui.tol_override_desc": "Passe outre le profil matériau (0 = utiliser la valeur du profil)",

        "ui.foldout.more_seg": "Plus de réglages de segmentation",
        "ui.foldout.more_seg_desc": "Afficher les options avancées de segmentation",
        "ui.foldout.more_conn": "Plus de réglages de connexion",
        "ui.foldout.more_conn_desc": "Afficher les options avancées de connexion/géométrie",
        "ui.foldout.more_tol": "Plus de réglages de tolérance",
        "ui.foldout.more_tol_desc": "Afficher les options avancées de tolérance",
        "ui.foldout.more_align": "Plus de réglages d’alignement",
        "ui.foldout.more_align_desc": "Afficher les options avancées d’alignement",

        "tooltip.planar_split": "Découpe la géométrie sélectionnée selon un plan ajusté.",
        "tooltip.adjust": "Ouvre les réglages fins de l’opération en cours.",
        "tooltip.show_split_preview": "Active/désactive l’aperçu visuel avant application.",

        "ui.segmentation_title": "Segmentation",
        "ui.less": "Moins",
        "ui.adjust": "Ajuster",
        "ui.cap_seams_during_split_slow": "Boucher les arêtes pendant la coupe (plus lent)",
        "ui.connections_title": "Connexions",
        "ui.add_connectors": "Ajouter des connecteurs",
        "ui.place_connectors_click": "Placer des connecteurs (clic)",
        "ui.pick_faces_hint": "Choisir des faces en mode Objet (A = cible, B = mobile)",
        "ui.face_a_none": "A : aucune",
        "ui.face_b_none": "B : aucune",
        "ui.pick_face_a": "Choisir face A",
        "ui.pick_face_b": "Choisir face B",
        "ui.align_faces": "Aligner les faces",
        "ui.align_faces_desc": "Aligner la face B sur la face A avec ajustement local et orientation",
    },

    # Spanish (Spain) - complete
    "es_ES": {
        "ui.panel.title": "SnapSplit",
        "ui.reload_language": "Recargar idioma de la interfaz",
        "ui.reload_language_desc": "Volver a registrar el complemento para aplicar el idioma de Blender a las etiquetas estáticas.",
        "ui.section.profiles": "Perfiles",
        "ui.section.tools": "Herramientas",
        "ui.button.apply": "Aplicar",
        "ui.button.cancel": "Cancelar",
        "ui.button.ok": "OK",
        "ui.section.export": "Exportar",
        "ui.section.settings": "Ajustes",
        "ui.label.collection": "Colección de exportación",
        "ui.tooltip.collection": "Colección utilizada para la salida de exportación",

        "prefs.title": "Preferencias de SnapSplit",
        "prefs.default_profile": "Perfil predeterminado",
        "prefs.create_export_collection": "Crear colección de exportación",
        "prefs.language_note": "El idioma sigue el de la interfaz de Blender. Tras cambiarlo, use «Recargar idioma de la interfaz».",
        "prefs.reload_language": "Recargar idioma de la interfaz",
        "prefs.reload_language_desc": "Volver a registrar el complemento para actualizar las etiquetas estáticas (operadores/propiedades).",

        "profiles.name": "Perfil",
        "profiles.description": "Perfil activo de SnapSplit",
        "profiles.enum.material": "Material",
        "profiles.enum.material_desc": "Estrategia de asignación de materiales",
        "profiles.enum.method": "Método",
        "profiles.enum.method_desc": "Método de división a utilizar",

        "op.adjust_axis.label": "Ajustar eje de corte",
        "op.adjust_axis.done": "Eje de corte ajustado.",
        "op.adjust_axis.cancelled": "Ajuste del eje de corte cancelado.",

        "op.split.label": "Corte planar",
        "op.split.desc": "Dividir caras a lo largo de un plano ajustado",
        "op.split.many_parts_hint": "Dividir en muchas partes puede llevar tiempo en mallas densas...",
        "op.split.autocap.none": "El cierre automático no encontró bucles válidos.",
        "op.split.autocap.count": "Cierres automáticos en {n} parte(s).",
        "op.split.fewer_parts": "Se crearon menos partes de las esperadas ({have} < {want}).",
        "op.split.parts_created": "Se crearon {n} partes.",

        "op.cap_now.label": "Cerrar bordes ahora",
        "op.cap_now.desc": "Rellenar entre exactamente dos bucles de aristas de corte (externo+interno) por plano. Seeds preferidos.",
        "op.cap_now.only_selected.name": "Solo objetos seleccionados",
        "op.cap_now.max_planes.name": "Planes máximos",
        "op.cap_now.max_planes.desc": "0 = todos los planes por objeto, 1 = solo el mayor",
        "op.cap_now.select_only.name": "Solo seleccionar (sin rellenar)",
        "op.cap_now.require_two_seeds.name": "Exigir exactamente dos aristas seed",
        "op.cap_now.require_two_seeds.desc": "Si hay exactamente dos aristas seleccionadas en Modo Edición, usarlas como seeds únicamente (sin autodetección).",
        "op.cap_now.no_targets": "No hay objetos de malla para cerrar. Seleccione piezas divididas o use la colección de piezas.",
        "op.cap_now.failed_one": "Error al procesar «{name}»: {err}",
        "op.cap_now.none_selected": "No se pudieron determinar los bucles de aristas de corte para seleccionar.",
        "op.cap_now.none_capped": "No se pudieron determinar y rellenar los bucles de aristas de corte.",
        "op.cap_now.selected_count": "Bucles de aristas de corte seleccionados en {n} objeto(s).",
        "op.cap_now.capped_count": "Bordes cerrados en {n} objeto(s).",

        "op.common.select_mesh": "Seleccione un objeto de malla.",

        "warn.unapplied_transforms": "El objeto tiene transformaciones no aplicadas",
        "warn.apply_transforms_hint": "Considere aplicar todas las transformaciones (Ctrl+A) para resultados precisos y predecibles.",

        "msg.no_active_object": "No hay objeto activo.",
        "msg.not_mesh": "El objeto activo no es una malla.",
        "msg.operation_done": "Operación finalizada.",
        "msg.operation_failed": "La operación falló.",
        "msg.unapplied_transforms": "El objeto tiene transformaciones no aplicadas",

        # profiles.py specific UI
        "ui.split_offset_mm": "Desplazamiento de corte (mm)",
        "ui.split_offset_desc": "Desplazamiento del plano de corte a lo largo del eje (positivo en la dirección del eje)",
        "ui.split_axis": "Eje de corte",
        "ui.split_along_x": "Cortar a lo largo de X",
        "ui.split_along_y": "Cortar a lo largo de Y",
        "ui.split_along_z": "Cortar a lo largo de Z",
        "ui.show_split_preview": "Mostrar vista previa de corte",
        "ui.show_split_preview_desc": "Mostrar planos naranjas temporales en posiciones de corte previstas",
        "ui.parts_count": "Número de partes",
        "ui.parts_count_desc": "Número de segmentos deseados (planos de corte = partes - 1)",

        "ui.cap_seams_during_split_short": "Cerrar bordes durante el corte",
        "ui.cap_seams_during_split_desc": "Cerrar automáticamente los bordes tras el corte. Con cavidad/carcasa interna: relleno preciso de los bucles externo/interno; sin cavidad: relleno simple. Puede aumentar el tiempo de ejecución.",

        "ui.connector_type": "Tipo de conector",
        "ui.cyl_pin": "Pasador cilíndrico",
        "ui.cyl_pin_desc": "Pasador + casquillo",
        "ui.rect_tenon": "Espiga rectangular",
        "ui.rect_tenon_desc": "Unión antirrotación",
        "ui.snap_pin": "Pasador a presión",
        "ui.snap_pin_desc": "Conector con esferas de enganche",
        "ui.snap_tenon": "Espiga a presión",
        "ui.snap_tenon_desc": "Espiga rectangular con esferas de enganche",

        "ui.distribution": "Distribución",
        "ui.distribution_desc": "Distribuir conectores a lo largo de una línea o en una cuadrícula sobre la superficie de la junta",
        "ui.line": "Línea",
        "ui.line_desc": "Colocar conectores a lo largo de una línea en la superficie de la junta",
        "ui.grid": "Cuadrícula",
        "ui.grid_desc": "Distribuir conectores en una cuadrícula sobre la superficie de la junta",
        "ui.connectors_per_seam": "Conectores por junta",
        "ui.rows_grid": "Filas (CUADRÍCULA)",
        "ui.rows_grid_desc": "Número de filas para la distribución en cuadrícula",
        "ui.margin_pct": "Margen (%)",
        "ui.margin_pct_desc": "Margen del borde a lo largo de la junta (y perpendicular en CUADRÍCULA) como porcentaje de la longitud de la pieza (0–40 % recomendado)",

        "ui.spheres_per_side": "Esferas por lado",
        "ui.spheres_per_side_desc": "Número de esferas de enganche por lado/alrededor",
        "ui.sphere_diameter_mm": "Diámetro de esfera (mm)",
        "ui.sphere_diameter_mm_desc": "Diámetro de las esferas de enganche",
        "ui.protrusion_mm": "Protrusión (mm)",
        "ui.protrusion_mm_desc": "Cuánto sobresalen las esferas de la superficie lateral",

        "ui.pin_diameter_mm": "Diámetro del pasador (mm)",
        "ui.pin_length_mm": "Longitud del pasador (mm)",
        "ui.segments": "Segmentos",
        "ui.segments_desc": "Segmentos radiales del pasador cilíndrico (suavidad visual)",
        "ui.tenon_width_mm": "Ancho de la espiga (mm)",
        "ui.tenon_depth_mm": "Profundidad de la espiga (mm)",
        "ui.chamfer_mm": "Chaflán (mm)",

        "ui.insert_depth_pct": "Profundidad de inserción (%)",
        "ui.insert_depth_pct_desc": "Porcentaje de la longitud del conector empotrado en la pieza A",

        "ui.material_profiles": "Perfiles de material",
        "ui.material_profile_desc": "Seleccione un perfil de material para rellenar automáticamente la tolerancia por lado",
        "profiles.mat.tooltip": "Tolerancia recomendada por lado: {val:.2f} mm",
        "ui.tol_per_face_mm": "Tolerancia por cara (mm)",
        "ui.tol_override_desc": "Sobrescribe el perfil de material (0 = usar valor del perfil)",

        "ui.foldout.more_seg": "Más ajustes de segmentación",
        "ui.foldout.more_seg_desc": "Mostrar opciones avanzadas de segmentación",
        "ui.foldout.more_conn": "Más ajustes de conexión",
        "ui.foldout.more_conn_desc": "Mostrar opciones avanzadas de conexión/geometría",
        "ui.foldout.more_tol": "Más ajustes de tolerancia",
        "ui.foldout.more_tol_desc": "Mostrar opciones avanzadas de tolerancia",
        "ui.foldout.more_align": "Más ajustes de alineación",
        "ui.foldout.more_align_desc": "Mostrar opciones avanzadas de alineación",

        "tooltip.planar_split": "Divide la geometría seleccionada según un plano de mejor ajuste.",
        "tooltip.adjust": "Abre los ajustes finos de la operación actual.",
        "tooltip.show_split_preview": "Activa/desactiva la vista previa antes de aplicar.",

        "ui.segmentation_title": "Segmentación",
        "ui.less": "Menos",
        "ui.adjust": "Ajustar",
        "ui.cap_seams_during_split_slow": "Cerrar bordes durante el corte (más lento)",
        "ui.connections_title": "Conexiones",
        "ui.add_connectors": "Añadir conectores",
        "ui.place_connectors_click": "Colocar conectores (clic)",
        "ui.pick_faces_hint": "Elegir caras en Modo Objeto (A = objetivo, B = móvil)",
        "ui.face_a_none": "A: ninguno",
        "ui.face_b_none": "B: ninguno",
        "ui.pick_face_a": "Elegir Cara A",
        "ui.pick_face_b": "Elegir Cara B",
        "ui.align_faces": "Alinear caras",
        "ui.align_faces_desc": "Alinear la cara B con la cara A usando ajuste local y orientación",
    },

    # Italian (Italy) - complete
    "it_IT": {
        "ui.panel.title": "SnapSplit",
        "ui.reload_language": "Ricarica lingua interfaccia",
        "ui.reload_language_desc": "Ri-registra l’add-on per applicare la lingua di Blender alle etichette statiche.",
        "ui.section.profiles": "Profili",
        "ui.section.tools": "Strumenti",
        "ui.button.apply": "Applica",
        "ui.button.cancel": "Annulla",
        "ui.button.ok": "OK",
        "ui.section.export": "Esporta",
        "ui.section.settings": "Impostazioni",
        "ui.label.collection": "Collezione di esportazione",
        "ui.tooltip.collection": "Collezione usata per l’output di esportazione",

        "prefs.title": "Preferenze SnapSplit",
        "prefs.default_profile": "Profilo predefinito",
        "prefs.create_export_collection": "Crea collezione di esportazione",
        "prefs.language_note": "La lingua segue quella dell’interfaccia di Blender. Dopo il cambio, usa «Ricarica lingua interfaccia».",
        "prefs.reload_language": "Ricarica lingua interfaccia",
        "prefs.reload_language_desc": "Ri-registra l’add-on per aggiornare le etichette statiche (operatori/proprietà).",

        "profiles.name": "Profilo",
        "profiles.description": "Profilo SnapSplit attivo",
        "profiles.enum.material": "Materiale",
        "profiles.enum.material_desc": "Strategia di assegnazione dei materiali",
        "profiles.enum.method": "Metodo",
        "profiles.enum.method_desc": "Metodo di suddivisione da utilizzare",

        "op.adjust_axis.label": "Regola asse di taglio",
        "op.adjust_axis.done": "Asse di taglio regolato.",
        "op.adjust_axis.cancelled": "Regolazione dell’asse di taglio annullata.",

        "op.split.label": "Taglio planare",
        "op.split.desc": "Dividi le facce lungo un piano adattato",
        "op.split.many_parts_hint": "La suddivisione in molte parti può richiedere tempo su mesh dense...",
        "op.split.autocap.none": "La chiusura automatica non ha trovato loop validi.",
        "op.split.autocap.count": "Chiusure automatiche su {n} parte/i.",
        "op.split.fewer_parts": "Create meno parti del previsto ({have} < {want}).",
        "op.split.parts_created": "Create {n} parti.",

        "op.cap_now.label": "Chiudi bordi ora",
        "op.cap_now.desc": "Riempi tra esattamente due loop di spigoli di taglio (esterno+interno) per piano. Seeds preferiti.",
        "op.cap_now.only_selected.name": "Solo oggetti selezionati",
        "op.cap_now.max_planes.name": "Piani massimi",
        "op.cap_now.max_planes.desc": "0 = tutti i piani per oggetto, 1 = solo il maggiore",
        "op.cap_now.select_only.name": "Solo seleziona (non riempire)",
        "op.cap_now.require_two_seeds.name": "Richiedi esattamente due spigoli seed",
        "op.cap_now.require_two_seeds.desc": "Se in Modalità Modifica sono selezionati esattamente due spigoli, usali solo come seeds (nessun rilevamento automatico).",
        "op.cap_now.no_targets": "Nessun oggetto mesh da chiudere. Seleziona parti divise o usa la collezione delle parti.",
        "op.cap_now.failed_one": "Elaborazione non riuscita su «{name}»: {err}",
        "op.cap_now.none_selected": "Impossibile determinare i loop di spigoli di taglio da selezionare.",
        "op.cap_now.none_capped": "Impossibile determinare e riempire i loop di spigoli di taglio.",
        "op.cap_now.selected_count": "Loop di spigoli di taglio selezionati su {n} oggetto/i.",
        "op.cap_now.capped_count": "Bordi chiusi su {n} oggetto/i.",

        "op.common.select_mesh": "Seleziona un oggetto mesh.",

        "warn.unapplied_transforms": "L’oggetto ha trasformazioni non applicate",
        "warn.apply_transforms_hint": "Valuta di applicare tutte le trasformazioni (Ctrl+A) per risultati precisi e prevedibili.",

        "msg.no_active_object": "Nessun oggetto attivo.",
        "msg.not_mesh": "L’oggetto attivo non è una mesh.",
        "msg.operation_done": "Operazione completata.",
        "msg.operation_failed": "Operazione non riuscita.",
        "msg.unapplied_transforms": "L’oggetto ha trasformazioni non applicate",

        # profiles.py specific UI
        "ui.split_offset_mm": "Offset di taglio (mm)",
        "ui.split_offset_desc": "Offset del piano di taglio lungo l’asse (positivo nella direzione dell’asse)",
        "ui.split_axis": "Asse di taglio",
        "ui.split_along_x": "Taglia lungo X",
        "ui.split_along_y": "Taglia lungo Y",
        "ui.split_along_z": "Taglia lungo Z",
        "ui.show_split_preview": "Mostra anteprima taglio",
        "ui.show_split_preview_desc": "Mostra piani arancioni temporanei nelle posizioni di taglio previste",
        "ui.parts_count": "Numero di parti",
        "ui.parts_count_desc": "Numero di segmenti desiderati (piani di taglio = parti - 1)",

        "ui.cap_seams_during_split_short": "Chiudi bordi durante il taglio",
        "ui.cap_seams_during_split_desc": "Chiudi automaticamente i bordi dopo il taglio. Con cavità/guscio interno: riempimento preciso dei loop esterno/interno; senza cavità: riempimento semplice. Può aumentare i tempi.",

        "ui.connector_type": "Tipo di connettore",
        "ui.cyl_pin": "Perno cilindrico",
        "ui.cyl_pin_desc": "Perno + boccola",
        "ui.rect_tenon": "Tenone rettangolare",
        "ui.rect_tenon_desc": "Giunto anti-rotazione",
        "ui.snap_pin": "Perno a scatto",
        "ui.snap_pin_desc": "Connettore con sfere a scatto",
        "ui.snap_tenon": "Tenone a scatto",
        "ui.snap_tenon_desc": "Tenone rettangolare con sfere a scatto",

        "ui.distribution": "Distribuzione",
        "ui.distribution_desc": "Distribuisci i connettori lungo una linea o in una griglia sulla superficie della giunzione",
        "ui.line": "Linea",
        "ui.line_desc": "Posiziona i connettori lungo una linea sulla superficie della giunzione",
        "ui.grid": "Griglia",
        "ui.grid_desc": "Distribuisci i connettori in una griglia sulla superficie della giunzione",
        "ui.connectors_per_seam": "Connettori per giunzione",
        "ui.rows_grid": "Righe (GRIGLIA)",
        "ui.rows_grid_desc": "Numero di righe per la distribuzione a griglia",
        "ui.margin_pct": "Margine (%)",
        "ui.margin_pct_desc": "Margine del bordo lungo la giunzione (e perpendicolare in GRIGLIA) come percentuale della lunghezza del pezzo (0–40% consigliato)",

        "ui.spheres_per_side": "Sfere per lato",
        "ui.spheres_per_side_desc": "Numero di sfere a scatto per lato/intorno",
        "ui.sphere_diameter_mm": "Diametro sfera (mm)",
        "ui.sphere_diameter_mm_desc": "Diametro delle sfere a scatto",
        "ui.protrusion_mm": "Sporgenza (mm)",
        "ui.protrusion_mm_desc": "Entità di sporgenza delle sfere dalla superficie laterale",

        "ui.pin_diameter_mm": "Diametro del perno (mm)",
        "ui.pin_length_mm": "Lunghezza del perno (mm)",
        "ui.segments": "Segmenti",
        "ui.segments_desc": "Segmenti radiali del perno cilindrico (morbidezza visiva)",
        "ui.tenon_width_mm": "Larghezza del tenone (mm)",
        "ui.tenon_depth_mm": "Profondeur del tenone (mm)",
        "ui.chamfer_mm": "Smusso (mm)",

        "ui.insert_depth_pct": "Profondità di inserimento (%)",
        "ui.insert_depth_pct_desc": "Percentuale della lunghezza del connettore incassata nella parte A",

        "ui.material_profiles": "Profili materiale",
        "ui.material_profile_desc": "Seleziona un profilo materiale per precompilare la tolleranza per lato",
        "profiles.mat.tooltip": "Tolleranza consigliata per lato: {val:.2f} mm",
        "ui.tol_per_face_mm": "Tolleranza per faccia (mm)",
        "ui.tol_override_desc": "Sovrascrive il profilo materiale (0 = usa valore del profilo)",

        "ui.foldout.more_seg": "Altre impostazioni di segmentazione",
        "ui.foldout.more_seg_desc": "Mostra le opzioni avanzate di segmentazione",
        "ui.foldout.more_conn": "Altre impostazioni di connessione",
        "ui.foldout.more_conn_desc": "Mostra le opzioni avanzate di connessione/geometria",
        "ui.foldout.more_tol": "Altre impostazioni di tolleranza",
        "ui.foldout.more_tol_desc": "Mostra le opzioni avanzate di tolleranza",
        "ui.foldout.more_align": "Altre impostazioni di allineamento",
        "ui.foldout.more_align_desc": "Mostra le opzioni avanzate di allineamento",

        "tooltip.planar_split": "Divide la geometria selezionata con un piano di miglior adattamento.",
        "tooltip.adjust": "Apre le regolazioni fini per l’operazione corrente.",
        "tooltip.show_split_preview": "Attiva/disattiva l’anteprima visiva prima di applicare.",

        "ui.segmentation_title": "Segmentazione",
        "ui.less": "Meno",
        "ui.adjust": "Regola",
        "ui.cap_seams_during_split_slow": "Chiudi bordi durante il taglio (più lento)",
        "ui.connections_title": "Connessioni",
        "ui.add_connectors": "Aggiungi connettori",
        "ui.place_connectors_click": "Posiziona connettori (clic)",
        "ui.pick_faces_hint": "Scegli facce in Modalità Oggetto (A = bersaglio, B = mobile)",
        "ui.face_a_none": "A: nessuna",
        "ui.face_b_none": "B: nessuna",
        "ui.pick_face_a": "Scegli Faccia A",
        "ui.pick_face_b": "Scegli Faccia B",
        "ui.align_faces": "Allinea facce",
        "ui.align_faces_desc": "Allinea la faccia B alla faccia A con adattamento locale e orientamento",
    },

    # Portuguese (Brazil) - complete
    "pt_BR": {
        "ui.panel.title": "SnapSplit",
        "ui.reload_language": "Recarregar idioma da interface",
        "ui.reload_language_desc": "Registrar novamente o add-on para aplicar o idioma do Blender aos rótulos estáticos.",
        "ui.section.profiles": "Perfis",
        "ui.section.tools": "Ferramentas",
        "ui.button.apply": "Aplicar",
        "ui.button.cancel": "Cancelar",
        "ui.button.ok": "OK",
        "ui.section.export": "Exportar",
        "ui.section.settings": "Configurações",
        "ui.label.collection": "Coleção de exportação",
        "ui.tooltip.collection": "Coleção usada para a saída de exportação",

        "prefs.title": "Preferências do SnapSplit",
        "prefs.default_profile": "Perfil padrão",
        "prefs.create_export_collection": "Criar coleção de exportação",
        "prefs.language_note": "O idioma segue o da interface do Blender. Após alterar, use «Recarregar idioma da interface».",
        "prefs.reload_language": "Recarregar idioma da interface",
        "prefs.reload_language_desc": "Registrar novamente o add-on para atualizar os rótulos estáticos (operadores/propriedades).",

        "profiles.name": "Perfil",
        "profiles.description": "Perfil ativo do SnapSplit",
        "profiles.enum.material": "Material",
        "profiles.enum.material_desc": "Estratégia de atribuição de materiais",
        "profiles.enum.method": "Método",
        "profiles.enum.method_desc": "Método de divisão a ser usado",

        "op.adjust_axis.label": "Ajustar eixo de corte",
        "op.adjust_axis.done": "Eixo de corte ajustado.",
        "op.adjust_axis.cancelled": "Ajuste do eixo de corte cancelado.",

        "op.split.label": "Corte planar",
        "op.split.desc": "Dividir faces ao longo de um plano ajustado",
        "op.split.many_parts_hint": "Dividir em muitas partes pode levar tempo em malhas densas...",
        "op.split.autocap.none": "O fechamento automático não encontrou loops válidos.",
        "op.split.autocap.count": "Fechamentos automáticos em {n} parte(s).",
        "op.split.fewer_parts": "Menos partes criadas do que o esperado ({have} < {want}).",
        "op.split.parts_created": "{n} partes criadas.",

        "op.cap_now.label": "Fechar bordas agora",
        "op.cap_now.desc": "Preencher entre exatamente dois loops de arestas de corte (externo+interno) por plano. Seeds preferidos.",
        "op.cap_now.only_selected.name": "Apenas objetos selecionados",
        "op.cap_now.max_planes.name": "Máx. planos",
        "op.cap_now.max_planes.desc": "0 = todos os planos por objeto, 1 = apenas o maior",
        "op.cap_now.select_only.name": "Apenas selecionar (sem preencher)",
        "op.cap_now.require_two_seeds.name": "Exigir exatamente duas arestas seed",
        "op.cap_now.require_two_seeds.desc": "Se exatamente duas arestas estiverem selecionadas no Modo de Edição, usá-las apenas como seeds (sem detecção automática).",
        "op.cap_now.no_targets": "Nenhum objeto de malha para fechar. Selecione partes divididas ou use a coleção de partes.",
        "op.cap_now.failed_one": "Falha ao processar «{name}»: {err}",
        "op.cap_now.none_selected": "Não foi possível determinar os loops de arestas de corte para selecionar.",
        "op.cap_now.none_capped": "Não foi possível determinar e preencher os loops de arestas de corte.",
        "op.cap_now.selected_count": "Loops de arestas de corte selecionados em {n} objeto(s).",
        "op.cap_now.capped_count": "Bordas fechadas em {n} objeto(s).",

        "op.common.select_mesh": "Selecione um objeto de malha.",

        "warn.unapplied_transforms": "O objeto possui transformações não aplicadas",
        "warn.apply_transforms_hint": "Considere aplicar todas as transformações (Ctrl+A) para resultados precisos e previsíveis.",

        "msg.no_active_object": "Nenhum objeto ativo.",
        "msg.not_mesh": "O objeto ativo não é uma malha.",
        "msg.operation_done": "Operação concluída.",
        "msg.operation_failed": "Falha na operação.",
        "msg.unapplied_transforms": "O objeto possui transformações não aplicadas",

        # profiles.py specific UI
        "ui.split_offset_mm": "Deslocamento de corte (mm)",
        "ui.split_offset_desc": "Deslocamento do plano de corte ao longo do eixo (positivo na direção do eixo)",
        "ui.split_axis": "Eixo de corte",
        "ui.split_along_x": "Cortar ao longo de X",
        "ui.split_along_y": "Cortar ao longo de Y",
        "ui.split_along_z": "Cortar ao longo de Z",
        "ui.show_split_preview": "Mostrar prévia de corte",
        "ui.show_split_preview_desc": "Mostrar planos laranja temporários nas posições de corte previstas",
        "ui.parts_count": "Número de partes",
        "ui.parts_count_desc": "Número de segmentos desejados (planos de corte = partes - 1)",

        "ui.cap_seams_during_split_short": "Fechar bordas durante o corte",
        "ui.cap_seams_during_split_desc": "Fechar automaticamente as bordas após o corte. Com cavidade/casca interna: preenchimento preciso dos loops externo/interno; sem cavidade: preenchimento simples. Pode aumentar o tempo de execução.",

        "ui.connector_type": "Tipo de conector",
        "ui.cyl_pin": "Pino cilíndrico",
        "ui.cyl_pin_desc": "Pino + bucha",
        "ui.rect_tenon": "Espiga retangular",
        "ui.rect_tenon_desc": "Junção anti-rotação",
        "ui.snap_pin": "Pino de encaixe",
        "ui.snap_pin_desc": "Conector com esferas de encaixe",
        "ui.snap_tenon": "Espiga de encaixe",
        "ui.snap_tenon_desc": "Espiga retangular com esferas de encaixe",

        "ui.distribution": "Distribuição",
        "ui.distribution_desc": "Distribua conectores ao longo de uma linha ou em uma grade na superfície da junta",
        "ui.line": "Linha",
        "ui.line_desc": "Coloque conectores ao longo de uma linha na superfície da junta",
        "ui.grid": "Grade",
        "ui.grid_desc": "Distribua conectores em uma grade na superfície da junta",
        "ui.connectors_per_seam": "Conectores por junta",
        "ui.rows_grid": "Linhas (GRADE)",
        "ui.rows_grid_desc": "Número de linhas para a distribuição em grade",
        "ui.margin_pct": "Margem (%)",
        "ui.margin_pct_desc": "Margem da borda ao longo da junta (e perpendicular na GRADE) como porcentagem do comprimento da peça (0–40% recomendado)",

        "ui.spheres_per_side": "Esferas por lado",
        "ui.spheres_per_side_desc": "Número de esferas de encaixe por lado/ao redor",
        "ui.sphere_diameter_mm": "Diâmetro da esfera (mm)",
        "ui.sphere_diameter_mm_desc": "Diâmetro das esferas de encaixe",
        "ui.protrusion_mm": "Saliente (mm)",
        "ui.protrusion_mm_desc": "O quanto as esferas se projetam da superfície lateral",

        "ui.pin_diameter_mm": "Diâmetro do pino (mm)",
        "ui.pin_length_mm": "Comprimento do pino (mm)",
        "ui.segments": "Segmentos",
        "ui.segments_desc": "Segmentos radiais do pino cilíndrico (suavidade visual)",
        "ui.tenon_width_mm": "Largura da espiga (mm)",
        "ui.tenon_depth_mm": "Profundidade da espiga (mm)",
        "ui.chamfer_mm": "Chanfro (mm)",

        "ui.insert_depth_pct": "Profundidade de inserção (%)",
        "ui.insert_depth_pct_desc": "Percentual do comprimento do conector embutido na peça A",

        "ui.material_profiles": "Perfis de material",
        "ui.material_profile_desc": "Selecione um perfil de material para preencher automaticamente a tolerância por lado",
        "profiles.mat.tooltip": "Tolerância recomendada por lado: {val:.2f} mm",
        "ui.tol_per_face_mm": "Tolerância por face (mm)",
        "ui.tol_override_desc": "Substitui o perfil de material (0 = usar valor do perfil)",

        "ui.foldout.more_seg": "Mais configurações de segmentação",
        "ui.foldout.more_seg_desc": "Mostrar opções avançadas de segmentação",
        "ui.foldout.more_conn": "Mais configurações de conexão",
        "ui.foldout.more_conn_desc": "Mostrar opções avançadas de conexão/geometria",
        "ui.foldout.more_tol": "Mais configurações de tolerância",
        "ui.foldout.more_tol_desc": "Mostrar opções avançadas de tolerância",
        "ui.foldout.more_align": "Mais configurações de alinhamento",
        "ui.foldout.more_align_desc": "Mostrar opções avançadas de alinhamento",

        "tooltip.planar_split": "Divide a geometria selecionada por um plano de melhor ajuste.",
        "tooltip.adjust": "Abre ajustes finos para a operação atual.",
        "tooltip.show_split_preview": "Ativa/desativa a prévia visual antes de aplicar.",

        "ui.segmentation_title": "Segmentação",
        "ui.less": "Menos",
        "ui.adjust": "Ajustar",
        "ui.cap_seams_during_split_slow": "Fechar arestas durante o corte (mais lento)",
        "ui.connections_title": "Conexões",
        "ui.add_connectors": "Adicionar conectores",
        "ui.place_connectors_click": "Posicionar conectores (clique)",
        "ui.pick_faces_hint": "Escolher faces no modo Objeto (A = alvo, B = móvel)",
        "ui.face_a_none": "A: nenhum",
        "ui.face_b_none": "B: nenhum",
        "ui.pick_face_a": "Escolher Face A",
        "ui.pick_face_b": "Escolher Face B",
        "ui.align_faces": "Alinhar faces",
        "ui.align_faces_desc": "Alinhar a face B à face A com ajuste local e orientação",
    },

    # Portuguese (Portugal) - complete
    "pt_PT": {
        "ui.panel.title": "SnapSplit",
        "ui.reload_language": "Recarregar idioma da interface",
        "ui.reload_language_desc": "Registar novamente o add-on para aplicar o idioma do Blender às etiquetas estáticas.",
        "ui.section.profiles": "Perfis",
        "ui.section.tools": "Ferramentas",
        "ui.button.apply": "Aplicar",
        "ui.button.cancel": "Cancelar",
        "ui.button.ok": "OK",
        "ui.section.export": "Exportar",
        "ui.section.settings": "Definições",
        "ui.label.collection": "Coleção de exportação",
        "ui.tooltip.collection": "Coleção usada para a saída de exportação",

        "prefs.title": "Preferências do SnapSplit",
        "prefs.default_profile": "Perfil predefinido",
        "prefs.create_export_collection": "Criar coleção de exportação",
        "prefs.language_note": "O idioma segue o da interface do Blender. Após alterar, utilize «Recarregar idioma da interface».",
        "prefs.reload_language": "Recarregar idioma da interface",
        "prefs.reload_language_desc": "Registar novamente o add-on para atualizar as etiquetas estáticas (operadores/propriedades).",

        "profiles.name": "Perfil",
        "profiles.description": "Perfil ativo do SnapSplit",
        "profiles.enum.material": "Material",
        "profiles.enum.material_desc": "Estratégia de atribuição de materiais",
        "profiles.enum.method": "Método",
        "profiles.enum.method_desc": "Método de divisão a utilizar",

        "op.adjust_axis.label": "Ajustar eixo de corte",
        "op.adjust_axis.done": "Eixo de corte ajustado.",
        "op.adjust_axis.cancelled": "Ajuste do eixo de corte cancelado.",

        "op.split.label": "Corte planar",
        "op.split.desc": "Dividir faces ao longo de um plano ajustado",
        "op.split.many_parts_hint": "Dividir em muitas partes pode demorar em malhas densas...",
        "op.split.autocap.none": "O fecho automático não encontrou loops válidos.",
        "op.split.autocap.count": "Fechos automáticos em {n} parte(s).",
        "op.split.fewer_parts": "Menos partes criadas do que o esperado ({have} < {want}).",
        "op.split.parts_created": "{n} partes criadas.",

        "op.cap_now.label": "Fechar arestas agora",
        "op.cap_now.desc": "Preencher entre exatamente dois loops de arestas de corte (externo+interno) por plano. Seeds preferidos.",
        "op.cap_now.only_selected.name": "Apenas objetos selecionados",
        "op.cap_now.max_planes.name": "Máx. planos",
        "op.cap_now.max_planes.desc": "0 = todos os planos por objeto, 1 = apenas o maior",
        "op.cap_now.select_only.name": "Apenas selecionar (sem preencher)",
        "op.cap_now.require_two_seeds.name": "Exigir exatamente duas arestas seed",
        "op.cap_now.require_two_seeds.desc": "Se exatamente duas arestas estiverem selecionadas no Modo de Edição, usá-las apenas como seeds (sem deteção automática).",
        "op.cap_now.no_targets": "Nenhum objeto de malha para fechar. Selecione partes divididas ou utilize a coleção de partes.",
        "op.cap_now.failed_one": "Falha ao processar «{name}»: {err}",
        "op.cap_now.none_selected": "Não foi possível determinar os loops de arestas de corte para selecionar.",
        "op.cap_now.none_capped": "Não foi possível determinar e preencher os loops de arestas de corte.",
        "op.cap_now.selected_count": "Loops de arestas de corte selecionados em {n} objeto(s).",
        "op.cap_now.capped_count": "Arestas fechadas em {n} objeto(s).",

        "op.common.select_mesh": "Selecione um objeto de malha.",

        "warn.unapplied_transforms": "O objeto tem transformações não aplicadas",
        "warn.apply_transforms_hint": "Considere aplicar todas as transformações (Ctrl+A) para resultados precisos e previsíveis.",

        "msg.no_active_object": "Nenhum objeto ativo.",
        "msg.not_mesh": "O objeto ativo não é uma malha.",
        "msg.operation_done": "Operação concluída.",
        "msg.operation_failed": "Falha na operação.",
        "msg.unapplied_transforms": "O objeto tem transformações não aplicadas",

        # profiles.py specific UI
        "ui.split_offset_mm": "Deslocamento de corte (mm)",
        "ui.split_offset_desc": "Deslocamento do plano de corte ao longo do eixo (positivo na direção do eixo)",
        "ui.split_axis": "Eixo de corte",
        "ui.split_along_x": "Cortar ao longo de X",
        "ui.split_along_y": "Cortar ao longo de Y",
        "ui.split_along_z": "Cortar ao longo de Z",
        "ui.show_split_preview": "Mostrar pré-visualização do corte",
        "ui.show_split_preview_desc": "Mostrar planos laranja temporários nas posições de corte previstas",
        "ui.parts_count": "Número de partes",
        "ui.parts_count_desc": "Número de segmentos desejados (planos de corte = partes - 1)",

        "ui.cap_seams_during_split_short": "Fechar arestas durante o corte",
        "ui.cap_seams_during_split_desc": "Fechar automaticamente as arestas após o corte. Com cavidade/revestimento interno: enchimento preciso dos loops externo/interno; sem cavidade: enchimento simples. Pode aumentar o tempo de execução.",

        "ui.connector_type": "Tipo de conector",
        "ui.cyl_pin": "Pino cilíndrico",
        "ui.cyl_pin_desc": "Pino + bucha",
        "ui.rect_tenon": "Espiga retangular",
        "ui.rect_tenon_desc": "União anti-rotação",
        "ui.snap_pin": "Pino de encaixe",
        "ui.snap_pin_desc": "Conector com esferas de encaixe",
        "ui.snap_tenon": "Espiga de encaixe",
        "ui.snap_tenon_desc": "Espiga retangular com esferas de encaixe",

        "ui.distribution": "Distribuição",
        "ui.distribution_desc": "Distribuir conectores ao longo de uma linha ou numa grelha sobre a superfície da junta",
        "ui.line": "Linha",
        "ui.line_desc": "Colocar conectores ao longo de uma linha na superfície da junta",
        "ui.grid": "Grelha",
        "ui.grid_desc": "Distribuir conectores numa grelha sobre a superfície da junta",
        "ui.connectors_per_seam": "Conectores por junta",
        "ui.rows_grid": "Linhas (GRELHA)",
        "ui.rows_grid_desc": "Número de linhas para a distribuição em grelha",
        "ui.margin_pct": "Margem (%)",
        "ui.margin_pct_desc": "Margem da aresta ao longo da junta (e perpendicular na GRELHA) como percentagem do comprimento da peça (0–40 % recomendado)",

        "ui.spheres_per_side": "Esferas por lado",
        "ui.spheres_per_side_desc": "Número de esferas de encaixe por lado/à volta",
        "ui.sphere_diameter_mm": "Diâmetro da esfera (mm)",
        "ui.sphere_diameter_mm_desc": "Diâmetro das esferas de encaixe",
        "ui.protrusion_mm": "Saliente (mm)",
        "ui.protrusion_mm_desc": "Quanto as esferas sobressaem da superfície lateral",

        "ui.pin_diameter_mm": "Diâmetro do pino (mm)",
        "ui.pin_length_mm": "Comprimento do pino (mm)",
        "ui.segments": "Segmentos",
        "ui.segments_desc": "Segmentos radiais do pino cilíndrico (suavidade visual)",
        "ui.tenon_width_mm": "Largura da espiga (mm)",
        "ui.tenon_depth_mm": "Profundidade da espiga (mm)",
        "ui.chamfer_mm": "Chanfro (mm)",

        "ui.insert_depth_pct": "Profundidade de inserção (%)",
        "ui.insert_depth_pct_desc": "Percentagem do comprimento do conector embutido na peça A",

        "ui.material_profiles": "Perfis de material",
        "ui.material_profile_desc": "Selecione um perfil de material para preencher automaticamente a tolerância por lado",
        "profiles.mat.tooltip": "Tolerância recomendada por lado: {val:.2f} mm",
        "ui.tol_per_face_mm": "Tolerância por face (mm)",
        "ui.tol_override_desc": "Substitui o perfil de material (0 = usar valor do perfil)",

        "ui.foldout.more_seg": "Mais definições de segmentação",
        "ui.foldout.more_seg_desc": "Mostrar opções avançadas de segmentação",
        "ui.foldout.more_conn": "Mais definições de ligação",
        "ui.foldout.more_conn_desc": "Mostrar opções avançadas de ligação/geometria",
        "ui.foldout.more_tol": "Mais definições de tolerância",
        "ui.foldout.more_tol_desc": "Mostrar opções avançadas de tolerância",
        "ui.foldout.more_align": "Mais definições de alinhamento",
        "ui.foldout.more_align_desc": "Mostrar opções avançadas de alinhamento",

        "tooltip.planar_split": "Divide a geometria selecionada segundo um plano de melhor ajuste.",
        "tooltip.adjust": "Abre os ajustes finos da operação atual.",
        "tooltip.show_split_preview": "Ativa/desativa a pré-visualização antes de aplicar.",

        "ui.segmentation_title": "Segmentação",
        "ui.less": "Menos",
        "ui.adjust": "Ajustar",
        "ui.cap_seams_during_split_slow": "Fechar arestas durante o corte (mais lento)",
        "ui.connections_title": "Ligações",
        "ui.add_connectors": "Adicionar conectores",
        "ui.place_connectors_click": "Colocar conectores (clique)",
        "ui.pick_faces_hint": "Escolher faces no modo Objeto (A = alvo, B = móvel)",
        "ui.face_a_none": "A: nenhum",
        "ui.face_b_none": "B: nenhum",
        "ui.pick_face_a": "Escolher Face A",
        "ui.pick_face_b": "Escolher Face B",
        "ui.align_faces": "Alinhar faces",
        "ui.align_faces_desc": "Alinhar a face B à face A com ajuste local e orientação",
    },

    # Dutch (Netherlands) - complete
    "nl_NL": {
        "ui.panel.title": "SnapSplit",
        "ui.reload_language": "UI-taal opnieuw laden",
        "ui.reload_language_desc": "Registreer de add-on opnieuw om de huidige Blender-taal toe te passen op statische labels.",
        "ui.section.profiles": "Profielen",
        "ui.section.tools": "Hulpmiddelen",
        "ui.button.apply": "Toepassen",
        "ui.button.cancel": "Annuleren",
        "ui.button.ok": "OK",
        "ui.section.export": "Exporteren",
        "ui.section.settings": "Instellingen",
        "ui.label.collection": "Exportcollectie",
        "ui.tooltip.collection": "Collectie die wordt gebruikt voor exportuitvoer",

        "prefs.title": "SnapSplit-voorkeuren",
        "prefs.default_profile": "Standaardprofiel",
        "prefs.create_export_collection": "Exportcollectie aanmaken",
        "prefs.language_note": "De taal volgt de Blender-UI-taal. Gebruik 'UI-taal opnieuw laden' na wijzigen van de taal.",
        "prefs.reload_language": "UI-taal opnieuw laden",
        "prefs.reload_language_desc": "Registreer de add-on opnieuw om statische labels (operators/eigenschappen) te verversen.",

        "profiles.name": "Profiel",
        "profiles.description": "Actief SnapSplit-profiel",
        "profiles.enum.material": "Materiaal",
        "profiles.enum.material_desc": "Strategie voor materiaaltoewijzing",
        "profiles.enum.method": "Methode",
        "profiles.enum.method_desc": "Te gebruiken splitsmethode",

        "op.adjust_axis.label": "Splitsas aanpassen",
        "op.adjust_axis.done": "Splitsas aangepast.",
        "op.adjust_axis.cancelled": "Aanpassen van de splitsas geannuleerd.",

        "op.split.label": "Planaire splitsing",
        "op.split.desc": "Vlakken splitsen langs een passend vlak",
        "op.split.many_parts_hint": "Splitsen in veel onderdelen kan bij dichte meshes even duren...",
        "op.split.autocap.none": "Automatisch afsluiten vond geen geldige lussen.",
        "op.split.autocap.count": "Automatisch afsluiten toegepast op {n} onderdeel/onderdelen.",
        "op.split.fewer_parts": "Minder onderdelen gemaakt dan verwacht ({have} < {want}).",
        "op.split.parts_created": "{n} onderdelen gemaakt.",

        "op.cap_now.label": "Randen nu afsluiten",
        "op.cap_now.desc": "Vullen tussen precies twee split-randlussen (buiten+binnen) per vlak. Seeds hebben voorkeur.",
        "op.cap_now.only_selected.name": "Alleen geselecteerde objecten",
        "op.cap_now.max_planes.name": "Max. vlakken",
        "op.cap_now.max_planes.desc": "0 = alle vlakken per object, 1 = alleen grootste",
        "op.cap_now.select_only.name": "Alleen selecteren (niet vullen)",
        "op.cap_now.require_two_seeds.name": "Precies twee seed-randen vereisen",
        "op.cap_now.require_two_seeds.desc": "Als in bewerkmodus precies twee randen zijn geselecteerd, alleen die als seeds gebruiken (geen autodetectie).",
        "op.cap_now.no_targets": "Geen mesh-objecten om af te sluiten. Selecteer gesplitste delen of gebruik de onderdelenverzameling.",
        "op.cap_now.failed_one": "Verwerking mislukt op ‘{name}’: {err}",
        "op.cap_now.none_selected": "Kon de split-randlussen om te selecteren niet bepalen.",
        "op.cap_now.none_capped": "Kon de split-randlussen niet bepalen en vullen.",
        "op.cap_now.selected_count": "Split-randlussen geselecteerd op {n} object(en).",
        "op.cap_now.capped_count": "Randen afgesloten op {n} object(en).",

        "op.common.select_mesh": "Selecteer een mesh-object.",

        "warn.unapplied_transforms": "Object heeft niet-toegepaste transformaties",
        "warn.apply_transforms_hint": "Overweeg alle transformaties toe te passen (Ctrl+A) voor precieze en voorspelbare resultaten.",

        "msg.no_active_object": "Geen actief object.",
        "msg.not_mesh": "Actief object is geen mesh.",
        "msg.operation_done": "Bewerking voltooid.",
        "msg.operation_failed": "Bewerking mislukt.",
        "msg.unapplied_transforms": "Object heeft niet-toegepaste transformaties",

        # profiles.py specific UI
        "ui.split_offset_mm": "Splits-offset (mm)",
        "ui.split_offset_desc": "Verschuiving van het snijvlak langs de as (positief in de asrichting)",
        "ui.split_axis": "Splitsas",
        "ui.split_along_x": "Splits langs X",
        "ui.split_along_y": "Splits langs Y",
        "ui.split_along_z": "Splits langs Z",
        "ui.show_split_preview": "Splitsvoorbeeld tonen",
        "ui.show_split_preview_desc": "Tijdelijke oranje vlakken tonen op geplande snijposities",
        "ui.parts_count": "Aantal onderdelen",
        "ui.parts_count_desc": "Gewenst aantal segmenten (snijvlakken = onderdelen - 1)",

        "ui.cap_seams_during_split_short": "Randen afsluiten tijdens splitsen",
        "ui.cap_seams_during_split_desc": "Sluit randen automatisch na het splitsen. Met holte/binnenschaal: nauwkeurige vulling van buiten-/binnenlussen; zonder holte: eenvoudige vulling. Kan de looptijd verhogen.",

        "ui.connector_type": "Verbindertype",
        "ui.cyl_pin": "Cilinderpen",
        "ui.cyl_pin_desc": "Paspen + bus",
        "ui.rect_tenon": "Rechthoekige pen",
        "ui.rect_tenon_desc": "Anti-rotatieverbinding",
        "ui.snap_pin": "Klikpen",
        "ui.snap_pin_desc": "Verbinder met klikkogels",
        "ui.snap_tenon": "Klikpen (rechthoek)",
        "ui.snap_tenon_desc": "Rechthoekige pen met klikkogels",

        "ui.distribution": "Verdeling",
        "ui.distribution_desc": "Verdeel verbinders langs een lijn of in een raster over het naadvlak",
        "ui.line": "Lijn",
        "ui.line_desc": "Plaats verbinders langs een lijn in het naadvlak",
        "ui.grid": "Raster",
        "ui.grid_desc": "Verdeel verbinders in een raster over het naadvlak",
        "ui.connectors_per_seam": "Verbinders per naad",
        "ui.rows_grid": "Rijen (RASTER)",
        "ui.rows_grid_desc": "Aantal rijen voor rasterverdeling",
        "ui.margin_pct": "Rand (%)",
        "ui.margin_pct_desc": "Randmarge langs de naad (en loodrecht in RASTER) als percentage van de onderdeellengte (0–40% aanbevolen)",

        "ui.spheres_per_side": "Kogels per zijde",
        "ui.spheres_per_side_desc": "Aantal klikkogels per zijde/rondom",
        "ui.sphere_diameter_mm": "Kogel diameter (mm)",
        "ui.sphere_diameter_mm_desc": "Diameter van de klikkogels",
        "ui.protrusion_mm": "Uitsteek (mm)",
        "ui.protrusion_mm_desc": "Hoe ver de kogels uit het zijvlak steken",

        "ui.pin_diameter_mm": "Pendiameter (mm)",
        "ui.pin_length_mm": "Penlengte (mm)",
        "ui.segments": "Segmenten",
        "ui.segments_desc": "Radiale segmenten van de cilinderpen (visuele gladheid)",
        "ui.tenon_width_mm": "Penbreedte (mm)",
        "ui.tenon_depth_mm": "Pendiepte (mm)",
        "ui.chamfer_mm": "Afschuining (mm)",

        "ui.insert_depth_pct": "Instekdiepte (%)",
        "ui.insert_depth_pct_desc": "Percentage van de connectorlengte verzonken in deel A",

        "ui.material_profiles": "Materiaalprofielen",
        "ui.material_profile_desc": "Selecteer een materiaalprofiel om de tolerantie per zijde automatisch in te vullen",
        "profiles.mat.tooltip": "Aanbevolen tolerantie per zijde: {val:.2f} mm",
        "ui.tol_per_face_mm": "Tolerantie per vlak (mm)",
        "ui.tol_override_desc": "Overschrijft het materiaalprofiel (0 = profielwaarde gebruiken)",

        "ui.foldout.more_seg": "Meer segmentatie-instellingen",
        "ui.foldout.more_seg_desc": "Geavanceerde segmentatieopties tonen",
        "ui.foldout.more_conn": "Meer verbindingsinstellingen",
        "ui.foldout.more_conn_desc": "Geavanceerde verbindings-/geometrieopties tonen",
        "ui.foldout.more_tol": "Meer toleranties-instellingen",
        "ui.foldout.more_tol_desc": "Geavanceerde tolerantiesopties tonen",
        "ui.foldout.more_align": "Meer uitlijningsinstellingen",
        "ui.foldout.more_align_desc": "Geavanceerde uitlijningsopties tonen",

        "tooltip.planar_split": "Splitst geselecteerde geometrie langs een best-fit vlak.",
        "tooltip.adjust": "Opent fijnafstemming voor de huidige bewerking.",
        "tooltip.show_split_preview": "Schakelt de visuele voorvertoning in/uit voor toepassen.",

        "ui.segmentation_title": "Segmentatie",
        "ui.less": "Minder",
        "ui.adjust": "Aanpassen",
        "ui.cap_seams_during_split_slow": "Randen afsluiten tijdens splitsen (trager)",
        "ui.connections_title": "Verbindingen",
        "ui.add_connectors": "Verbinders toevoegen",
        "ui.place_connectors_click": "Verbinders plaatsen (klik)",
        "ui.pick_faces_hint": "Vlakken kiezen in Objectmodus (A = doel, B = bewegend)",
        "ui.face_a_none": "A: geen",
        "ui.face_b_none": "B: geen",
        "ui.pick_face_a": "Kies Vlak A",
        "ui.pick_face_b": "Kies Vlak B",
        "ui.align_faces": "Vlakken uitlijnen",
        "ui.align_faces_desc": "Lijn vlak B uit met vlak A met lokale passing en oriëntatie",
    },

    # Polish (Poland) - complete
    "pl_PL": {
        "ui.panel.title": "SnapSplit",
        "ui.reload_language": "Przeładuj język interfejsu",
        "ui.reload_language_desc": "Ponownie zarejestruj dodatek, aby zastosować język Blender do statycznych etykiet.",
        "ui.section.profiles": "Profile",
        "ui.section.tools": "Narzędzia",
        "ui.button.apply": "Zastosuj",
        "ui.button.cancel": "Anuluj",
        "ui.button.ok": "OK",
        "ui.section.export": "Eksport",
        "ui.section.settings": "Ustawienia",
        "ui.label.collection": "Kolekcja eksportu",
        "ui.tooltip.collection": "Kolekcja używana do wyjścia eksportu",

        "prefs.title": "Preferencje SnapSplit",
        "prefs.default_profile": "Profil domyślny",
        "prefs.create_export_collection": "Utwórz kolekcję eksportu",
        "prefs.language_note": "Język podąża za językiem interfejsu Blender. Po zmianie użyj „Przeładuj język interfejsu”.",
        "prefs.reload_language": "Przeładuj język interfejsu",
        "prefs.reload_language_desc": "Ponownie zarejestruj dodatek, aby odświeżyć statyczne etykiety (operatory/właściwości).",

        "profiles.name": "Profil",
        "profiles.description": "Aktywny profil SnapSplit",
        "profiles.enum.material": "Materiał",
        "profiles.enum.material_desc": "Strategia przypisywania materiałów",
        "profiles.enum.method": "Metoda",
        "profiles.enum.method_desc": "Metoda dzielenia do użycia",

        "op.adjust_axis.label": "Dostosuj oś cięcia",
        "op.adjust_axis.done": "Oś cięcia dostosowana.",
        "op.adjust_axis.cancelled": "Anulowano dostosowanie osi cięcia.",

        "op.split.label": "Cięcie planarzne",
        "op.split.desc": "Podziel powierzchnie wzdłuż dopasowanej płaszczyzny",
        "op.split.many_parts_hint": "Dzielenie na wiele części może zająć trochę czasu przy gęstych siatkach...",
        "op.split.autocap.none": "Automatyczne zamykanie nie znalazło prawidłowych pętli.",
        "op.split.autocap.count": "Automatycznie zamknięto krawędzie w {n} częściach.",
        "op.split.fewer_parts": "Utworzono mniej części niż oczekiwano ({have} < {want}).",
        "op.split.parts_created": "Utworzono {n} część/części.",

        "op.cap_now.label": "Zamknij krawędzie teraz",
        "op.cap_now.desc": "Wypełnij między dokładnie dwiema pętlami krawędzi cięcia (zewnętrzną+wewnętrzną) na płaszczyznę. Preferowane seeds.",
        "op.cap_now.only_selected.name": "Tylko wybrane obiekty",
        "op.cap_now.max_planes.name": "Maks. płaszczyzn",
        "op.cap_now.max_planes.desc": "0 = wszystkie płaszczyzny na obiekt, 1 = tylko największa",
        "op.cap_now.select_only.name": "Tylko zaznacz (bez wypełniania)",
        "op.cap_now.require_two_seeds.name": "Wymagaj dokładnie dwóch krawędzi seed",
        "op.cap_now.require_two_seeds.desc": "Jeśli w trybie edycji zaznaczono dokładnie dwie krawędzie, użyj ich tylko jako seeds (bez autodetekcji).",
        "op.cap_now.no_targets": "Brak obiektów siatki do zamknięcia. Wybierz podzielone części lub użyj kolekcji części.",
        "op.cap_now.failed_one": "Przetwarzanie nie powiodło się dla „{name}”: {err}",
        "op.cap_now.none_selected": "Nie można określić pętli krawędzi cięcia do zaznaczenia.",
        "op.cap_now.none_capped": "Nie można określić i wypełnić pętli krawędzi cięcia.",
        "op.cap_now.selected_count": "Zaznaczono pętle krawędzi cięcia w {n} obiekcie/obiektach.",
        "op.cap_now.capped_count": "Zamknięto krawędzie w {n} obiekcie/obiektach.",

        "op.common.select_mesh": "Wybierz obiekt siatki.",

        "warn.unapplied_transforms": "Obiekt ma niezastosowane transformacje",
        "warn.apply_transforms_hint": "Rozważ zastosowanie wszystkich transformacji (Ctrl+A), aby uzyskać dokładne i przewidywalne wyniki.",

        "msg.no_active_object": "Brak aktywnego obiektu.",
        "msg.not_mesh": "Aktywny obiekt nie jest siatką.",
        "msg.operation_done": "Operacja zakończona.",
        "msg.operation_failed": "Operacja nie powiodła się.",
        "msg.unapplied_transforms": "Obiekt ma niezastosowane transformacje",

        # profiles.py specific UI
        "ui.split_offset_mm": "Przesunięcie cięcia (mm)",
        "ui.split_offset_desc": "Przesunięcie płaszczyzny cięcia wzdłuż osi (dodatnie w kierunku osi)",
        "ui.split_axis": "Oś cięcia",
        "ui.split_along_x": "Tnij wzdłuż X",
        "ui.split_along_y": "Tnij wzdłuż Y",
        "ui.split_along_z": "Tnij wzdłuż Z",
        "ui.show_split_preview": "Pokaż podgląd cięcia",
        "ui.show_split_preview_desc": "Pokaż tymczasowe pomarańczowe płaszczyzny w planowanych pozycjach cięcia",
        "ui.parts_count": "Liczba części",
        "ui.parts_count_desc": "Liczba pożądanych segmentów (płaszczyzny cięcia = części - 1)",

        "ui.cap_seams_during_split_short": "Zamykaj krawędzie podczas cięcia",
        "ui.cap_seams_during_split_desc": "Automatycznie zamykaj krawędzie po cięciu. Z wnęką/powłoką wewn.: precyzyjne wypełnienie pętli zewn./wewn.; bez wnęki: proste wypełnienie. Może wydłużyć czas działania.",

        "ui.connector_type": "Typ łącznika",
        "ui.cyl_pin": "Kołek cylindryczny",
        "ui.cyl_pin_desc": "Kołek + tuleja",
        "ui.rect_tenon": "Czop prostokątny",
        "ui.rect_tenon_desc": "Połączenie przeciwobrotowe",
        "ui.snap_pin": "Kołek zatrzaskowy",
        "ui.snap_pin_desc": "Łącznik z kulkami zatrzaskowymi",
        "ui.snap_tenon": "Czop zatrzaskowy",
        "ui.snap_tenon_desc": "Prostokątny czop z kulkami zatrzaskowymi",

        "ui.distribution": "Rozmieszczenie",
        "ui.distribution_desc": "Rozmieść łączniki wzdłuż linii lub w siatce na powierzchni szwu",
        "ui.line": "Linia",
        "ui.line_desc": "Umieść łączniki wzdłuż linii na powierzchni szwu",
        "ui.grid": "Siatka",
        "ui.grid_desc": "Rozmieść łączniki w siatce na powierzchni szwu",
        "ui.connectors_per_seam": "Łączniki na szew",
        "ui.rows_grid": "Rzędy (SIATKA)",
        "ui.rows_grid_desc": "Liczba rzędów dla rozmieszczenia w siatce",
        "ui.margin_pct": "Margines (%)",
        "ui.margin_pct_desc": "Margines krawędzi wzdłuż szwu (i prostopadle w SIATCE) jako procent długości części (zalecane 0–40%)",

        "ui.spheres_per_side": "Kule na stronę",
        "ui.spheres_per_side_desc": "Liczba kulek zatrzaskowych na stronę/wokół",
        "ui.sphere_diameter_mm": "Średnica kuli (mm)",
        "ui.sphere_diameter_mm_desc": "Średnica kulek zatrzaskowych",
        "ui.protrusion_mm": "Wystawanie (mm)",
        "ui.protrusion_mm_desc": "Jak daleko kule wystają z powierzchni bocznej",

        "ui.pin_diameter_mm": "Średnica kołka (mm)",
        "ui.pin_length_mm": "Długość kołka (mm)",
        "ui.segments": "Segmenty",
        "ui.segments_desc": "Segmenty promieniowe kołka cylindrycznego (gładkość wizualna)",
        "ui.tenon_width_mm": "Szerokość czopa (mm)",
        "ui.tenon_depth_mm": "Głębokość czopa (mm)",
        "ui.chamfer_mm": "Fazowanie (mm)",

        "ui.insert_depth_pct": "Głębokość osadzenia (%)",
        "ui.insert_depth_pct_desc": "Procent długości łącznika zagłębiony w części A",

        "ui.material_profiles": "Profile materiałów",
        "ui.material_profile_desc": "Wybierz profil materiału, aby automatycznie wypełnić tolerancję na stronę",
        "profiles.mat.tooltip": "Zalecana tolerancja na stronę: {val:.2f} mm",
        "ui.tol_per_face_mm": "Tolerancja na powierzchnię (mm)",
        "ui.tol_override_desc": "Nadpisuje profil materiału (0 = użyj wartości z profilu)",

        "ui.foldout.more_seg": "Więcej ustawień segmentacji",
        "ui.foldout.more_seg_desc": "Pokaż zaawansowane opcje segmentacji",
        "ui.foldout.more_conn": "Więcej ustawień połączeń",
        "ui.foldout.more_conn_desc": "Pokaż zaawansowane opcje połączeń/geometrii",
        "ui.foldout.more_tol": "Więcej ustawień tolerancji",
        "ui.foldout.more_tol_desc": "Pokaż zaawansowane opcje tolerancji",
        "ui.foldout.more_align": "Więcej ustawień wyrównania",
        "ui.foldout.more_align_desc": "Pokaż zaawansowane opcje wyrównania",

        "tooltip.planar_split": "Dzieli wybraną geometrię wzdłuż najlepiej dopasowanej płaszczyzny.",
        "tooltip.adjust": "Otwiera precyzyjne ustawienia bieżącej operacji.",
        "tooltip.show_split_preview": "Włącza/wyłącza podgląd przed zastosowaniem.",

        "ui.segmentation_title": "Segmentacja",
        "ui.less": "Mniej",
        "ui.adjust": "Dostosuj",
        "ui.cap_seams_during_split_slow": "Zamykaj krawędzie podczas cięcia (wolniej)",
        "ui.connections_title": "Połączenia",
        "ui.add_connectors": "Dodaj łączniki",
        "ui.place_connectors_click": "Umieść łączniki (klik)",
        "ui.pick_faces_hint": "Wybierz powierzchnie w trybie Obiekt (A = cel, B = ruchoma)",
        "ui.face_a_none": "A: brak",
        "ui.face_b_none": "B: brak",
        "ui.pick_face_a": "Wybierz Powierzchnię A",
        "ui.pick_face_b": "Wybierz Powierzchnię B",
        "ui.align_faces": "Wyrównaj powierzchnie",
        "ui.align_faces_desc": "Wyrównaj powierzchnię B do A z lokalnym dopasowaniem i orientacją",
    },

    # Japanese (Japan) - complete
    "ja_JP": {
        "ui.panel.title": "SnapSplit",
        "ui.reload_language": "UI言語を再読み込み",
        "ui.reload_language_desc": "アドオンを再登録して、Blenderの現在の言語を静的ラベルに適用します。",
        "ui.section.profiles": "プロファイル",
        "ui.section.tools": "ツール",
        "ui.button.apply": "適用",
        "ui.button.cancel": "キャンセル",
        "ui.button.ok": "OK",
        "ui.section.export": "エクスポート",
        "ui.section.settings": "設定",
        "ui.label.collection": "エクスポートコレクション",
        "ui.tooltip.collection": "エクスポート出力に使用するコレクション",

        "prefs.title": "SnapSplit 設定",
        "prefs.default_profile": "デフォルトプロファイル",
        "prefs.create_export_collection": "エクスポートコレクションを作成",
        "prefs.language_note": "言語はBlenderのUI言語に従います。変更後は「UI言語を再読み込み」を使用してください。",
        "prefs.reload_language": "UI言語を再読み込み",
        "prefs.reload_language_desc": "アドオンを再登録して、静的ラベル（オペレーター/プロパティ）を更新します。",

        "profiles.name": "プロファイル",
        "profiles.description": "アクティブな SnapSplit プロファイル",
        "profiles.enum.material": "マテリアル",
        "profiles.enum.material_desc": "マテリアル割り当て戦略",
        "profiles.enum.method": "方法",
        "profiles.enum.method_desc": "使用する分割方法",

        "op.adjust_axis.label": "分割軸を調整",
        "op.adjust_axis.done": "分割軸を調整しました。",
        "op.adjust_axis.cancelled": "分割軸の調整をキャンセルしました。",

        "op.split.label": "平面分割",
        "op.split.desc": "当てはめた平面に沿ってフェイスを分割",
        "op.split.many_parts_hint": "多数のパーツに分割すると、高密度メッシュでは時間がかかる場合があります...",
        "op.split.autocap.none": "自動キャップで有効なループが見つかりませんでした。",
        "op.split.autocap.count": "自動キャップを {n} 個のパーツで実行しました。",
        "op.split.fewer_parts": "期待よりパーツ数が少なく作成されました（{have} < {want}）。",
        "op.split.parts_created": "{n} 個のパーツを作成しました。",

        "op.cap_now.label": "エッジを今すぐキャップ",
        "op.cap_now.desc": "各平面につき、外側＋内側の2つの分割エッジループ間を充填します。シードを優先します。",
        "op.cap_now.only_selected.name": "選択オブジェクトのみ",
        "op.cap_now.max_planes.name": "最大平面数",
        "op.cap_now.max_planes.desc": "0 = 各オブジェクトの全平面、1 = 最大の平面のみ",
        "op.cap_now.select_only.name": "選択のみ（充填なし）",
        "op.cap_now.require_two_seeds.name": "シードエッジをちょうど2本要求",
        "op.cap_now.require_two_seeds.desc": "編集モードでエッジがちょうど2本選択されている場合、それらのみをシードとして使用します（自動検出なし）。",
        "op.cap_now.no_targets": "キャップするメッシュオブジェクトがありません。分割パーツを選択するか、パーツコレクションを使用してください。",
        "op.cap_now.failed_one": "「{name}」の処理に失敗しました: {err}",
        "op.cap_now.none_selected": "選択する分割エッジループを特定できませんでした。",
        "op.cap_now.none_capped": "分割エッジループを特定して充填できませんでした。",
        "op.cap_now.selected_count": "{n} 個のオブジェクトで分割エッジループを選択しました。",
        "op.cap_now.capped_count": "{n} 個のオブジェクトでエッジをキャップしました。",

        "op.common.select_mesh": "メッシュオブジェクトを選択してください。",

        "warn.unapplied_transforms": "オブジェクトに未適用の変換があります",
        "warn.apply_transforms_hint": "正確で予測可能な結果のため、すべての変換（Ctrl+A）の適用を検討してください。",

        "msg.no_active_object": "アクティブなオブジェクトがありません。",
        "msg.not_mesh": "アクティブなオブジェクトはメッシュではありません。",
        "msg.operation_done": "操作が完了しました。",
        "msg.operation_failed": "操作に失敗しました。",
        "msg.unapplied_transforms": "オブジェクトに未適用の変換があります",

        # profiles.py specific UI
        "ui.split_offset_mm": "カットオフセット (mm)",
        "ui.split_offset_desc": "分割軸に沿ったカット平面のオフセット（軸方向に正）",
        "ui.split_axis": "分割軸",
        "ui.split_along_x": "X に沿って分割",
        "ui.split_along_y": "Y に沿って分割",
        "ui.split_along_z": "Z に沿って分割",
        "ui.show_split_preview": "分割プレビューを表示",
        "ui.show_split_preview_desc": "予定された切断位置に一時的なオレンジ色の平面を表示",
        "ui.parts_count": "パーツ数",
        "ui.parts_count_desc": "希望するセグメント数（切断平面 = パーツ - 1）",

        "ui.cap_seams_during_split_short": "分割中にエッジをキャップ",
        "ui.cap_seams_during_split_desc": "分割後にエッジを自動的に閉じます。空洞/内殻あり: 外側/内側ループを精密に充填。空洞なし: 単純な充填。実行時間が増える場合があります。",

        "ui.connector_type": "コネクタタイプ",
        "ui.cyl_pin": "シリンダーピン",
        "ui.cyl_pin_desc": "ダボピン + ソケット",
        "ui.rect_tenon": "矩形ほぞ",
        "ui.rect_tenon_desc": "回り止め接合",
        "ui.snap_pin": "スナップピン",
        "ui.snap_pin_desc": "スナップ球付きコネクタ",
        "ui.snap_tenon": "スナップほぞ",
        "ui.snap_tenon_desc": "スナップ球付きの矩形ほぞ",

        "ui.distribution": "分布",
        "ui.distribution_desc": "継ぎ目面に沿ってラインまたはグリッドでコネクタを配置",
        "ui.line": "ライン",
        "ui.line_desc": "継ぎ目面に沿ってライン状にコネクタを配置",
        "ui.grid": "グリッド",
        "ui.grid_desc": "継ぎ目面にグリッド状にコネクタを配置",
        "ui.connectors_per_seam": "継ぎ目あたりのコネクタ数",
        "ui.rows_grid": "行（グリッド）",
        "ui.rows_grid_desc": "グリッド分布の行数",
        "ui.margin_pct": "マージン (%)",
        "ui.margin_pct_desc": "継ぎ目に沿った（グリッドでは垂直方向も）エッジマージン。部品長さに対する割合（推奨 0–40%）",

        "ui.spheres_per_side": "片側の球数",
        "ui.spheres_per_side_desc": "片側/周囲のスナップ球の数",
        "ui.sphere_diameter_mm": "球直径 (mm)",
        "ui.sphere_diameter_mm_desc": "スナップ球の直径",
        "ui.protrusion_mm": "突出量 (mm)",
        "ui.protrusion_mm_desc": "球が側面からどれだけ突出するか",

        "ui.pin_diameter_mm": "ピン直径 (mm)",
        "ui.pin_length_mm": "ピン長 (mm)",
        "ui.segments": "セグメント",
        "ui.segments_desc": "シリンダーピンの放射セグメント（見た目の滑らかさ）",
        "ui.tenon_width_mm": "ほぞ幅 (mm)",
        "ui.tenon_depth_mm": "ほぞ深さ (mm)",
        "ui.chamfer_mm": "面取り (mm)",

        "ui.insert_depth_pct": "挿入深さ (%)",
        "ui.insert_depth_pct_desc": "コネクタ長のうちパートAに埋め込む割合",

        "ui.material_profiles": "材料プロファイル",
        "ui.material_profile_desc": "側ごとの公差を自動入力するため材料プロファイルを選択",
        "profiles.mat.tooltip": "推奨公差（片側）: {val:.2f} mm",
        "ui.tol_per_face_mm": "面あたり公差 (mm)",
        "ui.tol_override_desc": "材料プロファイルを上書き（0 = プロファイル値を使用）",

        "ui.foldout.more_seg": "詳細なセグメント設定",
        "ui.foldout.more_seg_desc": "高度なセグメントオプションを表示",
        "ui.foldout.more_conn": "詳細な接続設定",
        "ui.foldout.more_conn_desc": "高度な接続/ジオメトリ オプションを表示",
        "ui.foldout.more_tol": "詳細な公差設定",
        "ui.foldout.more_tol_desc": "高度な公差オプションを表示",
        "ui.foldout.more_align": "詳細な位置合わせ設定",
        "ui.foldout.more_align_desc": "高度な位置合わせオプションを表示",

        "tooltip.planar_split": "最適平面に沿って選択ジオメトリを分割します。",
        "tooltip.adjust": "現在の操作の微調整を開きます。",
        "tooltip.show_split_preview": "適用前のプレビューを切り替えます。",

        "ui.segmentation_title": "セグメンテーション",
        "ui.less": "少なく",
        "ui.adjust": "調整",
        "ui.cap_seams_during_split_slow": "分割中にエッジをキャップ（低速）",
        "ui.connections_title": "接続",
        "ui.add_connectors": "コネクタを追加",
        "ui.place_connectors_click": "コネクタを配置（クリック）",
        "ui.pick_faces_hint": "オブジェクトモードで面を選ぶ（A = ターゲット, B = 移動）",
        "ui.face_a_none": "A: なし",
        "ui.face_b_none": "B: なし",
        "ui.pick_face_a": "面Aを選択",
        "ui.pick_face_b": "面Bを選択",
        "ui.align_faces": "面を整列",
        "ui.align_faces_desc": "ローカルフィットと向きを用いて面Bを面Aに整列",
    },

    # Chinese (Simplified, China) - complete
    "zh_CN": {
        "ui.panel.title": "SnapSplit",
        "ui.reload_language": "重新加载界面语言",
        "ui.reload_language_desc": "重新注册插件，以将当前 Blender 语言应用于静态标签。",
        "ui.section.profiles": "配置文件",
        "ui.section.tools": "工具",
        "ui.button.apply": "应用",
        "ui.button.cancel": "取消",
        "ui.button.ok": "确定",
        "ui.section.export": "导出",
        "ui.section.settings": "设置",
        "ui.label.collection": "导出集合",
        "ui.tooltip.collection": "用于导出输出的集合",

        "prefs.title": "SnapSplit 首选项",
        "prefs.default_profile": "默认配置文件",
        "prefs.create_export_collection": "创建导出集合",
        "prefs.language_note": "语言遵循 Blender 的界面语言。更改后请使用“重新加载界面语言”。",
        "prefs.reload_language": "重新加载界面语言",
        "prefs.reload_language_desc": "重新注册插件以刷新静态标签（操作/属性）。",

        "profiles.name": "配置文件",
        "profiles.description": "活动的 SnapSplit 配置文件",
        "profiles.enum.material": "材质",
        "profiles.enum.material_desc": "材质分配策略",
        "profiles.enum.method": "方法",
        "profiles.enum.method_desc": "要使用的切割方法",

        "op.adjust_axis.label": "调整切割轴",
        "op.adjust_axis.done": "切割轴已调整。",
        "op.adjust_axis.cancelled": "已取消调整切割轴。",

        "op.split.label": "平面切割",
        "op.split.desc": "沿拟合平面切割面",
        "op.split.many_parts_hint": "在高密度网格上分割为多个部分可能需要一些时间……",
        "op.split.autocap.none": "自动封盖未找到有效的循环。",
        "op.split.autocap.count": "已在 {n} 个部件上自动封盖。",
        "op.split.fewer_parts": "创建的部件少于预期（{have} < {want}）。",
        "op.split.parts_created": "已创建 {n} 个部件。",

        "op.cap_now.label": "立即封盖边界",
        "op.cap_now.desc": "每个平面在外环与内环两条切割边循环之间填充。优先使用种子。",
        "op.cap_now.only_selected.name": "仅所选对象",
        "op.cap_now.max_planes.name": "最大平面数",
        "op.cap_now.max_planes.desc": "0 = 每个对象的所有平面，1 = 仅最大平面",
        "op.cap_now.select_only.name": "仅选择（不填充）",
        "op.cap_now.require_two_seeds.name": "需要恰好两条种子边",
        "op.cap_now.require_two_seeds.desc": "如果编辑模式下恰好选择两条边，仅将其作为种子（不自动检测）。",
        "op.cap_now.no_targets": "没有可封盖的网格对象。请选择切割部件或使用部件集合。",
        "op.cap_now.failed_one": "处理“{name}”失败：{err}",
        "op.cap_now.none_selected": "无法确定要选择的切割边循环。",
        "op.cap_now.none_capped": "无法确定并填充切割边循环。",
        "op.cap_now.selected_count": "已在 {n} 个对象上选择切割边循环。",
        "op.cap_now.capped_count": "已在 {n} 个对象上封盖边界。",

        "op.common.select_mesh": "请选择一个网格对象。",

        "warn.unapplied_transforms": "对象存在未应用的变换",
        "warn.apply_transforms_hint": "为获得精确且可预测的结果，请考虑应用所有变换（Ctrl+A）。",

        "msg.no_active_object": "没有活动对象。",
        "msg.not_mesh": "活动对象不是网格。",
        "msg.operation_done": "操作完成。",
        "msg.operation_failed": "操作失败。",
        "msg.unapplied_transforms": "对象存在未应用的变换",

        # profiles.py specific UI
        "ui.split_offset_mm": "切割偏移 (mm)",
        "ui.split_offset_desc": "沿切割轴方向的切割平面偏移量（轴方向为正）",
        "ui.split_axis": "切割轴",
        "ui.split_along_x": "沿 X 切割",
        "ui.split_along_y": "沿 Y 切割",
        "ui.split_along_z": "沿 Z 切割",
        "ui.show_split_preview": "显示切割预览",
        "ui.show_split_preview_desc": "在计划的切割位置显示临时的橙色平面",
        "ui.parts_count": "部件数量",
        "ui.parts_count_desc": "所需的分段数量（切割平面 = 部件 - 1）",

        "ui.cap_seams_during_split_short": "切割时封盖边界",
        "ui.cap_seams_during_split_desc": "在切割后自动封盖边界。具有空腔/内壳：精确填充外/内环；无空腔：简单填充。可能会增加运行时间。",

        "ui.connector_type": "连接件类型",
        "ui.cyl_pin": "圆柱销",
        "ui.cyl_pin_desc": "圆柱销 + 套筒",
        "ui.rect_tenon": "矩形榫",
        "ui.rect_tenon_desc": "防转连接",
        "ui.snap_pin": "卡扣销",
        "ui.snap_pin_desc": "带卡扣球的连接件",
        "ui.snap_tenon": "卡扣榫",
        "ui.snap_tenon_desc": "带卡扣球的矩形榫",

        "ui.distribution": "分布",
        "ui.distribution_desc": "沿线或在网格中分布连接件，覆盖接缝面",
        "ui.line": "直线",
        "ui.line_desc": "沿接缝面上的直线放置连接件",
        "ui.grid": "网格",
        "ui.grid_desc": "在接缝面上以网格形式分布连接件",
        "ui.connectors_per_seam": "每个接缝的连接件数量",
        "ui.rows_grid": "行数（网格）",
        "ui.rows_grid_desc": "网格分布的行数",
        "ui.margin_pct": "边距 (%)",
        "ui.margin_pct_desc": "沿接缝（以及网格中垂直方向）的边缘边距，占部件长度的百分比（建议 0–40%）",

        "ui.spheres_per_side": "每侧球数",
        "ui.spheres_per_side_desc": "每侧/周围的卡扣球数量",
        "ui.sphere_diameter_mm": "球直径 (mm)",
        "ui.sphere_diameter_mm_desc": "卡扣球的直径",
        "ui.protrusion_mm": "突出量 (mm)",
        "ui.protrusion_mm_desc": "球从侧面表面突出的距离",

        "ui.pin_diameter_mm": "销直径 (mm)",
        "ui.pin_length_mm": "销长度 (mm)",
        "ui.segments": "分段数",
        "ui.segments_desc": "圆柱销的径向分段数（视觉平滑度）",
        "ui.tenon_width_mm": "榫宽 (mm)",
        "ui.tenon_depth_mm": "榫深 (mm)",
        "ui.chamfer_mm": "倒角 (mm)",

        "ui.insert_depth_pct": "插入深度 (%)",
        "ui.insert_depth_pct_desc": "嵌入到部件 A 的连接件长度百分比",

        "ui.material_profiles": "材料配置文件",
        "ui.material_profile_desc": "选择材料配置文件以自动填充每侧的公差",
        "profiles.mat.tooltip": "推荐每侧公差：{val:.2f} mm",
        "ui.tol_per_face_mm": "每个面的公差 (mm)",
        "ui.tol_override_desc": "覆盖材料配置文件（0 = 使用配置文件值）",

        "ui.foldout.more_seg": "更多分割设置",
        "ui.foldout.more_seg_desc": "显示高级分割选项",
        "ui.foldout.more_conn": "更多连接设置",
        "ui.foldout.more_conn_desc": "显示高级连接/几何选项",
        "ui.foldout.more_tol": "更多公差设置",
        "ui.foldout.more_tol_desc": "显示高级公差选项",
        "ui.foldout.more_align": "更多对齐设置",
        "ui.foldout.more_align_desc": "显示高级对齐选项",

        "tooltip.planar_split": "沿最佳拟合平面分割所选几何体。",
        "tooltip.adjust": "打开当前操作的微调选项。",
        "tooltip.show_split_preview": "在应用前切换可视化预览。",

        "ui.segmentation_title": "分割",
        "ui.less": "更少",
        "ui.adjust": "调整",
        "ui.cap_seams_during_split_slow": "切割时封盖边界（较慢）",
        "ui.connections_title": "连接",
        "ui.add_connectors": "添加连接件",
        "ui.place_connectors_click": "放置连接件（单击）",
        "ui.pick_faces_hint": "在对象模式中选择面（A = 目标，B = 移动）",
        "ui.face_a_none": "A：无",
        "ui.face_b_none": "B：无",
        "ui.pick_face_a": "选择面 A",
        "ui.pick_face_b": "选择面 B",
        "ui.align_faces": "对齐面",
        "ui.align_faces_desc": "使用局部拟合与方向将面 B 对齐到面 A",
    },

    # Chinese (Traditional, Taiwan) - complete
    "zh_TW": {
        "ui.panel.title": "SnapSplit",
        "ui.reload_language": "重新載入介面語言",
        "ui.reload_language_desc": "重新註冊外掛以將目前的 Blender 語言套用到靜態標籤。",
        "ui.section.profiles": "設定檔",
        "ui.section.tools": "工具",
        "ui.button.apply": "套用",
        "ui.button.cancel": "取消",
        "ui.button.ok": "確定",
        "ui.section.export": "匯出",
        "ui.section.settings": "設定",
        "ui.label.collection": "用於匯出的集合",
        "ui.tooltip.collection": "用於匯出輸出的集合",

        "prefs.title": "SnapSplit 偏好設定",
        "prefs.default_profile": "預設設定檔",
        "prefs.create_export_collection": "建立匯出集合",
        "prefs.language_note": "語言遵循 Blender 的介面語言。變更後請使用「重新載入介面語言」。",
        "prefs.reload_language": "重新載入介面語言",
        "prefs.reload_language_desc": "重新註冊外掛以更新靜態標籤（操作/屬性）。",

        "profiles.name": "設定檔",
        "profiles.description": "啟用中的 SnapSplit 設定檔",
        "profiles.enum.material": "材質",
        "profiles.enum.material_desc": "材質指派策略",
        "profiles.enum.method": "方法",
        "profiles.enum.method_desc": "要使用的切割方法",

        "op.adjust_axis.label": "調整切割軸",
        "op.adjust_axis.done": "已調整切割軸。",
        "op.adjust_axis.cancelled": "已取消調整切割軸。",

        "op.split.label": "平面切割",
        "op.split.desc": "沿擬合平面切割面",
        "op.split.many_parts_hint": "在高密度網格上分割為多個部分可能需要一些時間……",
        "op.split.autocap.none": "自動封蓋未找到有效迴圈。",
        "op.split.autocap.count": "已在 {n} 個部件上自動封蓋。",
        "op.split.fewer_parts": "建立的部件少於預期（{have} < {want}）。",
        "op.split.parts_created": "已建立 {n} 個部件。",

        "op.cap_now.label": "立即封蓋邊界",
        "op.cap_now.desc": "每個平面在外圈與內圈兩條切割邊迴圈之間填充。優先使用種子。",
        "op.cap_now.only_selected.name": "僅選取的物件",
        "op.cap_now.max_planes.name": "最大平面數",
        "op.cap_now.max_planes.desc": "0 = 每個物件的所有平面，1 = 僅最大平面",
        "op.cap_now.select_only.name": "僅選取（不填充）",
        "op.cap_now.require_two_seeds.name": "需要正好兩條種子邊",
        "op.cap_now.require_two_seeds.desc": "若在編輯模式中正好選取兩條邊，僅將其作為種子（不自動偵測）。",
        "op.cap_now.no_targets": "沒有可封蓋的網格物件。請選取切割部件或使用部件集合。",
        "op.cap_now.failed_one": "處理「{name}」失敗：{err}",
        "op.cap_now.none_selected": "無法判定要選取的切割邊迴圈。",
        "op.cap_now.none_capped": "無法判定並填充切割邊迴圈。",
        "op.cap_now.selected_count": "已在 {n} 個物件上選取切割邊迴圈。",
        "op.cap_now.capped_count": "已在 {n} 個物件上封蓋邊界。",

        "op.common.select_mesh": "請選取一個網格物件。",

        "warn.unapplied_transforms": "物件存在未套用的變換",
        "warn.apply_transforms_hint": "為獲得精確且可預期的結果，請考慮套用所有變換（Ctrl+A）。",

        "msg.no_active_object": "沒有使用中的物件。",
        "msg.not_mesh": "使用中的物件不是網格。",
        "msg.operation_done": "操作完成。",
        "msg.operation_failed": "操作失敗。",
        "msg.unapplied_transforms": "物件存在未套用的變換",

        # profiles.py specific UI
        "ui.split_offset_mm": "切割偏移 (mm)",
        "ui.split_offset_desc": "沿切割軸方向的切割平面偏移量（軸方向為正）",
        "ui.split_axis": "切割軸",
        "ui.split_along_x": "沿 X 切割",
        "ui.split_along_y": "沿 Y 切割",
        "ui.split_along_z": "沿 Z 切割",
        "ui.show_split_preview": "顯示切割預覽",
        "ui.show_split_preview_desc": "在計畫的切割位置顯示暫時的橘色平面",
        "ui.parts_count": "部件數量",
        "ui.parts_count_desc": "所需的分段數量（切割平面 = 部件 - 1）",

        "ui.cap_seams_during_split_short": "切割時封蓋邊界",
        "ui.cap_seams_during_split_desc": "在切割後自動封蓋邊界。具有空腔/內殼：精確填充外/內圈；無空腔：簡單填充。可能會增加執行時間。",

        "ui.connector_type": "連接件類型",
        "ui.cyl_pin": "圓柱銷",
        "ui.cyl_pin_desc": "圓柱銷 + 套筒",
        "ui.rect_tenon": "矩形榫",
        "ui.rect_tenon_desc": "防轉連接",
        "ui.snap_pin": "卡扣銷",
        "ui.snap_pin_desc": "帶卡扣球的連接件",
        "ui.snap_tenon": "卡扣榫",
        "ui.snap_tenon_desc": "帶卡扣球的矩形榫",

        "ui.distribution": "分佈",
        "ui.distribution_desc": "沿線或在網格中分佈連接件，覆蓋接縫面",
        "ui.line": "直線",
        "ui.line_desc": "沿接縫面上的直線放置連接件",
        "ui.grid": "網格",
        "ui.grid_desc": "在接縫面上以網格形式分佈連接件",
        "ui.connectors_per_seam": "每個接縫的連接件數量",
        "ui.rows_grid": "行數（網格）",
        "ui.rows_grid_desc": "網格分佈的行數",
        "ui.margin_pct": "邊距 (%)",
        "ui.margin_pct_desc": "沿接縫（以及網格中垂直方向）的邊緣邊距，佔部件長度的百分比（建議 0–40%）",

        "ui.spheres_per_side": "每側球數",
        "ui.spheres_per_side_desc": "每側/四周的卡扣球數量",
        "ui.sphere_diameter_mm": "球直徑 (mm)",
        "ui.sphere_diameter_mm_desc": "卡扣球的直徑",
        "ui.protrusion_mm": "突出量 (mm)",
        "ui.protrusion_mm_desc": "球從側面表面突出的距離",

        "ui.pin_diameter_mm": "銷直徑 (mm)",
        "ui.pin_length_mm": "銷長度 (mm)",
        "ui.segments": "分段數",
        "ui.segments_desc": "圓柱銷的徑向分段數（視覺平滑度）",
        "ui.tenon_width_mm": "榫寬 (mm)",
        "ui.tenon_depth_mm": "榫深 (mm)",
        "ui.chamfer_mm": "倒角 (mm)",

        "ui.insert_depth_pct": "插入深度 (%)",
        "ui.insert_depth_pct_desc": "嵌入到部件 A 的連接件長度百分比",

        "ui.material_profiles": "材料設定檔",
        "ui.material_profile_desc": "選擇材料設定檔以自動填入每側公差",
        "profiles.mat.tooltip": "建議每側公差：{val:.2f} mm",
        "ui.tol_per_face_mm": "每個面的公差 (mm)",
        "ui.tol_override_desc": "覆寫材料設定檔（0 = 使用設定檔值）",

        "ui.foldout.more_seg": "更多分割設定",
        "ui.foldout.more_seg_desc": "顯示進階的分割選項",
        "ui.foldout.more_conn": "更多連接設定",
        "ui.foldout.more_conn_desc": "顯示進階的連接/幾何選項",
        "ui.foldout.more_tol": "更多公差設定",
        "ui.foldout.more_tol_desc": "顯示進階的公差選項",
        "ui.foldout.more_align": "更多對齊設定",
        "ui.foldout.more_align_desc": "顯示進階的對齊選項",

        "tooltip.planar_split": "沿最佳擬合平面分割所選幾何體。",
        "tooltip.adjust": "開啟目前操作的微調選項。",
        "tooltip.show_split_preview": "在套用前切換視覺預覽。",

        "ui.segmentation_title": "分割",
        "ui.less": "更少",
        "ui.adjust": "調整",
        "ui.cap_seams_during_split_slow": "切割時封蓋邊界（較慢）",
        "ui.connections_title": "連接",
        "ui.add_connectors": "新增連接件",
        "ui.place_connectors_click": "放置連接件（點擊）",
        "ui.pick_faces_hint": "在物件模式中選擇面（A = 目標，B = 移動）",
        "ui.face_a_none": "A：無",
        "ui.face_b_none": "B：無",
        "ui.pick_face_a": "選擇面 A",
        "ui.pick_face_b": "選擇面 B",
        "ui.align_faces": "對齊面",
        "ui.align_faces_desc": "使用在地擬合與方向將面 B 對齊至面 A",
    },

    # Russian (Russia) - complete
    "ru_RU": {
        "ui.panel.title": "SnapSplit",
        "ui.reload_language": "Перезагрузить язык интерфейса",
        "ui.reload_language_desc": "Пере-регистрируйте аддон, чтобы применить текущий язык Blender к статическим подписям.",
        "ui.section.profiles": "Профили",
        "ui.section.tools": "Инструменты",
        "ui.button.apply": "Применить",
        "ui.button.cancel": "Отмена",
        "ui.button.ok": "OK",
        "ui.section.export": "Экспорт",
        "ui.section.settings": "Настройки",
        "ui.label.collection": "Коллекция экспорта",
        "ui.tooltip.collection": "Коллекция, используемая для вывода экспорта",

        "prefs.title": "Настройки SnapSplit",
        "prefs.default_profile": "Профиль по умолчанию",
        "prefs.create_export_collection": "Создать коллекцию экспорта",
        "prefs.language_note": "Язык следует языку интерфейса Blender. После изменения используйте «Перезагрузить язык интерфейса».",
        "prefs.reload_language": "Перезагрузить язык интерфейса",
        "prefs.reload_language_desc": "Пере-регистрируйте аддон для обновления статических подписей (операторы/свойства).",

        "profiles.name": "Профиль",
        "profiles.description": "Активный профиль SnapSplit",
        "profiles.enum.material": "Материал",
        "profiles.enum.material_desc": "Стратегия назначения материалов",
        "profiles.enum.method": "Метод",
        "profiles.enum.method_desc": "Используемый метод разрезания",

        "op.adjust_axis.label": "Настроить ось разреза",
        "op.adjust_axis.done": "Ось разреза настроена.",
        "op.adjust_axis.cancelled": "Настройка оси разреза отменена.",

        "op.split.label": "Плоскостной разрез",
        "op.split.desc": "Разделить полигоны вдоль подобранной плоскости",
        "op.split.many_parts_hint": "Разделение на множество частей может занять время на плотных сетках...",
        "op.split.autocap.none": "Автозакрытие не нашло допустимых петель.",
        "op.split.autocap.count": "Автозакрытие кромок выполнено на {n} части(ях).",
        "op.split.fewer_parts": "Создано меньше частей, чем ожидалось ({have} < {want}).",
        "op.split.parts_created": "Создано частей: {n}.",

        "op.cap_now.label": "Закрыть кромки сейчас",
        "op.cap_now.desc": "Заполнить между ровно двумя петлями разреза (внешняя+внутренняя) на плоскость. Seeds предпочтительны.",
        "op.cap_now.only_selected.name": "Только выбранные объекты",
        "op.cap_now.max_planes.name": "Макс. плоскостей",
        "op.cap_now.max_planes.desc": "0 = все плоскости на объект, 1 = только наибольшая",
        "op.cap_now.select_only.name": "Только выделение (без заполнения)",
        "op.cap_now.require_two_seeds.name": "Требовать ровно две seed-кромки",
        "op.cap_now.require_two_seeds.desc": "Если в режиме редактирования выбраны ровно две кромки, использовать их только как seeds (без автоопределения).",
        "op.cap_now.no_targets": "Нет объектов-сеток для закрытия. Выберите разрезанные части или используйте коллекцию частей.",
        "op.cap_now.failed_one": "Сбой обработки «{name}»: {err}",
        "op.cap_now.none_selected": "Не удалось определить петли кромок разреза для выделения.",
        "op.cap_now.none_capped": "Не удалось определить и заполнить петли кромок разреза.",
        "op.cap_now.selected_count": "Выбраны петли кромок разреза на {n} объект(ах).",
        "op.cap_now.capped_count": "Кромки закрыты на {n} объект(ах).",

        "op.common.select_mesh": "Выберите объект-сетку.",

        "warn.unapplied_transforms": "У объекта имеются неприменённые трансформации",
        "warn.apply_transforms_hint": "Рассмотрите применение всех трансформаций (Ctrl+A) для точных и предсказуемых результатов.",

        "msg.no_active_object": "Нет активного объекта.",
        "msg.not_mesh": "Активный объект не является сеткой.",
        "msg.operation_done": "Операция завершена.",
        "msg.operation_failed": "Сбой операции.",
        "msg.unapplied_transforms": "У объекта имеются неприменённые трансформации",

        # profiles.py specific UI
        "ui.split_offset_mm": "Смещение разреза (мм)",
        "ui.split_offset_desc": "Смещение плоскости разреза вдоль оси (положительно по оси)",
        "ui.split_axis": "Ось разреза",
        "ui.split_along_x": "Разделить вдоль X",
        "ui.split_along_y": "Разделить вдоль Y",
        "ui.split_along_z": "Разделить вдоль Z",
        "ui.show_split_preview": "Показать предварительный просмотр разреза",
        "ui.show_split_preview_desc": "Показать временные оранжевые плоскости в запланированных местах разреза",
        "ui.parts_count": "Количество частей",
        "ui.parts_count_desc": "Желаемое количество сегментов (плоскости разреза = части - 1)",

        "ui.cap_seams_during_split_short": "Закрывать кромки при разрезе",
        "ui.cap_seams_during_split_desc": "Автоматически закрывать кромки после разреза. С полостью/внутренней оболочкой: точное заполнение внешних/внутренних петель; без полости: простое заполнение. Может увеличить время выполнения.",

        "ui.connector_type": "Тип соединителя",
        "ui.cyl_pin": "Цилиндрический штифт",
        "ui.cyl_pin_desc": "Штифт + втулка",
        "ui.rect_tenon": "Прямоугольный шип",
        "ui.rect_tenon_desc": "Соединение против проворота",
        "ui.snap_pin": "Защёлкивающийся штифт",
        "ui.snap_pin_desc": "Соединитель с защёлкивающимися шариками",
        "ui.snap_tenon": "Защёлкивающийся шип",
        "ui.snap_tenon_desc": "Прямоугольный шип с шариками-защёлками",

        "ui.distribution": "Распределение",
        "ui.distribution_desc": "Распределить соединители вдоль линии или сеткой по поверхности шва",
        "ui.line": "Линия",
        "ui.line_desc": "Разместить соединители вдоль линии на поверхности шва",
        "ui.grid": "Сетка",
        "ui.grid_desc": "Распределить соединители сеткой по поверхности шва",
        "ui.connectors_per_seam": "Соединителей на шов",
        "ui.rows_grid": "Ряды (СЕТКА)",
        "ui.rows_grid_desc": "Количество рядов для распределения сеткой",
        "ui.margin_pct": "Край (%)",
        "ui.margin_pct_desc": "Крайовой зазор вдоль шва (и перпендикулярно в СЕТКЕ) как процент длины детали (рекомендуется 0–40%)",

        "ui.spheres_per_side": "Шариков на сторону",
        "ui.spheres_per_side_desc": "Количество защёлкивающихся шариков на сторону/вокруг",
        "ui.sphere_diameter_mm": "Диаметр шара (мм)",
        "ui.sphere_diameter_mm_desc": "Диаметр защёлкивающихся шариков",
        "ui.protrusion_mm": "Выступание (мм)",
        "ui.protrusion_mm_desc": "Насколько шарики выступают из боковой поверхности",

        "ui.pin_diameter_mm": "Диаметр штифта (мм)",
        "ui.pin_length_mm": "Длина штифта (мм)",
        "ui.segments": "Сегменты",
        "ui.segments_desc": "Радиальные сегменты цилиндрического штифта (визуальная гладкость)",
        "ui.tenon_width_mm": "Ширина шипа (мм)",
        "ui.tenon_depth_mm": "Глубина шипа (мм)",
        "ui.chamfer_mm": "Фаска (мм)",

        "ui.insert_depth_pct": "Глубина вставки (%)",
        "ui.insert_depth_pct_desc": "Процент длины соединителя, утопленный в деталь A",

        "ui.material_profiles": "Профили материалов",
        "ui.material_profile_desc": "Выберите профиль материала, чтобы автоматически заполнить допуск на сторону",
        "profiles.mat.tooltip": "Рекомендуемый допуск на сторону: {val:.2f} мм",
        "ui.tol_per_face_mm": "Допуск на грань (мм)",
        "ui.tol_override_desc": "Переопределяет профиль материала (0 = использовать значение профиля)",

        "ui.foldout.more_seg": "Дополнительные настройки сегментации",
        "ui.foldout.more_seg_desc": "Показать расширенные параметры сегментации",
        "ui.foldout.more_conn": "Дополнительные настройки соединений",
        "ui.foldout.more_conn_desc": "Показать расширенные параметры соединений/геометрии",
        "ui.foldout.more_tol": "Дополнительные настройки допусков",
        "ui.foldout.more_tol_desc": "Показать расширенные параметры допусков",
        "ui.foldout.more_align": "Дополнительные настройки выравнивания",
        "ui.foldout.more_align_desc": "Показать расширенные параметры выравнивания",

        "tooltip.planar_split": "Разрезает выбранную геометрию по наилучшей подходящей плоскости.",
        "tooltip.adjust": "Открывает тонкие настройки текущей операции.",
        "tooltip.show_split_preview": "Вкл./выкл. визуальный предпросмотр перед применением.",

        "ui.segmentation_title": "Сегментация",
        "ui.less": "Меньше",
        "ui.adjust": "Настроить",
        "ui.cap_seams_during_split_slow": "Закрывать кромки при разрезе (медленнее)",
        "ui.connections_title": "Соединения",
        "ui.add_connectors": "Добавить соединители",
        "ui.place_connectors_click": "Разместить соединители (клик)",
        "ui.pick_faces_hint": "Выберите грани в режиме Объект (A = цель, B = движ.)",
        "ui.face_a_none": "A: нет",
        "ui.face_b_none": "B: нет",
        "ui.pick_face_a": "Выбрать грань A",
        "ui.pick_face_b": "Выбрать грань B",
        "ui.align_faces": "Выровнять грани",
        "ui.align_faces_desc": "Выровнять грань B по грани A с локальным соответствием и ориентацией",
    },

    # Ukrainian (Ukraine) - complete
    "uk_UA": {
        "ui.panel.title": "SnapSplit",
        "ui.reload_language": "Перезавантажити мову інтерфейсу",
        "ui.reload_language_desc": "Повторно зареєструйте додаток, щоб застосувати поточну мову Blender до статичних міток.",
        "ui.section.profiles": "Профілі",
        "ui.section.tools": "Інструменти",
        "ui.button.apply": "Застосувати",
        "ui.button.cancel": "Скасувати",
        "ui.button.ok": "OK",
        "ui.section.export": "Експорт",
        "ui.section.settings": "Налаштування",
        "ui.label.collection": "Колекція експорту",
        "ui.tooltip.collection": "Колекція, що використовується для виводу експорту",

        "prefs.title": "Налаштування SnapSplit",
        "prefs.default_profile": "Профіль за замовчуванням",
        "prefs.create_export_collection": "Створити колекцію експорту",
        "prefs.language_note": "Мова відповідає мові інтерфейсу Blender. Після зміни скористайтеся «Перезавантажити мову інтерфейсу».",
        "prefs.reload_language": "Перезавантажити мову інтерфейсу",
        "prefs.reload_language_desc": "Повторно зареєструйте додаток, щоб оновити статичні мітки (оператори/властивості).",

        "profiles.name": "Профіль",
        "profiles.description": "Активний профіль SnapSplit",
        "profiles.enum.material": "Матеріал",
        "profiles.enum.material_desc": "Стратегія призначення матеріалів",
        "profiles.enum.method": "Метод",
        "profiles.enum.method_desc": "Метод поділу для використання",

        "op.adjust_axis.label": "Налаштувати вісь розрізу",
        "op.adjust_axis.done": "Вісь розрізу налаштовано.",
        "op.adjust_axis.cancelled": "Налаштування осі розрізу скасовано.",

        "op.split.label": "Площинний розріз",
        "op.split.desc": "Розділити грані уздовж підібраної площини",
        "op.split.many_parts_hint": "Поділ на багато частин може зайняти час на щільних сітках...",
        "op.split.autocap.none": "Автозакриття не знайшло ді��сних петель.",
        "op.split.autocap.count": "Автозакриття кромок на {n} частині(ях).",
        "op.split.fewer_parts": "Створено менше частин, ніж очікувалось ({have} < {want}).",
        "op.split.parts_created": "Створено частин: {n}.",

        "op.cap_now.label": "Закрити кромки зараз",
        "op.cap_now.desc": "Заповнити між двома петлями розрізу (зовнішня+внутрішня) на площину. Перевага seed.",
        "op.cap_now.only_selected.name": "Лише вибрані об’єкти",
        "op.cap_now.max_planes.name": "Макс. площин",
        "op.cap_now.max_planes.desc": "0 = усі площини на об’єкт, 1 = лише найбільша",
        "op.cap_now.select_only.name": "Лише вибір (без заповнення)",
        "op.cap_now.require_two_seeds.name": "Потрібно рівно дві seed-кромки",
        "op.cap_now.require_two_seeds.desc": "Якщо в режимі редагування вибрано рівно дві кромки, використовувати їх лише як seeds (без автодетекції).",
        "op.cap_now.no_targets": "Немає сітчастих об’єктів для закриття. Виберіть частини розрізу або використайте колекцію частин.",
        "op.cap_now.failed_one": "Помилка обробки «{name}»: {err}",
        "op.cap_now.none_selected": "Не вдалося визначити петлі кромок розрізу для вибору.",
        "op.cap_now.none_capped": "Не вдалося визначити та заповнити петлі кромок розрізу.",
        "op.cap_now.selected_count": "Вибрано петлі кромок розрізу на {n} об’єкті(ах).",
        "op.cap_now.capped_count": "Кромки закрито на {n} об’єкті(ах).",

        "op.common.select_mesh": "Будь ласка, виберіть сітчастий об’єкт.",

        "warn.unapplied_transforms": "Об’єкт має незастосовані перетворення",
        "warn.apply_transforms_hint": "Розгляньте застосування всіх перетворень (Ctrl+A) для точних і передбачуваних результатів.",

        "msg.no_active_object": "Немає активного об’єкта.",
        "msg.not_mesh": "Активний об’єкт не є сіткою.",
        "msg.operation_done": "Операцію завершено.",
        "msg.operation_failed": "Збій операції.",
        "msg.unapplied_transforms": "Об’єкт має незастосовані перетворення",

        # profiles.py specific UI
        "ui.split_offset_mm": "Зсув розрізу (мм)",
        "ui.split_offset_desc": "Зсув площини розрізу вздовж осі (додатно у напрямку осі)",
        "ui.split_axis": "Вісь розрізу",
        "ui.split_along_x": "Розрізати вздовж X",
        "ui.split_along_y": "Розрізати вздовж Y",
        "ui.split_along_z": "Розрізати вздовж Z",
        "ui.show_split_preview": "Показати попередній перегляд розрізу",
        "ui.show_split_preview_desc": "Показати тимчасові помаранчеві площини у запланованих місцях rozrizu",
        "ui.parts_count": "Кількість частин",
        "ui.parts_count_desc": "Бажана кількість сегментів (площини розрізу = частини - 1)",

        "ui.cap_seams_during_split_short": "Закривати кромки під час rozrizu",
        "ui.cap_seams_during_split_desc": "Автоматично закривати кромки після розрізу. З порожниною/внутрішньою оболонкою: точне заповнення зовнішніх/внутрішніх петель; без порожнини: просте заповнення. Може збільшити час в��конання.",

        "ui.connector_type": "Тип з’єднувача",
        "ui.cyl_pin": "Циліндричний штифт",
        "ui.cyl_pin_desc": "Штифт + втулка",
        "ui.rect_tenon": "Прямокутний шип",
        "ui.rect_tenon_desc": "З’єднання від провертання",
        "ui.snap_pin": "Фіксаторний штифт",
        "ui.snap_pin_desc": "З’єднувач зі сферами-защіпками",
        "ui.snap_tenon": "Фіксаторний шип",
        "ui.snap_tenon_desc": "Прямокутний шип зі сферами-защіпками",

        "ui.distribution": "Розподіл",
        "ui.distribution_desc": "Розподіляти з’єднувачі вздовж лінії або сіткою по поверхні шва",
        "ui.line": "Лінія",
        "ui.line_desc": "Розмістити з’єднувачі вздовж лінії на поверхні шва",
        "ui.grid": "Сітка",
        "ui.grid_desc": "Розподіляти з’єднувачі сіткою по поверхні шва",
        "ui.connectors_per_seam": "З’єднувачів на шов",
        "ui.rows_grid": "Ряди (СІТКА)",
        "ui.rows_grid_desc": "Кількість рядів для розподілу сіткою",
        "ui.margin_pct": "Поле (%)",
        "ui.margin_pct_desc": "Крайове поле вздовж шва (і перпендикулярно в СІТЦІ) як відсоток довжини деталі (рекомендовано 0–40%)",

        "ui.spheres_per_side": "Куль на сторону",
        "ui.spheres_per_side_desc": "Кількість фіксаторних куль на сторону/навколо",
        "ui.sphere_diameter_mm": "Діаметр кулі (мм)",
        "ui.sphere_diameter_mm_desc": "Діаметр фіксаторних куль",
        "ui.protrusion_mm": "Виступання (мм)",
        "ui.protrusion_mm_desc": "Наскільки кулі виступають із бічної поверхні",

        "ui.pin_diameter_mm": "Діаметр штифта (мм)",
        "ui.pin_length_mm": "Довжина штифта (мм)",
        "ui.segments": "Сегменти",
        "ui.segments_desc": "Радіальні сегменти циліндричного штифта (візуальна гладкість)",
        "ui.tenon_width_mm": "Ширина шипа (мм)",
        "ui.tenon_depth_mm": "Глибина шипа (мм)",
        "ui.chamfer_mm": "Фаска (мм)",

        "ui.insert_depth_pct": "Глибина вставки (%)",
        "ui.insert_depth_pct_desc": "Відсоток довжини з’єднувача, занурений у частину A",

        "ui.material_profiles": "Профілі матеріалів",
        "ui.material_profile_desc": "Виберіть профіль матеріалу, щоб автоматично заповнити допуск на сторону",
        "profiles.mat.tooltip": "Рекомендований допуск на сторону: {val:.2f} мм",
        "ui.tol_per_face_mm": "Допуск на грань (мм)",
        "ui.tol_override_desc": "Перевизначає профіль матеріалу (0 = використовувати значення профілю)",

        "ui.foldout.more_seg": "Більше налаштувань сегментації",
        "ui.foldout.more_seg_desc": "Показати розширені параметри сегментації",
        "ui.foldout.more_conn": "Більше налаштувань з’єднань",
        "ui.foldout.more_conn_desc": "Показати розширені параметри з’єднань/геометрії",
        "ui.foldout.more_tol": "Більше налаштувань допусків",
        "ui.foldout.more_tol_desc": "Показати розширені параметри допусків",
        "ui.foldout.more_align": "Більше налаштувань вирівнювання",
        "ui.foldout.more_align_desc": "Показати розширені параметри вирівнювання",

        "tooltip.planar_split": "Розрізає вибрану геометрію площиною найкращого прилягання.",
        "tooltip.adjust": "Відкриває точні налаштування поточної операції.",
        "tooltip.show_split_preview": "Увімк./вимк. попередній перегляд перед застосуванням.",

        "ui.segmentation_title": "Сегментація",
        "ui.less": "Менше",
        "ui.adjust": "Налаштувати",
        "ui.cap_seams_during_split_slow": "Закривати кромки під час розрізу (повільніше)",
        "ui.connections_title": "З’єднання",
        "ui.add_connectors": "Додати з’єднувачі",
        "ui.place_connectors_click": "Розмістити з’єднувачі (клік)",
        "ui.pick_faces_hint": "Виберіть грані в режимі Об’єкт (A = ціль, B = рухомий)",
        "ui.face_a_none": "A: немає",
        "ui.face_b_none": "B: немає",
        "ui.pick_face_a": "Вибрати грань A",
        "ui.pick_face_b": "Вибрати грань B",
        "ui.align_faces": "Вирівняти грані",
        "ui.align_faces_desc": "Вирівняти грань B до грані A з локальним узгодженням та орієнтацією",
    },

    # Turkish (Turkey) - complete
    "tr_TR": {
        "ui.panel.title": "SnapSplit",
        "ui.reload_language": "Arayüz dilini yeniden yükle",
        "ui.reload_language_desc": "Eklentiyi yeniden kaydedin, böylece Blender’ın geçerli dili statik etiketlere uygulanır.",
        "ui.section.profiles": "Profiller",
        "ui.section.tools": "Araçlar",
        "ui.button.apply": "Uygula",
        "ui.button.cancel": "İptal",
        "ui.button.ok": "Tamam",
        "ui.section.export": "Dışa aktar",
        "ui.section.settings": "Ayarlar",
        "ui.label.collection": "Dışa aktarma koleksiyonu",
        "ui.tooltip.collection": "Dışa aktarma çıktısı için kullanılan koleksiyon",

        "prefs.title": "SnapSplit Tercihleri",
        "prefs.default_profile": "Varsayılan profil",
        "prefs.create_export_collection": "Dışa aktarma koleksiyonu oluştur",
        "prefs.language_note": "Dil, Blender arayüz dilini takip eder. Değiştirdikten sonra «Arayüz dilini yeniden yükle»yi kullanın.",
        "prefs.reload_language": "Arayüz dilini yeniden yükle",
        "prefs.reload_language_desc": "Statik etiketleri (operatörler/özellikler) yenilemek için eklentiyi yeniden kaydedin.",

        "profiles.name": "Profil",
        "profiles.description": "Aktif SnapSplit profili",
        "profiles.enum.material": "Malzeme",
        "profiles.enum.material_desc": "Malzeme atama stratejisi",
        "profiles.enum.method": "Yöntem",
        "profiles.enum.method_desc": "Kullanılacak bölme yöntemi",

        "op.adjust_axis.label": "Bölme eksenini ayarla",
        "op.adjust_axis.done": "Bölme ekseni ayarlandı.",
        "op.adjust_axis.cancelled": "Bölme ekseni ayarı iptal edildi.",

        "op.split.label": "Düzlemsel bölme",
        "op.split.desc": "Uydurulmuş bir düzlem boyunca yüzleri böl",
        "op.split.many_parts_hint": "Birçok parçaya bölmek, yoğun ağlarda zaman alabilir...",
        "op.split.autocap.none": "Otomatik kapatma geçerli döngüler bulamadı.",
        "op.split.autocap.count": "{n} parçada otomatik kapatma uygulandı.",
        "op.split.fewer_parts": "Beklenenden daha az parça oluşturuldu ({have} < {want}).",
        "op.split.parts_created": "{n} parça oluşturuldu.",

        "op.cap_now.label": "Kenarları şimdi kapat",
        "op.cap_now.desc": "Her düzlem için tam olarak iki bölme kenar döngüsü (dış+iç) arasında doldurur. Seed’ler tercih edilir.",
        "op.cap_now.only_selected.name": "Yalnızca seçili nesneler",
        "op.cap_now.max_planes.name": "Azami düzlem",
        "op.cap_now.max_planes.desc": "0 = nesne başına tüm düzlemler, 1 = yalnızca en büyüğü",
        "op.cap_now.select_only.name": "Yalnızca seç (doldurma yok)",
        "op.cap_now.require_two_seeds.name": "Tam olarak iki seed kenarı gerekli",
        "op.cap_now.require_two_seeds.desc": "Düzenleme modunda tam olarak iki kenar seçiliyse, yalnızca bunları seed olarak kullan (otomatik algılama yok).",
        "op.cap_now.no_targets": "Kapatılacak ağ nesnesi yok. Bölünmüş parçaları seçin veya parçalar koleksiyonunu kullanın.",
        "op.cap_now.failed_one": "‘{name}’ işlenemedi: {err}",
        "op.cap_now.none_selected": "Seçilecek bölme kenar döngüleri belirlenemedi.",
        "op.cap_now.none_capped": "Bölme kenar döngüleri belirlenip doldurulamadı.",
        "op.cap_now.selected_count": "{n} nesnede bölme kenar döngüleri seçildi.",
        "op.cap_now.capped_count": "{n} nesnede kenarlar kapatıldı.",

        "op.common.select_mesh": "Lütfen bir ağ (mesh) nesnesi seçin.",

        "warn.unapplied_transforms": "Nesnede uygulanmamış dönüşümler var",
        "warn.apply_transforms_hint": "Doğru ve öngörülebilir sonuçlar için tüm dönüşümleri uygulamayı (Ctrl+A) düşünün.",

        "msg.no_active_object": "Etkin nesne yok.",
        "msg.not_mesh": "Etkin nesne bir ağ (mesh) değil.",
        "msg.operation_done": "İşlem tamamlandı.",
        "msg.operation_failed": "İşlem başarısız oldu.",
        "msg.unapplied_transforms": "Nesnede uygulanmamış dönüşümler var",

        # profiles.py specific UI
        "ui.split_offset_mm": "Kesme ofseti (mm)",
        "ui.split_offset_desc": "Bölme ekseni boyunca kesme düzleminin ofseti (eksen yönünde pozitif)",
        "ui.split_axis": "Bölme Ekseni",
        "ui.split_along_x": "X boyunca böl",
        "ui.split_along_y": "Y boyunca böl",
        "ui.split_along_z": "Z boyunca böl",
        "ui.show_split_preview": "Bölme önizlemesini göster",
        "ui.show_split_preview_desc": "Planlanan kesim konumlarında geçici turuncu düzlemler göster",
        "ui.parts_count": "Parça sayısı",
        "ui.parts_count_desc": "İstenen segment sayısı (kesme düzlemleri = parça - 1)",

        "ui.cap_seams_during_split_short": "Bölme sırasında kenarları kapat",
        "ui.cap_seams_during_split_desc": "Bölmeden sonra kenarları otomatik olarak kapatır. Boşluk/iç kabuk ile: dış/iç döngüleri hassas doldurma; boşluk yoksa: basit doldurma. Çalışma süresini artırabilir.",

        "ui.connector_type": "Bağlayıcı Türü",
        "ui.cyl_pin": "Silindir Pim",
        "ui.cyl_pin_desc": "Kılavuz pim + yuva",
        "ui.rect_tenon": "Dikdörtgen Zıvana",
        "ui.rect_tenon_desc": "Dönmeye karşı bağlantı",
        "ui.snap_pin": "Sistem Pim",
        "ui.snap_pin_desc": "Sistem küreli bağlayıcı",
        "ui.snap_tenon": "Sistem Zıvana",
        "ui.snap_tenon_desc": "Küreli dikdörtgen zıvana",

        "ui.distribution": "Dağıtım",
        "ui.distribution_desc": "Bağlayıcıları dikiş yüzeyi boyunca bir hat veya ızgara halinde dağıt",
        "ui.line": "Hat",
        "ui.line_desc": "Bağlayıcıları dikiş yüzeyinde bir hat boyunca yerleştir",
        "ui.grid": "Izgara",
        "ui.grid_desc": "Bağlayıcıları dikiş yüzeyinde ızgara halinde dağıt",
        "ui.connectors_per_seam": "Dikiş başına bağlayıcı",
        "ui.rows_grid": "Satırlar (IZGARA)",
        "ui.rows_grid_desc": "Izgara dağıtımı için satır sayısı",
        "ui.margin_pct": "Kenar payı (%)",
        "ui.margin_pct_desc": "Dikiş boyunca (ve IZGARA’da dik yönde) kenar payı, parça uzunluğuna göre yüzde (önerilen 0–40%)",

        "ui.spheres_per_side": "Yan başına küre",
        "ui.spheres_per_side_desc": "Yan başına/çevresinde sistem küresi sayısı",
        "ui.sphere_diameter_mm": "Küre çapı (mm)",
        "ui.sphere_diameter_mm_desc": "Sistem kürelerinin çapı",
        "ui.protrusion_mm": "Çıkıntı (mm)",
        "ui.protrusion_mm_desc": "Kürelerin yan yüzeyden ne kadar taştığı",

        "ui.pin_diameter_mm": "Pim çapı (mm)",
        "ui.pin_length_mm": "Pim uzunluğu (mm)",
        "ui.segments": "Segment",
        "ui.segments_desc": "Silindir pimin radyal segmentleri (görsel pürüzsüzlük)",
        "ui.tenon_width_mm": "Zıvana genişliği (mm)",
        "ui.tenon_depth_mm": "Zıvana derinliği (mm)",
        "ui.chamfer_mm": "Pah (mm)",

        "ui.insert_depth_pct": "Gömme derinliği (%)",
        "ui.insert_depth_pct_desc": "Bağlayıcı uzunluğunun parça A içine gömülen yüzdesi",

        "ui.material_profiles": "Malzeme Profilleri",
        "ui.material_profile_desc": "Her taraf için toleransı otomatik doldurmak üzere bir malzeme profili seçin",
        "profiles.mat.tooltip": "Taraf başına önerilen tolerans: {val:.2f} mm",
        "ui.tol_per_face_mm": "Yüzey başına tolerans (mm)",
        "ui.tol_override_desc": "Malzeme profilini geçersiz kılar (0 = profil değerini kullan)",

        "ui.foldout.more_seg": "Daha fazla bölme ayarı",
        "ui.foldout.more_seg_desc": "Gelişmiş bölme seçeneklerini göster",
        "ui.foldout.more_conn": "Daha fazla bağlantı ayarı",
        "ui.foldout.more_conn_desc": "Gelişmiş bağlantı/geometri seçeneklerini göster",
        "ui.foldout.more_tol": "Daha fazla tolerans ayarı",
        "ui.foldout.more_tol_desc": "Gelişmiş tolerans seçeneklerini göster",
        "ui.foldout.more_align": "Daha fazla hizalama ayarı",
        "ui.foldout.more_align_desc": "Gelişmiş hizalama seçeneklerini göster",

        "tooltip.planar_split": "Seçili geometriyi en uygun düzlemle böler.",
        "tooltip.adjust": "Geçerli işlem için ince ayarları açar.",
        "tooltip.show_split_preview": "Uygulamadan önce görsel önizlemeyi aç/kapat.",

        # Additional UI mentioned
        "ui.segmentation_title": "Segmentasyon",
        "ui.less": "Daha az",
        "ui.adjust": "Ayarla",
        "ui.cap_seams_during_split_slow": "Bölme sırasında kenarları kapat (daha yavaş)",
        "ui.connections_title": "Bağlantılar",
        "ui.add_connectors": "Bağlayıcı ekle",
        "ui.place_connectors_click": "Bağlayıcı yerleştir (tıkla)",
        "ui.pick_faces_hint": "Yüzleri Nesne Modunda seçin (A = hedef, B = hareketli)",
        "ui.face_a_none": "A: yok",
        "ui.face_b_none": "B: yok",
        "ui.pick_face_a": "Yüz A’yı seç",
        "ui.pick_face_b": "Yüz B’yi seç",
        "ui.align_faces": "Yüzleri hizala",
        "ui.align_faces_desc": "Yüz B’yi yerel uyum ve yönelimle Yüz A’ya hizala",
    },
}


# ---------------------------
# Optional: developer self-check to ensure all locales cover all keys
# Can be run manually in Blender’s console to print missing keys per locale.
# ---------------------------

def _debug_list_missing_keys() -> Dict[str, set]:
    """Return a dict mapping locale -> missing keys (compared to en_US)."""
    missing = {}
    base = translations.get("en_US", {})
    base_keys = set(base.keys())
    for loc, d in translations.items():
        # skip base buckets
        if loc in {"en", "de", "fr", "es", "it", "pt", "nl", "pl", "ja", "zh", "ru", "uk", "tr"}:
            continue
        keys = set(d.keys())
        miss = base_keys - keys
        if miss:
            missing[loc] = miss
    return missing
