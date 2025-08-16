FILE: /ccie/ccie/tools/visualization/topology_gen.py
----------------------------------------
#!/usr/bin/env python3
"""
Script: topology_gen.py
Purpose: Generate visual representations of the network topology.
Author: zwu Network Automation Team
Date: [Date]
"""

import networkx as nx
import matplotlib.pyplot as plt
import yaml
import os

def load_topology(file_path):
    """Load topology data from a YAML file."""
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)

def create_topology_graph(topology_data):
    """Create a network graph from topology data."""
    G = nx.Graph()
    for node in topology_data['nodes']:
        G.add_node(node['name'], **node['attributes'])
    for link in topology_data['links']:
        G.add_edge(link['source'], link['target'], **link['attributes'])
    return G

def visualize_topology(G):
    """Visualize the network topology using Matplotlib."""
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=2000, font_size=10, font_weight='bold')
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.title("Network Topology")
    plt.show()

if __name__ == "__main__":
    # Load topology data from a YAML file
    topology_file = os.path.join(os.path.dirname(__file__), 'topology.yml')
    topology_data = load_topology(topology_file)

    # Create and visualize the topology graph
    G = create_topology_graph(topology_data)
    visualize_topology(G)
----------------------------------------