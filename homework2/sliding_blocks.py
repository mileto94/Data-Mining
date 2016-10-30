from math import sqrt  # noqa
from heapq import heappush, heappop
from time import time

VISITED = set()
HEAP = []


class State:
    def __init__(self, arr):  # noqa
        self.elements = arr
        self.directions = []
        self.zero_index = self.elements.index(0)
        self.path = 0

    def __len__(self):
        return len(self.elements)

    def __lt__(self, other_state):
        return self.elements < other_state.elements

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return str(self.elements)

    def add_direction(self, direction):
        self.directions.append(direction)

    def copy_directions(self, other_state):
        self.directions = other_state.directions + self.directions

    @property
    def dict(self):
        return {item: (i // 3, i % 3) for i, item in enumerate(self.elements)}

    @property
    def str(self):
        return str(self.elements)

    def update_zero_index(self):
        self.zero_index = self.elements.index(0)


def change_elements(state, old, new):
    """Switch places of two elements in list."""
    # we should copy the list not refer to it
    new_state = State(state.elements[::])
    new_state.copy_directions(state)
    new_state.elements[old], new_state.elements[new] = new_state.elements[new], new_state.elements[old]
    new_state.update_zero_index()
    new_state.path = state.path + 1
    return new_state


def generate_children(state, end):
    """Generate children of current state and push them into the priority queue."""  # noqa
    row_length = int(sqrt(len(state)))
    index = state.zero_index
    if index - row_length > -1:
        new_state = change_elements(state, index, index - row_length)
        if new_state.str not in VISITED:
            new_state.add_direction('down')
            heappush(HEAP, (get_estimation(new_state, end), new_state))
    if index + row_length < len(state):
        new_state = change_elements(state, index, index + row_length)
        if new_state.str not in VISITED:
            new_state.add_direction('up')
            heappush(HEAP, (get_estimation(new_state, end), new_state))
    if index % 3 != 0 and index > 0:
        new_state = change_elements(state, index, index - 1)
        if new_state.str not in VISITED:
            new_state.add_direction('right')
            heappush(HEAP, (get_estimation(new_state, end), new_state))
    if index % 3 != 2 and index + 1 < len(state):
        new_state = change_elements(state, index, index + 1)
        if new_state.str not in VISITED:
            new_state.add_direction('left')
            heappush(HEAP, (get_estimation(new_state, end), new_state))


def g(state):
    """Return cost of the path till the current state."""
    return state.path


def h(state, end):
    """Return heuristic estimation from current state to goal."""
    state_dict = state.dict
    end_dict = end.dict
    return sum([
        abs(value[0] - state_dict[key][0]) + abs(value[1] - state_dict[key][1])
        for key, value in end_dict.items()])


def get_estimation(state, end):
    """Get estimate for the current state."""
    return h(state, end) + g(state)


def a_star(state, end):
    """Implement A* algorithm."""
    if state.str == end.str:
        return state
    VISITED.add(state.str)
    generate_children(state, end)
    while HEAP:
        _, current_state = heappop(HEAP)
        if current_state.str in VISITED: continue
        VISITED.add(current_state.str)
        if current_state.str == end.str:
            return current_state
        generate_children(current_state, end)
    return False


def read_user_input():
    """Read user input."""
    number = int(input('Enter count of non-zero elements in block: '))
    row_length = int(sqrt(number + 1))
    print('Fill in the block by entering each row on new line and numbers separated by " "(space).')  # noqa
    rows = []
    for row_index in range(row_length):
        rows.extend(map(int, input().split(' ')))
    end = list(range(1, number + 1))
    end.append(0)
    return number, State(rows), State(end)


def call_a_star():
    """Call A*."""
    n, start, end = read_user_input()
    s = time()
    # start = State([1, 2, 3, 4, 5, 6, 0, 7, 8])  # 2
    # end = State([1, 2, 3, 4, 5, 6, 7, 8, 0])
    # start = State([2, 3, 6, 1, 5, 8, 4, 7, 0])  # 8
    # start = State([6, 5, 3, 2, 4, 8, 7, 0, 1])  # 21
    # start = State([8, 7, 0, 2, 5, 6, 3, 4, 1])  # 30 INFINITY
    # start = State([7, 2, 8, 3, 1, 4, 0, 6, 5])  # 22
    # start = State([8, 1, 3, 5, 6, 7, 2, 4, 0])  # 18
    # start = State([0, 1, 2, 7, 4, 6, 8, 5, 3])  # 16
    # start = State([2, 7, 8, 6, 0, 1, 3, 5, 4])  # 26
    # start = State([1, 8, 7, 4, 0, 5, 6, 3, 2])  # 22
    # start = State([2, 1, 8, 5, 0, 6, 7, 3, 4])  # 22
    solution = a_star(start, end)
    if solution:
        print(solution.path)
        print(solution.directions)
    else:
        print('Sorry. Unable to find a solution...')
    print('TIME: {}ms'.format((time() - s) * 1000))

if __name__ == '__main__':
    call_a_star()
