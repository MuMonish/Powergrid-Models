# -*- coding: utf-8 -*-
"""
Created on Fri Oct 11 16:11:16 2019

@author: monis
"""
import logging, sys
import networkx as nx
import math

###############################################################################
############# Removing double underscores from conductor names ############
###############################################################################
def convert_colon_to_underscore(model_dict):
    count = 0
    model_dict_new = {}
    for uid in model_dict.keys():
        count =count+1
        if ':' in uid:
            #count =count+1
            uid_new = uid.replace(':','_')
            model_dict_new[uid_new] = model_dict[uid]
            # model_dict[uid_new] = model_dict.pop(uid)
            for uid_par in model_dict_new[uid_new]:
                if ':' in  model_dict_new[uid_new][uid_par]:
                    new_name =  model_dict_new[uid_new][uid_par].replace(':','_')
                    model_dict_new[uid_new][uid_par] = new_name
        else:            
            model_dict_new[uid] = model_dict[uid]
            for uid_par in model_dict[uid]:
                if ':' in  model_dict[uid][uid_par]:
                    new_name =  model_dict[uid][uid_par].replace(':','_')
                    model_dict_new[uid][uid_par] = new_name            
              
    return model_dict_new, count

###############################################################################
############# Removing double underscores from conductor names ############
############################################################################### 
  
def convert_coloncolon_to_colon_conductor(model_dict):
    count = 0
    model_dict_new = {}
    for uid in model_dict.keys():
        count =count+1
        if '__' in uid:
            #count =count+1
            uid_new = uid.replace('__','_')
            model_dict_new[uid_new] = model_dict[uid]
        else:            
            model_dict_new[uid] = model_dict[uid]        
              
    return model_dict_new, count

###############################################################################
####################### Erroneous Conductor Information  ######################
###############################################################################    
            ############## looking for zero values ################    
def correct_overhead_conductor_information(model_conductor_dict):
    flag = 0
    for cond in model_conductor_dict: 
        if float(model_conductor_dict[cond]['diameter']) == 0.000000:
            model_conductor_dict[cond]['diameter'] = str(0.398007)
            flag = 1
        if float(model_conductor_dict[cond]['geometric_mean_radius']) == 0.000000:
            model_conductor_dict[cond]['geometric_mean_radius'] = str(0.004460)
            flag = 1
        if float(model_conductor_dict[cond]['resistance']) == 0.000000:
            model_conductor_dict[cond]['resistance'] = str(1.040159)  
            flag = 1
        if flag == 1:
            logging.warning('Conductor {} have zero value of Diameter/Resistance/GMR'.format(cond))
    return model_conductor_dict    
        
###############################################################################
################# Fixing Transformer Winding Configuration  ###################
###############################################################################
    
def Fixing_transformer_winding_configuration(model_transformer_dict, model_transformer_config_dict):
    old_config_names =[]
    for xfmr in model_transformer_dict:
        if 'S' in model_transformer_dict[xfmr]['phases']:
            xfmr_config_split = model_transformer_dict[xfmr]['configuration']
            xfmr_config_new_split = xfmr_config_split.split('TI')[0]+ 'TI_'+ model_transformer_dict[xfmr]['phases'] + '"'
            model_transformer_dict[xfmr]['configuration'] = xfmr_config_new_split
            if  model_transformer_config_dict.get(xfmr_config_new_split) == None:
                old_config_names.append(xfmr_config_split)
                model_transformer_config_dict[xfmr_config_new_split] = model_transformer_config_dict[xfmr_config_split].copy()
                model_transformer_config_dict[xfmr_config_new_split]['connect_type'] = 'SINGLE_PHASE_CENTER_TAPPED' 
#                model_transformer_config_dict[xfmr_config_new_split]['resistance']  = '0.00725'
#                model_transformer_config_dict[xfmr_config_new_split]['resistance1'] = '0.01450'
#                model_transformer_config_dict[xfmr_config_new_split]['resistance2'] = '0.01450'
#                model_transformer_config_dict[xfmr_config_new_split]['reactance']   = '0.01320'
#                model_transformer_config_dict[xfmr_config_new_split]['reactance1']  = '0.00660'
#                model_transformer_config_dict[xfmr_config_new_split]['reactance2']  = '0.00660'
#                model_transformer_config_dict[xfmr_config_new_split]['shunt_reactance'] = '57.47'
#                model_transformer_config_dict[xfmr_config_new_split]['shunt_resistance'] = '212.77'
                model_transformer_config_dict[xfmr_config_new_split]['power_rating'] = str(float(model_transformer_config_dict[xfmr_config_split]['power_rating'])*1)
                new_key = 'power' + model_transformer_dict[xfmr]['phases'].split('S')[0] + '_rating'
                model_transformer_config_dict[xfmr_config_new_split][new_key] = model_transformer_config_dict[xfmr_config_new_split]['power_rating']
                model_transformer_config_dict[xfmr_config_new_split]['primary_voltage'] = str(float(model_transformer_config_dict[xfmr_config_split]['primary_voltage'])/math.sqrt(3))
                model_transformer_config_dict[xfmr_config_new_split]['secondary_voltage'] =  str(float(model_transformer_config_dict[xfmr_config_split]['secondary_voltage']))
