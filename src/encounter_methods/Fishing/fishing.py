import time

import emoji
import pyautogui

from src.automation import controls, in_game_menu_controls
from src.states.Pause import PauseStateManager
from src.states.Shutdown import ShutdownStateManager
from src.vision import encounter_detector
from src.vision.game_ui_detector import dialog_is_open


def fishing(encounters, walking_status=False):
    cast = 0
    encounter = 0
    exclamation_mark_found = False

    PauseStateManager.get_instance().get_encounter_pause_state().set()  # Resumes encounter detection

    # Negative encounters: Fish infinitely!
    # Positive encounters: Fish until the goal is reached.
    while encounters < 0 or encounter < encounters:
        try:
            # If fishing is not paused

            PauseStateManager.get_instance().check_search_encounter_breakpoint(
                f"Fishing is paused {emoji.emojize(':play_button:')}",
                f"Fishing {'and walking ' if walking_status else ''}now continues{emoji.emojize(':fishing_pole::hook:')}",
            )

            if ShutdownStateManager.get_instance().is_shutting_down():
                return

            in_game_menu_controls.use_registered_key_item()  # Use fishing rod

            while not exclamation_mark_found and not dialog_is_open():
                if not PauseStateManager.get_instance().get_search_encounter_pause_state().is_set():
                    break

                if ShutdownStateManager.get_instance().is_shutting_down():
                    return
                exclamation_mark_found = encounter_detector.find_exclamation_mark()

            if exclamation_mark_found:
                print("\nExclamation found❗")
                exclamation_mark_found = False
                cast = 0
                encounter += 1
                print(f"Encounters: ({encounter}/{encounters})" if encounters > 1 else "")
                # Secure fish on hook
                for i in range(6):
                    pyautogui.keyDown("e")
                    time.sleep(0.025)
                    pyautogui.keyUp("e")
                    print("\r", end=f"A button was pressed: {i + 1} times")
                time.sleep(0.5)  # Prevent use of fishing rod too quickly (in the loop) when encounter starts.

            # No fish on the hook
            elif dialog_is_open():
                time.sleep(0.2)
                controls.b_button()
                cast += 1
                print_encounters = f", Encounters: ({encounter}/{encounters})" if encounters > 1 else ""
                print("\r", end=f"No fish this time ({cast}){print_encounters}")

        except EnvironmentError:
            shutdown_manager = ShutdownStateManager.get_instance()
            shutdown_event = shutdown_manager.get_state()
            print("Incorrect fishing spot!❌")
            shutdown_event.set()  # Reset the internal flag to True (Shutting down)
            return

    print("\nMoving on to next fishing spot...")
