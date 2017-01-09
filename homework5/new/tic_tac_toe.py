from random import randint
from collections import OrderedDict


COMP_SIGN = 'O'
INFINITY = 100


class Board:
    def __init__(self, is_computer, fields=[]):
        self.size = 3
        self.empty = '_'
        self.fields = fields if fields else OrderedDict(
            {(i, j): self.empty for j in range(self.size) for i in range(self.size)})
        self.sign = COMP_SIGN if is_computer else self.get_enemy(COMP_SIGN)
        self.winnging=self.children = {}
        self.winning_states = [(i, j) for j in range(self.size) for i in range(self.size)] # rows
        self.winning_states.append([(i, j) for i in range(self.size) for j in range(self.size)])  # cols
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
        return 'O' if sign == 'x' else 'X'

    def get_empty_fields(self):
        return [pos for pos, val in self.fields.items() if val == self.empty]

    def get_sign(self, is_computer):
        return 'O' if is_computer else 'X'

    def generate_children(self, is_computer):
        self.children = []
        for pos in self.get_empty_fields():
            new_fields = self.fields.copy()
            new_fields[pos] = self.get_sign(is_computer)
            self.children[Board(is_computer, fields=new_fields)] = 0

    def wins(self, is_computer):
        current_player = COMP_SIGN if is_computer else self.get_enemy(COMP_SIGN)
        played_positions = [pos for pos, player in self.fields if player == current_player]
        for combo in self.winning_states:
            played = [True for win in combo if win in played_positions]
            if len(played) == self.size:
                return True
        return False

    def is_over(self, player):
        is_max = True if player == COMP_SIGN else False
        if self.empty not in self.fields or self.wins(is_max) is not None:
            return True
        return False

    def get_score(self):
        if self.wins(COMP_SIGN):
            return 10
        elif self.wins(self.get_enemy(COMP_SIGN)):
            return -10
        return 0

    def user_play(self):
        position = input('Enter position with space: ')
        x, y = map(int, position.split(' '))
        if -1 < x < 3 and -1 < y < 3 and self.fields[x, y] == self.empty:
            self.fields[x, y] = 'X'
        else:
            print('This filed is not empty or the coordinates are not valid!')
            self.user_play()

    def computer_play(self):
        val = minimax(self, COMP_SIGN, -INFINITY, INFINITY)
        print(val)
        print(self.get_empty_fields())
        print(self.children)

    def play(self, is_max):
        while True:
            if is_max:
                self.computer_play()
                is_max = False
            self.user_play()
            is_max = True


def minimax(board, player, alpha, beta):
    # check whether game is terminated
    if board.is_over(player):
        return board.get_score()

    val = INFINITY
    if player == COMP_SIGN:
        for child in board.children:
            # MOVEEEEE!!!
            val = minimax(child, child.get_enemy(player), alpha, beta)
            if val >= beta:
                # beta prunning
                return val
            alpha = val
            return val
    else:
        for child in board.children:
            # MOVEEEEE!!!
            val = minimax(child, child.get_enemy(player), alpha, beta)
            if val <= alpha:
                # alpha prunning
                return val
            beta = val
            return val


def main():
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

    board = Board(is_computer)

    board.play(is_computer)
    print(board)


if __name__ == '__main__':
    main()
