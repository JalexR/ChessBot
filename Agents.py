import random
import chess
import Visualize
import Monte_Carlo

    

def RandomAgent(board):
    moves = list(board.legal_moves)
    if len(moves) > 1:
        i = random.randint(0, len(moves)-1)
        return moves[i]
    elif len(moves) == 1:
        return moves[0]
    else:
        return None

class MonteCarloAgent():
    def __init__(self, policy, duration):
        self.agent = Monte_Carlo.Agent(policy, duration)

    def play(self, board):
        return self.agent.search(board)

def Tournament(Agent1, Agent2, n, push_to_window = False, print_debug = False):
    '''Play n games between two agents and return the results in array [agent1 wins][draws][agent2 wins] with agent1 as white and agent2 as black.'''
    print('Tournament started')
    result = [0 for i in range(3)]

    for n in range(n):
        board = chess.Board()
        move = Agent1(board)
        
        i = 0
        while move != None and not board.is_game_over():
            if push_to_window:
                Visualize.moves_que.put(board.board_fen())

            if board.turn == chess.WHITE:
                move = Agent1(board)
                if print_debug:
                    print(i, 'Agent ones move:', move)
            else:
                move = Agent2(board)
                if print_debug:
                    print(i, 'Agent twos move:', move)

            board.push(move)
            i += 1

        outcome = board.outcome()
        if outcome is not None:
            winner = outcome.winner
        else:
            winner = None

        if winner == chess.WHITE:
            result[0] += 1
            result_str = 'White'
        elif winner == chess.BLACK:
            result[2] += 1
            result_str = 'Black'
        else:
            result[1] += 1
            result_str = 'Draw'
        
        if print_debug:
            print('Played Game:', n + 1, '  Result:', result_str)
        board.reset()
    
    print(result)
    return result
