# -*- coding: utf-8 -*-
"""
Created on Fri Aug 30 18:39:47 2024

@author: pablo
"""

import random


# Function to generate fixed-size sets with constraints
def generate_fixed_size_sets(num_sets, num_elements, constraint='unconstrained', weighted_numbers=None, weight_factor=1):
    available_numbers = list(range(num_sets))
    list_of_sets = []

    # Adjust the pool of numbers for weighted generation
    if constraint == 'weighted' and weighted_numbers:
        weighted_pool = []
        for number in available_numbers:
            if number in weighted_numbers:
                weighted_pool.extend([number] * weight_factor)
            else:
                weighted_pool.append(number)
    else:
        weighted_pool = available_numbers

    for i in range(num_sets):
        while True:
            random_numbers = random.sample(weighted_pool, num_elements)
            if i in random_numbers:
                random_numbers = [num if num != i else random.choice([n for n in weighted_pool if n != i]) for num in random_numbers]

            if constraint == 'regular_uniqueness' and random_numbers in list_of_sets:
                continue
            if constraint == 'strict_uniqueness' and any(set(random_numbers) == set(existing_set) for existing_set in list_of_sets):
                continue

            list_of_sets.append(random_numbers)
            break

    return list_of_sets

# Function to generate irregular-size sets with constraints
def generate_irregular_size_sets(num_sets, min_elements, max_elements, constraint='unconstrained', weighted_numbers=None, weight_factor=1):
    available_numbers = list(range(num_sets))
    list_of_sets = []

    if constraint == 'weighted' and weighted_numbers:
        weighted_pool = []
        for number in available_numbers:
            if number in weighted_numbers:
                weighted_pool.extend([number] * weight_factor)
            else:
                weighted_pool.append(number)
    else:
        weighted_pool = available_numbers

    for i in range(num_sets):
        while True:
            num_elements = random.randint(min_elements, max_elements)
            random_numbers = random.sample(weighted_pool, num_elements)
            if i in random_numbers:
                random_numbers = [num if num != i else random.choice([n for n in weighted_pool if n != i]) for num in random_numbers]

            if constraint == 'regular_uniqueness' and random_numbers in list_of_sets:
                continue
            if constraint == 'strict_uniqueness' and any(set(random_numbers) == set(existing_set) for existing_set in list_of_sets):
                continue

            list_of_sets.append(random_numbers)
            break

    return list_of_sets

# Function to generate additional sets in continuous generation
def continuous_generation(existing_sets, num_new_sets, num_elements=None, min_elements=None, max_elements=None, constraint='unconstrained', weighted_numbers=None, weight_factor=1):
    num_sets = len(existing_sets)
    new_sets = []

    # Combine existing numbers with new indices for continuous generation
    available_numbers = list(range(num_sets + num_new_sets))

    # Adjust the pool of numbers for weighted generation
    if constraint == 'weighted' and weighted_numbers:
        weighted_pool = []
        for number in available_numbers:
            if number in weighted_numbers:
                weighted_pool.extend([number] * weight_factor)
            else:
                weighted_pool.append(number)
    else:
        weighted_pool = available_numbers

    # Determine element range based on fixed or irregular size
    if num_elements:
        for i in range(num_sets, num_sets + num_new_sets):
            while True:
                random_numbers = random.sample(weighted_pool, num_elements)
                if i in random_numbers:
                    random_numbers = [num if num != i else random.choice([n for n in weighted_pool if n != i]) for num in random_numbers]

                if constraint == 'regular_uniqueness' and random_numbers in existing_sets + new_sets:
                    continue
                if constraint == 'strict_uniqueness' and any(set(random_numbers) == set(existing_set) for existing_set in existing_sets + new_sets):
                    continue

                new_sets.append(random_numbers)
                break

    else:
        for i in range(num_sets, num_sets + num_new_sets):
            while True:
                num_elements = random.randint(min_elements, max_elements)
                random_numbers = random.sample(weighted_pool, num_elements)
                if i in random_numbers:
                    random_numbers = [num if num != i else random.choice([n for n in weighted_pool if n != i]) for num in random_numbers]

                if constraint == 'regular_uniqueness' and random_numbers in existing_sets + new_sets:
                    continue
                if constraint == 'strict_uniqueness' and any(set(random_numbers) == set(existing_set) for existing_set in existing_sets + new_sets):
                    continue

                new_sets.append(random_numbers)
                break

    return existing_sets + new_sets

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

    # Print 0th level and iteration explicitly
    output = []
    output.append(f"\nLevel 0: {marked_level_0[0]}; {marked_level_0[1]}")
    output.append(f"0th iteration repetitions: {marked_level_0[0]}; {marked_level_0[1]}")
    
    current_a = sets_dict[set_num_a]
    current_b = sets_dict[set_num_b]

    level = 1
    while True:
        output.append(f"\nLevel {level}: {current_a}; {current_b}")
        level_elements = current_a + current_b
        general_list.append(level_elements)

        # Print whether weak or strong differentiation is applied
        if differentiation == 'weak':
            output.append("Applying Weak Differentiation")
            cross_repeats = set()
            for element in level_elements:
                if level_elements.count(element) > 1:
                    cross_repeats.add(element)
                for element_prev in general_list[:-1]:
                    if element in element_prev:
                        cross_repeats.add(element)
        else:
            output.append("Applying Strong Differentiation")
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

        # Prepare for the next level
        next_a = []
        next_b = []
        for num in current_a:
            next_a.extend(sets_dict.get(num, [num]))
        for num in current_b:
            next_b.extend(sets_dict.get(num, [num]))

        current_a = next_a
        current_b = next_b
        level += 1

