
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import os
import numpy as np

# Device positions and types for the topology
devices = {
    'Spine01': {'pos': (2, 8), 'type': 'spine', 'ip': '10.77.0.1'},
    'Spine02': {'pos': (6, 8), 'type': 'spine', 'ip': '10.77.0.2'},
    'Leaf01': {'pos': (1, 6), 'type': 'leaf', 'ip': '10.77.0.11'},
    'Leaf02': {'pos': (3, 6), 'type': 'leaf', 'ip': '10.77.0.12'},
    'Leaf03': {'pos': (5, 6), 'type': 'leaf', 'ip': '10.77.0.13'},
    'Leaf04': {'pos': (7, 6), 'type': 'leaf', 'ip': '10.77.0.14'},
    'Border01': {'pos': (2, 4), 'type': 'border', 'ip': '10.77.0.21'},
    'Border02': {'pos': (6, 4), 'type': 'border', 'ip': '10.77.0.22'},
    'P01': {'pos': (3, 2), 'type': 'core', 'ip': '10.77.0.31'},
    'P02': {'pos': (5, 2), 'type': 'core', 'ip': '10.77.0.32'},
    'PE01': {'pos': (4, 0), 'type': 'core', 'ip': '10.77.0.41'},
}

# Connections (edges)
edges = [
    ('Spine01', 'Leaf01'), ('Spine01', 'Leaf02'),
    ('Spine02', 'Leaf03'), ('Spine02', 'Leaf04'),
    ('Leaf01', 'Border01'), ('Leaf02', 'Border01'),
    ('Leaf03', 'Border02'), ('Leaf04', 'Border02'),
    ('Border01', 'P01'), ('Border02', 'P02'),
    ('P01', 'PE01'), ('P02', 'PE01'),
]

# Icon paths (use simple shapes if icons not available)
icon_map = {
    'spine': 'router_icon.png',
    'leaf': 'router_icon.png',
    'border': 'router_icon.png',
    'core': 'router_icon.png',
}

# Edge protocol labels
edge_labels = {
    ('Spine01', 'Leaf01'): 'OSPF/MPLS',
    ('Spine01', 'Leaf02'): 'OSPF/MPLS',
    ('Spine02', 'Leaf03'): 'OSPF/MPLS',
    ('Spine02', 'Leaf04'): 'OSPF/MPLS',
    ('Leaf01', 'Border01'): 'BGP-EVPN/VXLAN',
    ('Leaf02', 'Border01'): 'BGP-EVPN/VXLAN',
    ('Leaf03', 'Border02'): 'BGP-EVPN/VXLAN',
    ('Leaf04', 'Border02'): 'BGP-EVPN/VXLAN',
    ('Border01', 'P01'): 'MPLS/Interconnect',
    ('Border02', 'P02'): 'MPLS/Interconnect',
    ('P01', 'PE01'): 'MPLS L3VPN',
    ('P02', 'PE01'): 'MPLS L3VPN',
}
def get_icon(device_type):
    # Use a colored circle if icon file is missing
    icon_file = icon_map.get(device_type)
    if icon_file and os.path.exists(icon_file):
        return plt.imread(icon_file)
    # fallback: colored circle
    color_map = {
        'spine': 'blue', 'leaf': 'green', 'border': 'red', 'core': 'orange'
    }
    fig, ax = plt.subplots(figsize=(0.5,0.5))
    ax.add_patch(plt.Circle((0.5,0.5), 0.4, color=color_map.get(device_type, 'gray')))
    ax.axis('off')
    fig.canvas.draw()
    buf = fig.canvas.buffer_rgba()
    image = np.asarray(buf)
    plt.close(fig)
    return image

def draw_topology():
    G = nx.Graph()
    G.add_nodes_from(devices.keys())
    G.add_edges_from(edges)
    plt.figure(figsize=(10, 8))
    pos = {dev: info['pos'] for dev, info in devices.items()}
    nx.draw_networkx_edges(G, pos, width=2, edge_color='gray')
    # Draw edge labels for protocols
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=9, font_color='purple')
    for dev, info in devices.items():
        icon = get_icon(info['type'])
        imagebox = OffsetImage(icon, zoom=0.15)
        ab = AnnotationBbox(imagebox, info['pos'], frameon=False)
        plt.gca().add_artist(ab)
        plt.text(info['pos'][0], info['pos'][1]+0.4, f"{dev}\n{info['ip']}", ha='center', fontsize=10)
    plt.axis('off')
    plt.title('zwu EVPN-VXLAN Fabric Topology')
    plt.savefig('/mnt/c/Users/cathe/OneDrive/Desktop/github/ccie/ccie/documentation/design/topology.png', bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    draw_topology()
