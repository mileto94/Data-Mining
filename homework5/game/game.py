from random import randint

from board import Board


def main():
    rand_num = randint(0, 1000)
    if rand_num % 2 == 0:
        # computer
        print('The first player is computer.')
        is_computer = True
    else:
        # player
        print('Yey, the first player is you!')
        is_computer = False

    board = Board(is_computer)
    print(board)
    board.play(is_computer)
    print(board)


def test_winner():
    board = Board(True)
    # Check rows
    # board.fields.update({(0, 0): 'X', (0, 1): 'X', (0, 2): 'X'})
    # board.fields.update({(1, 0): 'X', (1, 1): 'X', (1, 2): 'X'})
    # board.fields.update({(2, 0): 'X', (2, 1): 'X', (2, 2): 'X'})

    # Check cols
    # board.fields.update({(0, 0): 'X', (1, 0): 'X', (2, 0): 'X'})
    # board.fields.update({(0, 1): 'X', (1, 1): 'X', (2, 1): 'X'})
    # board.fields.update({(0, 2): 'X', (1, 2): 'X', (2, 2): 'X'})

    # Check diag
    # board.fields.update({(0, 0): 'X', (1, 1): 'X', (2, 2): 'X'})

    # Check rev_diag
    board.fields.update({(0, 2): 'X', (1, 1): 'X', (2, 0): 'X'})
    # board.fields.update({(0, 2): 'O', (1, 1): 'O', (2, 0): 'O'})

    print(board)
    wins = board.wins()
    print(wins)
    # wins, who = board.is_winner()
    assert wins == 1, 'Oops, NOT found a winner!'
    # assert who == 'X', 'Wrong sign for winner'


if __name__ == '__main__':
    main()
