import chess
import Visualize
import threading
import Agents

window_thread = threading.Thread(target=Visualize.create_window)
window_thread.start()

result = [3]
board = chess.Board()
for i in range(0,1000):
    Visualize.moves_que.put(board.board_fen())
    move = Agents.RandomAgent(board)
    if move == None:
        outcome = board.outcome()
        if 
        result.append()
        break
    else:
        board.push(move)

print(result)


