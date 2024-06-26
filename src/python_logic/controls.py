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


def open_bag():
    # keyboard.press('x')
    pyautogui.keyDown('x')
    pyautogui.keyUp('x')


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


def surf():
    for i in range(5):
        time.sleep(0.5)
        a_key()
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
    open_bag()

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
            a_key()
            time.sleep(1)
            match menu_num:
                case 3:  # Bag menu
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

        a_key()
        time.sleep(0.5)

        if pyautogui.pixelMatchesColor(save_box_p[0], save_box_p[1], start_save_box):
            print("Game is saved!")
            return True


def activate_repel():
    # pyautogui.screenshot("../images/test_max_repel.png", region=(10, 690, 110, 120))
    w, h = WindowStateManager.get_instance().get_window_size()
    is_searching_bag_menu = False
    p1 = int(0.02422680412371134 * w)
    p2 = int(0.5467289719626168 * h)
    while not is_searching_bag_menu:
        if pyautogui.pixelMatchesColor(p1, p2, (214, 82, 82)):
            is_searching_bag_menu = True
        else:
            left()
            time.sleep(0.3)

    x = int(w * 0.034536082474226806)
    y = int(h * 0.8761682242990654)

    direction_changed = False
    while True:
        try:
            time.sleep(0.1)
            match = pyautogui.locateCenterOnScreen("../images/max_repel.png", region=(10, 690, 110, 120), confidence=0.95)
            if match:
                for i in range(3):
                    time.sleep(0.2)
                    a_key()

                # Close bag and menu
                for i in range(5):
                    b_key()
                    time.sleep(0.5)
                return True

        except pyautogui.ImageNotFoundException:
            if ShutdownStateManager.get_instance().get_state():
                return

            start_p = pyautogui.pixel(x, y)

            if direction_changed:
                up()
            else:
                down()

            if not has_background_changed(x, y, start_p):
                direction_changed = True


def has_background_changed(x, y, pixel):
    if not pyautogui.pixelMatchesColor(x, y, pixel):
        #  print(f"P: {pyautogui.pixel(x, y)}, {shiny_p}")
        pyautogui.moveTo(x, y)
        return True
    else:
        return False
