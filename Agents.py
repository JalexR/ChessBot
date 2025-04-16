import random
def RandomAgent(board):
    moves = list(board.legal_moves)
    if len(moves) > 1:
        i = random.randint(0, len(moves)-1)
        return moves[i]
    elif len(moves) == 1:
        return moves[0]
    else:
        return None
