# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 14:42:42 2020

@author: mukh915
"""

import exec_query
from network_graph import create_graph
import networkx as nx
from colorama import Fore

if __name__ == '__main__':

    feeder_mrid = '_2f953656-602a-a613-10f5-6579d8ed4621'
    
    check_Service_connections = True
    check_transformer_winding_configuiration = False
    checking_service_voltage = False
    checking_islands_in_network = True

###############################################################################  
###################### Fetching Data from CIM file ############################
    
    load_dict = exec_query.query_load(feeder_mrid)
    #ac_line_spacing_dict = exec_query.query_line_spacing(feeder_mrid)
    xfmr_code_rating_dict = exec_query.query_transformer_code_rating(feeder_mrid)
    
    
############# Fetching Connectivity data from CIM file ########################
    
    ac_line_dict = exec_query.query_line_segment(feeder_mrid)
    load_break_switch_dict = exec_query.query_load_break_switch(feeder_mrid)
    jumper_dict = exec_query.query_jumpers(feeder_mrid)
    recloser_dict = exec_query.query_reclosers(feeder_mrid)
    breaker_dict = exec_query.query_breakers(feeder_mrid)
    fuse_dict = exec_query.query_fuses(feeder_mrid)
    disconnector_dict = exec_query.query_disconnectors(feeder_mrid)
    xfmr_dict = exec_query.query_transformer(feeder_mrid)
    
    Link_model ={}
    Link_model['line'] = ac_line_dict
    Link_model['load_break_switch'] = load_break_switch_dict
    Link_model['jumper'] = jumper_dict
    Link_model['recloser'] = recloser_dict
    Link_model['breaker'] = breaker_dict
    Link_model['fuse'] = fuse_dict
    Link_model['disconnector'] = disconnector_dict
    Link_model['transformer'] = xfmr_dict  
    
    
    text_file = open("Feeder_Checks.txt", "w")
    

###############################################################################  
############## Checking Service Connections Consistency #######################
###############################################################################
    
    if check_Service_connections is True:
    ################# Forming a graph network of the Feeder ###################
        feeder_network = create_graph(Link_model)
        G = nx.readwrite.json_graph.node_link_graph(feeder_network)
        print(Fore.GREEN + '\n Checking Phase Consistency of Service Connections')
        text_file.write('Service Phase Inconsistencies :\n')
        for line in ac_line_dict:
            edge_class = 'False'
            if ac_line_dict[line]['phases'] == 's1s2':
                from_node_start = ac_line_dict[line]['bus2']
                from_node = from_node_start
                while edge_class == 'False': 
                    to_node_new = from_node
                    from_node = list(G.predecessors(to_node_new))[0]
                    edge_info = (G.get_edge_data(from_node,to_node_new)[0])
                    edge_class = edge_info['Transformer']
                    if edge_class == 'True':
                        if 's' not in edge_info['edata']['phs2']:
                            print(Fore.RED + 'Warning Wrong Service Phase!!!!')
                            text_file.write('Warning Wrong Service Phase!!!! Triplex Node {} has an upstream transformer {} which is {} phase \n'.format(from_node_start,edge_info['ename'],edge_info['edata']['phs2']))
        text_file.write('\n\n\n')                
###############################################################################  
######### Checking Transformer Winding Configuration  Consistency #############
###############################################################################
                            
    if check_transformer_winding_configuiration is True:
    ################# Forming a graph network of the Feeder ###################
        feeder_network = create_graph(Link_model)
        G = nx.readwrite.json_graph.node_link_graph(feeder_network)
        print(Fore.GREEN + '\n Checking Consistency in Transformer Winding Configuiration')
        text_file.write('Transformer Winding Inconsistencies :\n')
        for xfmr in xfmr_dict:
            tank_winding =[]            
            if 's' in xfmr_dict[xfmr]['phs2']:
                xfmr_configuration = xfmr_dict[xfmr]['xfmrcode'].split('_TI')[0]
                for xfmr_configs in xfmr_code_rating_dict:
                    if xfmr_configuration in xfmr_configs:
                        tank_winding.append(xfmr_code_rating_dict[xfmr_configs]['conn'])
                if (tank_winding != ['I','I','I']):
                    print(Fore.RED + 'Warning Wrong XFMR Configuration!!!!')
                    text_file.write('Warning Wrong XFMR Configuration!!!! Split Phase Transformer\'s ({}) TANK Asset has {} ends and {} winding connections \n'.format(xfmr, len(tank_winding), tank_winding))
        text_file.write('\n\n\n')   
        
###############################################################################  
################ Checking Service Voltage Consistency #########################
###############################################################################      
    
    if checking_service_voltage is True:
    ################# Forming a graph network of the Feeder ###################
        feeder_network = create_graph(Link_model)
        G = nx.readwrite.json_graph.node_link_graph(feeder_network)
        print(Fore.GREEN + '\n Checking Voltage Consistency of Service Connections')
        text_file.write('Service Voltage Inconsistencies :\n')
        for line in ac_line_dict:
            edge_class = 'False'
            line_voltage = float(ac_line_dict[line]['basev'])
            if float(ac_line_dict[line]['basev']) < 1000:
                from_node_start = ac_line_dict[line]['bus2']
                from_node = from_node_start
                while edge_class == 'False': 
                    to_node_new = from_node
                    from_node = list(G.predecessors(to_node_new))[0]
                    edge_info = (G.get_edge_data(from_node,to_node_new)[0])
                    edge_class = edge_info['Transformer']
                    if edge_class == 'True':
                        #print(line_voltage,float(edge_info['edata']['basev2']))
                        if (line_voltage != float(edge_info['edata']['basev2'])):
                            print(Fore.RED + 'Warning Wrong Service Voltage')
                            text_file.write('Warning Wrong Service Voltage!!!! Triplex Line Voltage is {} and the upstream transformer secondary is {} \n'.format(line_voltage,edge_info['edata']['basev2']))
        text_file.write('\n\n\n')                              
                            
###############################################################################  
################ Checking for Possible Islands in Network #####################
###############################################################################
                            
    if checking_islands_in_network is True:
        ################# Forming a graph network of the Feeder ###################
        feeder_network = create_graph(Link_model,directed = bool(0), multigraph = bool(0))
        G = nx.readwrite.json_graph.node_link_graph(feeder_network)
        print(Fore.GREEN + '\n Checking For Islands in the Network')
        text_file.write('Island Inconsistencies for the Feeder :\n')
        islands = list(nx.connected_component_subgraphs(G))
        n_island = 1
        if len(islands) > 1:
            print(Fore.RED + 'Warning {} Islands are found. Network not completely connected'.format(len(islands)))
            for graph in islands:
                text_file.write('\n \n Nodes in Island {}:\n'.format(n_island))
                text_file.write(str(graph.nodes))
                text_file.write('\n \n Link objects in Island {}:\n'.format(n_island))
                for pair in graph.edges:
                    text_file.write("%s %s \n" % pair)
                n_island = n_island + 1
                
            


###############################################################################    
    text_file.close()          
###############################################################################    