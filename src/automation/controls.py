import sys
import time

import keyboard
import pyautogui

from src.core.App import app_context
from src.states.Pause import PauseStateManager
from src.states.Shutdown import ShutdownStateManager
from src.states.Hunt import HuntStateManager

_DEBUG_MODE = sys.gettrace() is not None
# When recording with OBS, use this key to switch (show/hide) code/emulator scene
_IS_RECORDING = False


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


def y_button():
    # print("Y")
    pyautogui.keyDown('b')
    pyautogui.keyUp('b')


def x_button():
    # keyboard.press('x')
    # print("X")
    pyautogui.keyDown('x')
    pyautogui.keyUp('x')


def a_button():
    # print("A")
    pyautogui.keyDown('e')
    pyautogui.keyUp('e')


def b_button():
    #     print("A")
    pyautogui.keyDown('space')
    pyautogui.keyUp('space')


def activate_run():
    pyautogui.keyDown('space')


def deactivate_run():
    pyautogui.keyUp('space')


def console_focus():
    pyautogui.hotkey("alt", "4")


def surf():
    for i in range(7):
        time.sleep(0.5)
        a_button()
        # print("A")


def in_game_click():
    pyautogui.mouseDown()
    time.sleep(0.1)
    pyautogui.mouseUp()


def switch_tab():
    pyautogui.hotkey("alt", "tab")

    if _IS_RECORDING:
        pyautogui.keyDown('ScrollLock')
        pyautogui.keyUp('ScrollLock')


def run_btn_coords():
    # Run button: region = (2300, 1100, 550, 300)
    HORIZONTAL = True
    BTN_X = 0.75 if HORIZONTAL else 0.5
    BTN_Y = 0.88 if HORIZONTAL else 0.95

    (window_width, window_height) = app_context.window_size
    x = int(window_width * BTN_X)
    y = int(window_height * BTN_Y)
    return x, y


def click_coord(x, y):
    pyautogui.moveTo(x, y)
    time.sleep(0.1)
    in_game_click()


def move(direction, steps=1):
    switch_tab_DEBUG()
    PauseStateManager.get_instance().check_pause_state()  # Ensure moving has the green light without any pause messages
    if steps == 0:  # Don't bother with turn movements
        if ShutdownStateManager.get_instance().check_shutdown_state():
            return

    move_dirs = ['a', 'w', 'd', 's']
    if direction is int:
        key = move_dirs[direction]
    else:
        if direction in move_dirs:
            key = direction
        else:
            print("Invalid movement key")
            exit(-1)

    # print(f"{steps} step(s): {key}")
    keyboard.press(key)
    # start = time.time()

    if steps == 0:  # Bey-blade
        time.sleep(0.05)  # Turn time
    else:
        # time.sleep(0.27 * steps)  # Walk time
        time.sleep(0.1 * steps)  # Walk time

    keyboard.release(key)
    HuntStateManager.get_instance().set_facing_direction(key)
    # if steps == 0:
    #     time.sleep(0.5)
    # else:
    time.sleep(0.2)  # Don't touch
    # time.sleep(0.5)  # Don't touch
    # end = time.time()
    # print(f"Step active for: {end - start}s")
    switch_tab_DEBUG()


def switch_tab_DEBUG():
    if _DEBUG_MODE:
        print("Debug mode tab switch!")
        switch_tab()
        time.sleep(1)
