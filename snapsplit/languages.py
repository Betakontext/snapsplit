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
# SPDX-License-Identifier: MIT
# languages.py - Centralized localization utilities for SnapSplit
#
# This module provides:
# - A translations dictionary keyed by language code and message keys
# - A normalize + fallback mechanism (exact -> base -> en_US)
# - A simple tr(key, default) function to fetch localized strings
# - Access to Blender's current UI language
#
# Notes:
# - We prefer 'en_US' as ultimate fallback.
# - Base code derivation: 'de_DE' -> 'de', 'en_AU' -> 'en'
# - Additional placeholder locales fr_FR, es_ES, it_IT are included
#   and will gracefully fall back to English where specific strings are missing.

from __future__ import annotations

from typing import Dict, Optional

try:
    import bpy
except Exception:
    bpy = None  # Allows limited import outside Blender, e.g., linters

# Cached language to optionally detect changes (not auto-reloading by default)
_CACHED_LANG: Optional[str] = None

def set_cached_lang(lang: str) -> None:
    # Cache last-known language to optionally detect changes
    global _CACHED_LANG
    _CACHED_LANG = lang

def get_cached_lang() -> Optional[str]:
    # Returns cached language or None
    return _CACHED_LANG

def get_current_language() -> str:
    # Reads Blender UI language; returns 'en_US' as safe default outside Blender
    if bpy is None:
        return "en_US"
    prefs = bpy.context.preferences if bpy.context else None
    if prefs and prefs.view:
        lang = prefs.view.language or ""
        if lang and lang != "DEFAULT":
            return lang
    # Map Blender DEFAULT (which means follow system) to English fallback
    return "en_US"

def lang_base(lang: str) -> str:
    # Extracts base lang code: 'de_DE' -> 'de', 'en' -> 'en'
    if not lang:
        return "en"
    if "_" in lang:
        return lang.split("_", 1)[0]
    return lang

def normalize_lang(lang: Optional[str]) -> str:
    # Normalizes language code to a known full form if possible
    if not lang:
        return "en_US"
    lang = lang.strip()
    if lang in translations:
        return lang
    # Try to expand known bases to default region
    base = lang_base(lang)
    mapping = {
        "en": "en_US",
        "de": "de_DE",
        "fr": "fr_FR",
        "es": "es_ES",
        "it": "it_IT",
    }
    return mapping.get(base, "en_US")

def _lookup(lang: str, key: str) -> Optional[str]:
    # Attempts to fetch a translation in sequence: exact -> base -> en_US
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
    # Public translation access. Provides fallback chain to English, then supplied default.
    lang = normalize_lang(get_current_language())
    value = _lookup(lang, key)
    if value is not None:
        return value
    return default or key

# Centralized translations.
# Keys are stable identifiers grouped by module/functionality.
# Keep English complete; other languages can be partial and will fall back.
translations: Dict[str, Dict[str, str]] = {
    # Base language buckets for base-only matches, if needed
    "en": {},
    "de": {},
    "fr": {},
    "es": {},
    "it": {},

    # Full locales
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
        "prefs.language_note": "Language follows Blender UI language. Use 'Reload UI Language' after changing Blender language.",
        "prefs.reload_language": "Reload UI Language",
        "prefs.reload_language_desc": "Re-register the add-on to refresh static labels (operators/properties).",

        # Profiles (properties)
        "profiles.name": "Profile",
        "profiles.description": "Active SnapSplit profile",
        "profiles.enum.material": "Material",
        "profiles.enum.material_desc": "Material assignment strategy",
        "profiles.enum.method": "Method",
        "profiles.enum.method_desc": "Splitting method to use",

        # Operators labels/descriptions (examples)
        "op.split.label": "Planar Split",
        "op.split.desc": "Split faces along a fitted plane",
        "op.align.label": "Align",
        "op.align.desc": "Align geometry to reference",
        "op.connectors.label": "Create Connectors",
        "op.connectors.desc": "Generate connector geometry for printing",

        # Reports / messages (examples)
        "msg.no_active_object": "No active object.",
        "msg.not_mesh": "Active object is not a mesh.",
        "msg.operation_done": "Operation finished.",
        "msg.operation_failed": "Operation failed.",
    },

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

        "op.split.label": "Planarer Schnitt",
        "op.split.desc": "Flächen entlang einer angepassten Ebene trennen",
        "op.align.label": "Ausrichten",
        "op.align.desc": "Geometrie an Referenz ausrichten",
        "op.connectors.label": "Verbinder erzeugen",
        "op.connectors.desc": "Verbinder-Geometrie für den Druck erzeugen",

        "msg.no_active_object": "Kein aktives Objekt.",
        "msg.not_mesh": "Aktives Objekt ist kein Mesh.",
        "msg.operation_done": "Vorgang abgeschlossen.",
        "msg.operation_failed": "Vorgang fehlgeschlagen.",
    },

    # Placeholders with partial coverage; fall back to English otherwise
    "fr_FR": {
        "ui.panel.title": "SnapSplit",
        "ui.reload_language": "Recharger la langue de l’UI",
        "ui.reload_language_desc": "Réenregistrer l’add-on pour appliquer la langue Blender aux libellés statiques.",
        "prefs.title": "Préférences SnapSplit",
        "prefs.reload_language": "Recharger la langue de l’UI",
        "prefs.reload_language_desc": "Réenregistrer l’add-on pour actualiser les libellés statiques (opérateurs/propriétés).",
    },
    "es_ES": {
        "ui.panel.title": "SnapSplit",
        "ui.reload_language": "Recargar idioma de la interfaz",
        "ui.reload_language_desc": "Volver a registrar el add-on para aplicar el idioma de Blender a las etiquetas estáticas.",
        "prefs.title": "Preferencias de SnapSplit",
        "prefs.reload_language": "Recargar idioma de la interfaz",
        "prefs.reload_language_desc": "Volver a registrar el add-on para actualizar las etiquetas estáticas (operadores/propiedades).",
    },
    "it_IT": {
        "ui.panel.title": "SnapSplit",
        "ui.reload_language": "Ricarica lingua UI",
        "ui.reload_language_desc": "Ri-registra l’add-on per applicare la lingua di Blender alle etichette statiche.",
        "prefs.title": "Preferenze SnapSplit",
        "prefs.reload_language": "Ricarica lingua UI",
        "prefs.reload_language_desc": "Ri-registra l’add-on per aggiornare le etichette statiche (operatori/proprietà).",
    },
}


