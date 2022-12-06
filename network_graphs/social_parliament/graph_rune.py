import numpy as np
import regex as re
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns

import networkx as nx

import matplotlib.patches as patches

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib import colors

#We first create the network directly with the unique actor IDs

#import politician_df from pickle
import pickle
with open('politician_df_python3-7.pkl', 'rb') as handle:
    politician_df = pickle.load(handle)

def create_color_map():

    #Create a color map for the parties
    color_map = {}
    color_map['Socialdemokratiet'] = 'firebrick'
    color_map['Venstre, Danmarks Liberale Parti'] = 'blue'
    color_map['Dansk Folkeparti'] = 'yellow'
    color_map['Enhedslisten'] = 'orange'
    color_map['Nye Borgerlige'] = 'teal'
    color_map['Ny Alliance'] = 'cyan'
    color_map['Liberal Alliance'] = 'cyan'
    color_map['Radikale Venstre'] = 'darkmagenta'
    color_map['Socialistisk Folkeparti'] = 'palevioletred'
    color_map['Danmarksdemokraterne'] = 'steelblue'
    color_map['Alternativet'] = 'green'
    color_map['Moderaterne'] = 'mediumpurple'
    color_map['Det Konservative Folkeparti'] = 'yellowgreen'

    #små partier og uspecificeret
    color_map['Frie Grønne'] = 'darkgrey'
    color_map['unknown'] = 'black'
    color_map['Uden for folketingsgrupperne'] = 'grey'
    color_map['Javnaðarflokkurin'] = 'darkgrey'
    color_map['Tjóðveldisflokkurin'] = 'darkgrey'
    color_map['Tjóðveldi'] = 'darkgrey'
    color_map['Fólkaflokkurin'] = 'darkgrey'
    color_map['Kristendemokraterne'] = 'darkgrey'
    color_map['Siumut'] = 'darkgrey'
    color_map['Sambandsflokkurin'] = 'darkgrey'
    color_map['Inuit Ataqatigiit'] = 'darkgrey'
    color_map['Nunatta Qitornai'] = 'darkgrey'

    return color_map

color_map = create_color_map()


def create_bipartite_graph(df):
    G = nx.Graph()
    #loop through each row of the df:
    for index, row in df.iterrows():
        #loop through each vote in the row
        #add a node with afstemnings_id as name and lovnummer, titel and periode as attribute and set attribute 'type' as law
        G.add_node(row['afstemnings_id_pfix'], lovnummer=row['lovnummer_num'], title=row['titel_kort'], periode_id = row['periode_id'], type='law', bipartite=0)
        for vote in row['votes_adjusted_active']:
            #add edge between the law and the politician if voteid = 1 (yes)
            if vote['typeid'] == 1:
                #if node does not exist, add node with politician id as name and party as attribute and set attribute 'type' as politician
                #if vote['aktor_id'] not in G:
                #    G.add_node(vote['aktor_id'], party=vote['party'], type='politician', bipartite=1, name=vote['name'])
                G.add_edge(row['afstemnings_id_pfix'], vote['aktørid'])
                #set attribute 'type' as politician
                #set node type to politician
                G.nodes[vote['aktørid']]['type'] = 'politician'
 
    
    return G



#function to loop through all politician nodes of the network and set attributes accordingly
#The function is split from the creation of the network, so that setting the attributes is not repeated for every law when politicians nodes are added
def set_politician_attributes(G):
    for node in G.nodes():
        if G.nodes[node]['type'] == 'politician':
            #set attribute 'party' as the party of the politician
            G.nodes[node]['party'] = politician_df[politician_df['politician_id'] == node]['party'].values[0]
            #set attribute 'name' as the name of the politician
            G.nodes[node]['name'] = politician_df[politician_df['politician_id'] == node]['politician_name'].values[0]
            #set attribute 'color' as the color of the party
            #Hacky way just to take the first element on the party list and assign color accordingly
            G.nodes[node]['color'] = color_map[list(G.nodes[node]['party'].values())[0]]
            #set node bipartite to 1
            G.nodes[node]['bipartite'] = 1
    return G