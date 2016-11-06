from collections import OrderedDict
from random import shuffle


MAX_CONFLICTS = [-1, {
    'row': -1,
    'column': -1,
    'conflicts': [],
}]


def print_board(board):
    """Print board."""
    b = ['_'] * len(board)
    for queen, position in board.items():
        b[position['row']] = ['_'] * len(board)
        b[position['row']][position['column']] = '*'
    b = ['|'.join(r) for r in b]
    for row in b:
        print(row)


def move_queen(board):
    """Move the queen with maximum number of conflicts."""
    global MAX_CONFLICTS
    calculate_conflicts(board)
    print('MAX_CONFLICTS: ', MAX_CONFLICTS)
    MAX_CONFLICTS = None


def calculate_conflicts(board):
    """Calculates all conflicts for each queen and gets the one with maximum conflicts."""
    print('calculate')
    print('BEFORE calculation', board)
    global MAX_CONFLICTS
    positions = board.values()
    for queen, position in board.items():
        print('\n CURRENT POSITION', queen, position)
        if len(list(filter(lambda pos: pos['row'] == board[queen]['row'], positions))) > 1:
            position['conflicts'].extend(list(filter(lambda pos: pos['row'] == board[queen]['row'], positions))[1:])
        if len(list(filter(lambda pos: pos['column'] == board[queen]['column'], positions))) > 1:
            position['conflicts'].extend(list(filter(lambda pos: pos['column'] == board[queen]['column'], positions))[1:])
        if len(list(filter(lambda pos: abs(board[queen]['column'] - pos['column']) == abs(board[queen]['row'] - pos['row']), positions))) > 1:
            position['conflicts'].extend(list(filter(lambda pos: abs(board[queen]['column'] - pos['column']) == abs(board[queen]['row'] - pos['row']), positions))[1:])

    # update MAX_CONFLICTS
    if len(position['conflicts']) > len(MAX_CONFLICTS[1]['conflicts']):
        MAX_CONFLICTS = [queen, position]
    print('AFTER calculation', board)


def main():
    # number = int(input('Enter the count of queens: '))
    number = 4
    row_indexes = list(range(number))
    shuffle(row_indexes)
    # generate board with queens one per row and one per column
    board = OrderedDict([
        (i, {
            'row': row_indexes[i],
            'column': i,
            'conflicts': []
        })
        for i in range(number)])
    print_board(board)
    while MAX_CONFLICTS:
        move_queen(board)
    # print(board)


if __name__ == '__main__':
    main()
