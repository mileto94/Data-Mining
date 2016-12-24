from math import log2


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


def main():
    attributes = ['gender', 'car ownership', 'travel cost', 'income level']  # , 'transportation'
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
        ('male', 1, 'standard', 'high', ''),  # Alex
        ('male', 0, 'cheap', 'medium', ''),  # Buddy,
        ('female', 1, 'cheap', 'high', '')  # Cherry
    ]

    class_id = -1
    all_gains = {}
    tree = {}

    # find probability for class
    calculated = get_attr_probabilities(data, class_id)
    # calculate entropy for class
    print(calculated)
    entropy = calculate_entropy(calculated)
    print('entropy', entropy)

    for attr_id, attr in enumerate(attributes):
        print(attr_id, attr)

        sorted_by_attr = sort_by_attr(data, attr_id, class_id)
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
    root_id = attributes.index(root[0])
    sorted_by_root = sort_by_attr(data, root_id, class_id)
    tree[root[0]] = {}
    for key, val in sorted_by_root.items():
        item_value = [i[1] for i in val]
        if len(set(item_value)) == 1:
            tree[root[0]][key] = item_value[0]
        else:
            class_id = root_id
            tree[root[0]][key] = {}
            print('CHANGE class_id', class_id)
    print(tree)

if __name__ == '__main__':
    main()
