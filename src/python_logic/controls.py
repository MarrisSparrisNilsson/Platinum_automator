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

    if steps == 0:
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


def select_in_game_menu_action(menu_num, option=1):
    x_button()

    # Menu start x: W * 0.3082474226804124
    # Menu start y: H * 0.10163551401869159

    # Menu end y: H * 0.9392523364485982

    # Menu Y: H * (0.24065420560747663 - 0.12967289719626168)

    window_width, window_height = WindowStateManager.get_instance().get_window_size()
    menu_p = (int(window_width * 0.3077319587628866), int(window_height * (0.18574766355140188 + ((menu_num - 1) * (0.24065420560747663 - 0.12967289719626168)))))
    # menu_p = (int(window_width * 0.3077319587628866), int(window_height * 0.6285046728971962))
    # save_box_p = (int(window_width * 0.12061855670103093), int(window_height * 0.32710280373831774))
    # start_save_box = pyautogui.pixel(save_box_p[0], save_box_p[1])
    pyautogui.moveTo(menu_p)

    is_done = False
    while not is_done:
        time.sleep(0.1)
        if ShutdownStateManager.get_instance().check_shutdown_state():
            return

        if pyautogui.pixelMatchesColor(menu_p[0], menu_p[1], (255, 107, 16)):
            a_button()
            time.sleep(1)
            match menu_num:
                case 3:
                    if option == 1:
                        is_done = activate_repel()
                case 5:
                    is_done = save_in_game()
                case _:
                    is_done = True

        else:
            if menu_num > 4:
                up()
            else:
                down()
    # time.sleep(0.5)


def save_in_game():
    window_width, window_height = WindowStateManager.get_instance().get_window_size()
    save_box_p = (int(window_width * 0.12061855670103093), int(window_height * 0.32710280373831774))
    start_save_box = pyautogui.pixel(save_box_p[0], save_box_p[1])
    while True:
        if ShutdownStateManager.get_instance().check_shutdown_state():
            return True

        a_button()
        time.sleep(0.5)

        if pyautogui.pixelMatchesColor(save_box_p[0], save_box_p[1], start_save_box):
            print("Game is saved!")
            return True


def activate_repel():
    # pyautogui.screenshot("../images/test_max_repel.png", region=(10, 690, 110, 120))
    while True:
        try:
            time.sleep(0.1)
            match = pyautogui.locateCenterOnScreen("../images/max_repel.png", region=(10, 690, 110, 120), confidence=0.9)
            if match:
                for i in range(3):
                    time.sleep(0.2)
                    a_button()

                # Close bag and menu
                for i in range(5):
                    b_button()
                    time.sleep(0.5)
                return True
        except pyautogui.ImageNotFoundException:
            if ShutdownStateManager.get_instance().get_state():
                return
            down()
