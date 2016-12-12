from random import randint, choice

INFINITY = 100


class Board:
    def __init__(self, is_computer):
        self.empty = '_'
        self.size = 3
        self.player = 'X'
        self.opponent = 'O'
        self.fields = {(i, j): self.empty for j in range(self.size) for i in range(self.size)}

        self.comp_sign = 'X' if is_computer else 'O'

        self.win_states = [[(i, j) for j in range(3)] for i in range(3)]  # col
        self.win_states.extend([[(j, i) for j in range(3)] for i in range(3)])  # row
        self.win_states.append([(i, i) for i in range(self.size)])  # diag
        self.win_states.append([(0, 2), (1, 1), (2, 0)])  # rev_diag

    def __str__(self):
        board = []
        for i in range(self.size):
            row = []
            for j in range(self.size):
                row.append(self.fields[i, j])
            board.append('|'.join(row))
        return '\n'.join(board)

    def get_available_moves(self):
        return [pos for pos, sign in self.fields.items() if sign == self.empty]

    def get_fields(self, player):
        return [pos for pos, sign in self.fields.items() if sign == player]

    def is_game_over(self):
        if self.empty not in self.fields.values() or self.get_winner() is not None:
            return True
        return False

    def min_max(self, player, alpha, beta):
        if self.is_game_over():
            wins = self.get_winner()
            if wins == self.comp_sign: return 1
            elif wins: return -1
            else: return 0

        current_value = -INFINITY if player == self.comp_sign else INFINITY
        for pos in self.get_available_moves():
            if player == self.comp_sign:
                self.move(*pos)
                val = self.min_max(self.opponent, alpha, beta)
                self.move(*pos, sign=self.empty)
                current_value = max(current_value, val)
                if current_value >= beta:
                    return current_value
                alpha = max(alpha, current_value)
            else:
                self.move(*pos)
                val = self.min_max(self.opponent, alpha, beta)
                self.move(*pos, sign=self.empty)
                current_value = min(current_value, val)
                if current_value <= alpha:
                    return current_value
                beta = min(beta, current_value)

        return current_value

    def get_best(self):
        final_res = -INFINITY
        winners = (self.opponent, 'Draw', self.player)

        positions = self.get_available_moves()
        if len(positions) == self.size ** 2:
            return 1, 1

        res = [[], []]
        for pos in self.get_available_moves():
            self.move(*pos)
            v = self.min_max(self.opponent, -2, 2)
            print("move:", pos[0] + 1, pos[1] + 1, "causes:", winners[v + 1])
            if v > -1:
                res[v].append(pos)
            self.move(*pos, sign=self.empty)
        final = 0
        if res[1]:
            final = choice(res[1])
        elif res[0]:
            final = choice(res[0])
        else:
            final = choice(self.get_available_moves())
        return final

    def get_winner(self):
        for player in [self.player, self.opponent]:
            positions = self.get_fields(player)
            if not positions: continue

            for win_state in self.win_states:
                win = True
                for pos in win_state:
                    if pos not in positions:
                        win = False
                if win:
                    return player

        return None

    def move(self, row, col, sign=None):
        sign = sign if sign else self.player
        # if (row, col) in self.get_available_moves():
        self.fields[row, col] = sign
        self.player, self.opponent = self.opponent, self.player
        return True
        # else:
        #     print('Illegal move! Try again...')
        #     return False

    def check_user_input(self, row, col):
        if row in range(1, 4) and col in range(1, 4) and self.fields[row - 1, col - 1] == self.empty:
            return True
        print('Illegal move! Try again...')
        return False

    def play(self, is_computer):

        while not self.is_game_over():

            if is_computer:
                best_position = self.get_best()
                self.move(*best_position)
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

        winner = self.get_winner()
        if winner:
            print('WINNER: {}'.format(winner))
        else:
            print('It\'s a tie...')
