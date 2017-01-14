import csv
from math import log2
from random import sample


class Node:
    def __init__(self, value, attr_id, children=[]):
        self.value = value
        self.attr_id = attr_id
        self.children = children

    def __str__(self):
        return '{val} => {children}'.format(
            val=self.value,
            children=self.children
        )

    def __repr__(self):
        return self.__str__()


class Tree:
    def __init__(self, root):
        self.root = root
        self.nodes = []

    def __str__(self):
        return '{root}: {nodes}'.format(
            root=self.root,
            nodes=self.nodes
        )

    def __repr__(self):
        return self.__str__()


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


def build_tree(id3_tree, old_attributes, data):
    attributes = old_attributes[::]
    all_attributes = attributes[::]

    tree = {}
    class_id = -1
    current_id = -1
    single = None
    level = 0
    current = {}
    attributes_order = []
    is_last = False
    while len(attributes):
        if current_id > len(attributes) - 1:
            current_id = -1
        attributes.pop(current_id)
        all_gains = {}

        # find probability for class
        calculated = get_attr_probabilities(data, class_id)
        # calculate entropy for class
        entropy = calculate_entropy(calculated)

        if not attributes:
            is_last = True
            attributes = [all_attributes[current_id]]
        for attr in attributes:
            attr_id = all_attributes.index(attr)

            sorted_by_attr = sort_by_attr(data, attr_id, class_id)

            if len(sorted_by_attr) == len(data):
                # build small tree
                for k, v in sorted_by_attr.items():
                    node = [leave for leave in id3_tree.nodes if leave.value == k]
                    if node:
                        node = id3_tree.nodes.pop(node[0])
                    else:
                        node = Node(k, attr_id)
                    node.children = (v[0][1])
                    id3_tree.nodes.append(node)
                empty = {}
                current[single] = empty
                for item in data:
                    empty[item[attr_id]] = sorted_by_attr[item[attr_id]][0][class_id]
                attributes_order.append(attr_id)

                return tree, attributes_order

            probabilities = get_attr_probabilities(data, attr_id)
            entropies = {}
            for key, values in sorted_by_attr.items():
                sorted_values = get_attr_probabilities(values, class_id)
                entropies[key] = calculate_entropy(sorted_values)
            # calculate gain
            gain = entropy
            for k, v in entropies.items():
                gain -= probabilities[k] * v
            all_gains[attr] = gain

        maximum_gain = max(all_gains.values())
        root = [(k, v) for k, v in all_gains.items() if v == maximum_gain][0]
        root_id = all_attributes.index(root[0])
        attributes_order.append(root_id)
        sorted_by_root = sort_by_attr(data, root_id, class_id)
        if not tree:  # if id3_tree.root is None:
            id3_tree.root = root[0]
            tree[root[0]] = {}
        for key, val in sorted_by_root.items():
            item_value = [i[1] for i in val]
            if len(set(item_value)) == 1:
                if level > 0:
                    current[key] = item_value[0]
                else:
                    tree[root[0]][key] = item_value[0]
                id3_tree.nodes.append(Node(key, attr_id, children=item_value[0]))
            else:
                node = [leave for leave in id3_tree.nodes if leave.value == key]
                # if node:
                #     node = id3_tree.nodes.pop(node[0])
                # else:
                #     node = Node(key)
                # id3_tree.nodes.append(node)
                if not node:
                    id3_tree.nodes.append(Node(key, attr_id))
                current_id = attributes.index(root[0])
                if level > 0:
                    current[key] = {}
                else:
                    tree[root[0]][key] = current

                single = key
        print(tree)
        level += 1
        data = [item for item in data if single in item]
        if is_last:
            attributes.pop()
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
    id3_tree = Tree(None)

    tree, attributes_order = build_tree(id3_tree, attributes, trainers)
    print(id3_tree)
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
