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
import bmesh
import subprocess
from os import listdir
from os.path import join, isdir, isfile
from mathutils import Vector

def generate_thumbnail():
    AM = bpy.context.window_manager.asset_m
    subsurf = ""
    smooth = ""
    group = ""
    material = "object" if AM.material_render == False else ""
    
    if len([obj for obj in bpy.context.scene.objects if obj.select]) and AM.group_name:
        if AM.with_main_parent:
            AM.render_list.append(AM.group_name)
        group = AM.group_name
        AM.add_subsurf=False
        AM.add_smooth=False

        
    asset = ';'.join(AM.render_list)
        
    current_dir = os.path.basename(os.path.dirname(os.path.abspath(__file__)))
    user_preferences = bpy.context.user_preferences
    addon_prefs = user_preferences.addons[current_dir].preferences      
    script_path = os.path.dirname(os.path.abspath(__file__))
    Asset_M_library = join(script_path, 'blend_tools', 'thumbnailer.blend')  
    Asset_M_generate_Thumbnail = join(script_path, "background_tools", 'generate_thumbnail.py')
    thumbnail_directory = join(addon_prefs.asset_M_library_path, AM.libraries, AM.categories, "icons")
    blend_dir = join(addon_prefs.asset_M_library_path, AM.libraries, AM.categories, "blends")
    
    if AM.render_type == 'render':
        if AM.add_subsurf:
            subsurf = "add subsurf"
            
        if AM.add_smooth:
            smooth = "add smooth"
  
    sub = subprocess.Popen([bpy.app.binary_path, Asset_M_library, '-b', '--python', Asset_M_generate_Thumbnail, asset, thumbnail_directory, subsurf, smooth, blend_dir, group, material])
    
    
def import_from_asset_management():
    AM = bpy.context.window_manager.asset_m
    current_dir = os.path.basename(os.path.dirname(os.path.abspath(__file__)))
    user_preferences = bpy.context.user_preferences
    addon_prefs = user_preferences.addons[current_dir].preferences      
    
    library_path = join(addon_prefs.asset_M_library_path, AM.libraries, AM.categories)
    object_to_import = bpy.context.window_manager.AssetM_previews.split(".png")[0]

    blendfile = join(library_path, "blends", object_to_import + ".blend")
    source_files = [blendfile]
    scn = bpy.context.scene
       
    with bpy.data.libraries.load(blendfile) as (data_from, data_to):
        data_to.objects = data_from.objects
        if data_from.groups:
            data_to.groups = data_from.groups
            asset_groups = [gp for gp in data_from.groups]
               
        if data_from.materials:
            if AM.existing_material:
                materials = [mat for mat in data_from.materials]
            
    bpy.ops.object.select_all(action='DESELECT')

    layer_obj = [(obj, layer) for obj in data_from.objects for layer in range(0, 20) if obj.layers[layer]]
    
    for item in layer_obj:
        scn.objects.link(item[0])
        if AM.existing_material and item[0].type == 'MESH':
            if item[0].data.materials:
                for mat in item[0].data.materials:
                    for MAT in materials:
                        if MAT in mat.name:
                            item[0].material_slots[mat.name].material = bpy.data.materials[MAT]
             
            for material in bpy.data.materials:
                if not material.users:
                    bpy.data.materials.remove(material)

        if AM.existing_group:
            if item[0].users_group:
                for a_group in asset_groups:
                    if a_group in bpy.data.groups:
                        for d_group in item[0].users_group:
                            if a_group in d_group.name:
                                bpy.context.scene.objects.active = item[0]
                                bpy.ops.object.group_link(group=a_group)
                            
                                if d_group.name not in a_group:
                                    bpy.ops.group.objects_remove(group=d_group.name)


        if not AM.active_layer:
            item[0].layers = [idx == item[1] for idx in range(20)]
        item[0].select=True
        
    if AM.existing_group:
        for group in bpy.data.groups:
            if not len(group.objects):
                bpy.data.groups.remove(group)  
    
        
    bpy.context.scene.objects.active = layer_obj[0][0]
        
    if not AM.active_layer:
        for layers in layer_obj:
            bpy.context.scene.layers[layers[1]]=True
    
    selected_objects = [obj for obj in bpy.context.scene.objects if obj.select]
            
    if len(selected_objects) == 1:
        selected_objects[0].location = bpy.context.scene.cursor_location
            
    else:
        bpy.ops.mesh.primitive_cube_add(location=(0, 0, 0))
        bpy.context.active_object.name = "main_tmp"
        main = bpy.data.objects["main_tmp"]
        bpy.context.object.draw_type = 'WIRE'
        for obj in selected_objects:
            if not obj.parent:
                obj.parent=bpy.data.objects["main_tmp"]
        bpy.ops.object.select_all(action='DESELECT')
        main.select=True
        main.location = bpy.context.scene.cursor_location

            
def run_preview_add_to_selection(self, context):
    AM = context.window_manager.asset_m
    if not AM.without_import:
        preview_add_to_selection()
    
    
