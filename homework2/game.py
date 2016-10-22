from math import sqrt  # noqa


def sliding_blocks(n, board, end):
    """Move blocks until end position."""
    return 0


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
    n, board, end = read_user_input()
    # n = 8
    # board = [[1, 2, 3], [4, 5, 6], [0, 7, 8]]
    # end = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
    sliding_blocks(n, board, end)


if __name__ == '__main__':
    main()
