import threading

from src.python_logic import detection, controls
from src.python_logic.state_manager import ShutdownStateManager


def fishing(_):
    cast = [0]
    while True:

        detection.check_pause_state("Fishing is paused▶️", "Fishing now continues🎣🪝")

        if detection.check_shutdown_state():
            return

        if controls.use_selected_item():
            detection.find_exclamation_mark(cast)
        else:
            shutdown_state = ShutdownStateManager.get_instance()
            shutdown_event = threading.Event()
            print("Incorrect fishing spot!❌")
            shutdown_event.clear()  # Reset the internal flag to false (Shutting down)
            shutdown_state.set_state(shutdown_event)  # Updating state
