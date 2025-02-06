bl_info = {
    "name": "DCC Integration Plugin",
    "author": "Kavi",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Sidebar > DCC Plugin",
    "description": "Plugin to send object transforms to a server.",
    "category": "Object",
}

import bpy
import requests
from bpy.props import EnumProperty, PointerProperty

class DCCPluginProperties(bpy.types.PropertyGroup):
    """Stores properties for the DCC Plugin"""
    endpoint: EnumProperty(
        name="Endpoint",
        description="Select server function",
        items=[
            ('/transform', "Transform", "Send all transforms"),
            ('/translation', "Translation", "Send position only"),
            ('/rotation', "Rotation", "Send rotation only"),
            ('/scale', "Scale", "Send scale only"),
            ('/file-path', "File Path", "Get the DCC file's path"),
        ],
        default='/transform'
    )

class OBJECT_OT_SubmitTransform(bpy.types.Operator):
    """Submit the selected object's transform data to the server"""
    bl_idname = "object.submit_transform"
    bl_label = "Submit Transform Data"

    def execute(self, context):
        obj = context.active_object
        if obj is None:
            self.report({'ERROR'}, "No active object selected!")
            return {'CANCELLED'}

        transform_data = {
            "name": obj.name,
            "location": list(obj.location),
            "rotation_euler": list(obj.rotation_euler),
            "scale": list(obj.scale)
        }

        endpoint = context.scene.dcc_plugin_props.endpoint
        url = f"http://localhost:5000{endpoint}"

        try:
            response = requests.post(url, json=transform_data)
            self.report({'INFO'}, f"Server Response: {response.status_code}")
        except Exception as e:
            self.report({'ERROR'}, f"Request failed: {e}")
            return {'CANCELLED'}

        return {'FINISHED'}

class VIEW3D_PT_DCCPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "DCC Integration Plugin"
    bl_idname = "VIEW3D_PT_dcc_plugin"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'DCC Plugin'

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        props = scene.dcc_plugin_props

        obj = context.active_object
        if obj:
            layout.label(text=f"Active Object: {obj.name}")
            col = layout.column()
            col.prop(obj, "location")
            col.prop(obj, "rotation_euler", text="Rotation")
            col.prop(obj, "scale")
        else:
            layout.label(text="No active object selected.")

        layout.prop(props, "endpoint")
        layout.operator("object.submit_transform")

# Registration
classes = (
    DCCPluginProperties,
    OBJECT_OT_SubmitTransform,
    VIEW3D_PT_DCCPanel,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    if hasattr(bpy.types.Scene, "dcc_plugin_props"):
        del bpy.types.Scene.dcc_plugin_props  # Fix: Remove old property before registering
    
    bpy.types.Scene.dcc_plugin_props = PointerProperty(type=DCCPluginProperties)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.dcc_plugin_props

if __name__ == "__main__":
    register()
