# -*- coding: utf-8 -*-
"""
Created on Fri Aug 30 19:17:02 2024

@author: pablo
"""

import matplotlib.pyplot as plt

def load_data(filename):
    data = []
    current_entry = None

    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()

            if "Set vs Rest:" in line or "All vs All:" in line:
                if "Set vs Rest:" in line:
                    current_entry['type'] = 'one_vs_all'
                elif "All vs All:" in line:
                    current_entry['type'] = 'all_vs_all'
                continue

            if line.startswith("Iteration"):
                iteration_info = line.split(",")[0].strip()
                num_sets_info = line.split(",")[1].strip()
                current_entry = {
                    'description': f"{iteration_info}, {num_sets_info}, {line.split('Running with')[1].strip()}",
                    'iteration': int(iteration_info.split("Iteration ")[1]),
                    'num_sets': int(num_sets_info.split("num_sets=")[1]),
                    'x_vals': [],
                    'y_vals': [],
                    'type': ''
                }
                data.append(current_entry)
                continue

            if current_entry:
                parts = line.split(": ")
                if len(parts) == 2:
                    try:
                        if current_entry['type'] == 'one_vs_all':
                            current_entry['x_vals'].append(int(parts[0].split(" ")[-1]))  
                            current_entry['y_vals'].append(int(parts[1]))
                        elif current_entry['type'] == 'all_vs_all':
                            comparison = parts[0].split("Comparison ")[1]
                            set_a, set_b = map(int, comparison.split("-"))
                            current_entry['x_vals'].append((set_a, set_b))
                            current_entry['y_vals'].append(int(parts[1]))
                    except ValueError:
                        print(f"Skipping line due to unexpected format: {line}")

    return data

def tags_match(tags, description):
    """Checks if all the selected tags are present in the description."""
    for tag in tags:
        if tag not in description:
            return False
    return True

def plot_all_vs_all(entry):
    """Plot data for the 'All vs All' type by extracting and organizing data for each set."""
    max_set = max(max(pair) for pair in entry['x_vals'])
    set_points = {i: [] for i in range(1, max_set + 1)}

    for (set_a, set_b), points in zip(entry['x_vals'], entry['y_vals']):
        set_points[set_a].append(points)
        set_points[set_b].append(points)

    for set_num, points in set_points.items():
        plt.plot(range(1, len(points) + 1), points, marker='o', label=f'Set {set_num}')

def plot_data_based_on_tags(data, selected_tags, num_sets=None, iteration=None, plot_all_num_sets=False, plot_all_iterations=False):
    plots_made = False
    for entry in data:
        if tags_match(selected_tags, entry['description']):
            if plot_all_num_sets and num_sets and entry['num_sets'] != num_sets:
                continue

            if not plot_all_num_sets and num_sets and entry['num_sets'] != num_sets:
                continue

            if plot_all_iterations or (iteration and entry['iteration'] == iteration):
                print(f"Plotting for description: {entry['description']}")
                if entry['type'] == 'all_vs_all':
                    plot_all_vs_all(entry)
                else:
                    plt.plot(entry['x_vals'], entry['y_vals'], marker='o', label=f"Iteration {entry['iteration']}")

                plots_made = True
    
    if plots_made:
        plt.title(f"{'All' if plot_all_iterations else ''} Iterations - {', '.join(selected_tags)}")
        plt.xlabel('Set Number' if entry['type'] == 'one_vs_all' else 'Comparison')
        plt.ylabel('Total Points')
        plt.grid(True)
        plt.legend()
        plt.show()
    else:
        print("No matching data found for the selected tags.")

def main():
    data_filename = "set_points_data.txt"

    data = load_data(data_filename)
    print(f"Loaded {len(data)} entries.")
    
    selected_tags = ['regular_uniqueness', 'strong', 'fixed', 'all_vs_all', 'continuous=False']  # Example tags
    
    # Example configurations
    num_sets = 10
    iteration = 3
    plot_all_num_sets = False
    plot_all_iterations = True  # Set this to True to plot all iterations

    plot_data_based_on_tags(data, selected_tags, num_sets=num_sets, iteration=iteration, plot_all_num_sets=plot_all_num_sets, plot_all_iterations=plot_all_iterations)

if __name__ == "__main__":
    main()

