from math import sqrt  # noqa

PATH_COST = 1
FINAL_COST = 0
VISITED = {}
STEPS = []


def sliding_blocks(n, board, end):
    """Move blocks until end position."""
    if board == end:
        return FINAL_COST

    return 100000


def h(board, end):
    """The heuristic function returns probable cost of path to end."""
    new_board = sum(board, [])
    for number in new_board:
        pass


def g():
    """Return cost so far to reach current state."""
    return FINAL_COST


def can_move(index, state, zero_index):
    """Check whether the empty sign could be moved."""
    if index < 0:
        return zero_index + index > -1
    return zero_index + index < len(state)


def change_elements(items, old_index, new_index):
    """Switch places of two elements in list collection."""
    new_items = items[:]
    new_items[old_index], new_items[new_index] = new_items[new_index], new_items[old_index]  # noqa
    return new_items


def read_user_input():
    """Read user input."""
    number = int(input('Enter count of non-zero elements in block: '))
    row_length = int(sqrt(number + 1))
    print('Fill in the block by entering each row on new line and numbers separated by " "(space).')  # noqa
    rows = []
    end = []
    for row_index in range(row_length):
        row = input().split(' ')
        rows.append(list(map(lambda x: int(x), row)))
        start = row_index * row_length + 1
        end.append(list(range(start, start + row_length)))
    end[-1][-1] = 0
    return number, rows, end


def main():
    """Build logic of the program."""
    # n, board, end = read_user_input()
    n = 8
    board = [[1, 2, 3], [4, 5, 6], [0, 7, 8]]
    end = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
    print(sliding_blocks(n, board, end))


if __name__ == '__main__':
    main()
