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
