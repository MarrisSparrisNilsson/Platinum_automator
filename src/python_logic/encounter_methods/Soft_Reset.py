import threading
import pyautogui
import time

from src.python_logic import controls
from src.python_logic.encounter_methods.Flee import soft_reset
from src.python_logic.state.state_manager import WindowStateManager, PauseStateManager, ShutdownStateManager


def static_encounter(_):
    pause_main_state = PauseStateManager.get_instance()
    pause_main_event = threading.Event()
    while True:
        pause_main_event.clear()  # Pauses encounter detection
        pause_main_state.set_main_state(pause_main_event)

        soft_reset()

        start_time = time.time()
        duration = 0

        # Press "a" during startup
        print("Started waiting")
        while duration < 15:  # Time until encounter detection starts

            if ShutdownStateManager.get_instance().check_shutdown_state():
                return

            time.sleep(0.3)
            controls.a_key()
            end_time = time.time()
            duration = end_time - start_time

        print("Finished waiting", duration)
        pause_main_event.set()  # Resumes encounter detection
        pause_main_state.set_main_state(pause_main_event)

        # Press "a" until encounter starts
        while True:
            if PauseStateManager.get_instance().check_pause_state("Button presses is paused.", "\nButton presses now continues."):
                break

            if ShutdownStateManager.get_instance().check_shutdown_state():
                return

            time.sleep(0.5)
            controls.a_key()
