# -*- coding: utf-8 -*-
"""
Created on Wed Aug 21 15:26:02 2019

@author: Monish Mukherjee
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Nov 13 17:05:41 2018

@author: mukh614
"""
import json
import numpy as np
import glmanip
import os
import networkx as nx
import csv
import math
import copy
import logging, sys
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

import cleaning_functions as clean
from create_json_for_networkx import createJson


def clean_raw_glm(feeder_name, wrk_dir):    
    path_parent = os.path.dirname(os.getcwd())
    os.chdir(path_parent)
    # glm_dir = os.getcwd()
    glm_dir = wrk_dir
    # feeder_name = '3HT12F7'
    # feeder_name = '3HT12F1'
    #feeder_name = '3HT12F5'
    dir_for_glm = glm_dir + '\\'+ feeder_name + '_base.glm'
    dir_for_symbols = glm_dir + '\\'+ feeder_name + '_symbols.json'
    
###############################################################################    
######################### Parsing GLM to Dictionary ###########################
###############################################################################    
    print(feeder_name)
    print(wrk_dir)
    print(glm_dir)
    glm_lines = glmanip.read(dir_for_glm,glm_dir,buf=[])
    [model,clock,directives,modules,classes] = glmanip.parse(glm_lines)

###############################################################################    
######################### Parsing GLM Dict to Graph ###########################
############################################################################### 
    
    feeder_network  = createJson(feeder_name, dir_for_symbols, model,clock,directives,modules,classes)
    G = nx.readwrite.json_graph.node_link_graph(feeder_network)
     
###############################################################################    
#################### Cleaning Line conductor naming ###########################
###############################################################################
    
    model['overhead_line_conductor'], count = clean.convert_coloncolon_to_colon_conductor( model['overhead_line_conductor'])
    model['underground_line_conductor'], count = clean.convert_coloncolon_to_colon_conductor( model['underground_line_conductor'])            
    
###############################################################################    
#################### Erroneous Conductor Information ##########################
###############################################################################
    
    model['overhead_line_conductor'] = clean.correct_overhead_conductor_information(model['overhead_line_conductor'])
    
    for cond in model['overhead_line_conductor']:
        for key in model['overhead_line_conductor'][cond]:
            if 'rating' in key:
                model['overhead_line_conductor'][cond][key] = str(1000.00)
    
    for cond in model['underground_line_conductor']:
        for key in model['underground_line_conductor'][cond]:
            if 'rating' in key:
                model['underground_line_conductor'][cond][key] = str(1000.00)
        
    
###############################################################################    
#########################  Substation Voltage Fix #############################
###############################################################################
    
    for substation_name in model['substation'].keys():
        if (model['substation'][substation_name]['positive_sequence_voltage'] == '$'):
            model['substation'][substation_name]['positive_sequence_voltage'] = '7620.00'
            model['substation'][substation_name]['nominal_voltage'] = '7620.00'

###############################################################################    
######################  Triplex Line Configuration Fix ########################
###############################################################################
    model['triplex_line_configuration'] = {}
    model['triplex_line_conductor'] = {}
    
    model['triplex_line_configuration'],  model['triplex_line_conductor'],  model['line_configuration'] = clean.Fixing_triplex_line_configuration(model['triplex_line_configuration'], model['triplex_line_conductor'], model['triplex_line'], model['line_configuration'])
     
###############################################################################    
######################  Transformer Configuration Fix #########################
###############################################################################
     
    #model['transformer'], model['transformer_configuration'] = clean.Fixing_transformer_winding_configuration(model['transformer'],model['transformer_configuration'])
    
#    for xfmr_conf in model['transformer_configuration']:
#        for key in model['transformer_configuration'][xfmr_conf]:
#            if 'rating' in key:
#                model['transformer_configuration'][xfmr_conf][key] = str(float(model['transformer_configuration'][xfmr_conf][key])*1)
                
            
###############################################################################    
######################  Regulator Configuration Fix ###########################
###############################################################################
    
    for reg_config_name in model['regulator_configuration']:
        for key in (model['regulator_configuration'][reg_config_name].keys()):
            if 'tap_pos' in key:
                model['regulator_configuration'][reg_config_name][key] = str('0')                
                
###############################################################################  
############# Checking Consistency of Service Connections  ####################      
###############################################################################
    
    model['triplex_line'], model['triplex_node'] = clean.Fixing_service_connection_inconsistency(model['triplex_line'], model['triplex_node'], G)
        
###############################################################################  
############# Checking Consistency of Service loads  ####################      
###############################################################################
    
    for tpx_ld_id in model['triplex_load']:
        parent_tpx_node = model['triplex_load'][tpx_ld_id]['parent']
        model['triplex_load'][tpx_ld_id]['phases'] = model['triplex_node'][parent_tpx_node]['phases']
    
###############################################################################  
####################### Adding Group IDs to Nodes ##3##########################       
###############################################################################

