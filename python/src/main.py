import threading

from src.StateMachine import StateMachine
from src.network.zones import setup_all_zones
from src.agent.agent import preload_llm

DEBUG_MODE_ENABLED = False

if __name__ == "__main__":

    if not DEBUG_MODE_ENABLED:
        # preload the llm while zones are being initialized
        t = threading.Thread(target=preload_llm)
        t.start()
        setup_all_zones()
        t.join()
    else:
        setup_all_zones()

    assistant = StateMachine(debug_mode=DEBUG_MODE_ENABLED)
    assistant.run()