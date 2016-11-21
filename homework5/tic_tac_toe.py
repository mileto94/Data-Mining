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

INFINITY = 1000000


def generate_children(node):
    return [['X', 'O', ''], ['', '', ''], ['', 'X', '']]


def minimax(node, depth, is_max_player, alpha, beta):
    if depth == 3:
        return node

    if is_max_player:
        print('MAX turn')
        best_value = -INFINITY
        for child in generate_children(node):
            value = minimax(node, depth + 1, False, alpha, beta)
            best_value = max(best_value, value)
            alpha = max(alpha, best_value)
            if beta <= alpha:
                break
        return best_value
    else:
        print('min turn')
        best_value = INFINITY
        for child in generate_children(node):
            value = minimax(node, depth + 1, True, alpha, beta)
            best_value = min(best_value, value)
            beta = min(beta, best_value)
            if beta <= alpha:
                break
        return best_value


def main():
    # Calling the function for the first time.
    print(minimax(0, 0, True, -INFINITY, INFINITY))


if __name__ == '__main__':
    main()
