from src.StateMachine import StateMachine
from src.network.zones import setup_all_zones

if __name__ == "__main__":
    setup_all_zones()
    assistant = StateMachine()
    assistant.run()