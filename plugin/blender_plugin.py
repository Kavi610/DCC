# bl_info = {
#     "name": "DCC Integration Plugin",
#     "author": "Your Name",
#     "version": (1, 0),
#     "blender": (2, 80, 0),
#     "location": "View3D > Sidebar > DCC Plugin",
#     "description": "Plugin to send object transforms to a server.",
#     "category": "Object",
# }

import bpy
import requests
from bpy.props import EnumProperty, PointerProperty

# Function to return endpoint options for dropdown
def get_endpoints(self, context):
    return [
        ('/transform', "Transform", "Send all transforms"),
        ('/translation', "Translation", "Send position only"),
        ('/rotation', "Rotation", "Send rotation only"),
        ('/scale', "Scale", "Send scale only"),
        ('/file-path', "File Path", "Get the DCC file's path"),
    ]

class DCCPluginProperties(bpy.types.PropertyGroup):
    endpoint: EnumProperty(
        name="Endpoint",
        description="Select server function",
        items=get_endpoints,
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

        # Gather transform data
        transform_data = {
            "name": obj.name,
            "location": list(obj.location),
            "rotation_euler": list(obj.rotation_euler),
            "scale": list(obj.scale)
        }

        # Get selected endpoint
        endpoint = context.scene.dcc_plugin_props.endpoint
        url = f"http://localhost:5000{endpoint}"

        try:
            response = requests.post(url, json=transform_data)
            response.raise_for_status()
            self.report({'INFO'}, f"Server Response: {response.status_code}")
        except requests.exceptions.RequestException as e:
            self.report({'ERROR'}, f"Request failed: {e}")
            return {'CANCELLED'}

        return {'FINISHED'}

class VIEW3D_PT_DCCPanel(bpy.types.Panel):
    """Creates a Panel in the 3D Viewport Sidebar"""
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
classes = (DCCPluginProperties, OBJECT_OT_SubmitTransform, VIEW3D_PT_DCCPanel)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.dcc_plugin_props = PointerProperty(type=DCCPluginProperties)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.dcc_plugin_props

if __name__ == "__main__":
    register()
