import bpy
import requests

bl_info = {
    "name": "DCC Plugin",
    "author": "Kaviyarasu",
    "version": (1, 0, 0),
    "blender": (4, 3, 0),
    "location": "View3D > Sidebar > DCC Plugin",
    "description": "A plugin to send object transforms to a Flask server",
    "warning": "",
    "wiki_url": "",
    "category": "Object",
}

SERVER_URL = "http://127.0.0.1:5000"

class TransformOperator(bpy.types.Operator):
    bl_idname = "object.send_transform"
    bl_label = "Send Transform to Server"

    def execute(self, context):
        obj = context.object
        if obj:
            # Collect object transform data (location, rotation, scale)
            data = {
                "name": obj.name,
                "position": list(obj.location),
                "rotation": list(obj.rotation_euler),
                "scale": list(obj.scale),
            }
            print(f"Sending data: {data}")  # Debugging line to check the data
            # Send the transform data to the Flask server via POST request
            response = requests.post(f"{SERVER_URL}/transform", json=data)
            self.report({'INFO'}, f"Response: {response.status_code}")
            if response.status_code == 200:
                self.report({'INFO'}, f"Data sent successfully: {response.json()}")
            else:
                self.report({'ERROR'}, f"Error sending data: {response.text}")
        return {'FINISHED'}

class OBJECT_PT_CustomPanel(bpy.types.Panel):
    bl_label = "DCC Plugin"
    bl_idname = "OBJECT_PT_custom_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'DCC Plugin'

    def draw(self, context):
        layout = self.layout
        obj = context.object
        if obj:
            # Add fields for location, rotation, and scale
            layout.prop(obj, "location")
            layout.prop(obj, "rotation_euler")
            layout.prop(obj, "scale")
            layout.operator("object.send_transform")

def register():
    bpy.utils.register_class(TransformOperator)
    bpy.utils.register_class(OBJECT_PT_CustomPanel)

def unregister():
    bpy.utils.unregister_class(TransformOperator)
    bpy.utils.unregister_class(OBJECT_PT_CustomPanel)

if __name__ == "__main__":
    register()
