import Visualize
import threading
import Agents
import Monte_Carlo
import time

MC_agent = Agents.MonteCarloAgent(Monte_Carlo.Playout_Policies.Random, 10)
game_thread = threading.Thread(
    target=Agents.Tournament,
    args=(MC_agent.play, Agents.RandomAgent, 20),
    kwargs={'push_to_window': False, 'print_debug': False}
)
game_thread2 = threading.Thread(
    target=Agents.Tournament,
    args=(MC_agent.play, Agents.RandomAgent, 20),
    kwargs={'push_to_window': False, 'print_debug': False}
)

game_thread3 = threading.Thread(
    target=Agents.Tournament,
    args=(MC_agent.play, Agents.RandomAgent, 20),
    kwargs={'push_to_window': False, 'print_debug': False}
)

game_thread4 = threading.Thread(
    target=Agents.Tournament,
    args=(MC_agent.play, Agents.RandomAgent, 20),
    kwargs={'push_to_window': False, 'print_debug': False}
)

game_thread5 = threading.Thread(
    target=Agents.Tournament,
    args=(MC_agent.play, Agents.RandomAgent, 20),
    kwargs={'push_to_window': False, 'print_debug': False}
)

game_thread.start()
game_thread2.start()
game_thread3.start()
game_thread4.start()
game_thread5.start()

