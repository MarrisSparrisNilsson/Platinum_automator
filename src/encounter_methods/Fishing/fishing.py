import threading

from src.automation import in_game_menu_controls
from src.states.Pause import PauseStateManager
from src.states.Shutdown import ShutdownStateManager
from src.vision import encounter_detector


def fishing(args):
    cast = [0]
    encounters = [0]
    while args is True or encounters[0] < args:  # args is bool or int

        PauseStateManager.get_instance().check_pause_state("Fishing is paused▶️", "Fishing now continues🎣🪝")
        if ShutdownStateManager.get_instance().check_shutdown_state():
            return

        if in_game_menu_controls.use_registered_key_item():
            encounter_detector.find_exclamation_mark(cast, encounters)
        else:
            shutdown_state = ShutdownStateManager.get_instance()
            shutdown_event = threading.Event()
            print("Incorrect fishing spot!❌")
            shutdown_event.clear()  # Reset the internal flag to false (Shutting down)
            shutdown_state.set_state(shutdown_event)  # Updating state
