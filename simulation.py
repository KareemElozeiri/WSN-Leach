from node import Node
import numpy as np 
import matplotlib.pyplot as plt
import pickle

def generate_topology(N,C, x1=0, x2=100, y1=0, y2=100, center=(50,50)):
    np.random.seed(70)
    potential_points = N**2
    X = np.linspace(x1, x2, potential_points)
    Y = np.linspace(y1, y2, potential_points)
    
    ind_x = np.random.choice(potential_points, size=N, replace=False)
    ind_y = np.random.choice(potential_points, size=N, replace=False)

    X = X[ind_x]
    Y = Y[ind_y]
    
    nodes = [Node(X[i], Y[i]) for i in range(len(X))]
    
    center_x, center_y = center
    angles = np.arctan2([node.y - center_y for node in nodes], [node.x - center_x for node in nodes])
    angles = (angles + 2 * np.pi) % (2 * np.pi) 
    
    sectors = np.linspace(0, 2 * np.pi, C + 1)
    groups = {i: [] for i in range(C)}
    for i, angle in enumerate(angles):
        for j in range(C):
            if sectors[j] <= angle < sectors[j + 1]:
                groups[j].append(nodes[i])
                break
    
    return nodes, groups, center

def graph_topology(nodes, sink_x, sink_y,sim_case, energies = None, cycle=None):
    X_coords = [node.x for node in nodes]
    y_coords = [node.y for node in nodes]
    
    fig = plt.figure(figsize=(10,10))
    if energies is not None:
        # plt.figure(figsize=(10, 8))
        scatter = plt.scatter(X_coords, y_coords, c=energies, cmap='viridis', s=100, edgecolor='k')
        cbar = plt.colorbar(scatter)
        cbar.set_label('Energy')
    else:
        plt.scatter(X_coords,y_coords, label="sensor", marker='x')
        
    
    plt.scatter(sink_x, sink_y, cmap="red", label="Sink", marker='o', s=250)
    plt.xlim(0,100)
    if sim_case == 'Out':
        plt.ylim(0,250)
    else:
        plt.ylim(0,100)
    title = f'{sim_case} {"Energy" if energies is not None else ""} Network Topology {("after" + cycle) if cycle is not None else ""}'
    plt.title(title)

    # title = f'{sim_case}_Topology'
    
        
    plt.xlabel('X position (m)')
    plt.ylabel('Y position (m)')
    plt.legend()
    plt.show()
    # fig.savefig(f'Figures//{sim_case}//{title}.jpg')

    # with open(f'Figures//{sim_case}//{title}.fig', 'wb') as fig_file:
    #     pickle.dump(fig, fig_file)

def graph_grpups(groups,center,C):
    colors = ['red', 'blue', 'green', 'purple', 'orange']
    plt.figure(figsize=(10, 10))
    center_x, center_y = center

    for group_id, cluster_nodes in groups.items():
        x_coords = [node.x for node in cluster_nodes]
        y_coords = [node.y for node in cluster_nodes]
        plt.scatter(x_coords, y_coords, color=colors[group_id], label=f'Group {group_id}')

    angles = np.linspace(0, 2 * np.pi, C + 1)
    for angle in angles:
        x_boundary = [center_x, center_x + 100 * np.cos(angle)]
        y_boundary = [center_y, center_y + 100 * np.sin(angle)]
        plt.plot(x_boundary, y_boundary, color='gray', linestyle='--')

    plt.scatter(center_x, center_y, color='black', label='Center')
    plt.title("Nodes Divided into Groups")
    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.legend()
    plt.xlim(0, 100)
    plt.ylim(0, 100)
    plt.grid(alpha=0.5)
    plt.axis('equal')
    plt.show()


def elect_cluster_head(groups,x_s,y_s):
    for group in groups:
        group_candidates = []
        for node in group:
            if node.energy() >= node.calculate_energy_head(x_s,y_s):
                group_candidates.append(node)
                            
    pass 

def run_iteration(nodes,groups, sink_x, sink_y, R, im_text = 'Given criteria'):
    dead_count = 0
    remaining_energies = np.zeros(len(nodes))

    return dead_count, remaining_energies

def run_simulation(sink_x, sink_y, N_sensors,sim_case,R,im_criteria, C=5):
    
    nodes, groups, center = generate_topology(N_sensors, C)

    graph_topology(nodes, 50, 50,'', energies = None, cycle=None)
    graph_grpups(groups,(sink_x,sink_y),C)
    
    pass
    dead_counts = []
    energies = []
    
    while True:
        dead_count, curr_energies = run_iteration(nodes, sink_x, sink_y,R, im_criteria)
        dead_counts.append(dead_count)
        energies.append(curr_energies)

        if dead_count == len(nodes):
            break
    
    dead_counts = np.array(dead_counts)
    special_cycles = [(np.argmin(np.abs(dead_counts-x))) for x in [1,N_sensors/2,N_sensors]] #first, half, last
    special_values = len(nodes) - dead_counts[special_cycles] # Corresponding Values, Cuz they're not necessarily 1,50,100 (Maybe more than one died at the same cycled)
    
    return len(nodes) - np.array(dead_counts), np.array(energies)[special_cycles], np.array(special_cycles)+1, np.array(special_values),nodes
    # In the prev line, returned special_cycles + 1 , to start at cycle 1 not 0
    
run_simulation(50,50, 100,'sim_case',30,'Given', 5)