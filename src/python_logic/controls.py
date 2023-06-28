import time

import keyboard
import pyautogui


# import time


def down():
    keyboard.press('s')
    # pyautogui.keyDown('s')
    # pyautogui.keyUp('s')


def up():
    keyboard.press('w')
    # pyautogui.keyDown('w')
    # pyautogui.keyUp('w')


def left():
    keyboard.press('a')
    # pyautogui.keyDown('a')
    # pyautogui.keyUp('a')


def right():
    keyboard.press('d')
    # pyautogui.keyDown('d')
    # pyautogui.keyUp('d')


def open_bag():
    # keyboard.press('x')

    pyautogui.keyDown('x')
    pyautogui.keyUp('x')


def use_selected_item():
    pyautogui.keyDown('b')
    pyautogui.keyUp('b')


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


def switch_tab():
    pyautogui.hotkey("alt", "tab")


def soft_reset():
    # pyautogui.hotkey("ctrl", "r")
    keyboard.press("ctrl+r")
    time.sleep(0.1)
    keyboard.release("ctrl+r")
