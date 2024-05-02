import threading
import keyboard

from src.python_logic import detection, controls
from src.python_logic.encounter_methods import Soft_Reset, Flee
from src.python_logic.states.Shutdown import ShutdownStateManager
from src.python_logic.states.Pause import PauseStateManager
from src.python_logic.states.Hunt import HuntStateManager
from src.python_logic.Enums import HuntMode, WalkTypes, FishingTypes
from src.python_logic.encounter_methods import Fishing, Regular


def pokeradar_hunt():
    # while not keyboard.is_pressed("q"):
    while True:
        # while - begin
        # Press b

        # --- Locate 1st grass patch to follow ---
        # Out of the maximum 4 patches that can spawn,
        # locate the furthest away grass patch of the same type (4 tiles away)
        # if it is an edge grass -> continue
        # elseif no grass patch of the same type was spotted 4 tiles away ->
        # - Find_safe_zone()
        # - Recharge_radar() (Run back and forth x steps in a safe direction and length until it's recharged.)
        # else -> break (Valid grass patch was located)

        # while - end

        # Walk into that grass patch

        # Faint pokemon

        return None


def fishing_hunt(search_encounter_func, search_args):
    detection.encounter_detection(search_encounter_func, end_encounter_func=Flee.flee_encounter, search_args=search_args)


def soft_reset_hunt():
    hunt_mode = HuntStateManager.get_instance().get_hunt_mode()
    print(f"Beginning {hunt_mode} hunt!")
    if not HuntStateManager.get_instance().get_was_hunted_today():
        controls.select_in_game_menu_action(5)
    if ShutdownStateManager.get_instance().check_shutdown_state():
        return
    detection.encounter_detection(search_encounter_func=Soft_Reset.static_encounter, end_encounter_func=Flee.soft_reset)


def regular_hunt(search_encounter_func, search_args):
    detection.encounter_detection(search_encounter_func, end_encounter_func=Flee.flee_encounter, search_args=search_args)


def watch_exit():
    shutdown_state = ShutdownStateManager.get_instance()
    shutdown_event = threading.Event()
    keyboard.wait("esc")
    print("\nEscape was pressed!🚨")
    shutdown_event.clear()  # Reset the internal flag to false (Shutting down)
    shutdown_state.set_state(shutdown_event)  # Updating states

    pause_main_event = PauseStateManager.get_instance().get_main_pause_state()
    if pause_main_event is not None:
        pause_main_event.set()  # Signal main pause event to get out of wait states
    HuntStateManager.get_instance().finish_hunt()
    controls.clear_movement()


action_types = {
    f"{HuntMode.POKERADAR.value}": {
        "action": None,
        "method_required": True,
    },
    f"{HuntMode.FISHING.value}": {
        "action": fishing_hunt,
        "method_required": True,
        "methods": [
            {
                "number": 1,
                "method_name": f"{FishingTypes.REGULAR.value}",
                "method": Fishing.fishing,
                "args": True  # Continue infinitely
            },
            {
                "number": 2,
                "method_name": f"{FishingTypes.FEEBAS.value}",
                "method": Fishing.feebas_fishing,
                "args": None
            }
        ]
    },
    f"{HuntMode.FOSSIL.value}": {
        "action": None,
        "method_required": True,
    },
    f"{HuntMode.SAFARI_ZONE.value}": {
        "action": None,
        "method_required": True,
    },
    f"{HuntMode.SOFT_RESET.value}": {
        "action": soft_reset_hunt,
        "method_required": False,
    },
    f"{HuntMode.EGG.value}": {
        "action": None,
        "method_required": True,
    },
    f"{HuntMode.REGULAR.value}": {
        "action": regular_hunt,
        "method_required": True,
        "methods": [
            {
                "number": 1,
                "method_name": f"{WalkTypes.RANDOM.value}",
                "method": Regular.walk_random,
                "args": None
            },
            {
                "number": 2,
                "method_name": f"{WalkTypes.CIRCLES.value}",
                "method": Regular.lets_try_spinning,
                "args": 1
            }
        ]
    }
}