#                del model_transformer_config_dict[xfmr_config_new_split]['impedance']
#                del model_transformer_config_dict[xfmr_config_new_split]['impedance1']
#                del model_transformer_config_dict[xfmr_config_new_split]['impedance2']

        elif 'ABCN' in model_transformer_dict[xfmr]['phases']:
            xfmr_config_ABCN = model_transformer_dict[xfmr]['configuration']
            xfmr_config_ABCN_new = xfmr_config_ABCN.split('TI')[0]+ 'TI_' + 'ABCN' + '"'
            model_transformer_dict[xfmr]['configuration'] = xfmr_config_ABCN_new
            if  model_transformer_config_dict.get(xfmr_config_ABCN_new) == None:
                old_config_names.append(xfmr_config_ABCN)
                model_transformer_config_dict[xfmr_config_ABCN_new] = model_transformer_config_dict[xfmr_config_ABCN].copy()
                model_transformer_config_dict[xfmr_config_ABCN_new]['connect_type'] = 'WYE_WYE'
#                model_transformer_config_dict[xfmr_config_ABCN_new]['reactance']   = '0.01770'
#                model_transformer_config_dict[xfmr_config_ABCN_new]['resistance']  = '0.01900'
                model_transformer_config_dict[xfmr_config_ABCN_new]['primary_voltage']   = str(round(float(model_transformer_config_dict[xfmr_config_ABCN]['primary_voltage'])/math.sqrt(3)))
                model_transformer_config_dict[xfmr_config_ABCN_new]['secondary_voltage'] = str(round(float(model_transformer_config_dict[xfmr_config_ABCN]['secondary_voltage'])))
                model_transformer_config_dict[xfmr_config_ABCN_new]['power_rating'] = str(float(model_transformer_config_dict[xfmr_config_ABCN]['power_rating'])*1)
                model_transformer_config_dict[xfmr_config_ABCN_new]['powerA_rating'] = str(float(model_transformer_config_dict[xfmr_config_ABCN_new]['power_rating'])/3)
                model_transformer_config_dict[xfmr_config_ABCN_new]['powerB_rating'] = str(float(model_transformer_config_dict[xfmr_config_ABCN_new]['power_rating'])/3)
                model_transformer_config_dict[xfmr_config_ABCN_new]['powerC_rating'] = str(float(model_transformer_config_dict[xfmr_config_ABCN_new]['power_rating'])/3)
#                model_transformer_config_dict[xfmr_config_ABCN_new]['shunt_reactance'] = '44.24'
#                model_transformer_config_dict[xfmr_config_ABCN_new]['shunt_resistance'] = '222.22'
#                del model_transformer_config_dict[xfmr_config_ABCN_new]['impedance']
                del model_transformer_config_dict[xfmr_config_ABCN_new]['impedance1']
                del model_transformer_config_dict[xfmr_config_ABCN_new]['impedance2']
        else:
            xfmr_config_AN = model_transformer_dict[xfmr]['configuration']
            secondary_voltage = model_transformer_config_dict[xfmr_config_AN]['secondary_voltage']
            primary_voltage = model_transformer_config_dict[xfmr_config_AN]['primary_voltage']
            xfmr_config_AN_new = xfmr_config_AN.split('TI')[0]+ 'TI_' + model_transformer_dict[xfmr]['phases'] + '"'
            model_transformer_dict[xfmr]['configuration'] = xfmr_config_AN_new
            if  model_transformer_config_dict.get(xfmr_config_AN_new) == None:
                old_config_names.append(xfmr_config_AN)
                model_transformer_config_dict[xfmr_config_AN_new] = model_transformer_config_dict[xfmr_config_AN].copy()
                model_transformer_config_dict[xfmr_config_AN_new]['connect_type'] = 'WYE_WYE'
