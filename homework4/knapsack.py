from random import randint, random  # noqa
from math import sqrt
from collections import OrderedDict
from copy import deepcopy
# M: max weight
# N: max count
# v want ot be max
MAX_POPULATION = 100
MUTATION_PROPABILITY = 0.05
MAX_ITERATIONS = 1000
GENERATIONS = []


def read_user_input():  # noqa
    global MAX_POPULATION
    """Read user input.
    result:
    items = {
        (w1, v1): 0,  # not selected
        (w2, v2): 1,  # selected
        ... ,
        (wi, vi): 0}
    """
    m = int(input('Enter max capacity of the knapsack: M = '))
    n = int(input('Enter max count of items in knapsack: N = '))
    print('Fill in the items by entering each item (benefit, cost) on new line and numbers separated by " "(space).')  # noqa
    items = OrderedDict()
    for item in range(n):
        item = map(int, input().split(' '))
        items[tuple(item[1], item[0])] = 0
    MAX_POPULATION = round(sqrt(n))
    return items, m, n


def get_population_cost(population):
    res = 0
    for item in population:
        res += sum([k[1] for k in item.keys()])
    return res


def generate_pop(items, population=[]):
    i = MAX_POPULATION
    while len(population) < MAX_POPULATION and i > 0:
        new_child = OrderedDict([(item, randint(0, 1)) for item in items.keys()])
        total_value = sum([sel for sel in new_child.values()])
        if new_child not in population and total_value and new_child not in GENERATIONS:
            population.append(new_child)
        else:
            i -= 1
    return population


def fitness_function(items, m):
    """Return sum of weight for child or 0(if sum > m)."""
    priority = sum([key[0] for key, is_selected in items.items() if is_selected])
    res = priority if priority <= m else 0
    return res


def do_crossover(population):
    """Do crossover matching."""
    if len(population) < 2:
        return population
    first, second = population
    rand_index = randint(1, len(first))
    f_vals = list(first.values())
    s_vals = list(second.values())
    keys = list(first.keys())
    print("RAND INDEX:", rand_index)
    child1 = f_vals[0:rand_index] + s_vals[rand_index:]
    child2 = s_vals[0:rand_index] + f_vals[rand_index:]
    return [
        OrderedDict([(keys[i], child1[i]) for i in range(len(keys))]),
        OrderedDict([(keys[i], child2[i]) for i in range(len(keys))])
    ]


def mutate_population(population, m):
    best = sorted(
        population,
        key=lambda child: fitness_function(child, m),
        reverse=True)[0]
    new_population = deepcopy(population)
    for i, child in enumerate(population):
        if child == best:
            continue
        for key, sel in child.items():
            mutation_prob = random()
            if mutation_prob <= MUTATION_PROPABILITY and child != best:
                new_population[i][key] = int(not sel)
    return new_population


def is_solution(population, m, n):
    global GENERATIONS
    current_best = population[0]
    GENERATIONS.append(current_best)
    if len(GENERATIONS) < 25:
        return False
    best = sorted(
        GENERATIONS,
        key=lambda child: fitness_function(child, m),
        reverse=True)[0]
    selected = [item for item, sel in best.items() if sel]
    weight = sum([w for w, v in selected])
    total_value = sum([v for w, v in selected])
    if sum(best.values()) <= n and weight <= m:
        return total_value
    return False


def select_parents(population):
    ordered_population = []
    total_cost = get_population_cost(population)
    for item in population:
        item_cost = get_population_cost([item])
        percentage = item_cost / total_cost
        rand_num = random()
        if percentage > rand_num:
            ordered_population.append(item)
    return ordered_population


def pseudo_user():
    global MAX_POPULATION
    items = OrderedDict({(2, 3): 0, (5, 1): 0, (3, 2): 0})
    m = 5
    n = 3
    MAX_POPULATION = round(sqrt(n))
    return items, m, n


def pseudo_user1():
    global MAX_POPULATION
    items = OrderedDict({(1, 11): 0, (21, 31): 0, (23, 33): 0, (33, 43): 0, (43, 53): 0, (45, 55): 0, (55, 65): 0})
    m = 110
    n = 7
    MAX_POPULATION = n
    return items, m, n


def pseudo_user2():
    global MAX_POPULATION
    items = OrderedDict({(3, 2): 0, (1, 5): 0, (2, 3): 0})
    m = 5
    n = 3
    MAX_POPULATION = n
    return items, m, n


def knapsack(items, m, n):
    """Define program flow.
    1. Read user input and create initial item with zeroes
    2. Generate population
    3. Sort population
    4. Make crossover with first 2 of the sorted population and append children to the population
    5. Generate up to MAX_POPULATION count new children and append them in population
    6. Choose 1 item from population on random. This item should be selected/unselected from the knapsack.
    DO NOT override the best item.

    7. CYCLE Again
    """
    population = generate_pop(items, population=[])
    i = 0
    while i < MAX_ITERATIONS:
        # sorted population
        population = sorted(
            population,
            key=lambda child: fitness_function(child, m),
            reverse=True)
        total_value = is_solution(population, m, n)
        if total_value:
            print('Found solution: {}'.format(population[0]))
            return total_value

        selected_items = select_parents(population)

        # the best couple of items
        population = do_crossover(selected_items[:2])

        # Step 5
        population = generate_pop(items, population=population)

        # Step 6:
        population = mutate_population(population, m)

    print('No solution found...')
    return False


def main():
    items, m, n = pseudo_user2()
    print(knapsack(items, m, n))


if __name__ == '__main__':
    main()
