import time
import sys
import keyboard
import pyautogui

from src.python_logic import detection, controls
from ..state_manager import WindowStateManager


def flee_encounter():
    x, y = controls.run_btn_coords()

    while True:
        if detection.check_shutdown_state():
            return

        time.sleep(0.1)
        if pyautogui.pixelMatchesColor(x, y, (41, 148, 206)):  # Blue run button
            controls.click_coord(x, y)
            # w, h = WindowStateManager.get_instance().get_window_size()
            size = WindowStateManager.get_instance().get_window_size()
            window = WindowStateManager.get_instance().get_window()
            print(window)
            print(size)
            w, h = size
            pyautogui.moveTo(int(w / 4), int(h / 2))
            # time.sleep(2.5)
            start_time = time.time()
            duration = 0
            while pyautogui.pixelMatchesColor(int(w / 4), int(h / 2), (0, 0, 0)):
                end_time = time.time()
                duration = end_time - start_time
                # if pyautogui.pixelMatchesColor(int(w / 4), int(h / 2), (0, 0, 0)):  # Black screen

                if duration > 6:
                    break
            if duration > 6:
                print("Error: Unable to escape for some reason...")
                sys.exit(0)
            else:
                print("Encounter ended. Search continues...")
                time.sleep(1.2)


def soft_reset():
    # pyautogui.hotkey("ctrl", "r")
    keyboard.press("ctrl+r")
    time.sleep(0.1)
    keyboard.release("ctrl+r")
