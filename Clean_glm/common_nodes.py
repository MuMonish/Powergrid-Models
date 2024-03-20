# -*- coding: utf-8 -*-
"""
Created on by WSU ESIC

@author: Monish Mukherjee (monish.mukherjee@wsu.edu)
"""

import logging, sys
import json
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import plotly
import plotly.graph_objs as go

def convert_to_color(voltage_level) :
    if (float(voltage_level) < 100):
        color = 'rgb(0,255,255)'
    elif (100 < float(voltage_level)) and (float(voltage_level) < 200):
        color = 'rgb(0,0,255)'
    elif (200 < float(voltage_level)) and (float(voltage_level) < 500):
         color = 'rgb(0,0,128)'
    elif (500 < float(voltage_level)) and (float(voltage_level) < 10000):
        color = 'rgb(255,0,0)'
    
    return color

def convert_transformer_to_color(flag) :
    if (flag == 'True'):
        color = 'rgb(255,255,0)'
    else:
        color = 'rgb(192,192,192)'
        
    return color


if __name__ == '__main__':
    
    if len(sys.argv)>1:
        Feeder_1 = sys.argv[1]
        Feeder_2 = sys.argv[2]
        path  = sys.argv[3]
    else:
        Feeder_1 = '3HT12F7'
        Feeder_2 = '3HT12F1'
        path = r'E:\CIMTool\CIM_Importer_raw_files'

    Feeder_1_main = json.loads(open(path+'\\'+Feeder_1+'_networkx.json').read())
    Feeder_2_main = json.loads(open(path+'\\'+Feeder_2+'_networkx.json').read())
    # Feeder_1_main['directed'] = False
    # Feeder_2_main['directed'] = False
    
    G_Feeder_1 = nx.readwrite.json_graph.node_link_graph(Feeder_1_main)   
    G_Feeder_2 = nx.readwrite.json_graph.node_link_graph(Feeder_2_main)
    
    common_node_F1_F2 = []
    common_node_F2_F1 = []
    
    for n_Feeder_1 in G_Feeder_1.nodes():
        if n_Feeder_1 in G_Feeder_2.nodes():
            common_node_F1_F2.append(n_Feeder_1)
    
    for n_Feeder_2 in G_Feeder_2.nodes():
        if n_Feeder_2 in G_Feeder_1.nodes():
            common_node_F2_F1.append(n_Feeder_2) 
            
    all_common_nodes = common_node_F1_F2 + common_node_F2_F1
    
    common_nodes= []
    # traverse for all elements
    for x in all_common_nodes:
        # check if exists in unique_list or not
        if x not in common_nodes:
            common_nodes.append(x)
    print('List of Common Nodes in Two Feeders', common_nodes)
    # G = nx.compose(G_Feeder_1,G_Feeder_2)

    
    xy1 = {}
    plotnodes1 = set()
    nodecolor1 = []
    Xn1=[]
    Yn1=[]
    Xn_common = []
    Yn_common = []
    labels1 =[]
    labelsC =[]
    for n in G_Feeder_1.nodes():
        #print (n)

        ndata = G_Feeder_1.nodes()[n]['ndata']
        if 'x' in ndata:
            busx = float(ndata['x'])
            busy = float(ndata['y'])
            nodecolor1.append(convert_to_color(ndata['color']))
            xy1[n] = [busx, busy]
            Xn1.append(busx)
            Yn1.append(busy)
            plotnodes1.add(n)
            label = G_Feeder_1.nodes()[n]['nclass']+ n + '\N{RIGHTWARDS ARROW}'+ 'Voltage:' + ndata['voltage']
            labels1.append(label)
            if n in common_nodes:
                Xn_common.append(busx)
                Yn_common.append(busy)
                labelsC.append(label)
                print('F7',n, round(busx,2), round(busy,2))
                
            
    # only plot the edges that have XY coordinates at both ends
    Xe1=[]
    Ye1 = []
    edge_labels1 = []
    edgecolor1 =[]
    plotedges1 = set()
    index = []
    for e in G_Feeder_1.edges():
        bFound = False
        
        if e[0] in xy1:
            if e[1] in xy1:
                plotedges1.add(e)
                bFound = True  
                Xe1.extend([xy1[e[0]][0], xy1[e[1]][0], None])
                Ye1.extend([xy1[e[0]][1], xy1[e[1]][1], None])
                    
        if not bFound:
            print ('unable to plot', e)

    xy2 = {}
    plotnodes2 = set()
    nodecolor2 = []
    Xn2=[]
    Yn2=[]
    labels2 =[]
    for n in G_Feeder_2.nodes():
        #print (n)

        ndata = G_Feeder_2.nodes()[n]['ndata']
        if 'x' in ndata:
            busx = float(ndata['x'])
            busy = float(ndata['y'])
            nodecolor2.append(convert_to_color(ndata['color']))
            xy2[n] = [busx, busy]
            Xn2.append(busx)
            Yn2.append(busy)
            plotnodes2.add(n)
            label = G_Feeder_2.nodes()[n]['nclass']+ n + '\N{RIGHTWARDS ARROW}'+ 'Voltage:' + ndata['voltage']
            labels2.append(label)
            if n in common_nodes:
                Xn_common.append(busx)
                Yn_common.append(busy)
                labelsC.append(label)
                print('F1',n, round(busx,2), round(busy,2))
            
    # only plot the edges that have XY coordinates at both ends
    Xe2=[];
    Ye2=[];
    edge_labels2 = []
    edgecolor2 =[]
    plotedges2 = set()
    index = []
    for e in G_Feeder_2.edges():
        bFound = False
        
        if e[0] in xy2:
            if e[1] in xy2:
                plotedges2.add(e)
                bFound = True  
                Xe2.extend([xy2[e[0]][0], xy2[e[1]][0], None])
                Ye2.extend([xy2[e[0]][1], xy2[e[1]][1], None])
                    
        if not bFound:
            print ('unable to plot', e)
            
    mapbox_access_token = 'pk.eyJ1IjoibW9uaXNobSIsImEiOiJjank2YWNydHgwYmd4M2hwam10amRjZ3A4In0.7CxXOmYRdOKVNde6tiNo5g'
    fig = go.Figure()   
    plot_name = 'Steet view map of Feeder: ' + 'F1+F7'
    
    fig.add_trace(go.Scattermapbox(#type='scatter',
                 lon=Xe1,
                 lat=Ye1,
                 mode='lines',
                 line=go.scattermapbox.Line(width=2, color = 'rgb(0,0,255)')
                 #line_color = edgecolor,
                 #text=edge_labels,
                 #hoverinfo='none'                  
                ))
    fig.add_trace(go.Scattermapbox(#type='scatter',
                 lon=Xe2,
                 lat=Ye2,
                 mode='lines',
                 line=go.scattermapbox.Line(width=2, color = 'rgb(0,255,0)')
                 #line_color = edgecolor,
                 #text=edge_labels,
                 #hoverinfo='none'                  
                ))    

    
    fig.add_trace(go.Scattermapbox(#type='scatter',
                 lon=Xn_common, 
                 lat=Yn_common,
                 mode='markers',
                 marker=go.scattermapbox.Marker(size=8),
                 marker_color = 'rgb(255,0,0)',
                 hoverinfo= 'text',
                 text= labelsC
                 )) 
    
    fig.add_trace(go.Scattermapbox(#type='scatter',
                 lon=Xn1, 
                 lat=Yn1,
                 mode='markers',
                 marker=go.scattermapbox.Marker(size=4),
                 marker_color = 'rgb(0,0,255)',
                 hoverinfo='text',
                 text= labels1
                 ))      
    fig.add_trace(go.Scattermapbox(#type='scatter',
                 lon=Xn2, 
                 lat=Yn2,
                 mode='markers',
                 marker=go.scattermapbox.Marker(size=4),
                 marker_color = 'rgb(0,255,0)',
                 hoverinfo='text',
                 text= labels2
                 )) 

        
        
    axis=dict(showline=False, # hide axis line, grid, ticklabels and  title
          zeroline=False,
          showgrid=False,
          showticklabels=False,
          title='' 
          )
    
    fig.layout.update(title= plot_name,  
                      font= dict(family='Balto'),
                      autosize=True,
                      showlegend=False,
                      hovermode='closest',
                      plot_bgcolor='#FFFAF0', #set background color   
                      mapbox=go.layout.Mapbox(
                              accesstoken=mapbox_access_token,
                              bearing=0,
                              center=go.layout.mapbox.Center(
                                      lat= np.median(Yn1),
                                      lon= np.median(Xn1),
                                ),
                              pitch=0,
                              zoom=15,
                              style='light' ),
                      )
            #hovermode='closest',
#            xaxis=axis,
#            yaxis=axis,
#            margin=dict(
#            l=40,
#            r=40,
#            b=85,
#            t=100,
#            pad=0,
       

       
          
            
    fig.show()
    plotly.offline.plot(fig, filename='networkx.html')
            

            
            