#    for node in model['node']:
#        model['node'][node]['groupid'] = {}
#        model['node'][node]['groupid'] = 'primary_nodes'
#        
#    for tpx_node in model['triplex_node']:
#        model['triplex_node'][tpx_node]['groupid'] = {}
#        model['triplex_node'][tpx_node]['groupid'] = 'triplex_nodes'
        
            
###############################################################################  
####################### Checking Voltage Consistency ##########################       
###############################################################################
    
#    for trafo in model['transformer']:
#        secondary_voltage = model['transformer'][trafo]['configuration'].split('/')[-1].split('V')[0]
#        secondary_node = model['transformer'][trafo]['to']
#        nodes = []
#        if 'S' in  model['transformer'][trafo]['phases']:
#            nodes_tpx = list(nx.dfs_postorder_nodes(G,secondary_node))
#            #nodes.append(secondary_node)
#            for nd_tpx in nodes_tpx:
#                model['triplex_node'][nd_tpx]['nominal_voltage'] = secondary_voltage
#        else:
#            nodes = list(nx.dfs_postorder_nodes(G,secondary_node))
#            for nd in nodes:
#                model['node'][nd]['nominal_voltage'] = secondary_voltage
#                
#            
    net_load = 0
    for loadid in model['load']:
        parentid = model['load'][loadid]['parent']
        if model['load'][loadid]['nominal_voltage'] !=  model['node'][parentid]['nominal_voltage']:
            print('Mismatch in Load and Parent Voltage',model['load'][loadid]['nominal_voltage'], model['node'][parentid]['nominal_voltage'])            
            model['load'][loadid]['nominal_voltage'] =  model['node'][parentid]['nominal_voltage']
        
        for key in model['load'][loadid]:
            if 'constant_power_' in key:
                model['load'][loadid][key] = str(complex(model['load'][loadid][key]).real*1000) + '+' + str(complex(model['load'][loadid][key]).imag*1000) + 'j'
                net_load = net_load + complex(model['load'][loadid][key]).real
#
#
    net_load_tpx = 0
    for loadid_tpx in model['triplex_load']:
        parentid_tpx = model['triplex_load'][loadid_tpx]['parent']
        if model['triplex_load'][loadid_tpx]['nominal_voltage'] !=  model['triplex_node'][parentid_tpx]['nominal_voltage']:
            print('Mismatch in Load and Parent Voltage',model['triplex_load'][loadid_tpx]['nominal_voltage'], model['triplex_node'][parentid_tpx]['nominal_voltage'])
            model['triplex_load'][loadid_tpx]['nominal_voltage'] =  model['triplex_node'][parentid_tpx]['nominal_voltage']
        
        for key in model['triplex_load'][loadid_tpx]:
            if 'base_power_' in key:
                model['triplex_load'][loadid_tpx][key] = str(float(model['triplex_load'][loadid_tpx][key])*1000)
                net_load_tpx = net_load_tpx + float(model['triplex_load'][loadid_tpx][key])


#    heavy_load = ['ld__2100704025','ld__1500466992','ld__4820565070','ld__5880439097','ld__2100704024','ld__5920109870']    
#    for ld in heavy_load:
#        ld_key = '\"' + ld + '\"'
#        del model['load'][ld_key]
  
                  
###############################################################################  
############## Checking Phase Consistency in Line Objects #####################   
###############################################################################           
    
#    model_dict_required = {keys: model[keys] for keys in ['node','overhead_line','underground_line','line_configuration']}
#    model['overhead_line'], model['underground_line'], model['line_configuration']   =  clean. Fixing_Phase_inconsistency_in_line(model_dict_required)

###############################################################################  
############## Closing the open Switches ###################################### 
###############################################################################
    
    if feeder_name == '3HT12F7':
        if '"swt__402-2046554-0"' in model['fuse'].keys():
            del model['fuse']['"swt__402-2046554-0"']
    
    elif feeder_name == '3HT12F1':
        if '"swt__402-36571-0"' in model['fuse'].keys():
             model['fuse']['"swt__402-36571-0"']['phases'] = 'ABN'
    
    elif feeder_name == '3HT12F5':
        del model['fuse']['"jump__403-1655962-0"']
        model['fuse']['"swt__402-52580-0"']['phases'] = 'ABCN'       
        model['fuse']['"swt__402-1526071-0"']['phases'] = 'ABCN' 
        model['fuse']['"swt__402-834766-0"']['phases'] = 'AN'
        model['node']['"_402-834766_SN"']['phases'] = 'AN'
        model['node']['"_402-834766_LN"']['phases'] = 'AN'
    
    
    for switchid in model['switch']:
        if model['switch'][switchid]['status'] != 'CLOSED':
             print(switchid)
             model['switch'][switchid]['status'] = str('CLOSED')     
    for rclsrid in model['recloser']:
        if model['recloser'][rclsrid]['status'] != 'CLOSED':
             print(switchid)
             model['recloser'][rclsrid]['status'] = str('CLOSED')  
  
    
