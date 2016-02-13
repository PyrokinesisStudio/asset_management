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
from bpy.types import Operator
from os.path import join, isfile, isdir
from os import remove, listdir
#from . utils import enum_blend_library, enum_blend_category
#from ..preview_utils import register_AssetM_pcoll_preview
 
 
#---------------------- LIBRARIES ---------------------- 
 
class AddAssetLibrary(Operator):
    ''' Add a new library in the Asset management library '''
    bl_idname = "object.add_asset_m_library"
    bl_label = "Add new library"
 
    def execute(self, context):
        AM = context.window_manager.asset_m
        current_dir_path = os.path.dirname(os.path.abspath(__file__))
        addon_dir = os.path.basename(os.path.split(current_dir_path)[-2])
        user_preferences = bpy.context.user_preferences
        addon_prefs = user_preferences.addons[addon_dir].preferences 
 
        # recuperation des librairies dans le dossier de librairie
        self.libraries = [lib for lib in os.listdir(addon_prefs.asset_M_library_path) if isdir(addon_prefs.asset_M_library_path)]
 
        # relance le popup si le nom donne a la librairie existe deja ou si aucun non n'est donner lors de la validation
        if AM.new_library_name in self.libraries or not AM.new_library_name:
            bpy.ops.object.add_asset_m_library('INVOKE_DEFAULT')
 
        else:
            os.makedirs(join(addon_prefs.asset_M_library_path, AM.new_library_name)) # creer le dossier librairie
 
        return {'FINISHED'}
 
    def invoke(self, context, event):
        AM = context.window_manager.asset_m
        AM.new_library_name = ""
        dpi_value = bpy.context.user_preferences.system.dpi
 
        return context.window_manager.invoke_props_dialog(self, width=dpi_value*3, height=100)
 
 
    def draw(self, context):
        layout = self.layout
        AM = context.window_manager.asset_m
 
        layout.label("Choose your library name:")
        layout.prop(AM, "new_library_name", text = "Name")
 
 
class RemoveAssetLibrary(Operator):
    ''' Remove the library from your Asset management library '''
    bl_idname = "object.remove_asset_m_library"
    bl_label = "Remove library"
 
    def execute(self, context):
        AM = context.window_manager.asset_m
        current_dir_path = os.path.dirname(os.path.abspath(__file__))
        addon_dir = os.path.basename(os.path.split(current_dir_path)[-2])
        user_preferences = bpy.context.user_preferences
        addon_prefs = user_preferences.addons[addon_dir].preferences 
        
        if AM.delete_library_choise == 'yes':
            shutil.rmtree(join(addon_prefs.asset_M_library_path, AM.libraries))
 
            return {'FINISHED'}
 
        else:
            return {'FINISHED'}       
 
    def invoke(self, context, event):
        AM = context.window_manager.asset_m
        AM.delete_library_choise = 'no'
        dpi_value = bpy.context.user_preferences.system.dpi
 
        return context.window_manager.invoke_props_dialog(self, width=dpi_value*3, height=100)
 
    def draw(self, context):
        layout = self.layout
        AM = context.window_manager.asset_m
 
        layout.label('Delete library " ' + AM.libraries + ' ".', icon='ERROR')
        layout.label("    All the categories will be deleted")
        layout.label('    Are you sure ?')
        row = layout.row(align=True)
        row.prop(AM, "delete_library_choise", expand=True)
 
 
 
class RenameLibrary(Operator):
    ''' Rename the current library '''
    bl_idname = "object.asset_m_rename_library"
    bl_label = "Rename library"
 
    def execute(self, context):
        AM = context.window_manager.asset_m
        current_dir_path = os.path.dirname(os.path.abspath(__file__))
        addon_dir = os.path.basename(os.path.split(current_dir_path)[-2])
        user_preferences = bpy.context.user_preferences
        addon_prefs = user_preferences.addons[addon_dir].preferences 
 
        os.rename(join(addon_prefs.asset_M_library_path, AM.libraries), join(addon_prefs.asset_M_library_path, AM.change_library_name)) 

        AM.change_library_name = ""
        AM.rename_library = False
 
        return {'FINISHED'}

