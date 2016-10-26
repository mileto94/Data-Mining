from math import sqrt  # noqa
from collections import OrderedDict
from heapq import heappush, heappop


PATH_COST = 1
FINAL_COST = 0
VISITED = {}
STEPS = []
OPTIONS = OrderedDict()


def sliding_blocks(n, board, end):
    """Move blocks until end position."""
    print(h(board, end))
    queue = [(h(board, end), None, board)]
    while queue:
        distance, path, state = heappop(queue)
        if state in VISITED: continue  # noqa
        VISITED.add(state)
        if state == end: return FINAL_COST  # noqa
        for children in 


    return 100000


def h(board, end):
    """The heuristic function returns probable cost of path to end."""
    # new_board = sum(board, [])
    final_sum = 0
    for number, position in board.items():
        final_sum += abs(end[number][0] - position[0]) + abs(end[number][1] - position[1])  # noqa
    return final_sum


def g():
    """Return cost so far to reach current state."""
    return FINAL_COST


def can_move(board, x=None, y=None):
    """Check whether the empty sign could be moved."""
    tuple_index = 0 if x is not None else 1
    value = x if x is not None else y
    if value < 0:
        return board[0][tuple_index] + value > -1
    return board[0][tuple_index] + value < sqrt(len(board))


def get_children(state, end):
    """Generate possible solutions."""
    children = [(h(state, end), None, state)]
    if can_move(state, x=-1):
        print('up')
        heappush(change_elements(state), 0, )
    if can_move(state, x=1):
        print('down')
    if can_move(state, y=-1):
        print('left')
    if can_move(state, y=1):
        print('right')


def change_elements(state, old_key, new_key):
    """Switch places of two elements in list collection."""
    new_state = state[:]
    new_state[old_key], new_state[new_key] = new_state[new_key], new_state[old_key]  # noqa
    return new_state


def read_user_input():
    """Read user input."""
    number = int(input('Enter count of non-zero elements in block: '))
    row_length = int(sqrt(number + 1))
    print('Fill in the block by entering each row on new line and numbers separated by " "(space).')  # noqa
    rows = OrderedDict()
    end = OrderedDict()
    for row_index in range(row_length):
        row = input().split(' ')
        for y, num in enumerate(row):
            rows[int(num)] = (row_index, y)

    for row_index in range(1, number + 1):
        end[row_index] = ((row_index - 1) // row_length, (row_index - 1) % row_length)  # noqa
    end[0] = (row_length - 1, row_length - 1)
    return number, rows, end


def main():
    """Build logic of the program."""
    # n, board, end = read_user_input()
    n = 8
    # board = [[1, 2, 3], [4, 5, 6], [0, 7, 8]]
    # end = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
    board = OrderedDict([
        ((0, 0), 1), ((0, 1), 2), ((0, 2), 3), ((1, 0), 4), ((1, 1), 5),
        ((1, 2), 6), ((2, 0), 0), ((2, 1), 7), ((2, 2), 8)])
    end = OrderedDict([
        ((0, 0), 1), ((0, 1), 2), ((0, 2), 3), ((1, 0), 4), ((1, 1), 5),
        ((1, 2), 6), ((2, 0), 7), ((2, 1), 8), ((2, 2), 0)])
    print(sliding_blocks(n, board, end))


if __name__ == '__main__':
    main()
