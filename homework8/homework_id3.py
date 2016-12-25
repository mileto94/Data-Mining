import csv
from math import log2
from random import sample


def read_data(filename):
    with open(filename, 'r') as data_doc:
        d = csv.reader(data_doc, delimiter=',')
        return [list(map(lambda x: x.replace("'", ""), item)) for item in d]


def get_attr_probabilities(data, attr_id):
    res = {}
    all_values = [item[attr_id] for item in data]
    n = len(all_values)
    for val in all_values:
        res[val] = res[val] + 1/n if val in res else 1/n
    return res


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
    level = 0
    current = {}
    attributes_order = []
    while len(attributes):
        attributes.pop(current_id)
        all_gains = {}

        # find probability for class
        calculated = get_attr_probabilities(data, class_id)
        # calculate entropy for class
        print(calculated)
        entropy = calculate_entropy(calculated)
        print('entropy', entropy)

        for attr in attributes:
            attr_id = all_attributes.index(attr)
            print(attr_id, attr)

            sorted_by_attr = sort_by_attr(data, attr_id, class_id)

            if len(sorted_by_attr) == len(data):
                # build small tree
                empty = {}
                current[single] = empty
                for item in data:
                    empty[item[attr_id]] = sorted_by_attr[attr_id][0][class_id]
                attributes_order.append(attr_id)

                print(empty)
                print(tree)

                return tree, attributes_order

            probabilities = get_attr_probabilities(data, attr_id)
            entropies = {}
            for key, values in sorted_by_attr.items():
                print(key, values)
                sorted_values = get_attr_probabilities(values, 1)
                print(key, sorted_values)
                entropies[key] = calculate_entropy(sorted_values)
            print(entropies)
            # calculate gain
            gain = entropy
            for k, v in entropies.items():
                gain -= probabilities[k] * v
            print('Gain: ', gain)
            all_gains[attr] = gain
            print('----------------------------------------------------')
        print("All gains", all_gains)
        maximum_gain = max(all_gains.values())
        root = [(k, v) for k, v in all_gains.items() if v == maximum_gain][0]
        print(root)
        root_id = all_attributes.index(root[0])
        attributes_order.append(root_id)
        sorted_by_root = sort_by_attr(data, root_id, class_id)
        if not tree:
            tree[root[0]] = {}
        for key, val in sorted_by_root.items():
            item_value = [i[1] for i in val]
            if len(set(item_value)) == 1:
                if level > 0:
                    current[key] = item_value[0]
                else:
                    tree[root[0]][key] = item_value[0]
            else:
                current_id = attributes.index(root[0])
                if level > 0:
                    current[key] = {}
                else:
                    tree[root[0]][key] = current
                single = key
                print('CHANGE class_id', current_id)
        print(tree)
        level += 1
        data = [item for item in data if single in item]
    print('FINALLY', tree)
    return tree, attributes_order


def get_test_data(data, k=20):
    test_data = sample(data, k)
    trainers = data[::]
    for item in test_data:
        trainers.remove(item)
    return trainers, test_data


def main():
    attributes = read_data('attributes.csv')[0]

    data = read_data('data.csv')

    trainers, test_data = get_test_data(data)

    tree, attributes_order = build_tree(attributes, trainers)
    print('***************************************************************************************')
    # get result
    for test in test_data:
        res = tree.get(attributes[attributes_order[0]])
        index = 0
        while type(res) is dict and index < len(attributes):
            res = res.get(test[attributes_order[index]], {})
            index += 1
        print(res)


if __name__ == '__main__':
    main()
