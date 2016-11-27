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


if __name__ == '__main__':
    main()