# Function to compare sets based on given parameters
def compare_sets(num_sets, num_elements, differentiation='weak', irregular=False, min_elements=None, max_elements=None,
                 constraint='unconstrained', weighted_numbers=None, weight_factor=1, continuous=False,
                 num_new_sets=0, comparison_strategy='one_vs_all'):
    if irregular:
        sets_list = generate_irregular_size_sets(num_sets, min_elements, max_elements, constraint=constraint, weighted_numbers=weighted_numbers, weight_factor=weight_factor)
    else:
        sets_list = generate_fixed_size_sets(num_sets, num_elements, constraint=constraint, weighted_numbers=weighted_numbers, weight_factor=weight_factor)

    if continuous:
        sets_list = continuous_generation(sets_list, num_new_sets, num_elements=num_elements, min_elements=min_elements, max_elements=max_elements, constraint=constraint, weighted_numbers=weighted_numbers, weight_factor=weight_factor)

    sets_dict = {i: sets_list[i] for i in range(len(sets_list))}

    output = []

    output.append("Generated Sets:")
    for idx, numbers_set in enumerate(sets_list):
        output.append(f"Set {idx}: {numbers_set}")

    results = []
    data_output = []

    if comparison_strategy == 'one_vs_all':
        # Compare Set 1 with all other sets
        for i in range(2, len(sets_list)):
            output.append(f"\nComparing Set 1 with Set {i}:")
            points, details = process_levels_until_c(1, i, sets_dict, differentiation=differentiation)
            results.append(points)
            data_output.append(f"Set 1 vs Set {i}: Total Points = {points}")
            output.append(details)
    elif comparison_strategy == 'all_vs_all':
        # Compare all sets with each other
        for i in range(1, len(sets_list)):
            for j in range(i + 1, len(sets_list)):
                output.append(f"\nComparing Set {i} with Set {j}:")
                points, details = process_levels_until_c(i, j, sets_dict, differentiation=differentiation)
                results.append((i, j, points))
                data_output.append(f"Set {i} vs Set {j}: Total Points = {points}")
                output.append(details)

    if comparison_strategy == 'one_vs_all':
        x_vals = list(range(2, len(sets_list)))
        y_vals = results
        title = f'Set 1 vs Other Sets ({differentiation.capitalize()} Differentiation)'
    else:
        x_vals = [f"{x[0]}-{x[1]}" for x in results]
        y_vals = [x[2] for x in results]
        title = f'All Sets vs All Sets ({differentiation.capitalize()} Differentiation)'

    return '\n'.join(output), '\n'.join(data_output), x_vals, y_vals, title

# Function to save the results to a text file
def save_results_to_file(filename, content):
    with open(filename, 'a') as file:
        file.write(content)
        file.write("\n" + "="*80 + "\n")

# Function to save data output for further analysis in a structured format
def save_data_output_to_file(filename, params_description, comparison_strategy, x_vals, y_vals):
    with open(filename, 'a') as file:
        file.write(params_description)
        if comparison_strategy == 'one_vs_all':
            file.write("Set vs Rest:\n")
            for x, y in zip(x_vals, y_vals):
                file.write(f"Set 1 vs Set {x}: {y}\n")
        else:
            file.write("All vs All:\n")
            for x, y in zip(x_vals, y_vals):
                file.write(f"Comparison {x}: {y}\n")
        file.write("\n" + "="*80 + "\n")

# Function to run all comparisons for a specified number of iterations
def run_comparisons(iterations=1):
    constraints = ['weighted', 'unconstrained', 'regular_uniqueness', 'strict_uniqueness']
    differentiations = ['weak', 'strong']
    sizes = ['fixed', 'irregular']
    comparison_strategies = ['one_vs_all', 'all_vs_all']
    continuous_options = [True, False]

    num_sets = 10  # Number of sets
    num_elements = 3  # Number of elements per set
    min_elements = 2
    max_elements = 5
    weighted_values = [2, 5]  # Values to weight more heavily
    weight_factor = 10  # Weight factor for weighted constraint
    num_new_sets = 5  # Number of new sets to add in continuous generation

    log_filename = "set_comparison_results.txt"
    data_filename = "set_points_data.txt"

    for iteration in range(iterations):
        print(f"\n--- Iteration {iteration + 1}/{iterations} ---\n")
        for constraint in constraints:
            for differentiation in differentiations:
                for size in sizes:
                    for comparison_strategy in comparison_strategies:
                        for continuous in continuous_options:
                            params_description = (f"Iteration {iteration + 1}, Running with {constraint}, {differentiation} differentiation, "
                                                  f"{size} size, {comparison_strategy}, continuous={continuous}\n")
                            print(params_description)
                            if size == 'fixed':
                                result, data_output, x_vals, y_vals, title = compare_sets(
                                    num_sets, num_elements, differentiation=differentiation, irregular=False,
                                    constraint=constraint, weighted_numbers=weighted_values, weight_factor=weight_factor,
                                    continuous=continuous, num_new_sets=num_new_sets, comparison_strategy=comparison_strategy)
                            else:
                                result, data_output, x_vals, y_vals, title = compare_sets(
                                    num_sets, num_elements, differentiation=differentiation, irregular=True,
                                    min_elements=min_elements, max_elements=max_elements, constraint=constraint,
                                    weighted_numbers=weighted_values, weight_factor=weight_factor, continuous=continuous,
                                    num_new_sets=num_new_sets, comparison_strategy=comparison_strategy)

                            save_results_to_file(log_filename, params_description + result)
                            save_data_output_to_file(data_filename, params_description, comparison_strategy, x_vals, y_vals)

# Example of running the comparisons 5 times
run_comparisons(iterations=5)