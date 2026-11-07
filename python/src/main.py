import threading

from src.StateMachine import StateMachine
from src.network.zones import setup_all_zones
from src.agent.agent import preload_llm

DEBUG_MODE_ENABLED = True

if __name__ == "__main__":

    # preload the llm while zones are being initialized
    preload_thread = threading.Thread(target=preload_llm)
    preload_thread.start()

    setup_all_zones()
    preload_thread.join()

    assistant = StateMachine(debug_mode=DEBUG_MODE_ENABLED)
    assistant.run()
