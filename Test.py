import Visualize
import threading
import Agents
import Monte_Carlo
import time

window_thread = threading.Thread(target=Visualize.create_window)
window_thread.start()

time.sleep(5)

MC_agent = Agents.MonteCarloAgent(Monte_Carlo.Playout_Policies.Random, 5)
game_thread = threading.Thread(
    target=Agents.Tournament,
    args=(MC_agent.play, Agents.RandomAgent, 20),
    kwargs={'push_to_window': True, 'print_debug': True}
)
game_thread.start()

