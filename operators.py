'''
Copyright (C) 2015 Pistiwique, Pitiwazou
 
Created by Pistiwique, Pitiwazou
 
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
 
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
 
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''


import bpy
import os
import shutil
import subprocess
from mathutils import Vector
from bpy.types import Operator
from os.path import join, isfile, isdir
from os import remove, listdir
from . preview_utils import register_AssetM_pcoll_preview
from . import_utils import generate_thumbnail, preview_add_to_selection

# -----------------------------------------------------------------------------
#   EDITING LIBRARY TOOLS
# -----------------------------------------------------------------------------


class AddInAssetManagement(Operator):
    bl_idname = "object.add_in_asset_management"
    bl_label = "Add in Asset Managemen"
    bl_description = "Add the active object in the asset library"
    bl_options = {'REGISTER'}

    def modal(self, context, event):
        
        AM = context.window_manager.asset_m
        current_dir = os.path.basename(os.path.dirname(os.path.abspath(__file__)))
        user_preferences = bpy.context.user_preferences
        addon_prefs = user_preferences.addons[current_dir].preferences     
        addon_path = os.path.dirname(os.path.abspath(__file__))
        
        asset_tmp = join(addon_path, "Asset_tmp.blend")
        import_script = join(addon_path, 'background_tools', 'add_in_asset_management.py')
        library_path = join(addon_prefs.asset_M_library_path)
        source_file = join(addon_path, "blend_tools", "base_library.blend")

        if isfile(asset_tmp):

            group_list = ""
            group_name = AM.group_name
            parent = "enabled" if AM.with_main_parent else ""
            
            if len([obj for obj in context.scene.objects if obj.select]) == 1: # if only one asset selected in the scene
                asset = ''.join([asset.name for asset in context.selected_objects if asset.type == 'MESH' or asset.type == 'CURVE' and (asset.data.extrude or asset.data.bevel_depth)])

                if asset:
                    AM.render_list.append(asset)
                    Asset_library = join(library_path, AM.libraries, AM.categories, "blends", asset + ".blend")
                    sub = subprocess.Popen([bpy.app.binary_path, source_file, '-b', '--python', import_script, asset_tmp, Asset_library, asset, group_list, group_name, parent])
                    sub.wait()
                    
                else:
                    AM.custom_thumbnail_path = ""
                    AM.render_name = ""
                    AM.options_enabled = False
                 
                    return {'FINISHED'}

            else:
                asset_list = [asset.name for asset in bpy.context.scene.objects if asset.select]

                for asset in asset_list:
                    OBJ = bpy.data.objects[asset]
                    AM.render_list.append(asset)
                    if OBJ.users_group:
                        for gp in OBJ.users_group:
                            if gp.name not in AM.group_list:
                                AM.group_list.append(gp.name)
                                
                group_list = ';'.join(AM.group_list)
                asset = ';'.join(asset_list)

                Asset_library = join(library_path, AM.libraries, AM.categories, "blends", AM.group_name + ".blend")
                sub = subprocess.Popen([bpy.app.binary_path, source_file, '-b', '--python', import_script, asset_tmp, Asset_library, asset, group_list, group_name, parent])
                sub.wait()
                     
            remove(join(addon_path, "Asset_tmp.blend"))  
 
            AM.render_running = True
            AM.options_enabled = False
            bpy.ops.object.run_generate_thumbnails('INVOKE_DEFAULT')
             
            return{'FINISHED'}
 
        else:
            return {'PASS_THROUGH'}    
     
    def invoke(self, context, event):
        AM = context.window_manager.asset_m
        addon_path = os.path.dirname(os.path.abspath(__file__))
        asset_tmp = bpy.path.abspath(join(addon_path, "Asset_tmp.blend"))
        
        del(AM.render_list[:])  
        del(AM.group_list[:])

        if isfile(asset_tmp):
            remove(asset_tmp)
        
        if AM.replace_rename == 'replace':
            bpy.ops.object.remove_asset_object()
        
        bpy.ops.wm.save_as_mainfile(filepath = asset_tmp, copy = True)
        
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}
                
        

class CancelPanelChoise(Operator):
    bl_idname = "object.cancel_panel_choise"
    bl_label = "Cancel"
    bl_description = "Cancel the panel choise"
    bl_options = {'REGISTER'}
    
    def execute(self, context):
        AM = context.window_manager.asset_m
        AM.replace_rename = 'rename'
        AM.new_name = ""
        AM.options_enabled = False
        AM.group_name = ""
        AM.custom_thumbnail_path = ""
        AM.render_name = ""
 
        return {'FINISHED'}


class RunGenerateThumbnails(Operator):
    ''' Generate the thumbnail and update the preview when added it '''
    bl_idname = "object.run_generate_thumbnails"
    bl_label = "Run generate thumbnails" 
    
       
    def is_thumbnail_updated(self):
        AM = bpy.context.window_manager.asset_m
        current_dir = os.path.basename(os.path.dirname(os.path.abspath(__file__)))
        user_preferences = bpy.context.user_preferences
        addon_prefs = user_preferences.addons[current_dir].preferences
        
        self.thumbnails_list = [f for f in listdir(join(addon_prefs.asset_M_library_path, AM.libraries, AM.categories, "icons")) if f.endswith(".png")]

        return self.thumbnails_list != self.thumbnails_directory_list
    
    
    def modal(self, context, event):
        AM = bpy.context.window_manager.asset_m
        current_dir = os.path.basename(os.path.dirname(os.path.abspath(__file__)))
        user_preferences = bpy.context.user_preferences
        addon_prefs = user_preferences.addons[current_dir].preferences
        script_path = os.path.dirname(os.path.abspath(__file__))
        
        if self.is_thumbnail_updated() and not isfile(join(addon_prefs.asset_M_library_path, AM.libraries, AM.categories, "icons", "rendering.txt")):

            thumbnails = [f for f in listdir(join(addon_prefs.asset_M_library_path, AM.libraries, AM.categories, "icons")) if f.endswith(".png")]
            
            if not AM.group_name:
                for asset in AM.render_list:
                    if asset + ".png" not in thumbnails:
                        print(asset + " was not added in the library")
            
            if "EMPTY.png" in thumbnails:
                os.remove(join(addon_prefs.asset_M_library_path, AM.libraries, AM.categories, "icons", "EMPTY.png"))
                
            register_AssetM_pcoll_preview()
            
            AM.render_running = False 
            AM.group_name = ""
            AM.new_name = ""
            AM.replace_rename = 'rename'
            AM.custom_thumbnail_path = ""

            del(AM.render_list[:])  
            del(AM.group_list[:])
      
            return {'FINISHED'}
        
        else:
            return {'PASS_THROUGH'}
    
    def invoke(self, context, event):
        AM = context.window_manager.asset_m
        current_dir = os.path.basename(os.path.dirname(os.path.abspath(__file__)))
        user_preferences = bpy.context.user_preferences
        addon_prefs = user_preferences.addons[current_dir].preferences
        library_path = join(addon_prefs.asset_M_library_path)
        
        if len([obj for obj in context.scene.objects if obj.select]) >= 2 and AM.group_name:
            blend_file = join(library_path, AM.libraries, AM.categories, "blends", AM.group_name + '.blend')
        else:
            blend_file = join(library_path, AM.libraries, AM.categories, "blends", AM.render_list[0] + '.blend')
        
        if isfile(blend_file):
            self.thumbnails_directory_list = [f for f in listdir(join(library_path, AM.libraries, AM.categories, "icons")) if f.endswith(".png")]
            
            if AM.render_type == 'render':
                generate_thumbnail()
            
            elif AM.render_type == 'opengl':
                bpy.context.scene.render.use_antialiasing = True
                bpy.context.scene.render.antialiasing_samples = '16'
                bpy.ops.render.opengl()
                if AM.group_name:
                    bpy.data.images['Render Result'].save_render(filepath=join(library_path, AM.libraries, AM.categories, "icons", AM.group_name + '.png'))
                else:
                    bpy.data.images['Render Result'].save_render(filepath=join(library_path, AM.libraries, AM.categories, "icons", bpy.context.object.name + '.png'))
            
            else:
                if AM.image_type == 'disk':
                    thumbnail = bpy.path.abspath(AM.custom_thumbnail_path)
                    asset_name = AM.group_name if AM.group_name else bpy.context.active_object.name
                    shutil.copy(thumbnail, join(library_path, AM.libraries, AM.categories, "icons", asset_name + ".png"))
                else:
                    asset_name = AM.group_name if AM.group_name else bpy.context.active_object.name
                    bpy.data.images[AM.render_name].save_render(filepath=join(library_path, AM.libraries, AM.categories, "icons", asset_name + '.png'))
                    
                

            context.window_manager.modal_handler_add(self)
            
            return {'RUNNING_MODAL'}
        
        else:
            AM.render_running = False 
            AM.group_name = ""
            AM.new_name = ""
            AM.replace_rename = 'rename'
            AM.custom_thumbnail_path = ""
             
            del(AM.render_list[:])  
            del(AM.group_list[:])
            
            return {'FINISHED'}

    

class RemoveObjectFromAssetManagement(Operator):
    ''' Remove the object from your library '''
    bl_idname = "object.remove_asset_object"
    bl_label = "Remove object"
 
    @classmethod
    def poll(cls, context):
        return not bpy.context.window_manager.asset_m.render_running
 
    def execute(self, context):
        AM = context.window_manager.asset_m
        current_dir = os.path.basename(os.path.dirname(os.path.abspath(__file__)))
        user_preferences = bpy.context.user_preferences
        addon_prefs = user_preferences.addons[current_dir].preferences 
        script_path = os.path.dirname(join(os.path.abspath(__file__)))
        library_path = join(addon_prefs.asset_M_library_path)
        
        if AM.replace_rename == 'replace':
            if AM.group_name:
                asset = AM.group_name
            else:
                asset = context.active_object.name
        else:
            asset = context.window_manager.AssetM_previews.split(".png")[0]
 
        favorites_files = [f for f in listdir(join(library_path, AM.libraries, AM.categories, "Favorites")) if f.endswith(".png")]
 
        if asset + ".png" in favorites_files:
            os.remove(join(library_path, AM.libraries, AM.categories, "Favorites", asset + ".png"))
            if not favorites_files:
                AM.favorites_enabled = False
 
        os.remove(join(library_path, AM.libraries, AM.categories, "blends", asset + ".blend"))
        os.remove(join(library_path, AM.libraries, AM.categories, "icons", asset + ".png"))
 
        thumbnails_list = [f for f in listdir(join(library_path, AM.libraries, AM.categories, "icons")) if f.endswith(".png")]
 
        if not thumbnails_list:
            source_file = join(script_path, "blend_tools", "base_library", "icons", "EMPTY.png")        
            shutil.copy(source_file, join(library_path, AM.libraries, AM.categories, "icons", "EMPTY.png"))
        
        if AM.replace_rename == 'replace':
            return {'FINISHED'}
        
        else:
            register_AssetM_pcoll_preview()
            return {'FINISHED'}
 
    def invoke(self, context, event):
        dpi_value = bpy.context.user_preferences.system.dpi
        return context.window_manager.invoke_props_dialog(self, width=dpi_value*4, height=100)
 
    def draw(self, context):
        layout = self.layout
        asset = context.window_manager.AssetM_previews.split(".png")[0]
 
        col = layout.column()
        col.label("Remove \" " + asset + " \"", icon='ERROR')
        col.label("    It will not longer exist in Asset management")


class ChangeNameInAssetManagement(Operator):
    bl_idname = "object.change_name_asset"
    bl_label = "Change name"
    
    
    def execute(self, context):
        AM = context.window_manager.asset_m
        current_dir = os.path.basename(os.path.dirname(os.path.abspath(__file__)))
        user_preferences = bpy.context.user_preferences
        addon_prefs = user_preferences.addons[current_dir].preferences
        
        script_path = os.path.dirname(join(os.path.abspath(__file__)))
        library_path = join(addon_prefs.asset_M_library_path, AM.libraries, AM.categories)
        target = bpy.context.window_manager.AssetM_previews.split(".png")[0]
        new_name = AM.new_name
         
        Asset_M_library = join(library_path, "blends", target + ".blend")
        Asset_M_change_name_script = join(script_path, "background_tools", "change_asset_name.py")
        Asset_M_thumbnails_directory = join(library_path, "icons")
 
        os.rename(join(Asset_M_thumbnails_directory, target + ".png"), join(Asset_M_thumbnails_directory, new_name + ".png"))
        
        favorites_files = [f for f in listdir(join(addon_prefs.asset_M_library_path, AM.libraries, AM.categories, "Favorites")) if f.endswith(".png")] 
        
        if target + ".png" in favorites_files:
            os.rename(join(library_path, "Favorites", target + ".png"), join(library_path, "Favorites", new_name + ".png"))
            
        simple = False
        with bpy.data.libraries.load(Asset_M_library) as (data_from, data_to):
            if len(data_from.objects) == 1:
                simple = True
                
        if simple:
            sub = subprocess.Popen([bpy.app.binary_path, Asset_M_library, '-b', '--python', Asset_M_change_name_script, target, new_name])
            sub.wait()
        
        os.rename(join(library_path, "blends", target + ".blend"), join(library_path, "blends", new_name + ".blend"))
        if isfile(join(library_path, "blends", target + ".blend1")):
            os.remove(join(library_path, "blends", target + ".blend1"))
        
        AM.new_name = ""
        
        register_AssetM_pcoll_preview()
        
        return {'FINISHED'} 
    

# -----------------------------------------------------------------------------
#   FAVORITES
# -----------------------------------------------------------------------------


class AddToFavorites(Operator):
    ''' Add the asset to your favorites '''
    bl_idname = "object.add_to_favorites"
    bl_label = "Add to favorites" 
    
    def execute(self, context):
        AM = context.window_manager.asset_m
        current_dir = os.path.basename(os.path.dirname(os.path.abspath(__file__)))
        user_preferences = bpy.context.user_preferences
        addon_prefs = user_preferences.addons[current_dir].preferences
        target = context.window_manager.AssetM_previews
        
        if not os.path.exists(join(addon_prefs.asset_M_library_path,AM.libraries, AM.categories, "Favorites")):
            os.makedirs(join(addon_prefs.asset_M_library_path, AM.libraries, AM.categories, "Favorites"))
        
        source_file = join(addon_prefs.asset_M_library_path, AM.libraries, AM.categories, "icons", target)
        destination = join(addon_prefs.asset_M_library_path, AM.libraries, AM.categories, "Favorites", target)
        shutil.copy(source_file, destination)
        
        return {'FINISHED'}



class RemoveFromFavorites(Operator):
    ''' Remove the asset from your favorites '''
    bl_idname = "object.remove_from_favorites"
    bl_label = "Remove from favorites"
    
    def execute(self, context):
        AM = context.window_manager.asset_m
        current_dir = os.path.basename(os.path.dirname(os.path.abspath(__file__)))
        user_preferences = bpy.context.user_preferences
        addon_prefs = user_preferences.addons[current_dir].preferences
        target = context.window_manager.AssetM_previews
        
        os.remove(join(addon_prefs.asset_M_library_path, AM.libraries, AM.categories, "Favorites", target))
         
        favorites_files = [f for f in listdir(join(addon_prefs.asset_M_library_path, AM.libraries, AM.categories, "Favorites")) if f.endswith(".png")] 

        register_AssetM_pcoll_preview()
        
        if not favorites_files:
            AM.favorites_enabled = False
      
        return {'FINISHED'}
    
    
# -----------------------------------------------------------------------------
#   ASSET MANAGEMENT TOOLS
# -----------------------------------------------------------------------------


class AssetLink(bpy.types.Operator):
    bl_idname = "object.asset_m_link"
    bl_label = "Link"
    bl_options = {"REGISTER"}
 
    def execute(self, context):
        bpy.ops.object.make_links_data(type='OBDATA')
        bpy.ops.object.make_links_data(type='MODIFIERS')
 
        return {"FINISHED"}


class AssetUnlink(Operator):
    bl_idname = "object.asset_m_unlink"
    bl_label = "Unlink"
    bl_options = {"REGISTER", "UNDO"}
 
    def execute(self, context):
 
        bpy.ops.object.make_single_user(type='SELECTED_OBJECTS', object=True, obdata=True, material=False, texture=False, animation=False)
        return {"FINISHED"}


class ObjectAddToSelection(bpy.types.Operator):
    ''' Add the selected object to selected faces '''
    bl_idname = "object.asset_m_add_to_selection"
    bl_label = "To selection"
 
    def execute(self, context):
        bpy.ops.object.mode_set(mode='OBJECT')
        obj_main = context.active_object
        obj_list = []

        obj1, obj2 = context.selected_objects
        OBJ2 = obj1 if obj2 == obj_main else obj2
            
        OBJ2.select=False
         
        bpy.ops.object.duplicate()
        bpy.context.active_object.name = "Dummy"
        obj = context.active_object
        bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
         
        mat_world = obj.matrix_world
        up = Vector((0, 0, 1))
        mesh = obj.data
         
        for face in mesh.polygons:
            if face.select:
                loc = mat_world * Vector(face.center)
                quat = face.normal.to_track_quat('Z', 'Y')
                quat.rotate(mat_world)
                
                bpy.ops.object.select_all(action='DESELECT')
                bpy.context.scene.objects.active = OBJ2
                OBJ2.select=True
                bpy.ops.object.duplicate()
     
                bpy.context.active_object.matrix_world *= quat.to_matrix().to_4x4()
                
                bpy.context.object.location = loc
 
                obj_list.append(context.object.name)
         
        bpy.ops.object.select_all(action='DESELECT')
        bpy.data.objects["Dummy"].select=True
        bpy.ops.object.delete()
         
        bpy.context.scene.objects.active = bpy.data.objects[obj_list[0]]
         
        for obj in obj_list:
            bpy.data.objects[obj].select=True
            bpy.ops.object.asset_m_link()
            bpy.data.objects[obj].select=False
        
        bpy.data.objects[obj_list[0]].select=True 
        del(obj_list[:])

        bpy.context.space_data.transform_orientation = 'LOCAL'
 
        return {'FINISHED'}



 
# Prepare Asset Bounding box
class PrepareAsset(bpy.types.Operator):
    bl_idname = "object.prepare_asset"
    bl_label = "Prepare Asset"
    bl_description = ""
    bl_options = {"REGISTER", "UNDO"}
 
    def execute(self, context):
        #Create a list for the selected objects
        obj_list = [obj for obj in bpy.context.scene.objects if obj.select]
        
        #Create a cube as parent object and hide it
        bpy.ops.mesh.primitive_cube_add(radius=4)
        bpy.context.object.draw_type = 'WIRE'
        bpy.context.object.hide_render = True
         
        bpy.context.object.cycles_visibility.camera = False
        bpy.context.object.cycles_visibility.diffuse = False
        bpy.context.object.cycles_visibility.glossy = False
        bpy.context.object.cycles_visibility.transmission = False
        bpy.context.object.cycles_visibility.scatter = False
        bpy.context.object.cycles_visibility.shadow = False
         
        #Set the Active object a name
        bpy.context.active_object.name = "Prep"
        
        # Parent the objects to the active object if they have no parent
        for obj in obj_list:
            if not obj.parent:
                obj.select=True
                bpy.ops.object.parent_set(type='OBJECT', keep_transform=True)
         
        bpy.ops.object.select_all(action='DESELECT')
        
        # Select the Active object 
        bpy.context.active_object.select = True
        
        # remove the obj_list
        del(obj_list[:])
        
        return {"FINISHED"}

# Prepare Asset Hardops
class Prepare_Asset_Hardops(bpy.types.Operator):
    bl_idname = "object.prepare_asset_hardops"
    bl_label = "Prepare Asset Hardops"
    bl_description = "Use your lastest selection as parent"
    bl_options = {"REGISTER", "UNDO"}
 
    def execute(self, context):
        # Create a list for the selected objects in the scene
        obj_list_ho = [obj for obj in bpy.context.scene.objects if obj.select]
        # Make the active object in wire and hide it from camera and rendering
        bpy.context.object.draw_type = 'WIRE'
        bpy.context.object.hide_render = True
        bpy.context.object.cycles_visibility.camera = False
        bpy.context.object.cycles_visibility.diffuse = False
        bpy.context.object.cycles_visibility.glossy = False
        bpy.context.object.cycles_visibility.transmission = False
        bpy.context.object.cycles_visibility.scatter = False
        bpy.context.object.cycles_visibility.shadow = False
        bpy.context.active_object.name = "BB_" + bpy.context.active_object.name
 
        bpy.ops.object.select_all(action='DESELECT')
 
        # Parent the objects to the active object if they have no parent
        for obj in obj_list_ho:
            if not obj.parent:
                obj.select=True
                bpy.ops.object.parent_set(type='OBJECT', keep_transform=True)

        for obj in obj_list_ho:
            obj.select=True

        del(obj_list_ho[:])

        return {"FINISHED"}

    
    
class DebugPreview(bpy.types.Operator):
    bl_idname = "object.debug_preview"
    bl_label = "Debug"
    bl_description = "Add a thumbnail if the render didn't go well, you can Delete or Update the Asset with better settings' "
    
    def execute(self, context):
        AM = bpy.context.window_manager.asset_m
        current_dir = os.path.basename(os.path.dirname(os.path.abspath(__file__)))
        user_preferences = bpy.context.user_preferences
        addon_prefs = user_preferences.addons[current_dir].preferences
        script_path = os.path.dirname(os.path.abspath(__file__))
        asset_tmp = join(script_path, 'Asset_tmp.blend')

        blend_list = [blend.split(".blend")[0] for blend in listdir(join(addon_prefs.asset_M_library_path, AM.libraries, AM.categories, "blends")) if blend.endswith(".blend")]
        
        tumbnail_list = [f.split(".png")[0] for f in listdir(join(addon_prefs.asset_M_library_path, AM.libraries, AM.categories, "icons")) if f.endswith(".png")]
        
        source_file = join(script_path, "icons", "error.png")
        
        for item in blend_list:
            if item not in tumbnail_list:   
                shutil.copy(source_file, join(addon_prefs.asset_M_library_path, AM.libraries, AM.categories, "icons", item + ".png"))
                
        if isfile(join(addon_prefs.asset_M_library_path, AM.libraries, AM.categories, "icons", "rendering.txt")):
            remove(join(addon_prefs.asset_M_library_path, AM.libraries, AM.categories, "icons", "rendering.txt"))
        
        AM.render_running = False 
        AM.mutli_object_action = "group"
        AM.group_name = ""
        if isfile(asset_tmp):
            remove(asset_tmp) 
         
        del(AM.render_list[:])  
        del(AM.group_list[:])
        
        return {'FINISHED'} 
    
    
class AddCamOGL(bpy.types.Operator):
    bl_idname = "object.add_cam_ogl_render"
    bl_label = "Add Cam "
    bl_description = "Add a Cam for OpenGl Rendering"
    bl_options = {"REGISTER", "UNDO"}
 
    def execute(self, context):
        AM = context.window_manager.asset_m
        #Add object in the list
        obj_list = [obj for obj in bpy.context.scene.objects if obj.select]
        active_obj = context.active_object

        #Add camera and remane it
        if not "AM_OGL_Camera" in [obj.name for obj in bpy.context.scene.objects]:
            AM.cam_reso_X = bpy.context.scene.render.resolution_x
            AM.cam_reso_Y = bpy.context.scene.render.resolution_y
            
            bpy.ops.object.camera_add()
            bpy.context.active_object.name = "AM_OGL_Camera"
            bpy.ops.view3d.object_as_camera()
            bpy.context.space_data.lock_camera=True
            bpy.context.object.data.clip_end = 10000
            bpy.context.object.data.lens = 85
            bpy.context.space_data.show_only_render = True
            
            bpy.ops.view3d.camera_to_view()

            #Setup the render settings
            bpy.context.scene.render.resolution_x = 256
            bpy.context.scene.render.resolution_y = 256
            bpy.context.scene.render.resolution_percentage = 100
 
            #Deselect All
            bpy.ops.object.select_all(action='DESELECT')
            
            #Select the objects in the list
            for obj in obj_list:
                obj.select=True
                bpy.context.scene.objects.active = active_obj
            
            bpy.ops.view3d.view_selected() 
 
        else:
            bpy.ops.object.select_all(action='DESELECT')
            bpy.data.objects['AM_OGL_Camera'].select=True
            bpy.context.scene.objects.active = bpy.data.objects['AM_OGL_Camera']
            bpy.ops.view3d.object_as_camera()
            bpy.ops.view3d.viewnumpad(type="CAMERA")
            bpy.context.space_data.lock_camera=True
            bpy.data.objects['AM_OGL_Camera'].select=False
            for obj in obj_list:
                obj.select=True
            bpy.context.scene.objects.active = active_obj
        return {"FINISHED"}

class DeleteCamOGL(bpy.types.Operator):
    bl_idname = "object.delete_cam_ogl_render"
    bl_label = "Delete"
    bl_description = "Delete the OGL camera"
    bl_options = {"REGISTER", "UNDO"}
 
    @classmethod
    def poll(cls, context):
        return "AM_OGL_Camera" in [obj.name for obj in bpy.context.scene.objects]
 
    def execute(self, context):
        AM = context.window_manager.asset_m
        objects = [obj for obj in bpy.context.selected_objects]
        bpy.ops.object.select_all(action='DESELECT')
        bpy.data.objects["AM_OGL_Camera"].select=True
        bpy.ops.object.delete()

        for obj in objects:
            obj.select=True
        bpy.context.space_data.show_only_render=False
        bpy.context.space_data.use_matcap = False
        bpy.context.space_data.fx_settings.use_ssao = False

        if AM.cam_reso_X:
            bpy.context.scene.render.resolution_x = AM.cam_reso_X
            bpy.context.scene.render.resolution_y = AM.cam_reso_Y
        AM.cam_reso_X = 0
        AM.cam_reso_Y = 0   
        return {"FINISHED"} 
    
    
def background_alpha(self, context):
    AM = bpy.context.window_manager.asset_m 
    if AM.background_alpha == 'TRANSPARENT': 
        alpha_mode = 'TRANSPARENT'
 
    elif AM.background_alpha == 'SKY':
        alpha_mode = 'SKY'
 
    bpy.context.scene.render.alpha_mode = alpha_mode
    

class AddActivePreview(bpy.types.Operator):
    bl_idname = "object.add_active_preview"
    bl_label = "Add Active Preview"
    bl_description = ""
    bl_options = {"REGISTER"}

    def execute(self, context):
        preview_add_to_selection()
        return {"FINISHED"}
        