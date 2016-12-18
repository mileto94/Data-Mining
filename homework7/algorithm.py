import csv
from heapq import heappush, heappop
from random import sample, choice, shuffle, randint


def read_data(filename):
    with open(filename, 'r') as data_doc:
        d = csv.reader(data_doc, delimiter=',')
        return [list(map(lambda x: x.replace("'", ""), item)) for item in d]


def group_elements(elements):
    bucket = {}
    for element in elements:
        name = element[-1]
        if name in bucket:
            bucket[name].append(element)
        else:
            bucket[name] = [element]
    return bucket


def group_by_count(elements):
    bucket = {}
    for element in elements:
        if element in bucket:
            bucket[element] += 1
        else:
            bucket[element] = 1
    return bucket


def get_mode(elements):
    sorted_el = group_by_count([i for i in elements if i != '?'])
    max_el = max(sorted_el.values())
    return [k for k, v in sorted_el.items() if v == max_el][0]


def get_cleaned_data(data):
    result = {}
    for party, votes in data.items():
        reduced_votes = [vote for vote in votes if vote.count('?') < 6]
        result[party] = reduced_votes
        for vote_id in range(len(reduced_votes[0])):
            all_votes = [i[vote_id] for i in reduced_votes]
            mode = get_mode(all_votes)
            while '?' in all_votes:
                index = all_votes.index('?')
                result[party][index][vote_id] = mode
                all_votes[index] = mode
    return result


def get_sets(elements, k=10):
    trainers, tested = [], []
    total = sum(elements.values(), [])
    n = len(total)
    group_count = len(total) // k

    selected = []
    for i in range(k - 1):
        trainer = []
        while len(trainer) < group_count:
            index = randint(0, n - 1)
            if index not in selected:
                trainer.append(total[index])
                selected.append(index)
        trainers.append(trainer)

    tested = [total[i] for i in range(len(total)) if i not in selected]

    return trainers, tested


def train(elements, parties):
    result = {party: [] for party in parties}
    for trainer in elements:
        for vote_id in range(len(trainer[0]) - 1):
            party = trainer[vote_id][-1]
            all_votes = [i[vote_id] for i in trainer]
            sorted_el = group_by_count([i for i in all_votes if i != '?'])
            result[party].append({vote_id + 1: sorted_el})
            # n = len(all_votes)
            # sorted_el = {k: v / n for k, v in sorted_el.items()}
    return result


def naive_bayes():
    # 1. Get data
    data = read_data('data.csv')

    # 2. Group data
    grouped = group_elements(data)
    print(grouped)

    # 3. Clean up data
    cleaned_data = get_cleaned_data(grouped)
    print(cleaned_data)

    # 4. Split data into train_set and test_set
    trainers, tested = get_sets(cleaned_data)
    print('Trainers', trainers)
    print('Tested', tested)

    # 5. create frequency table
    dataset = train(trainers, cleaned_data.keys())
    print(dataset)


def main():
    naive_bayes()


if __name__ == '__main__':
    main()
