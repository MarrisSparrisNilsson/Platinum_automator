import time
import sys
import keyboard
import pyautogui

from src.python_logic import controls
from src.python_logic.states.GameView import WindowStateManager
from src.python_logic.states.Shutdown import ShutdownStateManager


def flee_encounter():
    x, y = controls.run_btn_coords()

    while True:
        if ShutdownStateManager.get_instance().check_shutdown_state():
            return

        time.sleep(0.1)
        if pyautogui.pixelMatchesColor(x, y, (41, 148, 206)):  # Blue run button
            controls.click_coord(x, y)
            w, h = WindowStateManager.get_instance().get_window_size()
            start_time = time.time()
            duration = 0
            # While no black screen detected
            while not pyautogui.pixelMatchesColor(int(w / 4), int(h / 2), (0, 0, 0)) and not pyautogui.pixelMatchesColor(int(w - (w / 4)), int(h / 2), (0, 0, 0)):
                end_time = time.time()
                duration = end_time - start_time

                if duration > 6:
                    break
            if duration > 6:
                print("Error: Unable to escape for some reason...")
                sys.exit(0)
            else:
                print("Encounter ended.")
                time.sleep(1.2)
                break


def soft_reset():
    # pyautogui.hotkey("ctrl", "r")
    keyboard.press("ctrl+r")
    time.sleep(0.1)
    keyboard.release("ctrl+r")
