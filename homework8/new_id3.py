import csv
from math import log2
from random import sample


def get_attr_probabilities(data, attr_id):
    res = {}
    all_values = [item[attr_id] for item in data]
    n = len(all_values)
    for val in all_values:
        res[val] = res[val] + 1/n if val in res else 1/n
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

    tree = {}  # k: {} for k in attributes
    class_id = -1
    current_id = -1
    single = None
    attributes_order = []
    root_id = None
    while len(attributes):
        attributes.pop(current_id)
        all_gains = {}

        # find probability for class
        calculated = get_attr_probabilities(data, class_id)
        # calculate entropy for class
        # print(calculated)
        entropy = calculate_entropy(calculated)
        # print('entropy', entropy)

        for attr in attributes:
            attr_id = all_attributes.index(attr)
            # print(attr_id, attr)

            sorted_by_attr = sort_by_attr(data, attr_id, class_id)

            # if len(sorted_by_attr) == len(data):
            #     # build small tree
            #     for item in data:
            #         print('item id', item, item[attr_id], sorted_by_attr[attr_id][0][class_id])
            #         # tree[item[attr_id]] = sorted_by_attr[attr_id][0][class_id]
            #     attributes_order.append(attr_id)

            #     print(tree)

            #     return tree, attributes_order

            probabilities = get_attr_probabilities(data, attr_id)
            entropies = {}
            for key, values in sorted_by_attr.items():
                # print(key, values)
                sorted_values = get_attr_probabilities(values, 1)
                entropies[key] = calculate_entropy(sorted_values)
            # print(entropies)
            # calculate gain
            gain = entropy
            for k, v in entropies.items():
                gain -= probabilities[k] * v
            # print('Gain: ', gain)
            all_gains[attr] = gain
            # print('----------------------------------------------------')
        # print("All gains", all_gains)
        if all_gains:
            maximum_gain = max(all_gains.values())
            root = [(k, v) for k, v in all_gains.items() if v == maximum_gain][0]
        # print(root)
        new_root_id = all_attributes.index(root[0])

        if root_id is not None:
            print('---------------------------------------------------')
            print(tree[all_attributes[root_id]])
            print('---------------------------------------------------')
            for k, v in tree[all_attributes[root_id]].items():
                if len(v) == 0:
                    tree[all_attributes[root_id]][k] = all_attributes[new_root_id]
        root_id = new_root_id
        if root_id not in attributes_order:
            attributes_order.append(root_id)
        sorted_by_root = sort_by_attr(data, root_id, class_id)
        tree[root[0]] = {}
        print(tree)
        for key, val in sorted_by_root.items():
            item_value = [i[1] for i in val]
            if len(set(item_value)) == 1:
                tree[root[0]][key] = item_value[0]
            else:
                tree[root[0]][key] = {}
                current_id = root_id
                single = key
                # print('CHANGE class_id', current_id)
        print(tree)
        data = [item for item in data if single in item]
        # break
    print('FINALLY', tree)
    return tree, attributes_order


def get_test_data(data, k=20):
    test_data = sample(data, k)
    trainers = data[::]
    for item in test_data:
        trainers.remove(item)
    return trainers, test_data


def get_results(tree, test_data, attributes, attributes_order, end_values):
    res = {}
    for test in test_data:
        current_node = None
        for attr in attributes_order:
            val = attributes[attr]
            print('Looking for "{}"'.format(val))
            if tree.get(val, None) in attributes:
                print('GO Inside')
                current_node = tree.get(attributes[attr], {})
            else:
                print(tree.get(attributes[attr], {}))
                current_node = tree.get(attributes[attr], {}).get(test[attr], {})
                print(current_node)
            if current_node in end_values:
                print('Found!!!', current_node)
                res[test] = current_node
                break
    return res


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
    attributes = read_data('attributes.csv')[0]
    data = read_data('data.csv')

    trainers, test_data = get_test_data(data)

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



if __name__ == '__main__':
    main1()
