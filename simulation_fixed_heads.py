from node import Node
import numpy as np 
import matplotlib.pyplot as plt
import pickle
import random

def generate_topology_with_fixed_heads(N, R, x1=0, x2=100, y1=0, y2=100, sink_center=(50,50)):
    np.random.seed(70)
    potential_points = N**2
    X = np.linspace(x1, x2, potential_points)
    Y = np.linspace(y1, y2, potential_points)
    
    ind_x = np.random.choice(potential_points, size=N, replace=False)
    ind_y = np.random.choice(potential_points, size=N, replace=False)

    X = X[ind_x]
    Y = Y[ind_y]
    
    nodes = [Node(X[i], Y[i]) for i in range(len(X))]
    
    angles = np.linspace(0, 2 * np.pi, 6)[:-1]  # 5 equally spaced angles
    cluster_heads = []
    
    for angle in angles:
        x = sink_center[0] + R * np.cos(angle)
        y = sink_center[1] + R * np.sin(angle)
        head = Node(x, y)
        head.energy = 4  # Set initial energy to 4 joules
        head.MODE = "head"  # Set as permanent cluster head
        cluster_heads.append(head)
    
    groups = {i: [] for i in range(5)}  # 5 fixed groups
    
    for node in nodes:
        min_dist = float('inf')
        nearest_head_idx = -1
        
        for i, head in enumerate(cluster_heads):
            dist = node.distance_to_node(head)
            if dist < min_dist:
                min_dist = dist
                nearest_head_idx = i
        
        groups[nearest_head_idx].append(node)
    
    return nodes, cluster_heads, groups

def graph_topology_with_heads(nodes, cluster_heads, sink_x, sink_y, sim_case, energies=None, cycle=None):
    plt.figure(figsize=(10,10))
    
    # Plot regular nodes
    X_coords = [node.x for node in nodes]
    y_coords = [node.y for node in nodes]
    
    if energies is not None:
        scatter = plt.scatter(X_coords, y_coords, c=energies, cmap='viridis', s=100, edgecolor='k')
        cbar = plt.colorbar(scatter)
        cbar.set_label('Energy')
    else:
        plt.scatter(X_coords, y_coords, label="sensor", marker='x')
    
    # Plot cluster heads
    head_x = [head.x for head in cluster_heads]
    head_y = [head.y for head in cluster_heads]
    plt.scatter(head_x, head_y, c='red', marker='^', s=200, label='Cluster Heads')
    
    # Plot sink
    plt.scatter(sink_x, sink_y, c="black", label="Sink", marker='o', s=250)
    
    # Draw circle where cluster heads are placed
    circle = plt.Circle((sink_x, sink_y), np.sqrt((head_x[0]-sink_x)**2 + (head_y[0]-sink_y)**2), 
                       fill=False, linestyle='--', color='gray')
    plt.gca().add_artist(circle)
    
    plt.xlim(0,100)
    plt.ylim(0,100)
    title = f'{sim_case} {"Energy" if energies is not None else ""} Network Topology {("after " + str(cycle)) if cycle is not None else ""}'
    plt.title(title)
    plt.xlabel('X position (m)')
    plt.ylabel('Y position (m)')
    plt.legend()
    plt.grid(True)
    plt.show()

def run_fixed_head_iteration(nodes, cluster_heads, groups, sink_x, sink_y):
    dead_count = 0
    remaining_energies = []
    
    # Process regular nodes
    for node in nodes:
        if not node.isDead():
            nearest_head = None
            min_dist = float('inf')
            
            # Find nearest active cluster head
            for head in cluster_heads:
                if not head.isDead():
                    dist = node.distance_to_node(head)
                    if dist < min_dist:
                        min_dist = dist
                        nearest_head = head
            
            if nearest_head is not None:
                node.consume_energy(nearest_head.x, nearest_head.y)
                if node.isDead():
                    dead_count += 1
            else:
                node.set_dead()
                dead_count += 1
                
        else:
            dead_count += 1
        
        remaining_energies.append(node.energy)
    
    # Process cluster heads
    for head in cluster_heads:
        if not head.isDead():
            head.consume_energy(sink_x, sink_y)
        remaining_energies.append(head.energy)
    
    return dead_count, remaining_energies

def run_fixed_head_simulation(sink_x, sink_y, N_sensors, R):
    nodes, cluster_heads, groups = generate_topology_with_fixed_heads(N_sensors, R, sink_center=(sink_x, sink_y))
    
    # Initial topology visualization
    graph_topology_with_heads(nodes, cluster_heads, sink_x, sink_y, 'Initial')
    
    dead_counts = []
    energies = []
    iter = 0
    
    while True:
        dead_count, curr_energies = run_fixed_head_iteration(nodes, cluster_heads, groups, sink_x, sink_y)
        dead_counts.append(dead_count)
        energies.append(curr_energies)
        
        # Check if all cluster heads are dead or all nodes are dead
        all_heads_dead = all(head.isDead() for head in cluster_heads)
        if all_heads_dead or dead_count == len(nodes):
            break
            
        iter += 1
    
    dead_counts = np.array(dead_counts)
    total_nodes = len(nodes)
    special_cycles = [(np.argmin(np.abs(dead_counts-x))) for x in [1, total_nodes/2, total_nodes]]
    special_values = total_nodes - dead_counts[special_cycles]
    
    return (total_nodes - np.array(dead_counts), 
            np.array(energies)[special_cycles], 
            np.array(special_cycles)+1, 
            np.array(special_values),
            nodes,
            cluster_heads)

def find_optimal_R(sink_x, sink_y, N_sensors, R_range):
    """Find optimal R by testing different radii"""
    results = []
    
    for R in R_range:
        network_lifetime, _, cycles, _, _, _ = run_fixed_head_simulation(sink_x, sink_y, N_sensors, R)
        results.append((R, len(network_lifetime)))  # Store R and network lifetime
        
    # Find R with maximum lifetime
    optimal_R = max(results, key=lambda x: x[1])
    
    # Plot results
    Rs, lifetimes = zip(*results)
    plt.figure(figsize=(10, 6))
    plt.plot(Rs, lifetimes, 'bo-')
    plt.axvline(x=optimal_R[0], color='r', linestyle='--', label=f'Optimal R = {optimal_R[0]:.1f}m')
    plt.xlabel('Radius (m)')
    plt.ylabel('Network Lifetime (cycles)')
    plt.title('Network Lifetime vs. Cluster Head Placement Radius')
    plt.grid(True)
    plt.legend()
    plt.show()
    
    return optimal_R[0]

# Run Part E with R = 25
alive_nodes, energies, cycles, values, nodes, heads = run_fixed_head_simulation(50, 50, 100, 25)
print(energies)
# Run Part F to find optimal R
# R_range = np.linspace(1, 30, 7)  # Test R values from 15m to 45m
# optimal_R = find_optimal_R(50, 50, 100, R_range)
# print(f"Optimal cluster head placement radius: {optimal_R:.1f} meters")

# # Run simulation with optimal R for comparison
# alive_nodes_optimal, energies_optimal, cycles_optimal, values_optimal, nodes_optimal, heads_optimal = run_fixed_head_simulation(50, 50, 100, optimal_R)