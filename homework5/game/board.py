import json
from random import randint
from copy import deepcopy
from heapq import heappush, nlargest


INFINITY = 2


class Board:
    def __init__(self, is_computer):
        self.empty = '_'
        self.size = 3
        self.player = 'X'
        self.opponent = 'O'
        self.turn = 0
        self.fields = {(i, j): self.empty for j in range(self.size) for i in range(self.size)}
        self.comp_sign = 'X' if is_computer else 'O'
        self.moves = []

        self.next_moves = [pos for pos, sign in self.fields.items() if sign == self.empty]

    def __str__(self):
        board = []
        for i in range(self.size):
            row = []
            for j in range(self.size):
                row.append(self.fields[i, j])
            board.append('|'.join(row))
        return '\n'.join(board)

    def is_winner(self):
        if self.turn == 0: return False, None
        for i in range(self.size):
            row, col, diag, rev_diag = [], [], [], []
            for pos, sign in self.fields.items():
                if pos in self.next_moves: continue
                if pos[0] == i:
                    row.append(sign)
                if pos[1] == i:
                    col.append(sign)
                if pos == (i, i):
                    diag.append(sign)
                if pos[0] + pos[1] == 2:
                    rev_diag.append(sign)
            if row and len(row) == self.size and len(set(row)) == 1:
                print('row', row)
                return True, row[0]
            if col and len(col) == self.size and len(set(col)) == 1:
                print('col', col)
                return True, col[0]
            if diag and len(diag) == self.size and len(set(diag)) == 1:
                print('diag', diag)
                return True, diag[0]
            if rev_diag and len(rev_diag) == self.size and len(set(rev_diag)) == 1:
                print('rev_diag', rev_diag)
                return True, rev_diag[0]
        return False, None

    def wins(self):
        diag, rev_diag = [], []
        for i in range(self.size):
            row, col = [], []
            for pos, sign in self.fields.items():
                if sign != self.empty and pos[0] == i:
                    row.append(sign)
                if sign != self.empty and pos[1] == i:
                    col.append(sign)
                if sign != self.empty and pos == (i, i):
                    diag.append(sign)
                if sign != self.empty and pos[0] + pos[1] == 2:
                    rev_diag.append(sign)

                # print(row)
                # print(col)
                # print(diag)
                # print(rev_diag)
                if len(row) == 3 and len(set(row)) == 1:
                    if sign == self.comp_sign:
                        return 1
                    return -1

                if len(col) == 3 and len(set(col)) == 1:
                    if sign == self.comp_sign:
                        return 1
                    return -1

                if len(diag) == 3 and len(set(diag)) == 1:
                    if sign == self.comp_sign:
                        return 1
                    return -1

                if len(rev_diag) == 3 and len(set(rev_diag)) == 1:
                    if sign == self.comp_sign:
                        return 1
                    return -1
        return 0

    def move(self, row, col):
        # if row in range(1, 4) and col in range(1, 4) and self.fields[row - 1, col - 1] == self.empty:
        if (row, col) in self.next_moves:
            # self.fields[row - 1, col - 1] = self.player
            self.fields[row, col] = self.player
            self.player, self.opponent = self.opponent, self.player
            self.turn += 1
            # self.next_moves.remove((row - 1, col - 1))
            self.next_moves.remove((row, col))
            return True
        else:
            print("MOVE ILLEGAL!!!")
            1/0
            print('Illegal move! Try again...')
            return False

    def update_fields(self, values):
        self.fields = values
        self.player, self.opponent = self.opponent, self.player
        self.turn += 1
        self.next_moves = [pos for pos, sign in self.fields.items() if sign == self.empty]
        self.moves = []

    def check_user_input(self, row, col):
        if row in range(1, 4) and col in range(1, 4) and self.fields[row - 1, col - 1] == self.empty:
            return True
        print('Illegal move! Try again...')
        return False

    """
    Pseudo code:

    function minimax(node, depth, isMaximizingPlayer, alpha, beta):
        if node is a leaf node: // i.e. depth == 3
            return value of the node

        if isMaximizingPlayer:
            bestVal = -INFINITY
            for each child node:
                value = minimax(node, depth + 1, false, alpha, beta)
                bestVal = max(bestVal, value)
                alpha = max(alpha, bestVal)
                if beta <= alpha:
                    break
            return bestVal

        else:
            bestVal = +INFINITY
            for each child node:
                value = minimax(node, depth + 1, true, alpha, beta)
                bestVal = min(bestVal, value)
                beta = min(beta, bestVal)
                if beta <= alpha:
                    break
            return bestVal
    """

    def minimax(self, depth, is_max_player, alpha, beta):
        if depth == self.size:
            # print('DEPTH recursion')
            # print(self)
            # print()
            return self.wins()

        if is_max_player:
            # print('MAX turn')
            # best_value = -INFINITY
            for child in self.get_moves():
                # print_board(child)
                value = child.minimax(depth + 1, False, alpha, beta)
                if (value, str(child)) in self.moves:
                    self.moves.remove((value, str(child)))
                heappush(self.moves, (value, str(child)))
                # best_value = max(best_value, value)
                alpha = max(alpha, value)
                if beta <= alpha:
                    # print('(* β cut-off *)')
                    break
            return alpha
        else:
            # print('min turn')
            # best_value = INFINITY
            for child in self.get_moves():
                # print_board(child)
                value = child.minimax(depth + 1, True, alpha, beta)
                # best_value = min(best_value, value)
                if (value, str(child)) in self.moves:
                    self.moves.remove((value, str(child)))
                heappush(self.moves, (value, str(child)))
                beta = min(beta, value)
                if beta <= alpha:
                    # print('(* α cut-off *)')
                    break
            return beta

    def get_moves(self):
        res = []
        for pos in self.next_moves:
            new_board = deepcopy(self)
            new_board.move(*pos)
            res.append(new_board)
        return res

    def get_best_move(self):
        score, best_move = nlargest(1, self.moves)[0]
        fields = {}
        for i, row in enumerate(best_move.split('\n')):
            items = row.split('|')
            for j, item in enumerate(items):
                fields[i, j] = item
        print(fields)
        return fields

    def play_random(self):
        row, col = self.next_moves[randint(0, len(self.next_moves)) - 1]
        # row, col = randint(1, 3), randint(1, 3)
        print(row + 1, col + 1)
        print("PLAY RANDOM")
        self.move(row, col)

    def play(self, is_computer):
        who = None
        while True:
            if is_computer:
                if self.turn == 0:
                    self.play_random()
                else:
                    self.minimax(0, is_computer, -INFINITY, INFINITY)
                    values = self.get_best_move()
                    self.update_fields(values)
                    print('THE BEST MOVE', values)
                    # TODO: Play the best option
                    # if not val:
                    #     self.play_random()
                is_computer = False

            else:
                is_moved = False
                row, col = None, None
                while not is_moved:
                    row, col = tuple(map(lambda x: int(x), input('Enter a position: ').split(' ')))
                    is_moved = self.check_user_input(row, col)
                self.move(row - 1, col - 1)
                is_computer = True
            print(self)
            print()
            if self.wins(): break
        print('WINNER: {}'.format(who))

