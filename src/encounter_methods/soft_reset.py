import threading

# import pyautogui
import time

from src.automation import controls
from src.encounter_methods.flee import soft_reset
from src.states.Pause import PauseStateManager
from src.states.Shutdown import ShutdownStateManager


def static_encounter(_):
    pause_manager = PauseStateManager.get_instance()
    encounter_pause_event = pause_manager.get_encounter_pause_state()
    while True:
        encounter_pause_event.clear()  # Pauses encounter detection

        soft_reset()

        start_time = time.time()
        duration = 0

        # Press "a" during startup
        print("Started waiting")
        while duration < 15:  # Time until encounter detection starts

            if ShutdownStateManager.get_instance().is_shutting_down():
                return

            time.sleep(0.3)
            controls.a_button()
            end_time = time.time()
            duration = end_time - start_time

        print("Finished waiting", duration)
        encounter_pause_event.set()  # Resumes encounter detection

        # Press "a" until encounter starts
        while True:
            if PauseStateManager.get_instance().check_search_encounter_breakpoint(
                "Button presses is paused.",
                "\nButton presses now continues.",
            ):
                break

            if ShutdownStateManager.get_instance().is_shutting_down():
                return

            time.sleep(0.5)
            controls.a_button()
