# -*- coding: utf-8 -*-
"""
Created on Fri Aug 30 14:23:34 2024

@author: pablo
"""

import random
import matplotlib.pyplot as plt

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

            if constraint == 'uniqueness' and random_numbers in list_of_sets:
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

            if constraint == 'uniqueness' and random_numbers in list_of_sets:
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

    # Determine element range based on fixed or irregular size
    if num_elements:
        for i in range(num_sets, num_sets + num_new_sets):
            while True:
                random_numbers = random.sample(available_numbers, num_elements)
                if i in random_numbers:
                    random_numbers = [num if num != i else random.choice([n for n in available_numbers if n != i]) for num in random_numbers]

                if constraint == 'uniqueness' and random_numbers in existing_sets + new_sets:
                    continue
                if constraint == 'strict_uniqueness' and any(set(random_numbers) == set(existing_set) for existing_set in existing_sets + new_sets):
                    continue

                new_sets.append(random_numbers)
                break

    else:
        for i in range(num_sets, num_sets + num_new_sets):
            while True:
                num_elements = random.randint(min_elements, max_elements)
                random_numbers = random.sample(available_numbers, num_elements)
                if i in random_numbers:
                    random_numbers = [num if num != i else random.choice([n for n in available_numbers if n != i]) for num in random_numbers]

                if constraint == 'uniqueness' and random_numbers in existing_sets + new_sets:
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
    print(f"\nLevel 0: {marked_level_0[0]}; {marked_level_0[1]}")
    print(f"0th iteration repetitions: {marked_level_0[0]}; {marked_level_0[1]}")
    
    current_a = sets_dict[set_num_a]
    current_b = sets_dict[set_num_b]

    level = 1
    while True:
        print(f"\nLevel {level}: {current_a}; {current_b}")
        level_elements = current_a + current_b
        general_list.append(level_elements)

        # Print whether weak or strong differentiation is applied
        if differentiation == 'weak':
            print("Applying Weak Differentiation")
            cross_repeats = set()
            for element in level_elements:
                if level_elements.count(element) > 1:
                    cross_repeats.add(element)
                for element_prev in general_list[:-1]:
                    if element in element_prev:
                        cross_repeats.add(element)
        else:
            print("Applying Strong Differentiation")
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

        print(f"{level}th iteration repetitions:")
        print(f"{', '.join(marked_level_left)} ; {', '.join(marked_level_right)}")

        for i in range(level + 1):
            left_size = len(marked_levels[i]) // 2
            if all("(c)" in el for el in marked_levels[i][:left_size]) or all("(c)" in el for el in marked_levels[i][left_size:]):
                print(f"\nStopping at Level {level} because one side is fully canceled.")
                total_points = 0
                for j in range(level + 1):
                    points = sum(el.count("(c)") for el in marked_levels[j])
                    total_points += points * j
                print(f"Total points: {total_points}")
                return total_points

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

# Function to compare Set 1 with all other sets
def compare_set_1_with_others(num_sets, num_elements, differentiation='weak', irregular=False, min_elements=None, max_elements=None, constraint='unconstrained', weighted_numbers=None, weight_factor=1, continuous=False, num_new_sets=0):
    if irregular:
        sets_list = generate_irregular_size_sets(num_sets, min_elements, max_elements, constraint=constraint, weighted_numbers=weighted_numbers, weight_factor=weight_factor)
    else:
        sets_list = generate_fixed_size_sets(num_sets, num_elements, constraint=constraint, weighted_numbers=weighted_numbers, weight_factor=weight_factor)

    if continuous:
        sets_list = continuous_generation(sets_list, num_new_sets=num_new_sets, num_elements=num_elements, min_elements=min_elements, max_elements=max_elements, constraint=constraint, weighted_numbers=weighted_numbers, weight_factor=weight_factor)

    sets_dict = {i: sets_list[i] for i in range(len(sets_list))}

    print("Generated Sets:")
    for idx, numbers_set in enumerate(sets_list):
        print(f"Set {idx}: {numbers_set}")

    results = []

    for i in range(2, len(sets_list)):
        print(f"\nComparing Set 1 with Set {i}:")
        points = process_levels_until_c(1, i, sets_dict, differentiation=differentiation)
        results.append(points)

    plt.plot(range(2, len(sets_list)), results, marker='o')
    plt.title(f'Set 1 vs Other Sets ({differentiation.capitalize()} Differentiation)')
    plt.xlabel('Set Number')
    plt.ylabel('Total Points')
    plt.grid(True)
    plt.show()

# Example usage:
num_sets = 10  # Number of sets
num_elements = 3  # Number of elements per set

# For irregular size, specify the range of elements
min_elements = 2
max_elements = 5

# Set constraints
constraint_options = ['unconstrained', 'weighted', 'uniqueness', 'strict_uniqueness']
weighted_values = [2, 5]  # Values to weight more heavily (used only if constraint_type is 'weighted')
weight_factor = 10  # How much more frequently to include weighted values

# Compare using fixed size and weak differentiation with weighted constraint
compare_set_1_with_others(num_sets, num_elements, differentiation='weak', irregular=False, constraint='weighted', weighted_numbers=weighted_values, weight_factor=weight_factor)

# Compare using irregular size and strong differentiation with uniqueness constraint
compare_set_1_with_others(num_sets, num_elements, differentiation='strong', irregular=True, min_elements=min_elements, max_elements=max_elements, constraint='uniqueness')

# Test continuous generation and differentiation
compare_set_1_with_others(num_sets, num_elements, differentiation='weak', irregular=False, constraint='weighted', weighted_numbers=weighted_values, weight_factor=weight_factor, continuous=True, num_new_sets=5)
