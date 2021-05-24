# -*- coding: utf-8 -*-
"""
Created on Sat Sep 19 16:07:37 2020

@author: monish mukherjee
"""

import glmanip
import pandas as pd
import os
import json

if __name__ == '__main__':
    
    feeder_name = '3HT12F7'
    
###############################################################################    
################# Creating JSON for feeder Extentions  ########################
###############################################################################  
    feeder_mods = pd.read_csv(feeder_name+"_modifications.csv")
    mod_Property = {}
    for b in feeder_mods.index:
       data = feeder_mods.loc[b]
       for key in data.keys():
           if 'name' in key:
               object_name = data[key]
               mod_Property[object_name] =  {}
           else:
               mod_Property[object_name][key] =  data[key]
     
    model_feeder_ext = {}             
    model_feeder_ext['underground_line'] = {}
    model_feeder_ext['underground_line'] = mod_Property 
    
           
###############################################################################    
################# Creating JSON for New feeder Assets  ########################
###############################################################################  
    
    path_parent = os.path.dirname(os.getcwd())
    os.chdir(path_parent)
    glm_dir = os.getcwd()
    dir_for_glm = glm_dir + '\\' + 'CEF2TE.glm'
    
    glm_lines = glmanip.read(dir_for_glm,glm_dir,buf=[])
    [model,clock,directives,modules,classes] = glmanip.parse(glm_lines) 
    
    model_json = {}

    model_json['meter'] = model['meter']
    model_json['solar'] = model['solar']
    model_json['climate'] = model['climate']
    model_json['inverter'] = model['inverter']
#    model_json['battery'] = model['battery']
#    model_json['transformer'] = model['transformer']
#    model_json['transformer_configuration'] = model['transformer_configuration']
    
    
    Json_file = json.dumps(model_feeder_ext, sort_keys=True, indent=4, separators=(',', ': '))    
    fp = open(feeder_name+"_add_extensions.json", 'w')
    print(Json_file, file=fp)
    fp.close()   
    
    
    Json_file = json.dumps(model_json, sort_keys=True, indent=4, separators=(',', ': '))    
    fp = open(feeder_name+"_add_assets.json", 'w')
    print(Json_file, file=fp)
    fp.close()
           
           