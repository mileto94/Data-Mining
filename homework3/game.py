from collections import OrderedDict
from random import shuffle


MAX_CONFLICTS = (-1, -1)  # (queen_col, conflicts_count)


def print_board(board):
    """Print board."""
    b = ['_'] * len(board)
    for queen, position in board.items():
        b[position['row']] = ['_'] * len(board)
        b[position['row']][queen] = '*'
    b = ['|'.join(r) for r in b]
    for row in b:
        print(row)


def move_queen(board):
    """Move the queen with maximum number of conflicts."""
    global MAX_CONFLICTS
    calculate_conflicts(board)
    print('MAX_CONFLICTS: ', MAX_CONFLICTS)
    print(board[MAX_CONFLICTS[0]])
    # Should get the place with mim conflicts and put it there
    for i in board.keys():
        new_board = board.copy()
        new_board[MAX_CONFLICTS[0]] = {
            'row': i,
            'conflicts': 0
        }
        calculate_conflicts(new_board)
    MAX_CONFLICTS = None


def calculate_conflicts(board):
    """Calculates all conflicts for each queen and gets the one with maximum conflicts."""
    print('calculate')
    print('BEFORE calculation', board)
    global MAX_CONFLICTS
    positions = board.values()
    queens = board.keys()
    for queen, position in board.items():
        # print('\n CURRENT POSITION', queen, position)
        if len(list(filter(lambda pos: pos['row'] == board[queen]['row'], positions))) > 1:
            position['conflicts'] = len(list(filter(lambda pos: pos['row'] == board[queen]['row'], positions))) - 1
        if len(list(filter(lambda column: column == queen, queens))) > 1:
            position['conflicts'] = len(list(filter(lambda column: column == queen, queens))) - 1
        if len(list(filter(lambda pair: abs(queen - pair[0]) == abs(board[queen]['row'] - pair[1]['row']), board.items()))) > 1:
            position['conflicts'] = len(list(filter(lambda pair: abs(queen - pair[0]) == abs(board[queen]['row'] - pair[1]['row']), board.items()))) - 1

        # update MAX_CONFLICTS
        if position['conflicts'] > MAX_CONFLICTS[1]:
            MAX_CONFLICTS = [queen, position['conflicts']]
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
            'conflicts': 0
        })
        for i in range(number)])
    print(board)
    print_board(board)
    while MAX_CONFLICTS:
        move_queen(board)
    # print(board)


if __name__ == '__main__':
    main()
