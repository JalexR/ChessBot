import chess
import Visualize
import threading
import Agents

window_thread = threading.Thread(target=Visualize.create_window)
window_thread.start()



def RandomGames(n):
    result = [0 for i in range(3)]
    for n in range(n):
        board = chess.Board()
        move = Agents.RandomAgent(board)
        
        i = 0
        while move != None and i < 250:
            Visualize.moves_que.put(board.board_fen())
            board.push(move)
            move = Agents.RandomAgent(board)
            i += 1
        print('Played Game:', n)

        outcome = board.outcome()
        if outcome == chess.WHITE:
            result[0] += 1
        if outcome == chess.BLACK:
            result[2] += 1
        else:
            result[1] += 1
        board.reset()
    
    print(result)
    return result

game_thread = threading.Thread(target=RandomGames(1000))
game_thread.start()

