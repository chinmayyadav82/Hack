# Import dependencies

import numpy as np
import streamlit as st
st.set_page_config(layout="wide")
import streamlit.components.v1 as components
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network
import datetime
import time

# Read dataset
df_zena_deps = pd.read_csv('ZenaJobDependenciesTest2.csv')

# Set header title
st.title('Network Graph Visualization of CDP Zena Job Dependencies - Test')

# Define selection options and sort alphabetically
zena_list = df_zena_deps['zena_job_name'].to_list()
zena_set = set(zena_list)
zena_list_unique = list(zena_set)
zena_list_unique.sort()

# Define selection options and sort alphabetically (For Successors)
successor_list = df_zena_deps['successor_job_name'].to_list()
successor_list_unique = list(set(successor_list))
successor_list_unique.sort()

# Implement multiselect dropdown menu for option selection
#selected_zenas = st.multiselect('Select zena job(s) to visualize', zena_list_unique)


#Search bar

with st.form(key='searchform'):
            nav1,nav2,nav3 = st.columns([3,2,1])

            with nav1:
                #search_term = st.text_input("Search Zena Jobs")
                container = st.container()
                all = st.checkbox("Select All")
                if all:
                    selected_zenas = container.multiselect("Select Zena Job Names:",
                    zena_list_unique, zena_list_unique)
                else:
                    selected_zenas =  container.multiselect("Select Zena Job Names:",
                    zena_list_unique)
            with nav2:
                #ed_att = st.text_input("successor Job Name")
                ed_att = st.multiselect("Select Successor Job Names", successor_list_unique )
            with nav3:
                st.text("Search ")
                submit_search = st.form_submit_button(label='Search')

st.success("You searched for  {}  in  {} ".format(selected_zenas,ed_att))   
    
    
    
  
    
# Set info message on initial site load
if len(selected_zenas) == 0:
    st.text('Please choose at least 1 zena job to get started')

# Create network graph when user selects >= 1 item
else:
    df_select = df_zena_deps.loc[df_zena_deps['zena_job_name'].isin(selected_zenas) | \
                                df_zena_deps['successor_job_name'].isin(selected_zenas)]
    df_select = df_select.reset_index(drop=True)

    # Create networkx graph object from pandas dataframe
    G = nx.from_pandas_edgelist(df_select, 'zena_job_name', 'successor_job_name','edge_attribute')

    # Initiate PyVis network object
    zena_net = Network(height='1600px', width='100%', bgcolor='#222222', font_color='white', heading='CDP Zena Jobs')

    # Take Networkx graph and translate it to a PyVis graph format
    zena_net.from_nx(G)

    # Generate network with specific layout settings
    zena_net.repulsion(node_distance=150, central_gravity=0.33,
                       spring_length=110, spring_strength=0.10,
                       damping=0.95)


#Barnes hut algorithm

def map_algs(zena_net, alg = "barnes"):
    if alg=="barnes":
        zena_net.barnes_hut()

map_algs(zena_net)
zena_net.show_buttons()

#Test features(widgets)
#Calendar - 1    
d = st.date_input("Which date do you want to see", datetime.datetime(2022, 7, 6), datetime.datetime(2022, 5, 6) )
st.write("Date you have selected is", d)

#Sidebar - 2
with st.sidebar:
    with st.echo():
        st.write("Zena Data Network Graph")

    with st.spinner("Loading..."):
        time.sleep(5)
    st.success("Done!")
    
    #df_show = pd.DataFrame(df_zena_deps)
    #columns=('col %d' % i for i in range(20)))

st.dataframe(df_zena_deps)  # Same as st.write(df)

    
# Save and read graph as HTML file (locally)
path = 'html_files'
zena_net.save_graph(f'{path}/pyvis_graph.html')
HtmlFile = open(f'{path}/pyvis_graph.html', 'r', encoding='utf-8')

# Load HTML file in HTML component for display on Streamlit page
components.html(HtmlFile.read(), height=10000, width=1600)

#write_html(Widgets_pyvis_network_app_test.py, notebook=False)

pwd()

zena_net.show('karate.html')
display(HTML('karate.html'))
