'''
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
'''

import bpy
from bpy.types import AddonPreferences
from bpy.props import StringProperty, BoolProperty, FloatProperty

class SNAPADDON_Preferences(AddonPreferences):
    """Add-on preferences for SnapSplit."""
    bl_idname = __package__  # "snapsplit"

    default_profile: StringProperty(
        name="Default Profile",
        default="PLA",
        description="Default material/printer profile",
    )
    create_export_collection: BoolProperty(
        name="Create export collection",
        default=True,
        description="Create a collection for parts ready to export",
    )

    def draw(self, context):
        """Draw the add-on preferences UI."""
        layout = self.layout
        layout.prop(self, "default_profile")
        layout.prop(self, "create_export_collection")

classes = (SNAPADDON_Preferences,)

def register():
    """Register add-on preferences."""
    for c in classes:
        bpy.utils.register_class(c)

def unregister():
    """Unregister add-on preferences."""
    for c in reversed(classes):
        bpy.utils.unregister_class(c)
