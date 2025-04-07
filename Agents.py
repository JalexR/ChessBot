import random
def RandomAgent(board):
    moves = list(board.legal_moves)
    i = random.randint(0, len(moves)-1)
    return moves[i]
