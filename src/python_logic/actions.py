import threading
import keyboard

import detection
from src.python_logic.encounter_methods import Soft_Reset, Flee
from state_manager import HuntStateManager, PauseStateManager, ShutdownStateManager


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
    if not HuntStateManager.get_instance().get_was_hunted_today():
        Soft_Reset.save_in_game()
    if detection.check_shutdown_state():
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
    shutdown_state.set_state(shutdown_event)  # Updating state

    pause_main_event = PauseStateManager.get_instance().get_main_state()
    if pause_main_event is not None:
        pause_main_event.set()  # Signal main pause event to get out of wait state
    HuntStateManager.get_instance().finish_hunt()