#                model_transformer_config_dict[xfmr_config_AN_new]['reactance']   = '0.01320'
#                model_transformer_config_dict[xfmr_config_AN_new]['resistance']  = '0.00725'
                model_transformer_config_dict[xfmr_config_AN_new]['primary_voltage'] = str(round(float(primary_voltage)/math.sqrt(3)))
                model_transformer_config_dict[xfmr_config_AN_new]['secondary_voltage'] = str(round(float(secondary_voltage)))
                model_transformer_config_dict[xfmr_config_AN_new]['power_rating'] = str(float(model_transformer_config_dict[xfmr_config_AN]['power_rating'])*1)
                for ph in range(len(model_transformer_dict[xfmr]['phases'])):
                    ph_key = 'power' + model_transformer_dict[xfmr]['phases'][ph] + '_rating'
                    model_transformer_config_dict[xfmr_config_AN_new][ph_key] = str(float(model_transformer_config_dict[xfmr_config_AN]['power_rating'])/(len(model_transformer_dict[xfmr]['phases'])))
#                model_transformer_config_dict[xfmr_config_AN_new]['shunt_reactance'] = '44.24'
#                model_transformer_config_dict[xfmr_config_AN_new]['shunt_resistance'] = '222.22'
#                del model_transformer_config_dict[xfmr_config_AN_new]['impedance']
                del model_transformer_config_dict[xfmr_config_AN_new]['impedance1']
                del model_transformer_config_dict[xfmr_config_AN_new]['impedance2']   
    
    unique_old_config_names = []
    for xfmr_config in old_config_names: 
        # check if exists in unique_list or not 
        if xfmr_config not in unique_old_config_names: 
            unique_old_config_names.append(xfmr_config)  
    
    for unique_xfmr_config in unique_old_config_names:
        del model_transformer_config_dict[unique_xfmr_config]
    
    return model_transformer_dict, model_transformer_config_dict
###############################################################################
#################### Fixing Triplex Line Configuration  #######################
###############################################################################
        ############## Adding prper triplex configuration ################       
def Fixing_triplex_line_configuration(model_triplex_line_config_dict, model_triplex_line_conductor_dict, model_triplex_line_dict, model_line_config_dict):
    
    triplex_line_config =[]
    for triplex_line_name in model_triplex_line_dict.keys():
        if 'S' in model_triplex_line_dict[triplex_line_name]['phases']:
            triplex_line_config.append(model_triplex_line_dict[triplex_line_name]['configuration'])
    
    ## getting unique triplex line configs ##
    unique_triplex_line_config = []
    for tpx_config in triplex_line_config: 
        # check if exists in unique_list or not 
        if tpx_config not in unique_triplex_line_config: 
            unique_triplex_line_config.append(tpx_config)
    
    # Adding triple configuration as 'triplex_line_configuration' ##
    for tpx_config in unique_triplex_line_config:
        #del model['line_configuration'][tpx_config]
        model_triplex_line_config_dict[tpx_config] = {'conductor_1': 'triplex_conductor_1',
                                                           'conductor_2': 'triplex_conductor_1',
                                                           'conductor_N': 'triplex_conductor_1',
                                                           'insulation_thickness': '0.08',
                                                           'diameter': '0.368'}

        model_triplex_line_conductor_dict['triplex_conductor_1'] = {'resistance': '0.009',
                                                                  'geometric_mean_radius': '0.0111',
                                                                  'rating.summer.continuous': '1000',
                                                                  'rating.summer.continuous': '1000'}
        ## deleting the config to avoid duplicates ##
        del model_line_config_dict[tpx_config]
    
    return model_triplex_line_config_dict, model_triplex_line_conductor_dict, model_line_config_dict

###############################################################################
######################## Fixing Missing Line Spacing  #########################
###############################################################################
    
def Fixing_missing_line_spacing(model_line_configuration_dict, model_line_spacing_dict):
    
    line_spacings=[]
    for config_id in model_line_configuration_dict:
        line_spacings.append(model_line_configuration_dict[config_id]['spacing'])
        
    unique_line_spacings = []
    for y in line_spacings:
        if y not in unique_line_spacings:
            unique_line_spacings.append(y)
        
    missing_line_spacing = list(set(unique_line_spacings) - set(list(model_line_spacing_dict.keys())))
    logging.warning('Adding these missing line spacings {}'.format(missing_line_spacing))
        
    for line_spacing_id in missing_line_spacing:
        model_line_spacing_dict[line_spacing_id] = {}
        phasing = (line_spacing_id.split('_')[-1]).split('\"')[0]
        combinations  = []
        phasing2 = phasing
        for alpha in phasing:
            phasing2 = phasing2.replace(alpha,'')
            for beta in phasing2:
                if alpha != beta:
                    combinations.append('distance_'+alpha+beta)
        for keys in combinations:
            if 'N' in keys:
                model_line_spacing_dict[line_spacing_id][keys] = str('5.3853')
            else:
                model_line_spacing_dict[line_spacing_id][keys] = str('4.0001')
    
    return model_line_spacing_dict

