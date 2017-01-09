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
        self.children = []

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
            self.children.append(Board(is_computer, fields=new_fields))

    def play(self, is_max):
        while True:
            if is_max:
                self.computer_play()
                is_max = False
            self.user_play()
            is_max = True

    def user_play(self):
        position = input('Enter position with space: ')
        x, y = map(int, position.split(' '))
        if self.fields[x, y] == self.empty:
            self.fields[x, y] = 'X'

    def computer_play(self):
        print(self.get_empty_fields())
        self.generate_children(True)
        print(self.children)

    def minimax(self, board, player, alpha, beta):
        # is game terminated
        if player == COMP_SIGN:
            for child in self.children:
                pass


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
