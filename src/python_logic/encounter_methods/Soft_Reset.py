import threading
import pyautogui
import time

from src.python_logic import controls, detection
from src.python_logic.encounter_methods.Flee import soft_reset
from src.python_logic.state_manager import WindowStateManager, PauseStateManager


def save_in_game():
    window_width, window_height = WindowStateManager.get_instance().get_window_size()
    print(window_width, window_height)
    save_p = (int(window_width * 0.3077319587628866), int(window_height * 0.6285046728971962))
    save_box_p = (int(window_width * 0.12061855670103093), int(window_height * 0.32710280373831774))
    start_save_box = pyautogui.pixel(save_box_p[0], save_box_p[1])

    controls.open_bag()

    while True:
        time.sleep(0.1)
        if detection.check_shutdown_state():
            return

        if pyautogui.pixelMatchesColor(save_p[0], save_p[1], (255, 107, 16)):
            while True:
                if detection.check_shutdown_state():
                    return

                controls.a_key()
                time.sleep(0.5)

                if pyautogui.pixelMatchesColor(save_box_p[0], save_box_p[1], start_save_box):
                    print("Game is saved!")
                    return
        else:
            controls.up()


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
        while duration < 15:  # Time until encounter detection starts
            if detection.check_shutdown_state():
                return

            time.sleep(0.3)
            controls.a_key()
            end_time = time.time()
            duration = end_time - start_time

        pause_main_event.set()  # Resumes encounter detection
        pause_main_state.set_main_state(pause_main_event)

        # Press "a" until encounter starts
        while True:
            if detection.check_pause_state("Button presses is paused.", "\nButton presses now continues."):
                break

            if detection.check_shutdown_state():
                return

            time.sleep(0.5)
            controls.a_key()
