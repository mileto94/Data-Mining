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
    board.player, board.opponent = 'X', 'O'
    # X is computer
    # board.fields.update({
    #     (0, 0): 'X',
    #     (0, 1): 'O',
    #     (2, 0): 'O',
    #     # (2, 2): 'X'
    # })
    # board.player, board.opponent = board.opponent, board.player
    board.fields.update({
        (0, 0): 'O',
        (1, 0): 'O',
        (1, 1): 'X',
        (2, 2): 'X'
    })
    # O | _ | _
    # O | X | _
    # _ | _ | X
    print(board)
    # print(board.min_max(is_computer, -2, 2))
    res = [[], []]
    for pos in board.get_available_moves():
        board.move(*pos)
        v = board.min_max(is_computer, -2, 2)
        if v > -1:
            res[v].append(pos)
        else:
            # if pc is first, then we should check where has moved the opponent
            # if user is first, take board.player
            opp_moves = board.get_fields(board.player)  # player snd opponent have already changed
            for win_state in board.win_states:
                # check whether the opponent is about to win
                opp_moves = board.get_fields(board.player)  # last
                for win_state in board.win_states:
                    if len(opp_moves) > 1 and len(set(win_state).difference(set(opp_moves))) == 1:
                        for win in win_state:
                            if win not in opp_moves and win in board.get_available_moves():
                                print(win)
                                board.move(*pos, sign=board.empty)

                                #  ####
                                board.move(*win)
                                print(board)
                                return win
        print(board.get_winner())
        board.move(*pos, sign=board.empty)
    print(res)
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
