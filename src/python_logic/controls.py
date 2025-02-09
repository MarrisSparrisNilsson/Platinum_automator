import time

import keyboard
# import keyboard
import pyautogui

from src.python_logic.states.Window import WindowStateManager
from src.python_logic.states.Shutdown import ShutdownStateManager


def clear_movement():
    pyautogui.keyUp('w')
    pyautogui.keyUp('a')
    pyautogui.keyUp('d')
    pyautogui.keyUp('s')
    pyautogui.keyUp('space')


def turn(key):
    # pyautogui.keyDown(key)
    # pyautogui.keyUp(key)
    keyboard.press(key)
    time.sleep(0.1)
    keyboard.release(key)


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


def x_button():
    # keyboard.press('x')
    pyautogui.keyDown('x')
    pyautogui.keyUp('x')


def a_button():
    pyautogui.keyDown('e')
    pyautogui.keyUp('e')


def b_button():
    pyautogui.keyDown('space')
    pyautogui.keyUp('space')


def activate_run():
    pyautogui.keyDown('space')


def deactivate_run():
    pyautogui.keyUp('space')


def console_focus():
    pyautogui.hotkey("alt", "4")


def surf():
    for i in range(5):
        time.sleep(0.5)
        a_button()
        # print("A")


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


def move(direction, steps=1):
    if ShutdownStateManager.get_instance().check_shutdown_state():
        return

    move_dirs = ['a', 'w', 'd', 's']
    if direction is int:
        key = move_dirs[direction]
    else:
        key = direction

    # print(f"{steps} step(s): {key}")
    keyboard.press(key)
    # start = time.time()

    if steps == 0:  # Bey-blade
        time.sleep(0.05)  # Turn time
    else:
        # time.sleep(0.27 * steps)  # Walk time
        time.sleep(0.1 * steps)  # Walk time

    keyboard.release(key)

    # if steps == 0:
    #     time.sleep(0.5)
    # else:
    time.sleep(0.5)  # Don't touch
    # end = time.time()
    # print(f"Step active for: {end - start}s")