###############################################################################
############## Fixing Consistency of Service Connections  #####################
###############################################################################

def Fixing_service_connection_inconsistency(model_triplex_line_dict, model_triplex_node_dict, network_graph):
       
    for tpx in model_triplex_line_dict:
        phase = model_triplex_line_dict[tpx]['phases']
        initial_to_node= model_triplex_line_dict[tpx]['to']
        to_node = initial_to_node
        if phase == 'S':
            # Looking for upstream nodes for getting phase information
            while len(phase) <= 1:
                from_node = list(network_graph.predecessors(to_node))[0]
                phase = model_triplex_node_dict[from_node]['phases']
                to_node = from_node 
            # Phase Consistency for the downstream triplex lines and nodes
            all_downstream_single_paths = list(nx.all_simple_paths(network_graph, from_node, initial_to_node, cutoff=None))
            logging.warning(' Phase of Triplex Line {} is S. Plugginfg in phase from upstream node {}({})'.format(tpx, initial_to_node, phase))
    
            for node in all_downstream_single_paths:
                # Get all node pairs in path:
                # [1,2,3,4] -> [[1,2],[2,3],[3,4]]
                paths = [node[i: i + 2] for i in range(len(node)-1)]
                for edge in paths:
                    edge_from_node = edge[0] # Get From node of the edge
                    edge_to_node   = edge[1] # Get To node of the edge
                    edge_name= (network_graph.get_edge_data(edge_from_node,edge_to_node)[0]['ename']) # Get edge name
                    model_triplex_node_dict[edge_from_node]['phases'] =  phase
                    model_triplex_node_dict[edge_to_node]['phases'] =  phase
                    model_triplex_line_dict[edge_name]['phases'] =  phase
        if len(phase) > 2 and 'S' in phase:
            logging.warning('Warning !! Triplex Phase Inconsitency {} {} {}!'.format(tpx, initial_to_node, phase))
    
    
    return model_triplex_line_dict, model_triplex_node_dict


###############################################################################  
############## Fixing Phase inconsistency in Line Objects #####################   
###############################################################################           

def Fixing_Phase_inconsistency_in_line(model):
    
    Link_models = ['overhead_line','underground_line']
    for item in range(len(Link_models)):
        #### Looking for
        for link_item in model[Link_models[item]]:
            from_node = model[Link_models[item]][link_item]['from']
            from_node_phase = model['node'][from_node]['phases']
            to_node =   model[Link_models[item]][link_item]['to']            
            to_node_phase = model['node'][to_node]['phases']
            item_phase = model[Link_models[item]][link_item]['phases']
            if 'N' not in item_phase:
                item_phase = item_phase + 'N'
            if (to_node_phase != item_phase) and (from_node_phase != item_phase) : 
                logging.warning('Phase Mismatch: From node {}({}) -- link item {}({})  --> To node {}({})'.format(from_node,from_node_phase,link_item,item_phase,to_node,to_node_phase))
                if (to_node_phase == from_node_phase):
                    model[Link_models[item]][link_item]['phases'] = from_node_phase
                    old_configuration  = model[Link_models[item]][link_item]['configuration']
                    new_configuration = '_'.join(old_configuration.split('__')[0].split('_')[0:-1]) + '_' + from_node_phase + '__' + old_configuration.split('__')[-1]
                    model[Link_models[item]][link_item]['configuration'] = new_configuration
                    model['line_configuration'][new_configuration] = {}
                    model['line_configuration'][new_configuration] = model['line_configuration'][old_configuration]
                    for ph in range(len(from_node_phase)):
                        old_keys = [key for key in model['line_configuration'][new_configuration] if 'conductor_' in key] 
                        conductor_key = 'conductor_' + from_node_phase[ph]
                        if conductor_key not in  old_keys:
                            model['line_configuration'][new_configuration][conductor_key] = model['line_configuration'][new_configuration][old_keys[0]]
                            logging.debug('Adding {} to  Line configuration {} changed from {}'.format(conductor_key, new_configuration, old_configuration))
                    new_spacing  = '_'.join(model['line_configuration'][new_configuration]['spacing'].split('_')[0:-2])+ '_' + from_node_phase + '_' + from_node_phase + '"'
                    model['line_configuration'][new_configuration]['spacing'] = new_spacing    
                    logging.debug('Adding Line Spacing {} to  Line configuration {}'.format(new_spacing, new_configuration))    
                    
    return model['overhead_line'], model['underground_line'], model['line_configuration']   
                    
                    