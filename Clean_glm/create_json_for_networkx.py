# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 13:16:45 2019

@author: monish.mukherjee
"""

import json
import glmanip
import numpy as np

def createJson(feeder_name, dir_for_symbols, model,clock,directives,modules,classes): 

    symbols_dir = dir_for_symbols
    
    lp = open(symbols_dir).read()
    lp = lp[:11]+'{' +lp[12:]
    lp = lp[:len(lp)-3] + '}'
    symbols = json.loads(lp)
    
    feeder = {}
    feeder['directed'] = bool(1)
    feeder['graph'] = {}
    feeder['links'] = []
    feeder['multigraph'] = bool(1)
    feeder['nodes'] = []
    
   
    #######################    Feeder Links   #################################
    Link_models = ['overhead_line','underground_line','regulator','fuse','recloser','switch','transformer', 'triplex_line']
    for item in range(len(Link_models)):
        for link_item in model[Link_models[item]]:
            if Link_models[item] == 'transformer':
                feeder['links'].append({'eclass': Link_models[item],
                                    'edata': model[Link_models[item]][link_item],
                                    'ename': link_item,
                                    'source': model[Link_models[item]][link_item]['from'],
                                    'target': model[Link_models[item]][link_item]['to'],
                                    'Transformer': 'True'})
            else:
                feeder['links'].append({'eclass': Link_models[item],
                                    'edata': model[Link_models[item]][link_item],
                                    'ename': link_item,
                                    'source': model[Link_models[item]][link_item]['from'],
                                    'target': model[Link_models[item]][link_item]['to'],
                                    'Transformer': 'False'})
                
        
    ######### getting disconnectors and jumpers from symbol file ############## 
    
#    symbol_models = ['jumpers', 'disconnectors']
#    for item in range(len(symbol_models)):
#        for link_item_from_symbol in symbols['feeders'][symbol_models[item]]:
#            feeder['links'].append({'eclass': symbol_models[item],
#                                    'edata': link_item_from_symbol,
#                                    'ename': '\"'+link_item_from_symbol['name']+'\"',
#                                    'source': '\"'+link_item_from_symbol['from']+'\"',
#                                    'target': '\"'+link_item_from_symbol['to']+'\"'})    
 
    ################## feeder nodes, triplex_node and  substation #############
    node_models = ['node', 'triplex_node','substation']
    link_models_from_json = list(symbols['feeders'].keys())
    link_models_from_json.remove('swing_nodes')
    link_models_from_json.remove('capacitors')
    link_models_from_json.remove('synchronousmachines')
    link_models_from_json.remove('solarpanels')
    link_models_from_json.remove('breakers')
    link_models_from_json.remove('sectionalisers')
    link_models_from_json.sort(reverse = True)
    
    for it in range(len(node_models)):
        for node in model[node_models[it]]:
            flag = 0
            ##  ######### ##
            for link_item in range(len(link_models_from_json)):
                if flag == 1:
                    break
                for obj_item in symbols['feeders'][link_models_from_json[link_item]]:
                    node_name = node.replace('\"','')
                    if link_models_from_json[link_item] != 'swing_nodes':
                        if node_name == obj_item['from']:                        
                            feeder['nodes'].append({'id': node,
                                                'nclass': node_models[it],
                                                'ndata': {'x': str(obj_item['x1']),
                                                          'y': str(obj_item['y1']),
                                                          'voltage': (model[node_models[it]][node]['nominal_voltage']),
                                                          'color': (model[node_models[it]][node]['nominal_voltage'])}})
                            flag = 1
                            break

                        elif node_name == obj_item['to']:
                            feeder['nodes'].append({'id': node,
                                                    'nclass': node_models[it],
                                                    'ndata': {'x': str(obj_item['x2']),
                                                              'y': str(obj_item['y2']),
                                                              'voltage': (model[node_models[it]][node]['nominal_voltage']),
                                                              'color': (model[node_models[it]][node]['nominal_voltage'])}})
                            flag = 1
                            break

                    
             
            if flag == 0:
                print ('Couldnt find a match for {} {} having phase {}'.format(node, node_models[it], model[node_models[it]][node]['phases']))
            
    #################   Printing to Json  #####################
    Json_file = json.dumps(feeder, sort_keys=True, indent=4, separators=(',', ': '))    
    fp = open(feeder_name + '_networkx.json', 'w')
    print(Json_file, file=fp)
    fp.close()
    
    return feeder
    
                 
                
                
            
    
   
    
        
    
    
    
    
    