def preview_add_to_selection():
    
    bpy.context.scene.tool_settings.snap_element = 'FACE'
    bpy.context.scene.tool_settings.use_snap_align_rotation = True
    bpy.context.scene.tool_settings.use_snap_project = True
    multi = False
#    local_view = False
#    
#    for area in bpy.context.screen.areas:
#        if area.type == 'VIEW_3D':
#            if area.spaces.active.local_view is not None:
#                local_view = True
#                bpy.ops.view3d.localview()
    
    
    if bpy.context.object:          
        if bpy.context.object.mode == 'OBJECT':
            if bpy.context.selected_objects:
                cursor_location = bpy.context.scene.cursor_location.copy()
                bpy.ops.view3d.snap_cursor_to_selected() 
                import_from_asset_management()
                if bpy.context.active_object.name == "main_tmp":
                    objects = bpy.context.active_object.children
                    bpy.ops.object.transform_apply(location=True, rotation=False, scale=False)
                    bpy.ops.object.delete()
                    for obj in objects:
                        obj.select=True
                    bpy.context.scene.objects.active = objects[0]
                
                     
                bpy.context.scene.cursor_location = cursor_location

            else:
                import_from_asset_management()
                if bpy.context.active_object.name == "main_tmp":
                    objects = bpy.context.active_object.children
                    bpy.ops.object.transform_apply(location=True, rotation=False, scale=False)
                    bpy.ops.object.delete()
                    for obj in objects:
                        obj.select=True
                    bpy.context.scene.objects.active = objects[0]
                
                
        elif bpy.context.object.mode == 'EDIT':
            bpy.ops.object.mode_set(mode='OBJECT')
            
            selected_face = [f for f in bpy.context.active_object.data.polygons if f.select]
            
            if selected_face:
                obj_main = bpy.context.active_object
                second_obj = ""
                obj_list = []
                multi_list = []
                if len(bpy.context.selected_objects) > 1:
                    bpy.ops.object.select_all(action='DESELECT')
                    bpy.data.objects[obj_main.name].select=True

                bpy.ops.object.duplicate()
                bpy.context.active_object.name = "Dummy"
                obj = bpy.context.active_object
                bpy.ops.object.transform_apply(location=True, rotation=True, scale=True)
                
                copy_cursor = bpy.context.scene.cursor_location.copy()
                 
                mat_world = obj.matrix_world
                up = Vector((0, 0, 1))
                mesh = obj.data
                
                for face in mesh.polygons:
                    if face.select:
                        loc = mat_world * Vector(face.center)
                        quat = face.normal.to_track_quat('Z', 'Y')
                        quat.rotate(mat_world)

                        import_from_asset_management()
       
                        bpy.context.object.matrix_world *= quat.to_matrix().to_4x4()
                        
                        bpy.context.active_object.location = loc
                    
                        obj_list.append(bpy.context.object.name)
                        
                        if bpy.context.active_object.name == "main_tmp":
                            multi = True
                            if bpy.context.active_object.name != "main_tmp":
                                multi_list.append(bpy.context.active_object.name)

                        if bpy.context.active_object.name == "main_tmp":
                            objects = bpy.context.active_object.children
                            bpy.ops.object.transform_apply(location=True, rotation=True, scale=False)
                            bpy.ops.object.delete()
                            for obj in objects:
                                obj.select=True
                            bpy.context.scene.objects.active = objects[0]
                            
                if multi:
                    bpy.ops.object.select_all(action='DESELECT')
                    bpy.data.objects["Dummy"].select=True
                    bpy.ops.object.delete()
                    bpy.context.active_object.select=True
                    del(obj_list[:])
                    del(multi_list[:])
                    bpy.context.scene.cursor_location = copy_cursor
                
                else:
                    bpy.ops.object.select_all(action='DESELECT')
                    bpy.data.objects["Dummy"].select=True
                    bpy.ops.object.delete()
                    
                    bpy.context.scene.objects.active = bpy.data.objects[obj_list[0]]

                    for obj in obj_list:
                        bpy.data.objects[obj].select=True
                        bpy.ops.object.asset_m_link()
                        bpy.data.objects[obj].select=False

                    if second_obj:
                        bpy.data.objects[second_obj.name].select=True
                        
                    del(obj_list[:])
                    
                    bpy.context.scene.cursor_location = copy_cursor

#                    bpy.ops.object.mode_set(mode='EDIT') 
                    bpy.context.active_object.select=True              
#                    bpy.ops.mesh.select_all(action='SELECT')
                    bpy.context.space_data.transform_orientation = 'LOCAL'
            
            else:
                bpy.ops.object.mode_set(mode='EDIT')
    
    else:
        import_from_asset_management()
        if bpy.context.active_object.name == "main_tmp":
            objects = bpy.context.active_object.children
            bpy.ops.object.transform_apply(location=True, rotation=False, scale=False)
            bpy.ops.object.delete()
            for obj in objects:
                obj.select=True
            bpy.context.scene.objects.active = objects[0]
    
#    if local_view:
#        bpy.ops.view3d.localview()
#        local_view = False
        