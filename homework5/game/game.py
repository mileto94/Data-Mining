from random import randint, choice

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


def test_main():
    is_computer = True
    board = Board(is_computer)
    # X is computer
    # board.fields.update({
    #     (0, 0): 'X',
    #     (0, 1): 'O',
    #     (2, 0): 'O',
    #     # (2, 2): 'X'
    # })
    board.player, board.opponent = board.opponent, board.player
    board.fields.update({
        (0, 0): 'O',
        (0, 2): 'X',
        (1, 0): 'X',
        (1, 1): 'X',
        (2, 0): 'O'
    })
    print(board)
    print(board.min_max(is_computer, -2, 2))
    res = [[], []]
    for pos in board.get_available_moves():
        board.move(*pos)
        v = board.min_max(is_computer, -2, 2)
        if v > -1:
            res[v].append(pos)
        board.move(*pos, sign=board.empty)
    print(res)
    final = 0
    if res[1]:
        final = choice(res[1])
    elif res[0]:
        final = choice(res[0])
    else:
        final = choice(board.get_available_moves())
    board.move(*final)
    print(board)
    return final


if __name__ == '__main__':
    test_main()
