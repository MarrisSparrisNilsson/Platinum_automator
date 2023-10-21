import time
import keyboard
import pyautogui

from src.python_logic import detection, controls
from src.python_logic.state_manager import WindowStateManager


def flee_encounter():
    x, y = controls.run_btn_coords()

    while True:
        if detection.check_shutdown_state():
            return

        time.sleep(0.1)
        if pyautogui.pixelMatchesColor(x, y, (41, 148, 206)):  # Blue run button
            controls.click_coord(x, y)
            w, h = WindowStateManager.get_instance().get_window_size()
            time.sleep(3.5)
            if pyautogui.pixelMatchesColor(int(w / 4), int(h / 2), (0, 0, 0)):  # Black screen
                print("Encounter ended. Search continues...")
                time.sleep(1.2)
                break
            else:
                print("Error: Unable to escape for some reason...")
                exit()


def soft_reset():
    # pyautogui.hotkey("ctrl", "r")
    keyboard.press("ctrl+r")
    time.sleep(0.1)
    keyboard.release("ctrl+r")
