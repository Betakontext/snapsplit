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
from bpy.types import AddonPreferences
from bpy.props import StringProperty, BoolProperty, FloatProperty

class SNAPADDON_Preferences(AddonPreferences):
    bl_idname = __package__  # "snapsplit"

    default_profile: StringProperty(
        name="Standard-Profil",
        default="PLA",
        description="Standard-Material/Druckerprofil",
    )
    create_export_collection: BoolProperty(
        name="Export-Sammlung anlegen",
        default=True,
        description="Erzeuge Sammlung für exportfertige Teile",
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "default_profile")
        layout.prop(self, "create_export_collection")

classes = (SNAPADDON_Preferences,)

def register():
    for c in classes:
        bpy.utils.register_class(c)

def unregister():
    for c in reversed(classes):
        bpy.utils.unregister_class(c)