#---------------------- CATEGORIES ---------------------- 

class AddAssetCategory(Operator):
    ''' Add a new category in the Asset management library '''
    bl_idname = "object.add_asset_m_category"
    bl_label = "Add new category"
 
    def execute(self, context):
        AM = context.window_manager.asset_m
        current_dir_path = os.path.dirname(os.path.abspath(__file__))
        addon_dir = os.path.basename(os.path.split(current_dir_path)[-2])
        user_preferences = bpy.context.user_preferences
        addon_prefs = user_preferences.addons[addon_dir].preferences 
        
        # recuperation des categories dans le dossier de librairie
        self.categories = [cat for cat in os.listdir(join(addon_prefs.asset_M_library_path, AM.libraries)) if isdir(join(addon_prefs.asset_M_library_path, AM.libraries))]
        
        # relance le popup si le nom donne a la categorie existe deja ou si aucun non n'est donner lors de la validation
        if AM.new_category_name in self.categories or not AM.new_category_name:
            bpy.ops.object.add_asset_m_category('INVOKE_DEFAULT')
            
        else:
            addon_path =  current_dir_path.split("categories")[0]
            source_file = join(addon_path, "blend_tools", "base_library")
            shutil.copytree(source_file, join(addon_prefs.asset_M_library_path, AM.libraries, AM.new_category_name)) # copie et renomme le dossier "base_library"

        return {'FINISHED'}
    
    def invoke(self, context, event):
        AM = context.window_manager.asset_m
        AM.new_category_name = ""
        dpi_value = bpy.context.user_preferences.system.dpi
        
        return context.window_manager.invoke_props_dialog(self, width=dpi_value*3, height=100)
        
    
    def draw(self, context):
        layout = self.layout
        AM = context.window_manager.asset_m
        
        layout.label("Choose your category name:")
        layout.prop(AM, "new_category_name", text = "Name")


class RemoveAssetCategory(Operator):
    ''' Remove the category from your Asset management library '''
    bl_idname = "object.remove_asset_m_category"
    bl_label = "Remove category"
    
    def execute(self, context):
        AM = context.window_manager.asset_m
        current_dir_path = os.path.dirname(os.path.abspath(__file__))
        addon_dir = os.path.basename(os.path.split(current_dir_path)[-2])
        user_preferences = bpy.context.user_preferences
        addon_prefs = user_preferences.addons[addon_dir].preferences 
        
        if AM.delete_category_choise == 'yes':
            shutil.rmtree(join(addon_prefs.asset_M_library_path, AM.libraries, AM.categories))

            return {'FINISHED'}
            
        else:
            return {'FINISHED'}       
    
    def invoke(self, context, event):
        AM = context.window_manager.asset_m
        AM.delete_category_choise = 'no'
        dpi_value = bpy.context.user_preferences.system.dpi
        
        return context.window_manager.invoke_props_dialog(self, width=dpi_value*3, height=100)
    
    def draw(self, context):
        layout = self.layout
        AM = context.window_manager.asset_m
        
        layout.label('Delete category " ' + AM.categories + ' ".', icon='ERROR')
        layout.label("    All the assets will be deleted")
        layout.label('    Are you sure ?')
        row = layout.row(align=True)
        row.prop(AM, "delete_category_choise", expand=True)



class RenameCategories(Operator):
    ''' Rename the current category '''
    bl_idname = "object.asset_m_rename_category"
    bl_label = "Rename categorie"
    
    def execute(self, context):
        AM = context.window_manager.asset_m
        current_dir_path = os.path.dirname(os.path.abspath(__file__))
        addon_dir = os.path.basename(os.path.split(current_dir_path)[-2])
        user_preferences = bpy.context.user_preferences
        addon_prefs = user_preferences.addons[addon_dir].preferences 
        
        os.rename(join(addon_prefs.asset_M_library_path, AM.libraries, AM.categories), join(addon_prefs.asset_M_library_path, AM.libraries, AM.change_category_name)) 
             
        AM.change_category_name = ""
        AM.rename_category = False
        
        return {'FINISHED'}
