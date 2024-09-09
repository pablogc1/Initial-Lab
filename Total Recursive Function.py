# -*- coding: utf-8 -*-
"""
Created on Sat Aug 31 14:05:11 2024

@author: pablo
"""


import numpy as np

# Function to generate sets using a custom recursive function
def generate_sets(start_num, iterations, f):
    sets_dict = {}
    to_process = [(start_num, start_num + 1, f(start_num + 1))]  # Initialize with the first set
    seen = set()

    for _ in range(iterations):
        if not to_process:
            break
        s, s_plus_1, f_s_plus_1 = to_process.pop(0)
        sets_dict[s] = [s_plus_1, f_s_plus_1]

        if s_plus_1 not in seen:
            to_process.append((s_plus_1, s_plus_1 + 1, f(s_plus_1 + 1)))
            seen.add(s_plus_1)
        
        if f_s_plus_1 not in seen:
            to_process.append((f_s_plus_1, f(f_s_plus_1 + 1), f(f(f_s_plus_1 + 1))))
            seen.add(f_s_plus_1)

    return sets_dict

# Function to mark repeated elements with "(c)"
def mark_repeats_with_c(elements, repeated_elements):
    return [f"{el}(c)" if el in repeated_elements else str(el) for el in elements]

# Function to process levels and apply differentiation (weak or strong)
def process_levels_until_c(set_num_a, set_num_b, sets_dict, differentiation='weak'):
    general_list = []
    marked_levels = []

    def find_cross_repeats(current_a, current_b, all_previous_elements):
        """Find elements that are repeated across the left and right sides."""
        cross_repeats = set()
        for el in current_a:
            if el in current_b:
                cross_repeats.add(el)
            for level in all_previous_elements:
                if differentiation == 'strong' and el in level[len(level)//2:]:
                    cross_repeats.add(el)
        
        for el in current_b:
            for level in all_previous_elements:
                if differentiation == 'strong' and el in level[:len(level)//2]:
                    cross_repeats.add(el)
        
        return cross_repeats

    level_0_elements = [set_num_a, set_num_b]
    general_list.append(level_0_elements)
    
    marked_level_0 = mark_repeats_with_c(level_0_elements, set())
    marked_levels.append(marked_level_0)

    output = []
    output.append(f"\nLevel 0: {marked_level_0[0]}; {marked_level_0[1]}")
    output.append(f"0th iteration repetitions: {marked_level_0[0]}; {marked_level_0[1]}")
    
    current_a = sets_dict.get(set_num_a, [str(set_num_a)])
    current_b = sets_dict.get(set_num_b, [str(set_num_b)])

    undeveloped_elements = set()
    level = 1
    while True:
        output.append(f"\nLevel {level}: {current_a}; {current_b}")
        level_elements = current_a + current_b
        general_list.append(level_elements)

        if differentiation == 'weak':
            cross_repeats = set()
            for element in level_elements:
                if level_elements.count(element) > 1:
                    cross_repeats.add(element)
                for element_prev in general_list[:-1]:
                    if element in element_prev:
                        cross_repeats.add(element)
        else:
            cross_repeats = find_cross_repeats(current_a, current_b, general_list[:-1])

        marked_level_left = mark_repeats_with_c(current_a, cross_repeats)
        marked_level_right = mark_repeats_with_c(current_b, cross_repeats)

        for i in range(len(marked_levels)):
            left_size = len(general_list[i]) // 2
            marked_levels[i] = (
                mark_repeats_with_c(general_list[i][:left_size], cross_repeats) +
                mark_repeats_with_c(general_list[i][left_size:], cross_repeats)
            )

        marked_levels.append(marked_level_left + marked_level_right)

        output.append(f"{level}th iteration repetitions:")
        output.append(f"{', '.join(marked_level_left)} ; {', '.join(marked_level_right)}")

        for i in range(level + 1):
            left_size = len(marked_levels[i]) // 2
            if all("(c)" in el for el in marked_levels[i][:left_size]) or all("(c)" in el for el in marked_levels[i][left_size:]):
                output.append(f"\nStopping at Level {level} because one side is fully canceled.")
                total_points = 0
                for j in range(level + 1):
                    points = sum(el.count("(c)") for el in marked_levels[j])
                    total_points += points * j
                output.append(f"Total points: {total_points}")
                return total_points, '\n'.join(output)

        next_a = []
        next_b = []
        for num in current_a:
            next_a.extend(sets_dict.get(num, [str(num)]))
        for num in current_b:
            next_b.extend(sets_dict.get(num, [str(num)]))

        current_a = next_a
        current_b = next_b
        level += 1

        # Convert undeveloped elements to integers before adding to the set
        for el in current_a + current_b:
            try:
                undeveloped_elements.add(int(el))
            except ValueError:
                undeveloped_elements.add(el)

# Function to expand undeveloped elements in sets_dict
def expand_undeveloped_elements(undeveloped_elements, sets_dict, f, iterations=5):
    for el in undeveloped_elements:
        if isinstance(el, int):  # Ensure `el` is an integer
            s_plus_1 = el + 1
            f_s_plus_1 = f(el + 1)
            sets_dict[el] = [s_plus_1, f_s_plus_1]
            # Develop further if necessary
            to_process = [(s_plus_1, s_plus_1 + 1, f(s_plus_1 + 1)),
                          (f_s_plus_1, f(f_s_plus_1 + 1), f(f(f_s_plus_1 + 1)))]
            for _ in range(iterations):
                if not to_process:
                    break
                s, s_plus_1, f_s_plus_1 = to_process.pop(0)
                if s not in sets_dict:
                    sets_dict[s] = [s_plus_1, f_s_plus_1]
                    to_process.append((s_plus_1, s_plus_1 + 1, f(s_plus_1 + 1)))
                    to_process.append((f_s_plus_1, f(f_s_plus_1 + 1), f(f(f_s_plus_1 + 1))))


# Function to select and compare a set with others
def select_and_compare(sets_dict, selected_set, f, iterations=5, differentiation='weak'):
    output = []
    output.append(f"\nComparing Set {selected_set} with other sets:")
    results = []
    compared_sets = []

    for set_num_b in list(sets_dict.keys()):  # Compare with all other sets
        if selected_set != set_num_b:
            output.append(f"\nComparing Set {selected_set} with Set {set_num_b}:")
            points, output_details = process_levels_until_c(selected_set, set_num_b, sets_dict, differentiation)
            results.append((set_num_b, points))
            compared_sets.append(set_num_b)

            output.append(output_details)
            
            undeveloped_elements = {int(el) for el in output_details.split() if el.isdigit()}
            if undeveloped_elements:
                output.append("\nExpanding undeveloped elements...")
                expand_undeveloped_elements(undeveloped_elements, sets_dict, f, iterations)
                output.append("\nRe-running the comparison after expanding undeveloped elements:")
                points, new_output_details = process_levels_until_c(selected_set, set_num_b, sets_dict, differentiation)
                output.append(new_output_details)

    # Sort results by set number for plotting
    results.sort(key=lambda x: x[0])
    x_values = [set_num for set_num, _ in results]
    y_values = [points for _, points in results]

    # Return both results and detailed output
    return results, x_values, y_values, '\n'.join(output)

# Function to save the results to a text file
def save_results_to_file(filename, content):
    with open(filename, 'a') as file:
        file.write(content)
        file.write("\n" + "="*80 + "\n")

# Function to save data output for further analysis in a structured format
def save_data_output_to_file(filename, params_description, x_vals, y_vals):
    with open(filename, 'a') as file:
        file.write(params_description)
        file.write("Set vs Rest:\n")
        for x, y in zip(x_vals, y_vals):
            file.write(f"Set 1 vs Set {x}: {y}\n")
        file.write("\n" + "="*80 + "\n")

# Function to run comparisons for multiple iterations with both weak and strong differentiation
def run_comparisons(iterations_range, f=None):
    log_filename = "recursive_function_results.txt"
    data_filename = "recursive_function_data.txt"

    for iterations in iterations_range:
        for differentiation in ['weak', 'strong']:
            print(f"Running comparison for {iterations} iterations with {differentiation} differentiation...")
            sets_dict = generate_sets(start_num=1, iterations=iterations, f=f)
            results, x_vals, y_vals, detailed_output = select_and_compare(
                sets_dict, selected_set=1, f=f, iterations=iterations, differentiation=differentiation)

            # Save results and data output to files
            params_description = f"Iterations={iterations}, {differentiation.capitalize()} Differentiation\n"
            save_results_to_file(log_filename, params_description + detailed_output)
            save_data_output_to_file(data_filename, params_description, x_vals, y_vals)

# Example of using a custom function
def custom_function(x):
    return np.sin(x)  # You can replace this with any function you like

# Run comparisons with the custom function, varying iterations, and other parameters
run_comparisons(iterations_range=[10, 20, 50], f=custom_function)
