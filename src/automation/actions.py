import keyboard

from src.automation import controls, in_game_menu_controls
from src.core.App import app_context
from src.core.enums import InGameMenuSlots
from src.encounter_methods import egg, flee, soft_reset
from src.states.Hunt import HuntStateManager
from src.states.Pause import PauseStateManager
from src.states.Shutdown import ShutdownStateManager
from src.vision import encounter_detector


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
    encounter_detector.encounter_detection(search_encounter_func, end_encounter_func=flee.flee_encounter, search_args=search_args)


def egg_hunt(_a, _b):
    egg.hatch_egg()

    # encounter_detector.encounter_detection(search_encounter_func, end_encounter_func=Flee.flee_encounter, search_args=search_args)


def soft_reset_hunt(_a, _b):
    hunt_mode = HuntStateManager.get_instance().get_hunt_mode()
    print(f"Beginning {hunt_mode} hunt!")
    if not HuntStateManager.get_instance().get_was_hunted_today():
        in_game_menu_controls.execute_inGame_menu_action(InGameMenuSlots.SAVE)
    if ShutdownStateManager.get_instance().check_shutdown_state():
        return
    encounter_detector.encounter_detection(search_encounter_func=soft_reset.static_encounter, end_encounter_func=flee.soft_reset)


def regular_hunt(search_encounter_func, search_args):
    encounter_detector.encounter_detection(search_encounter_func, end_encounter_func=flee.flee_encounter, search_args=search_args)


def watch_exit():
    """
    Await the escape button being pressed to signal a shutdown request.
    """
    # shutdown_state = ShutdownStateManager.get_instance()
    shutdown_event = app_context.shutdown_event
    keyboard.wait("esc")
    print("\nEscape was pressed!🚨")
    shutdown_event.set()  # Set the internal flag to True (Send Shutdown signal)
    # shutdown_state.set_state(shutdown_event)  # Updating states

    pause_main_event = PauseStateManager.get_instance().get_main_pause_state()
    if pause_main_event is not None:
        pause_main_event.set()  # Signal main pause event to get out of wait states
        PauseStateManager.get_instance().set_main_state(pause_main_event)

    # HuntStateManager.get_instance().save_hunt()
    controls.clear_movement()
