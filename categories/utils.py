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
from os import listdir
from os.path import join, isdir


def enum_blend_library(self, context):
    current_dir_path = os.path.dirname(os.path.abspath(__file__))
    addon_dir = os.path.basename(os.path.split(current_dir_path)[-2])
    user_preferences = bpy.context.user_preferences
    addon_prefs = user_preferences.addons[addon_dir].preferences 

    libraries = [(lib, lib, '') for lib in os.listdir(addon_prefs.asset_M_library_path) if isdir(join(addon_prefs.asset_M_library_path, lib))]

    return libraries


def enum_blend_category(self, context):
    AM = context.window_manager.asset_m
    current_dir_path = os.path.dirname(os.path.abspath(__file__))
    addon_dir = os.path.basename(os.path.split(current_dir_path)[-2])
    user_preferences = bpy.context.user_preferences
    addon_prefs = user_preferences.addons[addon_dir].preferences 
 
    categories = [(cat, cat, '') for cat in os.listdir(join(addon_prefs.asset_M_library_path, AM.libraries)) if isdir(join(addon_prefs.asset_M_library_path, AM.libraries)) and isdir(join(addon_prefs.asset_M_library_path, AM.libraries, cat))] 

    return categories