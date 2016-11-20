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
POPULATION_COUNTER = 20
from time import time


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
        item = list(map(int, input().split(' ')))
        items[tuple(item[::-1])] = 0
    MAX_POPULATION = round(sqrt(n))
    return items, m, n


def get_population_cost(population):
    res = 0
    for item in population:
        res += sum([k[1] for k in item.keys()])
    return res


def generate_pop(items, population=[]):
    global POPULATION_COUNTER
    i = MAX_POPULATION
    while len(population) < MAX_POPULATION and i > 0:
        new_child = OrderedDict([(item, randint(0, 1)) for item in items.keys()])
        total_value = sum([sel for sel in new_child.values()])
        if new_child not in population and total_value and new_child not in GENERATIONS:
            population.append(new_child)
        else:
            i -= 1
    POPULATION_COUNTER -= 1
    if POPULATION_COUNTER == 0:
        print('20th population', population)
    return population


def fitness_function(items, m):
    """Return sum of cost for child if weight < m otherwise return 0."""
    cost = 0
    weight = 0
    for key, is_selected in items.items():
        if is_selected:
            weight += key[0]
            cost += key[1]
    res = cost if weight <= m else 0
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
    if len(GENERATIONS) < 30:
        return False
    best = sorted(
        population,
        key=lambda child: fitness_function(child, m),
        reverse=True)[0]
    selected = [item for item, sel in best.items() if sel]
    weight = sum([w for w, v in selected])
    total_value = sum([v for w, v in selected])
    if sum(best.values()) <= n and weight <= m:
        return total_value
    return False


def select_parents(population, m):
    fitness_population = sorted(
            population,
            key=lambda child: fitness_function(child, m),
            reverse=True)
    ordered_population = []
    total_cost = get_population_cost(fitness_population)
    for item in fitness_population:
        item_cost = get_population_cost([item])
        percentage = item_cost / total_cost
        rand_num = random()
        if percentage > rand_num:
            ordered_population.append(item)
    return ordered_population if ordered_population else fitness_population


def pseudo_user():
    global MAX_POPULATION
    items = OrderedDict({(2, 3): 0, (5, 1): 0, (3, 2): 0})
    m = 5
    n = 3
    MAX_POPULATION = round(sqrt(n))
    return items, m, n


def pseudo_user1():
    global MAX_POPULATION
    items = OrderedDict({
        (90, 150): 0,
        (130, 35): 0,
        (1530, 200): 0,
        (500, 160): 0,
        (150, 60): 0,
        (680, 45): 0,
        (270, 60): 0,
        (390, 40): 0,
        (230, 30): 0,
        (520, 10): 0,
        (110, 70): 0,
        (320, 30): 0,
        (240, 15): 0,
        (480, 10): 0,
        (730, 40): 0,
        (420, 70): 0,
        (430, 75): 0,
        (220, 80): 0,
        (70, 20): 0,
        (180, 12): 0,
        (40, 50): 0,
        (300, 10): 0,
        (900, 1): 0,
        (2000, 150): 0
    })
    m = 5000
    n = 24
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
        # population = sorted(
        #     population,
        #     key=lambda child: fitness_function(child, m),
        #     reverse=True)

        # selected parents
        population = select_parents(population, m)

        # the best couple of items
        population = do_crossover(population[:2])

        # Step 5
        population = generate_pop(items, population=population)

        # Step 6:
        population = mutate_population(population, m)

        total_value = is_solution(population, m, n)
        if total_value:
            print('Found solution: {}'.format(population[0]))
            return total_value

    print('No solution found...')
    return False


def main():
    # items, m, n = pseudo_user1()
    items, m, n = read_user_input()
    start = time()
    print(knapsack(items, m, n))
    print((time() - start)*1000, 's')

if __name__ == '__main__':
    main()
