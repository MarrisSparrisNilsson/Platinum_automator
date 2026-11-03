import time

import keyboard
import pyautogui

from src.automation import controls
from src.core.App import app_context
from src.states.Shutdown import ShutdownStateManager


def flee_encounter():
    x, y = controls.run_btn_coords()

    while True:
        if ShutdownStateManager.get_instance().is_shutting_down():
            return

        time.sleep(0.1)
        if pyautogui.pixelMatchesColor(x, y, (41, 148, 206)):  # Blue run button
            controls.click_coord(x, y)
            w, h = app_context.window_size
            start_time = time.time()
            duration = 0
            flee_time = 3.2 + 2.8  # 6 seconds
            # Loop until black screen is detected on both screens or break after 6 seconds (in case of some error).
            # Usually flee_time is around 3.20 seconds, but we give it a buffer of 2.8 seconds to be safe.
            while not pyautogui.pixelMatchesColor(int(w / 4), int(h / 2), (0, 0, 0)) and not pyautogui.pixelMatchesColor(
                int(w - (w / 4)), int(h / 2), (0, 0, 0)
            ):
                end_time = time.time()
                duration = end_time - start_time

                if duration > flee_time:
                    break

            if duration > flee_time:
                print("Error: Unable to escape for some reason...")
                exit(0)
            else:
                print("Encounter ended.")
                time.sleep(1.2)
                break


def soft_reset():
    # pyautogui.hotkey("ctrl", "r")
    keyboard.press("ctrl+r")
    time.sleep(0.1)
    keyboard.release("ctrl+r")
