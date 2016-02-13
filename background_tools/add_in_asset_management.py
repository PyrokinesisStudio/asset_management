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
import sys
from os import remove
from os.path import join

if __name__ == '__main__':
    blendfile = sys.argv[5] # get the directory to the object to add
    Asset_library = sys.argv[6]
    object = sys.argv[7] # get the object's name
    group_list = sys.argv[8]
    group_name = sys.argv[9]
    parent = sys.argv[10]
    assets = object.split(";")
   
    scn = bpy.context.scene 

    with bpy.data.libraries.load(blendfile) as (data_from, data_to):
        data_to.objects = [obj for obj in data_from.objects if obj in assets]
        if group_list:
            groups = group_list.split(";")
            data_to.groups = [gp for gp in data_from.groups if gp in groups]
    
    if data_to.objects: # test if objects exist in the source file
        layer_obj = [(obj, layer) for obj in data_from.objects for layer in range(0, 20) if obj in assets and bpy.data.objects[obj].layers[layer]]
     
        for item in layer_obj:
            scn.objects.link(bpy.data.objects[item[0]])
            bpy.data.objects[item[0]].layers = [idx == item[1] for idx in range(20)]
            bpy.data.objects[item[0]].select=True
        
        selection = [obj for obj in bpy.context.scene.objects if obj.select]        
        if len(selection) >= 2  and parent:
            bpy.ops.mesh.primitive_plane_add(radius=2)
            main = bpy.context.active_object
            main.name = group_name
            main.draw_type = 'WIRE'
            main.hide_render = True
            main.cycles_visibility.camera = False
            main.cycles_visibility.diffuse = False
            main.cycles_visibility.glossy = False
            main.cycles_visibility.transmission = False
            main.cycles_visibility.scatter = False
            main.cycles_visibility.shadow = False
            
            for obj in selection:
                if not obj.parent:
                    obj.parent = main
                      
        bpy.ops.wm.save_as_mainfile(filepath=Asset_library, copy=True)
        bpy.ops.wm.quit_blender()
        
    else:
        bpy.ops.wm.quit_blender()