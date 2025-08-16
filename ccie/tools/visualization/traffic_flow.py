FILE: /ccie/ccie/tools/visualization/traffic_flow.py
----------------------------------------
#!/usr/bin/env python3
"""
Script: traffic_flow.py
Purpose: Analyze and visualize traffic flow in the network.
Author: zwu Network Automation Team
Date: [Date]
"""

import matplotlib.pyplot as plt
import networkx as nx

def create_traffic_flow_graph(traffic_data):
    """
    Create a directed graph to represent traffic flow.

    Parameters:
    traffic_data (dict): A dictionary where keys are tuples (source, destination)
                         and values are the traffic volume between them.

    Returns:
    G (networkx.DiGraph): A directed graph representing the traffic flow.
    """
    G = nx.DiGraph()

    for (src, dst), volume in traffic_data.items():
        G.add_edge(src, dst, weight=volume)

    return G

def visualize_traffic_flow(G):
    """
    Visualize the traffic flow graph.

    Parameters:
    G (networkx.DiGraph): The directed graph representing traffic flow.
    """
    pos = nx.spring_layout(G)
    weights = nx.get_edge_attributes(G, 'weight').values()

    plt.figure(figsize=(12, 8))
    nx.draw(G, pos, with_labels=True, node_size=2000, node_color='lightblue', font_size=10, font_weight='bold', arrows=True)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G, 'weight'))
    plt.title("Network Traffic Flow Visualization")
    plt.show()

if __name__ == "__main__":
    # Example traffic data
    traffic_data = {
        ('Router1', 'Router2'): 100,
        ('Router2', 'Router3'): 150,
        ('Router1', 'Router3'): 200,
        ('Router3', 'Router4'): 50,
    }

    # Create and visualize the traffic flow graph
    traffic_flow_graph = create_traffic_flow_graph(traffic_data)
    visualize_traffic_flow(traffic_flow_graph)
----------------------------------------