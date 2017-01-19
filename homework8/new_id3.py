import csv
import pprint
from math import log2
from random import sample


def get_attr_probabilities(data, attr_id):
    res = {}
    all_values = [item[attr_id] for item in data]
    n = len(all_values)
    for val in all_values:
        res[val] = res[val] + 1 / n if val in res else 1 / n
    return res


def read_data(filename):
    with open(filename, 'r') as data_doc:
        d = csv.reader(data_doc, delimiter=',')
        return [list(map(lambda x: x.replace("'", ""), item)) for item in d]


def calculate_entropy(data):
    res = 0
    for key, val in data.items():
        res += val * log2(val)
    return -res


def sort_by_attr(data, attr_id, class_id):
    res = {}
    for item in data:
        if item[attr_id] in res:
            res[item[attr_id]].append([item[attr_id], item[class_id]])
        else:
            res[item[attr_id]] = [[item[attr_id], item[class_id]]]
    return res


def build_tree(old_attributes, data):
    attributes = old_attributes[::]
    all_attributes = attributes[::]

    tree = {}
    class_id = -1
    current_id = -1
    single = None
    attributes_order = []
    root_id = None
    while len(attributes):

        # if there is an error with the indexes always get the last one
        if current_id >= len(attributes):
            current_id = -1
        attributes.pop(current_id)
        all_gains = {}

        # find probability for class
        calculated = get_attr_probabilities(data, class_id)

        # calculate entropy for class
        entropy = calculate_entropy(calculated)
        # print('entropy', entropy)

        for attr in attributes:
            attr_id = all_attributes.index(attr)

            sorted_by_attr = sort_by_attr(data, attr_id, class_id)

            probabilities = get_attr_probabilities(data, attr_id)
            entropies = {}
            for key, values in sorted_by_attr.items():
                # calculate entropies for each attribute
                sorted_values = get_attr_probabilities(values, 1)
                entropies[key] = calculate_entropy(sorted_values)
            # print(entropies)

            # calculate gain for each attribute
            gain = entropy
            for k, v in entropies.items():
                gain -= probabilities[k] * v
            # print('Gain: ', gain)
            all_gains[attr] = gain
        # print("All gains", all_gains)
        if all_gains:
            # get the attribute with max gain fot subroot of the tree
            maximum_gain = max(all_gains.values())
            root = [(k, v) for k, v in all_gains.items() if v == maximum_gain][0]
        new_root_id = all_attributes.index(root[0])

        if root_id is not None:
            # update previous {} values to relate the new key(subroot)
            for k, v in tree[all_attributes[root_id]].items():
                if len(v) == 0:
                    tree[all_attributes[root_id]][k] = all_attributes[new_root_id]
        root_id = new_root_id

        if root_id not in attributes_order:
            # update ordered list of attributes
            attributes_order.append(root_id)

        sorted_by_root = sort_by_attr(data, root_id, class_id)
        tree[root[0]] = {}
        for key, val in sorted_by_root.items():
            # add new subroot to the tree and fill in its values
            item_value = [i[1] for i in val]
            if len(set(item_value)) == 1:
                tree[root[0]][key] = item_value[0]
            else:
                tree[root[0]][key] = {}
                current_id = root_id
                single = key
        # continue filtering only filterd by current subroot instances (not the whole data)
        data = [item for item in data if single in item]
    # print('FINALLY', tree)
    return tree, attributes_order


def get_test_data(data, k=20):
    test_data = sample(data, k)
    trainers = data[::]
    for item in test_data:
        trainers.remove(item)
    return trainers, test_data


def get_results(tree, test_data, attributes, attributes_order, end_values):
    res = {}
    count = 0
    for test in test_data:
        current_node = None
        for attr in attributes_order:
            val = attributes[attr]
            if tree.get(val, None) in attributes:
                current_node = tree.get(attributes[attr], {})
            else:
                current_node = tree.get(attributes[attr], {}).get(test[attr], {})
            if current_node and current_node in end_values:
                res[tuple(test)] = (current_node, test[-1], test[-1] == current_node)
                break
        count = count + 1 if test[-1] == current_node else count
    accuracy = 100 * count / len(test_data)
    print('Accuracy: {}%'.format(accuracy))
    return res, accuracy


def main():
    attributes = ['gender', 'car ownership', 'travel cost', 'income level', 'transportation']

    data = [
        ('male', 0, 'cheap', 'low', 'bus'),
        ('male', 1, 'cheap', 'medium', 'bus'),
        ('female', 1, 'cheap', 'medium', 'train'),
        ('female', 0, 'cheap', 'low', 'bus'),
        ('male', 1, 'cheap', 'medium', 'bus'),
        ('male', 0, 'standard', 'medium', 'train'),
        ('female', 1, 'standard', 'medium', 'train'),
        ('female', 1, 'expensive', 'high', 'car'),
        ('male', 2, 'expensive', 'medium', 'car'),
        ('female', 2, 'expensive', 'high', 'car')
    ]

    test_data = [
        ('male', 1, 'standard', 'high', ''),  # Alex  =>  train
        ('male', 0, 'cheap', 'medium', ''),  # Buddy  =>  bus
        ('female', 1, 'cheap', 'high', '')  # Cherry  =>  train
    ]

    end_values = set([i[len(i) - 1] for i in data])
    print(end_values)

    tree, attributes_order = build_tree(attributes, data)
    print(attributes_order)
    print('***************************************************************************************')
    # get result
    print(get_results(tree, test_data, attributes, attributes_order, end_values))


def main1():
    count = 0
    res = []
    while count < 3:
        attributes = read_data('attributes.csv')[0]
        data = read_data('data.csv')

        trainers, test_data = get_test_data(data, k=70)
        # print('test data:')
        # print(test_data)
        # print()

        end_values = set([i[len(i) - 1] for i in data])
        # print('End values:', end_values)
        # print()

        tree, attributes_order = build_tree(attributes, data)
        # get result
        results, accuracy = get_results(tree, test_data, attributes, attributes_order, end_values)
        # pprint.pprint(results)
        res.append(accuracy)
        count += 1
    print(count)
    print(sum(res) / (count))


if __name__ == '__main__':
    main1()
