from simulation import run_simulation, graph_topology
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pickle
from simulation_fixed_heads import run_fixed_head_simulation, graph_topology_with_heads, find_optimal_R

N_SENSORS = 100 # No. of Sensors



def plot_dead_counts(dead_counts,special_cycles,special_values,sim_case):
    X_coords = range(1,len(dead_counts)+1)
    y_coords = dead_counts
    
    fig = plt.figure(figsize=(10,10))
    plt.plot(X_coords,y_coords)
    plt.scatter(special_cycles,special_values,marker='X',color = 'red')
    cycles = ['the First Node','Half of the Nodes', 'the Last Node']
    for i, (x, y) in enumerate(zip(special_cycles, special_values)):
        plt.text(x, y, f'  Death of {cycles[i]} \n  at cycle {x}', fontsize=10, verticalalignment='bottom', color='black')

    
    title = f'{sim_case}_Active Counts per cycle'
    plt.title(title)
    plt.xlabel('Cycle')
    plt.ylabel('Active Node Count')
    plt.show()
    # fig.savefig(f'Figures//{sim_case}//{im_text},{title}.jpg')

    # with open(f'Figures//{sim_case}//{im_text},{title}.fig', 'wb') as fig_file:
    #     pickle.dump(fig, fig_file)
    

def plot_remaining_energies(rem_energies,sim_case,nodes):
    cycles = [f'After {d} Death' for d in ['First', 'Half Nodes', 'Last']]
    for i in range(len(rem_energies)):
        # X_coords = np.linspace(1, 101, len(rem_energies[i]))
        X_coords = range(1,len(rem_energies[i])+1) #Cycle
        y_coords = rem_energies[i]
        
        # Scatter plot
        fig = plt.figure(figsize=(14, 6))
        
        # Scatter plot on the left
        plt.subplot(1, 2, 1)
        # plt.scatter(X_coords, y_coords, marker='x', color='blue', alpha=0.6)
        plt.bar(X_coords, y_coords, color='blue', alpha=0.6)
        plt.xlim(0, 100)
        plt.ylim(0, 2)
        title = f'{sim_case_str} - Remaining Node Energies {cycles[i]}'
        plt.title(title)
        plt.xlabel('Node')
        plt.ylabel('Energy (Joule)')
        plt.grid(True)
        
        # Distribution plot (histogram + KDE) on the right
        plt.subplot(1, 2, 2)
        sns.histplot(y_coords, bins=20, kde=True, color='purple', alpha=0.6)
        plt.xlim(0, 2)
        plt.title(f'{sim_case_str} - Energy Distribution {cycles[i]}')
        plt.xlabel('Energy (Joule)')
        plt.ylabel('Density')
        plt.show()
        
        # title = f'{sim_case} {im_text} {title}'
        # fig.savefig(f'Figures//{sim_case}//{im_text},{title}.jpg')
        # fig_path = f'Figures//{sim_case}//{im_text},{title}.fig'
        # with open(fig_path, 'wb') as fig_file:
        #     pickle.dump(fig, fig_file)
        #     plt.tight_layout()
        #     plt.show()
        if sim_case_str == "Rotation":
            graph_topology(nodes, s[0],s[1],sim_case_str,rem_energies[i],cycles[i])

if __name__ == "__main__":
    simulations = [(50,50)]
    sim_case = 1
    C = 5

    for s in simulations:

        sim_case_str = 'Rotation'
        dead_counts , rem_energies, special_cycles, special_values, nodes = run_simulation(s[0],s[1], N_SENSORS,sim_case_str, C)
        plot_dead_counts(dead_counts,special_cycles,special_values,sim_case_str) 
        plot_remaining_energies(rem_energies,sim_case_str, nodes)
        
        sim_case_str = 'optimum C'
        best_remaining_energies = run_simulation(s[0],s[1], N_SENSORS,sim_case_str, C)
        plot_remaining_energies([best_remaining_energies, best_remaining_energies, best_remaining_energies],sim_case_str, nodes)
        
        sim_case_str = 'Fixed'
        dead_counts , rem_energies, special_cycles, special_values, nodes, cluster_heads = run_fixed_head_simulation(s[0],s[1], N_SENSORS,R = 25)
        plot_dead_counts(dead_counts,special_cycles,special_values,sim_case_str) 
        plot_remaining_energies(rem_energies,sim_case_str, nodes.extend(cluster_heads))

        R_range = np.linspace(1, 30, 7)  # Test R values from 15m to 45m
        optimal_R = find_optimal_R(50, 50, 100, R_range)

        



