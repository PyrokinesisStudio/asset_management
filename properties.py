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
from .categories.utils import enum_blend_library, enum_blend_category
from . preview_utils import update_asset_m_preview
from . operators import background_alpha

class AssetManagementCollectionGroup(bpy.types.PropertyGroup):

#---------------------- LIBRARIES ----------------------  

    libraries = bpy.props.EnumProperty(
        items=enum_blend_library,
        update=update_asset_m_preview 
        )  
    
    change_library_name = bpy.props.StringProperty(
        default=""
        )  
         
    new_library_name = bpy.props.StringProperty(
        default=""
        )
        
    rename_library = bpy.props.BoolProperty(
        default=False,
        description = "Rename the current library"
        )
    
    delete_library_choise = bpy.props.EnumProperty(
        items=(('no', "No", ''),
                ('yes', 'Yes', '')),
                default='no')

#---------------------- CATEGORIES ---------------------- 
    
    categories = bpy.props.EnumProperty(
        items=enum_blend_category,
        update=update_asset_m_preview
        )   
     
    change_category_name = bpy.props.StringProperty(
        default=""
        )  
     
    new_category_name = bpy.props.StringProperty(
        default=""
        )
     
    rename_category = bpy.props.BoolProperty(
        default=False,
        description = "Rename the current category"
        )
     
    delete_category_choise = bpy.props.EnumProperty(
        items=(('no', "No", ''),
                ('yes', 'Yes', '')),
                default='no')
    
    
    options_enabled = bpy.props.BoolProperty(
        default=False,
        description="Add the active object in the asset library"
        )
     
    new_name = bpy.props.StringProperty(
        default=""
        )
    
    replace_rename = bpy.props.EnumProperty(
        items=(('replace', "Update", " Replace the object in Asset management by the active object"),
               ('rename', "Rename", "Change the object's name to add in Asset management")),
               default='rename')
          
    add_subsurf = bpy.props.BoolProperty(
        default=False,
        description="Thumbnail render with subsurf"
        )   
     
    add_smooth = bpy.props.BoolProperty(
        default=False,
        description="Thumbnail render with smooth"
        )
    
    render_running = bpy.props.BoolProperty(
        default=False
        )
    
    favorites_enabled = bpy.props.BoolProperty(
        default=False,
        update=update_asset_m_preview
        )  
    
    without_import = bpy.props.BoolProperty(
        default=False,
        description = "Do not import the Asset into the scene"
        )
  
    rename_asset = bpy.props.BoolProperty(
        default=False,
        description = "Rename the current Asset"
        )

    
    group_name = bpy.props.StringProperty(
        default=""
        )
        
    Link_Scene_Asset_To_Faces = bpy.props.BoolProperty(
        default=False,
        description = "Copy an Asset to a selections of faces and Link/Unlink differents Assets "
        )
    
    show_name_assets = bpy.props.BoolProperty(
        default=False,
        description = "Show the name of the current Asset"
        ) 
    
    show_prefs_cat = bpy.props.BoolProperty(
        default=False,
        description = "Show the preferences of the Category"
        ) 
        
    show_prefs_lib = bpy.props.BoolProperty(
        default=False,
        description = "Show the preferences of the Library"
        ) 
        
    render_list = []  
    group_list = []
    
    material_render = bpy.props.BoolProperty(
        default=True,
        description="Disable to render with the objet materials"
        )
    
    documentation = bpy.props.BoolProperty(
        default=False,
        description="Documentation of the Asset Management Addon"
        )
    
    tools = bpy.props.BoolProperty(
        default=False,
        description="Tools of the Asset Management Addon"
        )
    
    debug_tools = bpy.props.BoolProperty(
        default=False,
        description="Tools To Prepare the Asset"
        )
    
    prepare_asset = bpy.props.BoolProperty(
        default=False,
        description="Tools To Prepare the Asset"
        )
    
    prepare_OGL = bpy.props.BoolProperty(
        default=False,
        description="Tools To Prepare the OpenGL Render"
        )
        
        
    with_main_parent = bpy.props.BoolProperty(
        default=False,
        description="Parent the objects to an Empty"
        )
        
    custom_thumbnail = bpy.props.BoolProperty(
        default=False,
        description="Choose your custom thumbnail"
        )
        
    custom_thumbnail_path = bpy.props.StringProperty(
        default="",
        subtype='FILE_PATH'
        )
        
    render_type = bpy.props.EnumProperty(
        items=(('render', "Render", ""),
              ('opengl', "OpenGL", ""),
              ('image', "Image", "")),
              default='opengl'
              )

    rename_lib = bpy.props.BoolProperty(
        default=False,
        description="Rename the Library"
        )
        
    rename_cat = bpy.props.BoolProperty(
        default=False,
        description="Rename the Category"
        )
        
    background_alpha = bpy.props.EnumProperty(
        items=(('SKY', "SKY", ''),
              ('TRANSPARENT', "TRANSPARENT", '')),
              default='SKY',
              update=background_alpha)
              
    cam_reso_X = bpy.props.IntProperty(
        default=0
        )
        
    cam_reso_Y = bpy.props.IntProperty(
        default=0
        )
    
    ao_options = bpy.props.BoolProperty(
        default=False,
        description="Ambiant Occlusion Options"
        )
    
    matcap_options = bpy.props.BoolProperty(
        default=True,
        description="Matcap Options"
        )
    
    image_type = bpy.props.EnumProperty(
        items=(('disk', "On disk", ''),
            ('rendered', "Rendered", '')),
            default='disk'
            )
    
    render_name = bpy.props.StringProperty()