import csv
from heapq import heappush, heappop
from math import sqrt
from random import sample, choice


def group_classes(elements):
    bucket = {}
    for element in elements:
        name = element[1][-1]
        if name in bucket:
            bucket[name] += 1
        else:
            bucket[name] = 1
    return bucket


def generate_queue(item, trainers, k):
    queue = []
    for element in trainers:
        current_sum = 0
        for i in range(len(element) - 1):
            current_sum += (float(item[i]) - float(element[i])) ** 2
        heappush(queue, (sqrt(current_sum), element))

    queue.sort()
    new_elements = queue[:k]
    most_spread_class = group_classes(new_elements)

    if len(set(most_spread_class.values())) == len(set(most_spread_class.keys())):
        found_class = sorted(list(most_spread_class.items()), key=lambda x: x[1])[-1][0]
    else:
        k = max(most_spread_class.values())
        classes = [item for item, cl in most_spread_class.items() if cl == k]
        closest_cl = heappop(new_elements)
        found_class = closest_cl if closest_cl in classes else choice(classes)
    return found_class


def read_data(filename):
    with open(filename, 'r') as data_doc:
        d = csv.reader(data_doc, delimiter=',')
        return [tuple(item) for item in d]


def main():
    count = 0
    k = int(input('Enter k = '))
    dataset = read_data('data.csv')
    test_data = sample(dataset, 20)
    trainers = set(dataset).difference(set(test_data))
    for item in test_data:
        item = list(item)
        cl = item.pop()
        found_class = generate_queue(item, trainers, k)
        count = count + 1 if cl == found_class else count
        print(item, found_class, cl == found_class)
    print('Accuracy: {}%'.format(100 * count / len(test_data)))


if __name__ == '__main__':
    main()
