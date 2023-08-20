import time

# import keyboard
import pyautogui

import detection
from state_manager import WindowStateManager


def clear_movement():
    pyautogui.keyUp('w')
    pyautogui.keyUp('a')
    pyautogui.keyUp('d')
    pyautogui.keyUp('s')
    pyautogui.keyUp('space')


def down():
    # keyboard.press('s')
    pyautogui.keyDown('s')
    pyautogui.keyUp('s')


def up():
    #     keyboard.press('w')
    pyautogui.keyDown('w')
    pyautogui.keyUp('w')


def left():
    #     keyboard.press('a')
    pyautogui.keyDown('a')
    pyautogui.keyUp('a')


def right():
    #     keyboard.press('d')
    pyautogui.keyDown('d')
    pyautogui.keyUp('d')


def open_bag():
    # keyboard.press('x')
    pyautogui.keyDown('x')
    pyautogui.keyUp('x')


def use_selected_item():
    window_width, window_height = WindowStateManager.get_instance().get_window_size()

    dialog_p1 = (int(window_width * 0.032474226804123714), int(window_height * 0.802570093457944))
    dialog_p2 = (int(window_width * 0.4747422680412371), int(window_height * 0.9217289719626168))

    start_p = pyautogui.pixel(dialog_p2[0], dialog_p2[1])

    pyautogui.keyDown('b')
    pyautogui.keyUp('b')

    time.sleep(0.5)

    return False if detection.dialog_is_open(dialog_p1, dialog_p2, start_p) else True


def a_key():
    pyautogui.keyDown('e')
    pyautogui.keyUp('e')


def b_key():
    pyautogui.keyDown('space')
    pyautogui.keyUp('space')


def activate_run():
    pyautogui.keyDown('space')


def deactivate_run():
    pyautogui.keyUp('space')


def console_focus():
    pyautogui.hotkey("alt", "4")


def in_game_click():
    pyautogui.mouseDown()
    time.sleep(0.1)
    pyautogui.mouseUp()


def switch_tab():
    pyautogui.hotkey("alt", "tab")


def run_btn_coords():
    # Run button: region = (2300, 1100, 550, 300)
    window_width, window_height = WindowStateManager.get_instance().get_window_size()
    x, y = (int(window_width * 0.75), int(window_height * 0.88))
    return x, y


def click_coord(x, y):
    pyautogui.moveTo(x, y)
    time.sleep(0.1)
    in_game_click()
