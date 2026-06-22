import threading as thread
import time

import pyautogui
import pygetwindow as pywindow

from src.automation import controls
from src.core.App import app_context


def set_window_focus():
    with thread.Lock():
        window = app_context.get_window()

        # print(f"{window}\n")
        try:
            window.activate()
        except pywindow.PyGetWindowException:
            controls.switch_tab()
            print("Something went wrong when trying to activate the window")
            window.minimize()
            window.maximize()
            window.restore()

        time.sleep(1)


def find_pause_and_resume():
    try:
        res = pyautogui.locateCenterOnScreen("../images/paused.png", region=(0, 0, 210, 100), confidence=0.9)
        # if res is None:
        #     print("The game is up and running!")
        # else:
        pyautogui.click(res)
    except OSError:
        print("Incorrect image source.")
    except pyautogui.ImageNotFoundException:
        # print("The game is up and running!\n")
        pass
