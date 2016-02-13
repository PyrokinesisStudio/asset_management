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
from bpy.props import (StringProperty,
                       BoolProperty,
                       EnumProperty,
                       IntProperty)
from .categories.utils import enum_blend_library, enum_blend_category
from . preview_utils import update_asset_m_preview
from . operators import background_alpha


class AssetManagementCollectionGroup(bpy.types.PropertyGroup):
 
# -----------------------------------------------------------------------------
#   LIBRARY PROPERTIES
# -----------------------------------------------------------------------------

    libraries = EnumProperty(
        items=enum_blend_library,
        update=update_asset_m_preview 
        ) 
    
    rename_lib = BoolProperty(
        default=False,
        description="Rename the Library"
        )

    show_prefs_lib = BoolProperty(
        default=False,
        description = "Show the preferences of the Library"
        )
    
    new_library_name = StringProperty(
        default=""
        )
    
    delete_library_choise = EnumProperty(
        items=(('no', "No", ''),
            ('yes', 'Yes', '')),
            default='no'
            )
    
    rename_library = BoolProperty(
        default=False,
        description = "Rename the current library"
        )
            
    change_library_name = StringProperty(
        default=""
        )  

# -----------------------------------------------------------------------------
#   CATEGORY PROPERTIES
# -----------------------------------------------------------------------------
    
    categories = EnumProperty(
        items=enum_blend_category,
        update=update_asset_m_preview
        ) 
    
    rename_cat = BoolProperty(
        default=False,
        description="Rename the Category"
        )
        
    show_prefs_cat = BoolProperty(
        default=False,
        description = "Show the preferences of the Category"
        ) 
        
    new_category_name = StringProperty(
        default=""
        )
     
    delete_category_choise = EnumProperty(
        items=(('no', "No", ''),
              ('yes', 'Yes', '')),
              default='no'
              )
    
    rename_category = BoolProperty(
        default=False,
        description = "Rename the current category"
        )
    
    change_category_name = StringProperty(
        default=""
        )  

# -----------------------------------------------------------------------------
#   ADDING OPTIONS PROPERTIES
# -----------------------------------------------------------------------------
    
    options_enabled = BoolProperty(
        default=False,
        description="Add the active object in the asset library"
        )
    
    render_type = EnumProperty(
        items=(('render', "Render", ""),
              ('opengl', "OpenGL", ""),
              ('image', "Image", "")),
              default='opengl'
              )
    
    replace_rename = EnumProperty(
        items=(('replace', "Update", " Replace the object in Asset management by the active object"),
              ('rename', "Rename", "Change the object's name to add in Asset management")),
              default='rename'
              )
    
    group_name = StringProperty(
        default=""
        )
    
    with_main_parent = BoolProperty(
        default=False,
        description="Parent the objects to an Empty"
        )
    
    # ---------------- #          
    #   RENDER MODE    #
    # ---------------- #
    
    add_subsurf = BoolProperty(
        default=False,
        description="Thumbnail render with subsurf"
        )   
     
    add_smooth = BoolProperty(
        default=False,
        description="Thumbnail render with smooth"
        )
    
    material_render = BoolProperty(
        default=True,
        description="Disable to render with the objet materials"
        )
    
    # ---------------- #          
    #   OPENGL MODE    #
    # ---------------- #
    
    background_alpha = EnumProperty(
        items=(('SKY', "SKY", ''),
              ('TRANSPARENT', "TRANSPARENT", '')),
              default='SKY',
              update=background_alpha
              )
    
    matcap_options = BoolProperty(
        default=True,
        description="Matcap Options"
        )
    
    ao_options = BoolProperty(
        default=False,
        description="Ambiant Occlusion Options"
        )    
    
    # ---------------- #          
    #   IMAGES MODE    #
    # ---------------- #
    
    image_type = EnumProperty(
        items=(('disk', "On disk", ''),
              ('rendered', "Rendered", '')),
              default='disk'
              )

    custom_thumbnail_path = StringProperty(
        default="",
        subtype='FILE_PATH'
        )
    
    custom_thumbnail = BoolProperty(
        default=False,
        description="Choose your custom thumbnail"
        )
     
    render_name = StringProperty(
        default=""
        )
    
# -----------------------------------------------------------------------------
#   PANEL OPTIONS PROPERTIES
# -----------------------------------------------------------------------------
    
    favorites_enabled = BoolProperty(
        default=False,
        update=update_asset_m_preview
        )  
        
    rename_asset = BoolProperty(
        default=False,
        description = "Rename the current Asset"
        )
    
    new_name = StringProperty(
        default=""
        )
    
    without_import = BoolProperty(
        default=False,
        description = "Do not import the Asset into the scene"
        )
    
    tools = BoolProperty(
        default=False,
        description="Tools of the Asset Management Addon"
        )
        
    debug_tools = BoolProperty(
        default=False,
        description="Tools To Prepare the Asset"
        )
    
    Link_Scene_Asset_To_Faces = BoolProperty(
        default=False,
        description = "Copy an Asset to a selections of faces and Link/Unlink differents Assets "
        )
    
    prepare_asset = BoolProperty(
        default=False,
        description="Tools To Prepare the Asset"
        )
        
    prepare_OGL = BoolProperty(
        default=False,
        description="Tools To Prepare the OpenGL Render"
        )
    

# -----------------------------------------------------------------------------
#   POPUP MENU PROPERTIES
# -----------------------------------------------------------------------------


    active_layer = BoolProperty(
        default=True,
        description="Import the asset in active layer"
        )
    
    existing_material = BoolProperty(
        default=True,
        description="Use the existing materials if they ever in the datas"
        )
    
    existing_group = BoolProperty(
        default=True,
        description="Use the existing groups if they ever in the datas"
        )
    
    show_name_assets = BoolProperty(
        default=False,
        description = "Show the name of the current Asset"
        )
        
    show_labels = BoolProperty(
            default=True,
            description="Display name asset in the preview"
            )  
     

# -----------------------------------------------------------------------------
#   OPERATORS PROPERTIES
# -----------------------------------------------------------------------------

    
    render_running = BoolProperty(
        default=False
        )

    render_list = []  
    group_list = []

    cam_reso_X = IntProperty(
        default=0
        )
        
    cam_reso_Y = IntProperty(
        default=0
        )
 
#    documentation = BoolProperty(
#        default=False,
#        description="Documentation of the Asset Management Addon"
#        )