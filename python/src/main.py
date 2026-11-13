import threading

from src.StateMachine import StateMachine
from src.network.zones import setup_all_zones, validate_zone_data, zone_activation_data, device_nickname_data
from src.agent.agent import preload_llm

DEBUG_MODE_ENABLED = False

if __name__ == "__main__":

    # preload the llm while zones are being initialized
    preload_thread = threading.Thread(target=preload_llm)
    preload_thread.start()

    validate_zone_data()
    setup_all_zones()

    print(zone_activation_data)
    print(device_nickname_data)

    preload_thread.join()

    assistant = StateMachine(debug_mode=DEBUG_MODE_ENABLED)
    assistant.run()
