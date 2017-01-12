import json
from random import randint
from collections import OrderedDict
from heapq import heappush, nlargest


COMP_SIGN = 'O'
PLAYER_SIGN = 'X'
INFINITY = 100


class Board:
    def __init__(self, fields=[]):
        self.size = 3
        self.empty = '_'
        self.fields = fields if fields else OrderedDict(
            {(i, j): self.empty for j in range(self.size) for i in range(self.size)})

        self.winning_states = [[(i, j) for j in range(self.size)] for i in range(self.size)]  # rows
        self.winning_states.extend([[(i, j) for i in range(self.size)] for j in range(self.size)])  # cols
        self.winning_states.append([(i, i) for i in range(self.size)])
        self.winning_states.append([(0, 2), (1, 1), (2, 0)])

    def __str__(self):
        board = []
        for i in range(self.size):
            board.append('|'.join([self.fields[i, j] for j in range(self.size)]))
        return '\n'.join(board)

    def __repr__(self):
        return str(self.fields)

    def get_enemy(self, sign):
        return PLAYER_SIGN if sign == COMP_SIGN else COMP_SIGN

    def get_empty_fields(self):
        return [pos for pos, val in self.fields.items() if val == self.empty]

    def get_played_fields(self, player):
        return [field for field, pl in self.fields.items() if pl == player]

    def wins(self):
        played = {
            COMP_SIGN: self.get_played_fields(COMP_SIGN),
            PLAYER_SIGN: self.get_played_fields(PLAYER_SIGN)
        }
        for sign, positions in played.items():
            if positions:
                for combo in self.winning_states:
                    played = [True for win in combo if win in positions]
                    if len(played) == self.size:
                        return sign
        return None

    def is_over(self):
        if len(self.get_empty_fields()) == 0 or self.wins() is not None:
            return True
        return False

    def get_score(self):
        if self.wins() == COMP_SIGN:
            return 10
        elif self.wins() == PLAYER_SIGN:
            return -10
        return 0

    def user_play(self):
        print(self)
        print(self.get_empty_fields())
        position = input('Enter position with space: ')
        x, y = map(int, position.split(' '))
        if -1 < x < 3 and -1 < y < 3 and self.fields[x, y] == self.empty:
            self.fields[x, y] = PLAYER_SIGN
        else:
            print('This filed is not empty or the coordinates are not valid!')
            self.user_play()

    def computer_play(self):
        # board, val = minimax(self, COMP_SIGN, -INFINITY, INFINITY)
        # print('Result from minimax:', val)
        # self.fields = board.fields.copy()
        scores = []
        for pos in self.get_empty_fields():
            b1 = Board(fields=self.fields.copy())
            b1.move(pos, COMP_SIGN)
            _, v = minimax(b1, PLAYER_SIGN, -INFINITY, INFINITY)
            heappush(scores, (v, pos))
        print(scores)
        sc, best_position = nlargest(1, scores)[0]
        self.move(best_position, COMP_SIGN)

    def play(self, is_max):
        while True:
            print(self)
            print(self.get_empty_fields())

            if self.is_over():
                return self.wins()
            elif is_max:
                self.computer_play()
                is_max = False
            else:
                self.user_play()
                is_max = True

    def move(self, position, sign):
        if tuple(position) in self.fields.keys() and position in self.get_empty_fields():
            self.fields[position] = sign


def minimax(board, player, alpha, beta, depth=0):
    if board.is_over():
        # print('GAME IS OVER')
        # print('GAME OVER score:', board.get_score(), board.get_score() - depth)
        return board, board.get_score() - depth

    if player == COMP_SIGN:
        best_value = -INFINITY
        for pos in board.get_empty_fields():
            # child is the same board with 1 additional move on one of the free places
            child = Board(fields=board.fields.copy())
            child.move(pos, player)
            # print(child)
            _, current_value = minimax(child, board.get_enemy(player), alpha, beta, depth=depth + 1)
            best_value = max(current_value, best_value)
            alpha = max(best_value, alpha)
            if alpha >= beta:
                # beta prunning
                break
        return child, best_value - depth

    else:
        best_value = INFINITY
        for pos in board.get_empty_fields():
            # child is the same board with 1 additional move on one of the free places
            child = Board(fields=board.fields.copy())
            child.move(pos, player)
            # print(child)
            _, current_value = minimax(child, board.get_enemy(player), alpha, beta, depth=depth + 1)
            best_value = min(current_value, best_value)
            beta = min(current_value, beta)
            if beta <= alpha:
                # alpha prunning
                break
        return child, best_value - depth

    # for pos in empty_fields:
    #     # child is the same board with 1 additional move on one of the free places
    #     child = Board(fields=board.fields.copy())
    #     child.move(pos, player)
    #     # print(child)
    #     _, current_value = minimax(child, board.get_enemy(player), alpha, beta, depth=depth + 1)
    #     if player == COMP_SIGN:
    #         best_value = max(current_value, best_value)
    #         if current_value >= beta:
    #             # beta prunning
    #             break
    #         alpha = current_value
    #     else:
    #         best_value = min(current_value, best_value)
    #         if current_value <= alpha:
    #             # alpha prunning
    #             break
    #         beta = current_value
    # return child, best_value - depth


def tic_tac_toe():
    rand_num = randint(0, 1000)
    print('Fill in board with 0-based numbers!!!')
    if rand_num % 2 == 0:
        # computer
        print('The first player is computer. He plays with O. You play with X.')
        is_computer = True
    else:
        # player
        print('Yey, the first player is you! The computer plays with O. You play with X.')
        is_computer = False

    board = Board()

    board.play(is_computer)
    print(board)


def main():
    # tic_tac_toe()
    rand_num = randint(0, 1000)
    print('Fill in board with 0-based numbers!!!')
    if rand_num % 2 == 0:
        # computer
        print('The first player is computer. He plays with O. You play with X.')
        is_computer = True
    else:
        # player
        print('Yey, the first player is you! The computer plays with O. You play with X.')
        is_computer = False

    board = Board()

    # # test fixes
    # board.fields.update({
    #     (0, 1): 'X',
    #     (1, 2): 'X',
    #     (2, 0): 'O',
    #     (2, 1): 'O',
    #     (2, 2): 'X'
    # })
    # global COMP_SIGN, PLAYER_SIGN
    # COMP_SIGN = 'X'
    # PLAYER_SIGN = 'O'
    # is_computer = False

    board.play(is_computer)
    print(board)


if __name__ == '__main__':
    main()
