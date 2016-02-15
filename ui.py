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
from os.path import join, isdir, isfile
from os import listdir
from . icons.icons import load_icons
from . categories.operators import *


#UI Panel
class AM_UI(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_label = "Asset Management"
 
    def draw(self, context):
        layout = self.layout
        current_dir = os.path.basename(os.path.dirname(os.path.abspath(__file__)))
        user_preferences = bpy.context.user_preferences
        addon_prefs = user_preferences.addons[current_dir].preferences
        view = context.space_data
        fx_settings = view.fx_settings
        ssao_settings = fx_settings.ssao

        
        if addon_prefs.asset_M_library_path:

#---------------------- LIBRARIES ---------------------- 

            icons = load_icons()
            AM = context.window_manager.asset_m
            if isdir(join(addon_prefs.asset_M_library_path, AM.libraries, AM.categories, "icons")):
                thumbnails_list = [f for f in listdir(join(addon_prefs.asset_M_library_path, AM.libraries, AM.categories, "icons")) if f.endswith(".png")]
            if isdir(join(addon_prefs.asset_M_library_path, AM.libraries, AM.categories, "Favorites")):          
                favorites_files = [f.split(".png")[0] for f in listdir(join(addon_prefs.asset_M_library_path, AM.libraries, AM.categories, "Favorites")) if f.endswith(".png")]  
            
            
 
            # Add/Remove
            row = layout.row(align=True) 
            if AM.libraries:
                row.label("Libraries")
                row.prop(AM, "libraries", text="")
                row.prop(AM, "show_prefs_lib", text="", icon='TRIA_UP' if AM.show_prefs_lib else 'TRIA_DOWN')
            else:
                AM.show_prefs_lib=False
                row.operator("object.add_asset_m_library", text="Add library", icon='ZOOMIN')
                
            if AM.show_prefs_lib:
                box = layout.box()
                row = box.row(align=True)
                row.operator("object.add_asset_m_library", text="Add")
                row.operator("object.remove_asset_m_library", text="Remove")
                
                rename = icons.get("rename_asset")
                no_rename = icons.get("no_rename_asset")
                row.prop(AM, "rename_library", text="", icon_value=rename.icon_id if AM.rename_library else no_rename.icon_id)
                if AM.rename_library:
                    
                    row = box.row(align=True) 
                    row.label("Rename:")
                    row.prop(AM, "change_library_name", text="")
                    
                    
                libraries = [lib for lib in os.listdir(addon_prefs.asset_M_library_path) if isdir(addon_prefs.asset_M_library_path)]
                if AM.change_library_name:
                    if AM.change_library_name in libraries:

                        row = layout.row()
                        row.label("\" " + AM.change_library_name + " \" Already exist.", icon='ERROR')  
                    else:
                            row.operator("object.asset_m_rename_library", text="", icon='FILE_TICK')

#---------------------- CATEGORIES ---------------------- 
                    
            if AM.libraries and isdir(join(addon_prefs.asset_M_library_path, AM.libraries)):
                 
                icons = load_icons()
                AM = context.window_manager.asset_m
                 
                # Add/Remove
                row = layout.row(align=True) 
                if AM.categories:
                    row.label("Categories")
                    row.prop(AM, "categories", text="")
                    row.prop(AM, "show_prefs_cat", text="", icon='TRIA_UP' if AM.show_prefs_cat else 'TRIA_DOWN')

                    
                else:
                    AM.show_prefs_cat=False
                    row.operator("object.add_asset_m_category", text="Add category", icon='ZOOMIN')
                
                if AM.show_prefs_cat:
                    box = layout.box()
                    row = box.row(align=True)
                    row.operator("object.add_asset_m_category", text="Add")
                    row.operator("object.remove_asset_m_category", text="Remove")
                    
                    rename = icons.get("rename_asset")
                    no_rename = icons.get("no_rename_asset")
                    row.prop(AM, "rename_category", text="", icon_value=rename.icon_id if AM.rename_category else no_rename.icon_id)
                    if AM.rename_category:
                        row = box.row(align=True) 
                        row.label("Rename:")
                        row.prop(AM, "change_category_name", text="")
                 
                categories = [cat for cat in os.listdir(join(addon_prefs.asset_M_library_path, AM.libraries)) if isdir(join(addon_prefs.asset_M_library_path, AM.libraries))]
                if AM.change_category_name:
                    if AM.change_category_name in categories:
                        row = layout.row()
                        row.label("\" " + AM.change_category_name + " \" Already exist.", icon='ERROR')  
                    else:
                        row.operator("object.asset_m_rename_category", text="", icon='FILE_TICK')
                
#-------------------------------------------- 

                if AM.options_enabled and context.selected_objects: 
                    box = layout.box()
                    OBJ = context.active_object
                    object_list = [obj for obj in context.scene.objects if obj.select]
                    multi_object = False
                    is_subsurf=False
                    if len(object_list) >= 2:
                        asset_name = AM.group_name
                        multi_object = True
                    else:
                        asset_name = OBJ.name
                        if OBJ.modifiers:
                            for mod in context.object.modifiers:
                                if mod.type == 'SUBSURF': 
                                    is_subsurf=True

                    if not asset_name + ".png" in thumbnails_list or asset_name + ".png" in thumbnails_list and AM.replace_rename == 'replace':
                        if asset_name + ".png" in thumbnails_list and AM.replace_rename == 'replace':
                            box.label('" ' + asset_name + ' " already exist', icon='ERROR')
                            box.separator()
                            row = box.row(align=True)
                            row.prop(AM, "replace_rename", text=" ", expand=True)
                            if AM.replace_rename == 'rename':
                                if multi_object:
                                    box.prop(AM, "group_name", text="")
                                else:
                                    ob = context.object
                                    box.prop(ob, "name", text="")
                                row = box.row()

                        if multi_object:
                            box.label("Choose the asset name")
                            box.prop(AM, "group_name", text="")
                            box.prop(AM, "with_main_parent", text="With main parent")   
                            row = box.row(align=True)
                        

                        row = box.row(align=True)
                        row.prop(AM, "render_type", text=" ", expand=True)
                        if AM.render_type == 'render':
                            if not multi_object and not is_subsurf:
                                box.prop(AM, "add_subsurf", text="Subsurf")
                                box.prop(AM, "add_smooth", text="Smooth")  
                                
                            box.prop(AM, "material_render", text="Addon material") 
                        
                        #OpenGL    
                        elif AM.render_type == 'opengl':
                            row = box.row(align=True)
                            row.operator("object.add_cam_ogl_render", text="Add Camera" if not "AM_OGL_Camera" in [obj.name for obj in context.scene.objects] else "View camera", icon='ZOOMIN')
                            row.operator("object.delete_cam_ogl_render", text="", icon='ZOOMOUT')
                            row = layout.column()
                            view = context.space_data
                            scene = context.scene
                            fx_settings = view.fx_settings
                            row = box.row(align=True) 
                            row.label("Background:")
                            row.prop(AM, "background_alpha", text="")
                            row = box.row(align=True)
                            row.prop(view, "show_only_render")
                            row = box.row(align=True)
                            row.prop(view, "use_matcap")
                            if view.use_matcap :
                                row.prop(AM, "matcap_options", text="", icon='TRIA_UP' if AM.matcap_options else 'TRIA_DOWN')    
                                if AM.matcap_options:
                                    row = box.row(align=True)
                                    row.template_icon_view(view, "matcap_icon")
                            row = box.row(align=True)
                            row.prop(fx_settings, "use_ssao", text="Ambient Occlusion")
                            if fx_settings.use_ssao:
                                ssao_settings = fx_settings.ssao
                             
                                row.prop(AM, "ao_options", text="", icon='TRIA_UP' if AM.ao_options else 'TRIA_DOWN')    
                                if AM.ao_options:
                                    subcol = box.column(align=True)
                                    subcol.prop(ssao_settings, "factor")
                                    subcol.prop(ssao_settings, "distance_max")
                                    subcol.prop(ssao_settings, "attenuation")
                                    subcol.prop(ssao_settings, "samples")
                                    subcol.prop(ssao_settings, "color")
                            
                        elif AM.render_type == 'image':
                            row = box.row(align=True)
                            row.prop(AM, "image_type", text=" ", expand=True)
                            if AM.image_type == 'disk':
                                box.label("Choose your thumbnail")
                                box.prop(AM, "custom_thumbnail_path", text="")
                            else:
                                box.prop_search(AM, "render_name", bpy.data, "images", text="") 
                        
                        row = box.row(align=True)
                        if not multi_object:
                            if (not asset_name + ".png" in thumbnails_list or AM.replace_rename == 'replace') and (AM.render_type in ['opengl', 'render'] or AM.render_type == 'image' and (AM.image_type == 'disk' and AM.custom_thumbnail_path or AM.image_type == 'rendered' and AM.render_name)):
                                row.operator("object.add_in_asset_management", text="OK", icon='FILE_TICK') 
                        else:
                            if AM.group_name and (not asset_name + ".png" in thumbnails_list or AM.replace_rename == 'replace') and (AM.render_type in ['opengl', 'render'] or AM.render_type == 'image' and (AM.image_type == 'disk' and AM.custom_thumbnail_path or AM.image_type == 'rendered' and AM.render_name)):
                            
                                row.operator("object.add_in_asset_management", text="OK", icon='FILE_TICK') 
                        row.operator("object.cancel_panel_choise", text="Cancel", icon='X')
                        
                    else:
                        box.label('" ' + asset_name + ' " already exist', icon='ERROR')
                        box.separator()
                        row = box.row(align=True)
                        row.prop(AM, "replace_rename", text=" ", expand=True)
                        if AM.replace_rename == 'rename':
                            if multi_object:
                                box.prop(AM, "group_name", text="")
                            else:
                                ob = context.object
                                box.prop(ob, "name", text="")
                            row = box.row()
 
                else:   
                    #Show Only Favoris
                    row = layout.row()
                    favorites = icons.get("favorites_asset")
                    no_favorites = icons.get("no_favorites_asset")
                    if favorites_files:
                        row.prop(AM, "favorites_enabled", text="Show Only favorites")
         
                    #Asset Preview  
                    row = layout.row(align=True)  
                    sub = row.row()
                    sub.scale_y = 1.17 
                    sub.template_icon_view(context.window_manager, "AssetM_previews", show_labels=True if addon_prefs.show_labels else False)
                    
                    #Add/Remove Objects from library
                    col = row.column(align=True)
                    if context.selected_objects and not AM.render_running:
                        col.prop(AM, "options_enabled", text="", icon='ZOOMIN')
                    col.operator("object.remove_asset_object", text="", icon='ZOOMOUT')
                 
                    #Render Thumbnail 
                    if bpy.context.window_manager.asset_m.render_running:

                        layout.label("Thumbnail rendering", icon='RENDER_STILL')

                        layout.label("Please wait... ")
                        layout.operator("wm.console_toggle", text="Check/Hide Console")
                        
                    #Favoris
                    if isdir(join(addon_prefs.asset_M_library_path, AM.libraries, AM.categories, "Favorites")):
                        if favorites_files:
                            if context.window_manager.AssetM_previews.split(".png")[0] in favorites_files:       
                                col.operator("object.remove_from_favorites", text="", icon_value=favorites.icon_id)
                            else:
                                col.operator("object.add_to_favorites", text="", icon_value=no_favorites.icon_id)   
                        else:
                            col.operator("object.add_to_favorites", text="", icon_value=no_favorites.icon_id)
         
                    #Show Name
                    name = icons.get("name_asset")
                    no_name = icons.get("no_name_asset")
                    
                    col.prop(AM, "show_name_assets", text="", icon_value=name.icon_id if AM.show_name_assets else no_name.icon_id)
                    if AM.show_name_assets:
                        row = layout.row(align=True)
                        row.label("Name :")
         
                        sub = row.row()
                        sub.scale_x = 2.0
                        sub.label(context.window_manager.AssetM_previews.split("GP_")[-1].split(".png")[0])
         
                    #Name/Rename  
                    rename = icons.get("rename_asset")
                    no_rename = icons.get("no_rename_asset")
         
                    col.prop(AM, "rename_asset", text="", icon_value=rename.icon_id if AM.rename_asset else no_rename.icon_id)
                    if AM.rename_asset:
                        row = layout.row(align=True)
                        row.label("Rename :")
                        row.prop(AM, "new_name", text="")
                        #Check icon List
                        if thumbnails_list:
                            if AM.new_name:
                                if AM.new_name + ".png" in thumbnails_list:
                                    row = layout.row()
                                    row.label('" ' + AM.new_name + ' " already exist', icon='ERROR')
                                else:
                                    row.operator("object.change_name_asset", text="", icon='FILE_TICK') 
                        
         
                    #Without Import
                    if AM.without_import:
                        col.prop(AM, "without_import", icon='LOCKED', icon_only=True)
                    else:
                        col.prop(AM, "without_import", icon='UNLOCKED', icon_only=True)

                    #AM_tools
                    if AM.tools:
                        col.prop(AM, "tools", text="", icon='TRIA_UP') 
                        
                        #Debug Tools
                        layout.prop(AM, "debug_tools", text="Debug tools", icon='TRIA_UP' if AM.debug_tools else 'TRIA_DOWN')
                        if AM.debug_tools:
                            box = layout.box()
                            box.operator("object.debug_preview", text="Debug", icon='FILE_REFRESH')
                            box.operator("wm.console_toggle", text="Check/Hide Console", icon='CONSOLE')
                        
                        if context.object is not None and context.selected_objects:
                            #Asset to faces
                            if AM.Link_Scene_Asset_To_Faces:
                                layout.prop(AM, "Link_Scene_Asset_To_Faces", text="Asset To Selection", icon='TRIA_UP') 
                                
                                box = layout.box()
                                if len(context.selected_objects) >= 2 and context.object.mode == 'EDIT':
                                    row = box.row(align=True)
                                    row.operator("object.asset_m_add_to_selection", text="Scene Asset To Faces", icon="MOD_MULTIRES")
                 
                                #Link Objects
                                if len(context.selected_objects) >= 2 and context.object.mode == 'OBJECT':     
                                    row = box.row(align=True)
                                    row.operator("object.asset_m_link", text = "Link Objects", icon='CONSTRAINT' )
                 
                                #Unlink Objects
                                if context.object.mode == 'OBJECT':
                                    row = box.row(align=True)
                                    row.operator("object.asset_m_unlink", text = "Unlink Objects", icon='UNLINKED' )
                            
                            else:
                                layout.prop(AM, "Link_Scene_Asset_To_Faces", text="Asset To Selection", icon='TRIA_DOWN')
                        
                            
                            #Prepare Asset
                            layout.prop(AM, "prepare_asset", text="Setup Asset", icon='TRIA_UP' if AM.prepare_asset else 'TRIA_DOWN')
                            if AM.prepare_asset:
                                box = layout.box()
                                row = box.row(align=True)
                                row.operator("object.prepare_asset", text="Add Cube Parent", icon='MESH_CUBE')
                                row = box.row(align=True)
                                hardops = icons.get("hardops_asset")
                                row.operator("object.prepare_asset_hardops", text="Setup HardOps Asset", icon_value=hardops.icon_id)
                        
                        #Prepare OpenGL Render        
                        layout.prop(AM, "prepare_OGL", text="Setup OpenGl Render", icon='TRIA_UP' if AM.prepare_OGL else 'TRIA_DOWN')    
                        if AM.prepare_OGL:    
                            box = layout.box()
                            row = box.row(align=True)
                            row.operator("object.add_cam_ogl_render", text="Add Camera" if not "AM_OGL_Camera" in [obj.name for obj in context.scene.objects] else "View camera", icon='ZOOMIN')
                            row.operator("object.delete_cam_ogl_render", text="", icon='ZOOMOUT')
                            row = layout.column()
                            view = context.space_data
                            scene = context.scene
                            fx_settings = view.fx_settings
                            row = box.row(align=True) 
                            row.label("Background:")
                            row.prop(AM, "background_alpha", text="")
                            row = box.row(align=True)
                            row.prop(view, "show_only_render")
                            row = box.row(align=True)
                            row.prop(view, "use_matcap")
                            if view.use_matcap :
                                row.prop(AM, "matcap_options", text="", icon='TRIA_UP' if AM.matcap_options else 'TRIA_DOWN')    
                                if AM.matcap_options:
                                    row = box.row(align=True)
                                    row.template_icon_view(view, "matcap_icon")
                            row = box.row(align=True)
                            row.prop(fx_settings, "use_ssao", text="Ambient Occlusion")
                            if fx_settings.use_ssao:
                                ssao_settings = fx_settings.ssao
                       
                                row.prop(AM, "ao_options", text="", icon='TRIA_UP' if AM.ao_options else 'TRIA_DOWN')    
                                if AM.ao_options:
                                    subcol = box.column(align=True)
                                    subcol.prop(ssao_settings, "factor")
                                    subcol.prop(ssao_settings, "distance_max")
                                    subcol.prop(ssao_settings, "attenuation")
                                    subcol.prop(ssao_settings, "samples")
                                    subcol.prop(ssao_settings, "color")
                    else:
                        col.prop(AM, "tools", text="", icon='TRIA_DOWN')
                    
       
        else:
            layout.label("Define the library path", icon='ERROR')
            layout.label("in the addon preferences please.")
            layout.operator("screen.userpref_show", icon='PREFERENCES')



class AM_Tools(bpy.types.Panel):
    bl_label = "Asset Management"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "Tools"

    def draw(self, context):
        layout = self.layout
        current_dir = os.path.basename(os.path.dirname(os.path.abspath(__file__)))
        user_preferences = bpy.context.user_preferences
        addon_prefs = user_preferences.addons[current_dir].preferences
        view = context.space_data
        fx_settings = view.fx_settings
        ssao_settings = fx_settings.ssao
 
 
        if addon_prefs.asset_M_library_path:
 
#---------------------- LIBRARIES ---------------------- 
 
            icons = load_icons()
            AM = context.window_manager.asset_m
            if isdir(join(addon_prefs.asset_M_library_path, AM.libraries, AM.categories, "icons")):
                thumbnails_list = [f for f in listdir(join(addon_prefs.asset_M_library_path, AM.libraries, AM.categories, "icons")) if f.endswith(".png")]
            if isdir(join(addon_prefs.asset_M_library_path, AM.libraries, AM.categories, "Favorites")):          
                favorites_files = [f.split(".png")[0] for f in listdir(join(addon_prefs.asset_M_library_path, AM.libraries, AM.categories, "Favorites")) if f.endswith(".png")]  
 
 
 
            # Add/Remove
            row = layout.row(align=True) 
            if AM.libraries:
                row.label("Libraries")
                row.prop(AM, "libraries", text="")
                row.prop(AM, "show_prefs_lib", text="", icon='TRIA_UP' if AM.show_prefs_lib else 'TRIA_DOWN')
            else:
                AM.show_prefs_lib=False
                row.operator("object.add_asset_m_library", text="Add library", icon='ZOOMIN')
 
            if AM.show_prefs_lib:
                box = layout.box()
                row = box.row(align=True)
                row.operator("object.add_asset_m_library", text="Add")
                row.operator("object.remove_asset_m_library", text="Remove")
 
                rename = icons.get("rename_asset")
                no_rename = icons.get("no_rename_asset")
                row.prop(AM, "rename_library", text="", icon_value=rename.icon_id if AM.rename_library else no_rename.icon_id)
                if AM.rename_library:
 
                    row = box.row(align=True) 
                    row.label("Rename:")
                    row.prop(AM, "change_library_name", text="")
 
 
                libraries = [lib for lib in os.listdir(addon_prefs.asset_M_library_path) if isdir(addon_prefs.asset_M_library_path)]
                if AM.change_library_name:
                    if AM.change_library_name in libraries:
 
                        row = layout.row()
                        row.label("\" " + AM.change_library_name + " \" Already exist.", icon='ERROR')  
                    else:
                            row.operator("object.asset_m_rename_library", text="", icon='FILE_TICK')
 
#---------------------- CATEGORIES ---------------------- 
 
            if AM.libraries and isdir(join(addon_prefs.asset_M_library_path, AM.libraries)):
 
                icons = load_icons()
                AM = context.window_manager.asset_m
 
                # Add/Remove
                row = layout.row(align=True) 
                if AM.categories:
                    row.label("Categories")
                    row.prop(AM, "categories", text="")
                    row.prop(AM, "show_prefs_cat", text="", icon='TRIA_UP' if AM.show_prefs_cat else 'TRIA_DOWN')
 
 
                else:
                    AM.show_prefs_cat=False
                    row.operator("object.add_asset_m_category", text="Add category", icon='ZOOMIN')
 
                if AM.show_prefs_cat:
                    box = layout.box()
                    row = box.row(align=True)
                    row.operator("object.add_asset_m_category", text="Add")
                    row.operator("object.remove_asset_m_category", text="Remove")
 
                    rename = icons.get("rename_asset")
                    no_rename = icons.get("no_rename_asset")
                    row.prop(AM, "rename_category", text="", icon_value=rename.icon_id if AM.rename_category else no_rename.icon_id)
                    if AM.rename_category:
                        row = box.row(align=True) 
                        row.label("Rename:")
                        row.prop(AM, "change_category_name", text="")
 
                categories = [cat for cat in os.listdir(join(addon_prefs.asset_M_library_path, AM.libraries)) if isdir(join(addon_prefs.asset_M_library_path, AM.libraries))]
                if AM.change_category_name:
                    if AM.change_category_name in categories:
                        row = layout.row()
                        row.label("\" " + AM.change_category_name + " \" Already exist.", icon='ERROR')  
                    else:
                        row.operator("object.asset_m_rename_category", text="", icon='FILE_TICK')
 
#-------------------------------------------- 
 
                if AM.options_enabled and context.selected_objects: 
                    box = layout.box()
                    OBJ = context.active_object
                    object_list = [obj for obj in context.scene.objects if obj.select]
                    multi_object = False
                    is_subsurf=False
                    if len(object_list) >= 2:
                        asset_name = AM.group_name
                        multi_object = True
                    else:
                        asset_name = OBJ.name
                        if OBJ.modifiers:
                            for mod in context.object.modifiers:
                                if mod.type == 'SUBSURF': 
                                    is_subsurf=True
 
                    if not asset_name + ".png" in thumbnails_list or asset_name + ".png" in thumbnails_list and AM.replace_rename == 'replace':
                        if asset_name + ".png" in thumbnails_list and AM.replace_rename == 'replace':
                            box.label('" ' + asset_name + ' " already exist', icon='ERROR')
                            box.separator()
                            row = box.row(align=True)
                            row.prop(AM, "replace_rename", text=" ", expand=True)
                            if AM.replace_rename == 'rename':
                                if multi_object:
                                    box.prop(AM, "group_name", text="")
                                else:
                                    ob = context.object
                                    box.prop(ob, "name", text="")
                                row = box.row()
 
                        if multi_object:
                            box.label("Choose the asset name")
                            box.prop(AM, "group_name", text="")
                            box.prop(AM, "with_main_parent", text="With main parent")   
                            row = box.row(align=True)
 
 
                        row = box.row(align=True)
                        row.prop(AM, "render_type", text=" ", expand=True)
                        if AM.render_type == 'render':
                            if not multi_object and not is_subsurf:
                                box.prop(AM, "add_subsurf", text="Subsurf")
                                box.prop(AM, "add_smooth", text="Smooth")  
 
                            box.prop(AM, "material_render", text="Addon material") 
 
                        #OpenGL    
                        elif AM.render_type == 'opengl':
                            row = box.row(align=True)
                            row.operator("object.add_cam_ogl_render", text="Add Camera" if not "AM_OGL_Camera" in [obj.name for obj in context.scene.objects] else "View camera", icon='ZOOMIN')
                            row.operator("object.delete_cam_ogl_render", text="", icon='ZOOMOUT')
                            row = layout.column()
                            view = context.space_data
                            scene = context.scene
                            fx_settings = view.fx_settings
                            row = box.row(align=True) 
                            row.label("Background:")
                            row.prop(AM, "background_alpha", text="")
                            row = box.row(align=True)
                            row.prop(view, "show_only_render")
                            row = box.row(align=True)
                            row.prop(view, "use_matcap")
                            if view.use_matcap :
                                row.prop(AM, "matcap_options", text="", icon='TRIA_UP' if AM.matcap_options else 'TRIA_DOWN')    
                                if AM.matcap_options:
                                    row = box.row(align=True)
                                    row.template_icon_view(view, "matcap_icon")
                            row = box.row(align=True)
                            row.prop(fx_settings, "use_ssao", text="Ambient Occlusion")
                            if fx_settings.use_ssao:
                                ssao_settings = fx_settings.ssao
 
                                row.prop(AM, "ao_options", text="", icon='TRIA_UP' if AM.ao_options else 'TRIA_DOWN')    
                                if AM.ao_options:
                                    subcol = box.column(align=True)
                                    subcol.prop(ssao_settings, "factor")
                                    subcol.prop(ssao_settings, "distance_max")
                                    subcol.prop(ssao_settings, "attenuation")
                                    subcol.prop(ssao_settings, "samples")
                                    subcol.prop(ssao_settings, "color")
 
                        elif AM.render_type == 'image':
                            row = box.row(align=True)
                            row.prop(AM, "image_type", text=" ", expand=True)
                            if AM.image_type == 'disk':
                                box.label("Choose your thumbnail")
                                box.prop(AM, "custom_thumbnail_path", text="")
                            else:
                                box.prop_search(AM, "render_name", bpy.data, "images", text="") 
 
                        row = box.row(align=True)
                        if not multi_object:
                            if (not asset_name + ".png" in thumbnails_list or AM.replace_rename == 'replace') and (AM.render_type in ['opengl', 'render'] or AM.render_type == 'image' and (AM.image_type == 'disk' and AM.custom_thumbnail_path or AM.image_type == 'rendered' and AM.render_name)):
                                row.operator("object.add_in_asset_management", text="OK", icon='FILE_TICK') 
                        else:
                            if AM.group_name and (not asset_name + ".png" in thumbnails_list or AM.replace_rename == 'replace') and (AM.render_type in ['opengl', 'render'] or AM.render_type == 'image' and (AM.image_type == 'disk' and AM.custom_thumbnail_path or AM.image_type == 'rendered' and AM.render_name)):
 
                                row.operator("object.add_in_asset_management", text="OK", icon='FILE_TICK') 
                        row.operator("object.cancel_panel_choise", text="Cancel", icon='X')
 
                    else:
                        box.label('" ' + asset_name + ' " already exist', icon='ERROR')
                        box.separator()
                        row = box.row(align=True)
                        row.prop(AM, "replace_rename", text=" ", expand=True)
                        if AM.replace_rename == 'rename':
                            if multi_object:
                                box.prop(AM, "group_name", text="")
                            else:
                                ob = context.object
                                box.prop(ob, "name", text="")
                            row = box.row()
 
                else:   
                    #Show Only Favoris
                    row = layout.row()
                    favorites = icons.get("favorites_asset")
                    no_favorites = icons.get("no_favorites_asset")
                    if favorites_files:
                        row.prop(AM, "favorites_enabled", text="Show Only favorites")
 
                    #Asset Preview  
                    row = layout.row(align=True)  
                    sub = row.row()
                    sub.scale_y = 1.17 
                    sub.template_icon_view(context.window_manager, "AssetM_previews", show_labels=True if addon_prefs.show_labels else False)
 
                    #Add/Remove Objects from library
                    col = row.column(align=True)
                    if context.selected_objects and not AM.render_running:
                        col.prop(AM, "options_enabled", text="", icon='ZOOMIN')
                    col.operator("object.remove_asset_object", text="", icon='ZOOMOUT')
 
                    #Render Thumbnail 
                    if bpy.context.window_manager.asset_m.render_running:
 
                        layout.label("Thumbnail rendering", icon='RENDER_STILL')
 
                        layout.label("Please wait... ")
                        layout.operator("wm.console_toggle", text="Check/Hide Console")
 
                    #Favoris
                    if isdir(join(addon_prefs.asset_M_library_path, AM.libraries, AM.categories, "Favorites")):
                        if favorites_files:
                            if context.window_manager.AssetM_previews.split(".png")[0] in favorites_files:       
                                col.operator("object.remove_from_favorites", text="", icon_value=favorites.icon_id)
                            else:
                                col.operator("object.add_to_favorites", text="", icon_value=no_favorites.icon_id)   
                        else:
                            col.operator("object.add_to_favorites", text="", icon_value=no_favorites.icon_id)
 
                    #Show Name
                    name = icons.get("name_asset")
                    no_name = icons.get("no_name_asset")
 
                    col.prop(AM, "show_name_assets", text="", icon_value=name.icon_id if AM.show_name_assets else no_name.icon_id)
                    if AM.show_name_assets:
                        row = layout.row(align=True)
                        row.label("Name :")
 
                        sub = row.row()
                        sub.scale_x = 2.0
                        sub.label(context.window_manager.AssetM_previews.split("GP_")[-1].split(".png")[0])
 
                    #Name/Rename  
                    rename = icons.get("rename_asset")
                    no_rename = icons.get("no_rename_asset")
 
                    col.prop(AM, "rename_asset", text="", icon_value=rename.icon_id if AM.rename_asset else no_rename.icon_id)
                    if AM.rename_asset:
                        row = layout.row(align=True)
                        row.label("Rename :")
                        row.prop(AM, "new_name", text="")
                        #Check icon List
                        if thumbnails_list:
                            if AM.new_name:
                                if AM.new_name + ".png" in thumbnails_list:
                                    row = layout.row()
                                    row.label('" ' + AM.new_name + ' " already exist', icon='ERROR')
                                else:
                                    row.operator("object.change_name_asset", text="", icon='FILE_TICK') 
 
 
                    #Without Import
                    if AM.without_import:
                        col.prop(AM, "without_import", icon='LOCKED', icon_only=True)
                    else:
                        col.prop(AM, "without_import", icon='UNLOCKED', icon_only=True)
 
                    #AM_tools
                    if AM.tools:
                        col.prop(AM, "tools", text="", icon='TRIA_UP') 
 
                        #Debug Tools
                        layout.prop(AM, "debug_tools", text="Debug tools", icon='TRIA_UP' if AM.debug_tools else 'TRIA_DOWN')
                        if AM.debug_tools:
                            box = layout.box()
                            box.operator("object.debug_preview", text="Debug", icon='FILE_REFRESH')
                            box.operator("wm.console_toggle", text="Check/Hide Console", icon='CONSOLE')
 
                        if context.object is not None and context.selected_objects:
                            #Asset to faces
                            if AM.Link_Scene_Asset_To_Faces:
                                layout.prop(AM, "Link_Scene_Asset_To_Faces", text="Asset To Selection", icon='TRIA_UP') 
 
                                box = layout.box()
                                if len(context.selected_objects) >= 2 and context.object.mode == 'EDIT':
                                    row = box.row(align=True)
                                    row.operator("object.asset_m_add_to_selection", text="Scene Asset To Faces", icon="MOD_MULTIRES")
 
                                #Link Objects
                                if len(context.selected_objects) >= 2 and context.object.mode == 'OBJECT':     
                                    row = box.row(align=True)
                                    row.operator("object.asset_m_link", text = "Link Objects", icon='CONSTRAINT' )
 
                                #Unlink Objects
                                if context.object.mode == 'OBJECT':
                                    row = box.row(align=True)
                                    row.operator("object.asset_m_unlink", text = "Unlink Objects", icon='UNLINKED' )
 
                            else:
                                layout.prop(AM, "Link_Scene_Asset_To_Faces", text="Asset To Selection", icon='TRIA_DOWN')
 
 
                            #Prepare Asset
                            layout.prop(AM, "prepare_asset", text="Setup Asset", icon='TRIA_UP' if AM.prepare_asset else 'TRIA_DOWN')
                            if AM.prepare_asset:
                                box = layout.box()
                                row = box.row(align=True)
                                row.operator("object.prepare_asset", text="Add Cube Parent", icon='MESH_CUBE')
                                row = box.row(align=True)
                                hardops = icons.get("hardops_asset")
                                row.operator("object.prepare_asset_hardops", text="Setup HardOps Asset", icon_value=hardops.icon_id)
 
                        #Prepare OpenGL Render        
                        layout.prop(AM, "prepare_OGL", text="Setup OpenGl Render", icon='TRIA_UP' if AM.prepare_OGL else 'TRIA_DOWN')    
                        if AM.prepare_OGL:    
                            box = layout.box()
                            row = box.row(align=True)
                            row.operator("object.add_cam_ogl_render", text="Add Camera" if not "AM_OGL_Camera" in [obj.name for obj in context.scene.objects] else "View camera", icon='ZOOMIN')
                            row.operator("object.delete_cam_ogl_render", text="", icon='ZOOMOUT')
                            row = layout.column()
                            view = context.space_data
                            scene = context.scene
                            fx_settings = view.fx_settings
                            row = box.row(align=True) 
                            row.label("Background:")
                            row.prop(AM, "background_alpha", text="")
                            row = box.row(align=True)
                            row.prop(view, "show_only_render")
                            row = box.row(align=True)
                            row.prop(view, "use_matcap")
                            if view.use_matcap :
                                row.prop(AM, "matcap_options", text="", icon='TRIA_UP' if AM.matcap_options else 'TRIA_DOWN')    
                                if AM.matcap_options:
                                    row = box.row(align=True)
                                    row.template_icon_view(view, "matcap_icon")
                            row = box.row(align=True)
                            row.prop(fx_settings, "use_ssao", text="Ambient Occlusion")
                            if fx_settings.use_ssao:
                                ssao_settings = fx_settings.ssao
 
                                row.prop(AM, "ao_options", text="", icon='TRIA_UP' if AM.ao_options else 'TRIA_DOWN')    
                                if AM.ao_options:
                                    subcol = box.column(align=True)
                                    subcol.prop(ssao_settings, "factor")
                                    subcol.prop(ssao_settings, "distance_max")
                                    subcol.prop(ssao_settings, "attenuation")
                                    subcol.prop(ssao_settings, "samples")
                                    subcol.prop(ssao_settings, "color")
                    else:
                        col.prop(AM, "tools", text="", icon='TRIA_DOWN')
 
 
        else:
            layout.label("Define the library path", icon='ERROR')
            layout.label("in the addon preferences please.")
            layout.operator("screen.userpref_show", icon='PREFERENCES')

 
class AM_Preview(Operator):
   bl_idname = "view3d.asset_m_pop_up_preview"
   bl_label = "Asset preview"
   
   def execute(self, context):
       return {'FINISHED'}
          
   def invoke(self, context, event):
       dpi_value = bpy.context.user_preferences.system.dpi
       
       return context.window_manager.invoke_props_dialog(self, width=dpi_value*2, height=100)
   
   def draw(self, context):
       layout = self.layout
       AM = context.window_manager.asset_m
       current_dir = os.path.basename(os.path.dirname(os.path.abspath(__file__)))
       user_preferences = bpy.context.user_preferences
       addon_prefs = user_preferences.addons[current_dir].preferences
       icons = load_icons()
       
       
       if isdir(join(addon_prefs.asset_M_library_path, AM.libraries, AM.categories, "icons")):
           thumbnails_list = [f for f in listdir(join(addon_prefs.asset_M_library_path, AM.libraries, AM.categories, "icons")) if f.endswith(".png")]
       if isdir(join(addon_prefs.asset_M_library_path, AM.libraries, AM.categories, "Favorites")):          
           favorites_files = [f.split(".png")[0] for f in listdir(join(addon_prefs.asset_M_library_path, AM.libraries, AM.categories, "Favorites")) if f.endswith(".png")]  
       
       
       layout.prop(AM, "libraries", text="")
       layout.prop(AM, "categories", text="")
       row = layout.row()
       sub = row.row()
       sub.scale_y = 1.2
       sub.template_icon_view(context.window_manager, "AssetM_previews", show_labels=True if addon_prefs.show_labels else False)
       
       #Name
       row = layout.row(align=True)
       row.label("Name:")
        
       sub = row.row()
       sub.scale_x = 2.0
       sub.label(context.window_manager.AssetM_previews.split("GP_")[-1].split(".png")[0])

               
       #Show Only Favorites
       layout.prop(AM, "favorites_enabled", text="Show Favorites")        
       
       if context.object is not None and context.selected_objects:
        
           layout.separator()
           if len(context.selected_objects) >1 and context.object.mode == 'EDIT':
               row = layout.row()
               row.operator("object.asset_m_add_to_selection", text="Asset To Faces", icon="MOD_MULTIRES")
    
           #Link Objects
           if len(context.selected_objects) > 1 and context.object.mode == 'OBJECT':     
               row = layout.split(align=True) 
               row.operator("object.asset_m_link", text = "Link Objects", icon='CONSTRAINT' )
    
           #Unlink Objects
           if context.object.mode == 'OBJECT':
               row = layout.split(align=True)
               row.operator("object.asset_m_unlink", text = "Unlink Objects", icon='UNLINKED' )