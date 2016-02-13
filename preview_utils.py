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
import bpy.utils.previews
from bpy.types import WindowManager
from bpy.props import EnumProperty
from os import listdir
from os.path import join, isdir
from . import_utils import run_preview_add_to_selection
 
 
AssetM_preview_collections = {}


def update_asset_m_preview(self, context):
    register_AssetM_pcoll_preview()
     
 
def enum_previews_from_directory_items(self, context):
    AM = context.window_manager.asset_m
    enum_items = []
 
    if bpy.context is None:
        return enum_items
    current_dir = os.path.basename(os.path.dirname(os.path.abspath(__file__)))
    user_preferences = bpy.context.user_preferences
    addon_prefs = user_preferences.addons[current_dir].preferences 
    
    if isdir(join(addon_prefs.asset_M_library_path, AM.libraries, AM.categories, "Favorites")):          
        favorites_files = [f.split(".png")[0] for f in listdir(join(addon_prefs.asset_M_library_path, AM.libraries, AM.categories, "Favorites")) if f.endswith(".png")]  
    
    if favorites_files and AM.favorites_enabled: 
        directory = join(addon_prefs.asset_M_library_path, AM.libraries, AM.categories, "Favorites")
    else:
        directory = join(addon_prefs.asset_M_library_path, AM.libraries, AM.categories, "icons")
 
    # Get the preview collection (defined in register func).
    pcoll = AssetM_preview_collections["main"]
 
    if directory == pcoll.AssetM_previews_dir:
        return pcoll.AssetM_previews
 
    if directory and os.path.exists(directory):
        # Scan the directory for jpg files
        image_paths = []
        for fn in os.listdir(directory):
            if fn.lower().endswith(".png"):
                image_paths.append(fn)
 
        for i, name in enumerate(image_paths):
            # generates a thumbnail preview for a file.
            filepath = os.path.join(directory, name)
            thumb = pcoll.load(filepath, filepath, 'IMAGE')
            enum_items.append((name, name.split(".png")[0], name, thumb.icon_id, i))
 
    pcoll.AssetM_previews = enum_items
    pcoll.AssetM_previews_dir = directory
    
    return pcoll.AssetM_previews
 
 
def register_AssetM_pcoll_preview():
    wm = bpy.context.window_manager
 
    global AssetM_preview_collections
    for pcoll in AssetM_preview_collections.values():
        bpy.utils.previews.remove(pcoll)
 
    WindowManager.AssetM_previews = EnumProperty(
            items=enum_previews_from_directory_items,
            update=run_preview_add_to_selection
            )  
 
    pcoll = bpy.utils.previews.new() # pcoll pour preview collection
    pcoll.AssetM_previews_dir = ""
    pcoll.AssetM_previews = ()
 
    AssetM_preview_collections = {}
    AssetM_preview_collections["main"] = pcoll
 
 
def unregister_AssetM_pcoll_preview():
 
    del WindowManager.AssetM_previews
 
    for pcoll in AssetM_preview_collections.values():
        bpy.utils.previews.remove(pcoll)
    AssetM_preview_collections.clear()