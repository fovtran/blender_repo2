#!/usr/bin/Python -v
# -*- encoding: utf-8 -*-
# blender.exe --background --python cycles_render_by_uuid.py -- <UUID>
#
__author__ = 'dmc <dcadogan@live.com.ar>'
__version__ = '0.1.0'
__licence__ = 'GPL'

import bpy, sys, os
import time
import json

def writeJobData(uuid):
    config = {}
    config['output-uuid'] = uuid
    config['samples'] = 20
    config['volume_step_size'] = 0.2
    config['sample_clamp_direct'] = 9
    config['sample_clamp_indirect'] = 9
    config['caustics_reflective'] = False
    config['max_bounces'] = 128
    config['transparent_max_bounces'] = 128
    config['diffuse_bounces'] = 3
    config['glossy_bounces'] = 3
    config['volume_bounces'] = 3
    config['transmission_bounces'] = 128
    config['shading_system']= False
    config['debug_use_spatial_splits'] = False
    config['use_persistent_data'] = False
    config['file_format'] = 'JPEG'
    
    with open(uuid + '.json', 'w') as f:
        json.dump(config, f)
                
def readJobData(uuid):
    with open(uuid + '.json', 'r') as f:
        config = json.load(f)
    return config

uuid = sys.argv[-1]
job_settings = readJobData(uuid)
imagePath=job_settings['output-uuid']
current_dir = os.path.dirname(os.path.abspath(__file__)) 

if os.path.exists(current_dir):
    # Render Context
    bpy.context.scene.cycles.samples = int(job_settings['samples'])
    bpy.context.scene.cycles.volume_step_size = int(job_settings['volume_step_size'])
    bpy.context.scene.cycles.sample_clamp_direct = int(job_settings['sample_clamp_direct'])
    bpy.context.scene.cycles.sample_clamp_indirect = int(job_settings['sample_clamp_indirect'])
    bpy.context.scene.cycles.caustics_reflective = bool(job_settings['caustics_reflective'])
    bpy.context.scene.cycles.max_bounces = int(job_settings['max_bounces'])
    bpy.context.scene.cycles.transparent_max_bounces = int(job_settings['transparent_max_bounces'])
    bpy.context.scene.cycles.diffuse_bounces = int(job_settings['diffuse_bounces'])
    bpy.context.scene.cycles.glossy_bounces = int(job_settings['glossy_bounces'])
    bpy.context.scene.cycles.volume_bounces = int(job_settings['volume_bounces'])
    bpy.context.scene.cycles.transmission_bounces = int(job_settings['transmission_bounces'])
    bpy.context.scene.cycles.shading_system = bool(job_settings['shading_system'])
    bpy.context.scene.cycles.debug_use_spatial_splits = bool(job_settings['debug_use_spatial_splits'])
    bpy.context.scene.render.use_persistent_data = int(job_settings['use_persistent_data'])
    # Set render resolution
    #scene = bpy.data.scenes["Scene"]
    #scene.render.resolution_x = 480
    #scene.render.resolution_y = 359
    
    #bpy.ops.script.python_file_run(filepath="E:\\BIN\\blender\\blender-2.75a-windows64\\2.75\\scripts\\presets\\render\\DVCPRO_HD_1080p.py")
    #bpy.ops.script.python_file_run(filepath="E:\\BIN\\blender\\blender-2.75a-windows64\\2.75\\scripts\\presets\\render\\TV_PAL_4_colon_3.py")
    #bpy.context.scene.compression = 0
    bpy.context.scene.render.image_settings.file_format = job_settings['file_format']
    imageBaseName = bpy.path.abspath(current_dir)
    bpy.context.scene.render.filepath = imageBaseName + '//' + uuid + '.' + str(time.time())
    
    # Render Scene and store the scene
    bpy.ops.render.render( write_still=True )
else:
    print("Missing Image:", imagePath)
