class TicTacToe:
    """Management of a Tic-Tac-Toe game (does not do strategy)."""

    def __init__(self):
        """Start a new game."""
        self. board = [[' '] * 3 for _ in range(3)]
        self. player = 'X'

    def mark(self, i, j):
        """Put an X or O mark at position (i,j) for next player s turn."""
        if not (0 <= i <= 2 and 0 <= j <= 2):
            raise ValueError('Invalid board position')
        if self. board[i][j] != ' ':
            raise ValueError('Board position occupied')
        if self.winner( ) is not None:
            raise ValueError('Game is already complete')
        self.board[i][j] = self.player
        if self.player == 'X':
            self.player = 'O'
        else:
            self.player = 'X'

    def is_win(self, mark):
        """Check whether the board configuration is a win for the given player."""
        board = self.board # local variable for shorthand
        return (
            mark == board[0][0] == board[0][1] == board[0][2] or # row 0
            mark == board[1][0] == board[1][1] == board[1][2] or # row 1
            mark == board[2][0] == board[2][1] == board[2][2] or # row 2
            mark == board[0][0] == board[1][0] == board[2][0] or # column 0
            mark == board[0][1] == board[1][1] == board[2][1] or # column 1
            mark == board[0][2] == board[1][2] == board[2][2] or # column 2
            mark == board[0][0] == board[1][1] == board[2][2] or # diagonal
            mark == board[0][2] == board[1][1] == board[2][0]) # rev diag

    def winner(self):
        """Return mark of winning player, or None to indicate a tie."""
        for mark in 'XO':
            if self.is_win(mark):
                return mark
        return None

    def __str__(self):
        """Return string representation of current game board."""
        rows = ['|' .join(self. board[r]) for r in range(3)]
        return '\n-----\n' .join(rows)
