import chess
import Visualize
import threading
import Agents

window_thread = threading.Thread(target=Visualize.create_window)
window_thread.start()

result = [0 for i in range(3)]
for n in range(20):
    board = chess.Board()
    move = Agents.RandomAgent(board)
    
    while move != None:
        Visualize.moves_que.put(board.board_fen())
        board.push(move)
        move = Agents.RandomAgent(board)

    outcome = board.outcome()
    if outcome == chess.WHITE:
        result[0] += 1
    if outcome == chess.BLACK:
        result[2] += 1
    else:
        result[1] += 1
    result.append()
    board.reset()

print(result)


