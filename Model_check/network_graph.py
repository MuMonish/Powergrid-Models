
import networkx as nx


def create_graph(Link_model,directed = bool(1), multigraph = bool(1)):
###############################################################################
####### Fucntion creates the network graph for the feeder in Blazegraph #######
###############################################################################
    feeder = {}
    feeder['directed'] = directed
    feeder['graph'] = {}
    feeder['links'] = []
    feeder['multigraph'] = multigraph
    feeder['nodes'] = []
    
    node_model = {}
    
    for item in Link_model:
        for link_item in Link_model[item]:
            from_node = Link_model[item][link_item]['bus1']
            to_node   = Link_model[item][link_item]['bus2']
################### Storing all the nodes in a  Dictionary ####################

###################### Creaing the Link model Dictionary ######################           
            if item == 'transformer':
                feeder['links'].append({'eclass': Link_model[item],
                                        'edata': Link_model[item][link_item],
                                        'ename': link_item,
                                        'source': from_node,
                                        'target': to_node,
                                        'Transformer': 'True'})
                
                node_model[from_node] = {'x':  Link_model[item][link_item]['bus1x'],
                                         'y':  Link_model[item][link_item]['bus1y'],
                                         'voltage': Link_model[item][link_item]['basev1'],
                                         'color': Link_model[item][link_item]['basev1']}
                node_model[to_node]   = {'x':  Link_model[item][link_item]['bus2x'],
                                         'y':  Link_model[item][link_item]['bus2y'],
                                         'voltage': Link_model[item][link_item]['basev2'],
                                         'color': Link_model[item][link_item]['basev2']}
            else:
                feeder['links'].append({'eclass': Link_model[item],
                                        'edata': Link_model[item][link_item],
                                        'ename': link_item,
                                        'source': from_node,
                                        'target': to_node,
                                        'Transformer': 'False'})
                    
                node_model[from_node] = {'x':  Link_model[item][link_item]['bus1x'],
                                         'y':  Link_model[item][link_item]['bus1y'],
                                         'voltage': Link_model[item][link_item]['basev'],
                                         'color': Link_model[item][link_item]['basev']}
                node_model[to_node]   = {'x':  Link_model[item][link_item]['bus2x'],
                                         'y':  Link_model[item][link_item]['bus2y'],
                                         'voltage': Link_model[item][link_item]['basev'],
                                         'color': Link_model[item][link_item]['basev']}
                
###################### Creaing the Node model Dictionary ######################        
    for node in node_model:
        feeder['nodes'].append({'id': node,
                                'nclass':'node',
                                'ndata': {'x': node_model[node]['x'],
                                          'y': node_model[node]['y'],
                                          'voltage': node_model[node]['voltage'],
                                          'color': node_model[node]['color']}})
    return feeder    
###############################################################################  