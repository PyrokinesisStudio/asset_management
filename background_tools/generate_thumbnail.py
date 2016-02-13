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
import os
from os.path import join, isfile
from os import remove
from mathutils import Vector

if __name__ == '__main__':
    
    current_dir_path = os.path.dirname(os.path.abspath(__file__))
    addon_dir = os.path.basename(os.path.split(current_dir_path)[-2])
    user_preferences = bpy.context.user_preferences
    addon_prefs = user_preferences.addons[addon_dir].preferences 
     
    
    # thumbnails resolution
    if addon_prefs.thumbnails_resolution == '128x128':
        bpy.context.scene.render.resolution_x = 128
        bpy.context.scene.render.resolution_y = 128
    elif addon_prefs.thumbnails_resolution == '256x256':
        bpy.context.scene.render.resolution_x = 256
        bpy.context.scene.render.resolution_y = 256
    
    bpy.context.scene.cycles.samples = addon_prefs.samples_value
    
    # object color
    bpy.data.materials["Color"].node_tree.nodes["Fresnel"].inputs[0].default_value = addon_prefs.obj_fresnel
    bpy.data.materials["Color"].node_tree.nodes["Diffuse BSDF"].inputs[0].default_value = (addon_prefs.obj_color[0], addon_prefs.obj_color[1], addon_prefs.obj_color[2], 1)
    bpy.data.materials["Color"].node_tree.nodes["Diffuse BSDF"].inputs[1].default_value = addon_prefs.obj_color_roughness
    bpy.data.materials["Color"].node_tree.nodes["Glossy BSDF"].inputs[0].default_value = (addon_prefs.obj_glossy_color[0], addon_prefs.obj_glossy_color[1], addon_prefs.obj_glossy_color[2], 1)
    bpy.data.materials["Color"].node_tree.nodes["Glossy BSDF"].inputs[1].default_value = addon_prefs.obj_glossy_color_roughness
    bpy.data.materials["Color"].node_tree.nodes["Mix Shader.001"].inputs[0].default_value = addon_prefs.obj_mix
    bpy.data.materials["Color"].node_tree.nodes["Anisotropic BSDF"].inputs[0].default_value = (addon_prefs.aniso_color[0], addon_prefs.aniso_color[1], addon_prefs.aniso_color[2], 1)
    bpy.data.materials["Color"].node_tree.nodes["Anisotropic BSDF"].inputs[1].default_value = addon_prefs.aniso_roughness
    bpy.data.materials["Color"].node_tree.nodes["Anisotropic BSDF"].inputs[2].default_value = addon_prefs.anisotropy
    
    bpy.data.materials["Color"].node_tree.nodes["Ambient Occlusion"].inputs[0].default_value = (addon_prefs.ao_color[0], addon_prefs.ao_color[1], addon_prefs.ao_color[2], 1)
    bpy.data.materials["Color"].node_tree.nodes["Mix Shader.002"].inputs[0].default_value = addon_prefs.ao_object
    
    # ground color
    bpy.data.materials["ground"].node_tree.nodes["Fresnel"].inputs[0].default_value = addon_prefs.ground_fresnel
    bpy.data.materials["ground"].node_tree.nodes["Diffuse BSDF"].inputs[0].default_value = (addon_prefs.ground_color[0], addon_prefs.ground_color[1], addon_prefs.ground_color[2], 1)
    bpy.data.materials["ground"].node_tree.nodes["Diffuse BSDF"].inputs[1].default_value = addon_prefs.ground_color_roughness
    bpy.data.materials["ground"].node_tree.nodes["Glossy BSDF"].inputs[0].default_value = (addon_prefs.ground_glossy_color[0], addon_prefs.ground_glossy_color[1], addon_prefs.ground_glossy_color[2], 1)
    bpy.data.materials["ground"].node_tree.nodes["Glossy BSDF"].inputs[1].default_value = addon_prefs.ground_glossy_color_roughness
    bpy.data.materials["ground"].node_tree.nodes["Mix Shader.001"].inputs[0].default_value = addon_prefs.opacity
    
    bpy.data.materials["ground"].node_tree.nodes["Ambient Occlusion"].inputs[0].default_value = (addon_prefs.ao_ground_color[0], addon_prefs.ao_ground_color[1], addon_prefs.ao_ground_color[2], 1)
    bpy.data.materials["ground"].node_tree.nodes["Mix Shader.002"].inputs[0].default_value = addon_prefs.ao_ground
    
    # light color
    bpy.data.materials["light"].node_tree.nodes["Emission"].inputs[0].default_value = (addon_prefs.light_color[0], addon_prefs.light_color[1], addon_prefs.light_color[2], 1)
    bpy.data.materials["light"].node_tree.nodes["Emission"].inputs[1].default_value = addon_prefs.light_strength

    
    #Compositing
    bpy.context.scene.node_tree.nodes["Mix.002"].inputs[0].default_value = addon_prefs.ao_mix
    bpy.context.scene.node_tree.nodes["Mix.001"].inputs[0].default_value = addon_prefs.glow
    
    # Render Type
    if addon_prefs.render_type == 'GPU':
        bpy.context.scene.cycles.device = 'GPU'
        bpy.context.scene.render.tile_x = 256
        bpy.context.scene.render.tile_y = 256
                        
    elif addon_prefs.render_type == 'CPU':
        bpy.context.scene.cycles.device = 'CPU'
        bpy.context.scene.render.tile_x = 32
        bpy.context.scene.render.tile_y = 32
        
    
    
    object = sys.argv[5]
    thumbnail_directory = sys.argv[6]
    subsurf = sys.argv[7]
    smooth = sys.argv[8]
    blend_dir = sys.argv[9]
    group = sys.argv[10]
    material = sys.argv[11]
    
    asset_list = []
    particles_list = []
    shape_keys_list = []
    scn = bpy.context.scene
    bpy.context.scene.layers[0] = True
    bpy.context.scene.layers[1] = True
    
    
    def apply_shape_key():
        for asset in bpy.context.selected_objects:
            if (asset.type == 'MESH') and (asset.active_shape_key):
                ob_copy = asset.copy()
                ob_data_copy = asset.data.copy()
                ob_copy.name = asset.name + "_clean"
     
                shape_keys_list.append(ob_copy.name)
     
                bpy.context.scene.objects.link(ob_copy)
                bpy.context.scene.objects.active = asset
     
                bpy.ops.object.shape_key_add(from_mix=True)
                asset.active_shape_key.value =1.0
                asset.active_shape_key.name = "All shape"
     
                i = asset.active_shape_key_index
                for n in range(1,i):

                    asset.active_shape_key_index = 1
                    bpy.ops.object.shape_key_remove()

                bpy.ops.object.shape_key_remove()   
                bpy.ops.object.shape_key_remove()


    def create_bounding_box(item):   
        verts_coord = []
        if group:
            bbox_list = [obj for obj in asset_list if obj not in [item.split("_clean")[0] for item in shape_keys_list]] + shape_keys_list + particles_list
        else:
            bbox_list = [obj for obj in [item] if obj not in [item.split("_clean")[0] for item in shape_keys_list]] + shape_keys_list + particles_list
        
     
        for obj in bbox_list:
            OBJ = bpy.data.objects[obj]
            if OBJ.type == 'MESH':
                if OBJ.hide_select or OBJ.hide_render:
                    pass
                else:
                    for vert in OBJ.data.vertices:
                        verts_coord.append(OBJ.matrix_world * Vector(vert.co))

 
        max_x = max([vert[0] for vert in verts_coord])
        min_x = min([vert[0] for vert in verts_coord])
     
        max_y = max([vert[1] for vert in verts_coord])
        min_y = min([vert[1] for vert in verts_coord])
     
        max_z = max([vert[2] for vert in verts_coord])
        min_z = min([vert[2] for vert in verts_coord])
     
        del(verts_coord[:]) 
     
        dimX = max_x - min_x
        dimY = max_y - min_y
        dimZ = max_z - min_z
     
        loc = Vector(((min_x + dimX/2), (min_y + dimY/2), (min_z + dimZ/2)))
     
     
        verts = [(-dimX/2, -dimY/2, -dimZ/2),
                (-dimX/2, -dimY/2, dimZ/2),
                (-dimX/2, dimY/2, -dimZ/2),
                (-dimX/2, dimY/2, dimZ/2),
                (dimX/2, -dimY/2, -dimZ/2),
                (dimX/2, -dimY/2, dimZ/2),
                (dimX/2, dimY/2, -dimZ/2),
                (dimX/2, dimY/2, dimZ/2),
                ]
     
        edges = [(0, 1), (1, 3),
                (3, 2), (2, 0),
                (0, 4), (1, 5),
                (3, 7), (2, 6),
                (4, 5), (5, 7),
                (7, 6), (6, 4)
                ]
     
        faces = []
     
        myMesh = bpy.data.meshes.new("bbox")
     
        BBOX = bpy.data.objects.new("bbox", myMesh)
     
        BBOX.location = loc
        bpy.context.scene.objects.link(BBOX)
        myMesh.from_pydata(verts, edges, [])
        myMesh.update(calc_edges=True)
        bpy.ops.object.select_all(action='DESELECT')
        BBOX.hide_render = True
        BBOX.select = True
        bpy.context.scene.objects.active = BBOX
        if group:
            for obj in asset_list:
                OBJ = bpy.data.objects[obj]
                if OBJ.hide_select:
                    pass
                
                if OBJ.hide:
                    OBJ.hide_render=True

                if not OBJ.parent:
                    OBJ.select=True
                    bpy.ops.object.parent_set(type='OBJECT', keep_transform=True)
                    OBJ.select=False
                
        else:
            bpy.data.objects[item].select=True
            bpy.ops.object.parent_set(type='OBJECT', keep_transform=True)
            bpy.data.objects[item].select=False
 
        if particles_list or shape_keys_list:
            for item in particles_list + shape_keys_list:
                bpy.data.objects[item].hide_render=True
                bpy.data.objects[item].hide=True
        
        del(particles_list[:])
        del(shape_keys_list[:])
            
                
    def generate(name):
        scene_obj = ["ThumbNailer_SCENE", "ThumbNailer_Cameras", "ThumbNailer_Camera", "ThumbNailer_Camera_Circle", "ThumbNailer_Light", "ThumbNailer_ground"]
        
        BBOX = bpy.context.active_object
         
        bpy.ops.object.transform_apply(location=False, rotation=True, scale=True)
         
        # Determine OBJ dimensions
        maxDimension = 1.0
        scaleFactor = maxDimension / max(BBOX.dimensions)
         
        # Scale uniformly
        BBOX.scale = (scaleFactor,scaleFactor,scaleFactor)
         
        # Center pivot
        bpy.ops.object.origin_set(type='GEOMETRY_ORIGIN', center='BOUNDS')
         
        # Move object to origin
        bpy.ops.object.location_clear()
         
        # Move mesh up by half of Z dimension
        dimX = BBOX.dimensions[0]/2
        dimY = BBOX.dimensions[1]/2
        dimZ = BBOX.dimensions[2]/2
        BBOX.location = (0,0,dimZ)
         
        # Manual adjustments to CAMERAS
        CAMERAS = bpy.data.objects["ThumbNailer_Cameras"]
        scalevalue = 1
        camScale = 0.5+(dimX*scalevalue+dimY*scalevalue+dimZ*scalevalue)/3
        CAMERAS.scale = (camScale,camScale,camScale)
        CAMERAS.location = (0,0,dimZ)
         
        # Make smooth, add SubSurf modifier and increase subdivisions
        if not group:
            bpy.ops.object.select_all(action='DESELECT')
            OBJ = bpy.data.objects[name]
            bpy.context.scene.objects.active = OBJ
            OBJ.select=True
            if smooth:
                bpy.ops.object.shade_smooth()

            if subsurf:
                if OBJ.modifiers:
                    for mod in OBJ.modifiers:
                        if mod.type != "SUBSURF":
                            bpy.context.scene.objects.active = OBJ
                            bpy.ops.object.modifier_add(type='SUBSURF')
                            bpy.context.object.modifiers["Subsurf"].levels = 2
                        else:
                            bpy.context.object.modifiers["Subsurf"].levels = 2
                else:
                    bpy.ops.object.modifier_add(type='SUBSURF')
                    OBJ.modifiers["Subsurf"].levels = 2
        
        if not material:
            if group:
                for obj in asset_list:
                    OBJ = bpy.data.objects[obj]
                    if OBJ.material_slots:
                        if OBJ.hide_select:
                            OBJ.hide_select=False
                        bpy.context.scene.objects.active = OBJ
                        for slots in OBJ.material_slots:
                            bpy.ops.object.material_slot_remove()
                    OBJ.active_material = bpy.data.materials["Color"]
            else:
                OBJ = bpy.data.objects[name]
                if OBJ.material_slots:
                    bpy.context.scene.objects.active = OBJ
                    for slots in OBJ.material_slots:
                        bpy.ops.object.material_slot_remove()
                OBJ.active_material = bpy.data.materials["Color"]
        
        #Freestyle contour
        if addon_prefs.freestyle_on_off == True:
            bpy.context.scene.render.use_freestyle = True

    
        elif addon_prefs.freestyle_on_off == False: 
            bpy.context.scene.render.use_freestyle = False 
            bpy.context.scene.render.layers["Freestyle"].use = False
            bpy.data.objects["ThumbNailer_ground"].layers = [layer==1 for layer in range(20)]
            bpy.data.objects["ThumbNailer_Light"].layers = [layer==1 for layer in range(20)]
           
            bpy.context.scene.render.layers["Floor"].use = False


        bpy.data.linestyles["LineStyle.001"].thickness = addon_prefs.contour_size
        bpy.data.linestyles["LineStyle.001"].color = addon_prefs.contour_color
        bpy.data.linestyles["LineStyle.001"].alpha = addon_prefs.contour_opacity
        
                
        bpy.ops.render.render()
        
        if group:
            bpy.data.images['Render Result'].save_render(filepath=join(thumbnail_directory, group + '.png'))
        else:
            bpy.data.images['Render Result'].save_render(filepath=join(thumbnail_directory, name + '.png'))

        for obj in bpy.context.scene.objects:
            if obj.name not in scene_obj:
                obj.select=True
                bpy.ops.object.delete()
        

    if group:
        bpy.ops.object.select_all(action='DESELECT')
        with bpy.data.libraries.load(join(blend_dir, group + ".blend")) as (data_from, data_to):
            data_to.objects = data_from.objects
     
     
        for obj in data_to.objects:
            if obj is not None:
                scn.objects.link(obj)
                obj.select=True
                asset_list.append(obj.name)
        
        apply_shape_key()
        bpy.ops.object.make_single_user(type='SELECTED_OBJECTS', object=False, obdata=True, material=False, texture=False, animation=False)
        bpy.ops.object.select_all(action='DESELECT') 

        for asset in asset_list:
            OBJ = bpy.data.objects[asset]
            if OBJ.hide:
                pass
            else:
                if OBJ.type == 'MESH':
                    if OBJ.modifiers:
                        bpy.context.scene.objects.active = OBJ
                        for mod in OBJ.modifiers:
                            if mod.type == 'PARTICLE_SYSTEM':
                                mod.show_viewport=True
                                particles = mod.particle_system
                                if particles.settings.render_type == 'PATH':
                                    bpy.ops.object.modifier_convert(modifier=mod.name)
                                    bpy.context.active_object.name = mod.name
                                    particles_list.append(mod.name)
                                    bpy.ops.object.select_all(action='DESELECT')
                                    bpy.context.scene.objects.active = OBJ
         
                                else:
                                    bpy.ops.object.select_all(action='DESELECT')
                                    if particles.settings.render_type == 'GROUP':
                                        bpy.ops.object.select_same_group(group=particles.settings.dupli_group.name)
                                        obj_dupli = bpy.context.selected_objects
                                        for obj in obj_dupli:
                                            obj.layers = [idx==4 for idx in range(20)]
                                            obj.select=False

                                    elif particles.settings.render_type == 'OBJECT':
                                        obj_dupli = particles.settings.dupli_object
                                        obj_dupli.layers = [idx==4 for idx in range(20)]
         
                                    OBJ.select=True
                                    bpy.ops.object.duplicates_make_real()
                                    bpy.ops.object.make_single_user(type='SELECTED_OBJECTS', object=False, obdata=True, material=False, texture=False, animation=False)
                                    bpy.context.scene.objects.active = bpy.context.selected_objects[0]
                                    OBJ.select = False
                                    
                                    bpy.ops.object.join()
                                           
                                    particles_list.append(bpy.context.active_object.name)
                                    dupli_obj = [obj for obj in bpy.context.scene.objects if obj.layers[4]]
                                    for obj in dupli_obj:
                                        if obj.parent:
                                            bpy.context.scene.layers[4]=True
                                            obj.select=True
                                            bpy.ops.object.parent_clear(type='CLEAR')
                                            bpy.context.scene.layers[4]=False
                                        obj.hide_select=True
         
                            if mod.type in ['ARRAY', 'CURVE', 'MIRROR']:
                                bpy.ops.object.modifier_apply(modifier = mod.name)
                
                elif OBJ.type == 'CURVE':
                    bpy.context.scene.objects.active = OBJ
                    CURVE = bpy.context.active_object
                    if CURVE.data.bevel_depth or CURVE.data.bevel_object or CURVE.data.extrude:
                        CURVE.select=True
                        bpy.ops.object.convert(target='MESH')
                
        create_bounding_box(group)
        generate(group)
        
        if isfile(join(thumbnail_directory, "rendering.txt")):
            remove(join(thumbnail_directory, "rendering.txt")) 
        
        bpy.ops.wm.quit_blender()
        

     
    else:
        bpy.ops.object.select_all(action='DESELECT')

        with bpy.data.libraries.load(join(blend_dir, object + ".blend")) as (data_from, data_to):
            data_to.objects = data_from.objects
           
        for OBJ in data_to.objects:
            if OBJ is not None:
                scn.objects.link(OBJ)
                OBJ.select=True
                
                apply_shape_key() 
                
                if OBJ.type == 'MESH':
                    if OBJ.modifiers:
                        bpy.context.scene.objects.active = OBJ
                        for mod in OBJ.modifiers:
                            if mod.type == 'PARTICLE_SYSTEM':
                                mod.show_viewport=True
                                particles = mod.particle_system
                                if particles.settings.render_type == 'PATH':
                                    bpy.ops.object.modifier_convert(modifier=mod.name)
                                    bpy.context.active_object.name = mod.name
                                    particles_list.append(mod.name)
                                    bpy.ops.object.select_all(action='DESELECT')
                                    bpy.context.scene.objects.active = OBJ
                            if mod.type == 'MIRROR':
                                bpy.ops.object.modifier_apply(modifier = mod.name)
                
                elif OBJ.type == 'CURVE':
                    bpy.context.scene.objects.active = OBJ
                    CURVE = bpy.context.active_object
                    if CURVE.data.bevel_depth or CURVE.data.bevel_object or CURVE.data.extrude:
                        CURVE.select=True
                        bpy.ops.object.convert(target='MESH')
                                        
                create_bounding_box(object)
                generate(object)
                
                if isfile(join(thumbnail_directory, "rendering.txt")):
                    remove(join(thumbnail_directory, "rendering.txt")) 

                bpy.ops.wm.quit_blender()