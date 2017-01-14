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

from copy import deepcopy

INFINITY = 1000000


def generate_children(node):
    result = []
    for i, row in enumerate(node):
        if '_' in row:
            for idx in range(3):
                if row[idx] == '_':
                    child = deepcopy(node)
                    child[idx][i] = 'X'
                    result.append(child)
    return result


def minimax(node, depth, is_max_player, alpha, beta):
    mark = 'X'
    if depth == 3:
        # return 1
        if (mark == node[0][0] == node[0][1] == node[0][2] or  # row 0
        mark == node[1][0] == node[1][1] == node[1][2] or  # row 1
        mark == node[2][0] == node[2][1] == node[2][2] or  # row 2
        mark == node[0][0] == node[1][0] == node[2][0] or  # column 0
        mark == node[0][1] == node[1][1] == node[2][1] or  # column 1
        mark == node[0][2] == node[1][2] == node[2][2] or  # column 2
        mark == node[0][0] == node[1][1] == node[2][2] or  # diagonal
        mark == node[0][2] == node[1][1] == node[2][0]):  # rev diag
            return 1
        elif ('O' == node[0][0] == node[0][1] == node[0][2] or  # row 0
                              'O' == node[1][0] == node[1][1] == node[1][2] or  # row 1
                              'O' == node[2][0] == node[2][1] == node[2][2] or  # row 2
                              'O' == node[0][0] == node[1][0] == node[2][0] or  # column 0
                              'O' == node[0][1] == node[1][1] == node[2][1] or  # column 1
                              'O' == node[0][2] == node[1][2] == node[2][2] or  # column 2
                              'O' == node[0][0] == node[1][1] == node[2][2] or  # diagonal
                              'O' == node[0][2] == node[1][1] == node[2][0]):
            return -1
        else:
            return 0

    if is_max_player:
        # print('MAX turn')
        best_value = -INFINITY
        for child in generate_children(node):
            # print_board(child)
            value = minimax(node, depth + 1, False, alpha, beta)
            best_value = max(best_value, value)
            alpha = max(alpha, best_value)
            if beta <= alpha:
                break
        return best_value
    else:
        # print('min turn')
        best_value = INFINITY
        for child in generate_children(node):
            # print_board(child)
            value = minimax(node, depth + 1, True, alpha, beta)
            best_value = min(best_value, value)
            beta = min(beta, best_value)
            if beta <= alpha:
                break
        return best_value


def print_board(node):
    rows = ['|'.join(node[r]) for r in range(3)]
    print('\n'.join(rows))
    print()


def main():
    # Calling the function for the first time.
    node = [['_', '_', '_'], ['_', '_', '_'], ['_', '_', '_']]
    print_board(node)
    res = minimax(node, 0, True, -INFINITY, INFINITY)
    # TODO: If there is still place in the board, make a move.
    if res == 0:
        print('0 : 0')
    elif res == 1:
        print('X wins!')
    else:
        print('O wins!')
    print_board(node)

if __name__ == '__main__':
    main()