###############################################################################    
######################  Missing Line spacing Fix ##############################
###############################################################################
    
    model['line_spacing'] = clean.Fixing_missing_line_spacing(model['line_configuration'], model['line_spacing'])
                   
###############################################################################    
####################  Missing Conductor Type Fix ##############################
###############################################################################
    
    model['underground_line_conductor']['"unknown_"'] = model['underground_line_conductor']['"cncab_1CN15"']
    model['underground_line_conductor']['"unknown_"']['conductor_resistance'] = str(0.15)
   # model['capacitor'] = {}

###############################################################################
######################### Edits for GLM script#################################
###############################################################################
    
    if clock == {}:
        clock = {'timezone': 'PST8',
         'starttime': "'2019-03-28 00:00:00'",
         'stoptime': "'2019-03-28 00:05:00'"}
        
    if directives == []:
        directives.append('#define stylesheet=http://gridlab-d.svn.sourceforge.net/viewvc/gridlab-d/trunk/core/gridlabd-2_0')
        directives.append('#set profiler=1')
        directives.append('#set relax_naming_rules=1')
        directives.append('#set randomseed=10')
        directives.append('#set suppress_repeat_messages=True')
        
    if modules == {}:
        modules = {'market': {},
                   'tape': {},
                   'climate': {},
                   'reliability': {},
                   'residential': {'implicit_enduses': 'NONE'},
                   'powerflow': {'solver_method': 'NR', 
                   'default_maximum_voltage_error': '1e-4',
                   'line_limits': 'TRUE'}}
    
    if model.get('fault_check') == None:
        model['fault_check']={'test_fault': {'check_mode': 'SINGLE',
                                            'output_filename': 'model_inconsistency.txt'}}
    

    for rlcsr_id in model['recloser']:
        to_node = model['recloser'][rlcsr_id]['to']
        from_node = model['recloser'][rlcsr_id]['from']
        if from_node == next(iter(model['substation'])):
                if model.get('meter') == None:
                    model['meter'] ={}
                model['meter'][to_node] = {}
                model['meter'][to_node] = model['node'][to_node]
                recorder_string = ' { \n \t \t property  measured_current_A.real, measured_current_A.imag,' + \
                'measured_current_B.real, measured_current_B.imag, measured_current_C.real, measured_current_C.imag,' + \
                ' measured_power_A.real, measured_power_B.real, measured_power_C.real,' + \
                ' measured_power_A.imag, measured_power_B.imag, measured_power_C.imag;' +  \
                ' \n \t \t interval 300;' + \
                ' \n \t \t file "Outputs/' + feeder_name[:3] + 'CB' + feeder_name[3:] + '.csv" ; \n \t \t}'
                model['meter'][to_node]['object recorder'] = recorder_string
                del model['node'][to_node]
    
    
    swing_node = list(model['substation'].keys())[0]
    file  = "Outputs/" + feeder_name + '_substation.csv'
    if model.get('recorder') == None:
        model['recorder']={'recorder1': {'parent': swing_node,
                                        'property': 'positive_sequence_voltage, distribution_power_A, distribution_power_B, distribution_power_C',
                                        'file': file}}
    
    fileA  = "Outputs/" + feeder_name + '_primary_voltages_A.csv'
    fileB  = "Outputs/" + feeder_name + '_primary_voltages_B.csv'
    fileC  = "Outputs/" + feeder_name + '_primary_voltages_C.csv'
    if model.get('group_recorder') == None:
        model['group_recorder'] = {'voltage_A': {'group': 'class=node',
                                                 'property': 'voltage_A',
                                                 'file': fileA},
                                   'voltage_B': {'group': 'class=node',
                                                 'property': 'voltage_B',
                                                 'file': fileB},
                                   'voltage_C': {'group': 'class=node',
                                                 'property': 'voltage_C',
                                                 'file': fileC}}
    
    file = "Outputs/" + feeder_name + '_currents.csv'
    if model.get('currdump') == None:
        model['currdump']={'currdump_object': {'filename': file}}        
    
    if model.get('collector') == None:
        model['collector']={'loss_OH': {'group': 'class=overhead_line',
                                        'property': 'sum(power_losses_A.real), sum(power_losses_B.real), sum(power_losses_C.real)',
                                        'interval': str(60),
                                        'file':  "Outputs/" +'OH_lines_losses.csv'},
                           'loss_UG': {'group': 'class=underground_line',
                                       'property': 'sum(power_losses_A.real), sum(power_losses_B.real), sum(power_losses_C.real)',
                                       'interval': str(60),
                                       'file':  "Outputs/" + 'UG_lines_losses.csv'}}
    
        
    #ofn = '3HT12F7_clean.glm'
    ofn = glm_dir + '\\'+ feeder_name + '_clean.glm'
    glmanip.write(ofn,model,clock,directives,modules,classes)

    return 

if __name__ == '__main__':
    # print(sys.argv[0])
    clean_raw_glm(sys.argv[1], sys.argv[2]) 
    