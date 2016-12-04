from heapq import heappush, nlargest, heappop
from math import sqrt


def update_class(bucket, name):
    if name in bucket:
        bucket[name] += 1
    else:
        bucket[name] = 1
    return bucket


def generate_queue(item, elements, k):
    current_sum = 0
    queue = []
    most_spread_class = {}
    for element in elements:
        update_class(most_spread_class, element[-1])
        for i in range(len(element) - 1):
            current_sum += (item[i] - element[i]) ** 2
        heappush(queue, (sqrt(current_sum), element))
    
    new_elements = nlargest(k, queue)
    for element in new_elements:
        update_class(most_spread_class, element[1][-1])
    if len(set(most_spread_class.values())) == 1:
        _, el = heappop(new_elements)
        found_class = el[-1]
    else:
        found_class = sorted(list(most_spread_class.items()), key=lambda x: x[1])[-1][0]
    
    return found_class, new_elements


def main():
    dataset = [
        [5.1, 3.5, 1.4, 0.2, 'Iris-setosa'],
        [4.9, 3.0, 1.4, 0.2, 'Iris-setosa'],
        [4.7, 3.2, 1.3, 0.2, 'Iris-setosa'],
        [4.6, 3.1, 1.5, 0.2, 'Iris-setosa'],
        [5.0, 3.3, 1.4, 0.2, 'Iris-setosa'],
        [6.0, 2.2, 4.0, 1.0, 'Iris-versicolor'],
        # [6.1, 2.9, 4.7, 1.4, 'Iris-versicolor'],
        [5.4, 3.0, 4.5, 1.5, 'Iris-versicolor'],
        [6.0, 3.4, 4.5, 1.6, 'Iris-versicolor'],
        [6.7, 3.1, 4.7, 1.5, 'Iris-versicolor'],
        [5.1, 2.5, 3.0, 1.1, 'Iris-versicolor'],
        [5.7, 2.8, 4.1, 1.3, 'Iris-versicolor'],
        [6.3, 3.3, 6.0, 2.5, 'Iris-virginica'],
        [5.8, 2.7, 5.1, 1.9, 'Iris-virginica'],
        [7.1, 3.0, 5.9, 2.1, 'Iris-virginica'],
        [6.3, 2.9, 5.6, 1.8, 'Iris-virginica'],
        [6.5, 3.0, 5.8, 2.2, 'Iris-virginica']
    ]
    test_data = {
        (5.6, 2.7, 4.2, 1.3): 'Iris-versicolor',
        (5.7, 3.0, 4.2, 1.2): 'Iris-versicolor',
        (5.7, 2.9, 4.2, 1.3): 'Iris-versicolor',
    }
    results = {}
    for item, cl in test_data.items():
        spread, q = generate_queue(item, dataset, 8)
        # results[item] = 100 if  
        # print(item, spread, q)
        print(spread)

if __name__ == '__main__':
    main()
