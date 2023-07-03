import keyboard
import pygetwindow as pywindow
import pyautogui
import time
import math
import os
import threading as thread

import controls
# from actions import walk_random
from state_manager import ExitStateManager, PauseStateManager


def find_pause_and_resume():
    # screenshot = pyautogui.screenshot(region=(0, 0, 210, 100))
    # screenshot.save("../images/test.png")

    # pyautogui.moveTo(res)
    try:
        res = pyautogui.locateCenterOnScreen("../images/paused.png", region=(0, 0, 210, 100), confidence=0.9)
        if res is None:
            print("Pause button was not found.")
        else:
            pyautogui.click(res)
            print(res)
    except OSError:
        print("Incorrect image source.")


def find_sparkles(habitat):
    try:
        # screenshot = pyautogui.screenshot(region=(850, 100, 850, 1000))
        # screenshot = pyautogui.screenshot(region=(850, 700, 850, 400))
        # screenshot.save("../images/test/shiny_area.png")

        # sparkles_list = ["cave", "eterna_forest_day", "snow_day", "snow_evening", "water_day"]
        # sparkles_list_len = len(sparkles_list)

        folder_dir = f"../images/sparkles/{habitat}"
        counter = 1
        for image in os.listdir(folder_dir):

            # for i in range(len(sparkles_list)):
            sparkles = None
            print(f"Looking for shiny {counter}")
            counter += 1
            if image.endswith(".png"):
                # sparkles = pyautogui.locateOnScreen(f"../images/sparkles/other/indoor.png",
                sparkles = pyautogui.locateOnScreen(f"{folder_dir}/{image}",
                                                    region=(800, 100, 950, 1000),
                                                    # region=(850, 700, 850, 400),
                                                    confidence=0.6)
            if sparkles:
                pyautogui.moveTo(pyautogui.center(sparkles))
                pyautogui.screenshot(region=(800, 100, 920, 960)).save("../images/test/detected_sparkle.png")
                print(f"Sparkles was found for the {habitat} habitat, matching {image}!")
                return True

        print(f"Sparkles was not found in {habitat}.")
        return False
        # return True
    except OSError:
        print("Incorrect image source.")
        quit()


def get_mouse_coords():
    mouse = pyautogui.position()
    print(mouse)


def get_encounter_pixels(window_width, window_height):
    w_rounder = window_width % 100
    w_hundred = math.floor(window_width / 100)

    h_rounder = window_height % 100
    h_hundred = math.floor(window_height / 100)

    if w_rounder < 50:
        width = w_hundred * 100
    else:
        width = (w_hundred + 1) * 100

    if h_rounder < 50:
        height = h_hundred * 100
    else:
        height = (h_hundred + 1) * 100

    print(f"W: {width}, H: {height}")
    w1 = int(width / 4)
    w2 = int(width - (width / 4))
    h = int(height / 2)
    pixel_one = (w1, h)
    pixel_two = (w2, h)

    return pixel_one, pixel_two


def encounter_started(pixel_coord_one, pixel_coord_two):
    # print(f"Left_P: {pixel_coord_one}\nRight_P: {pixel_coord_two}")
    x1, y1 = pixel_coord_one
    x2, y2 = pixel_coord_two

    pixel_one = pyautogui.pixel(x1, y1)
    pixel_two = pyautogui.pixel(x2, y2)

    # print(f"Left_P_rgb: {pixel_one}\nRight_P_rgb: {pixel_two}")

    if pixel_one == (0, 0, 0) and pixel_two == (0, 0, 0):
        # pause_state = PauseStateManager.get_instance()
        # pause_state.set_state(True)
        print("Encounter started!")
        start_time = time.time()
        controls.clear_movement()
        time.sleep(0.1)
        controls.switch_tab()
        # time.sleep(1)
        time.sleep(3)
        # keyboard.unhook_all()
        return start_time, True
    else:
        return 0, False


def encounter_detection(window_width, window_height, habitat, search_encounter_func):
    p1, p2 = get_encounter_pixels(window_width, window_height)

    pause_state = PauseStateManager.get_instance()
    shutdown_state = ExitStateManager.get_instance()
    # is_paused = pause_state.get_state()

    pause_event = thread.Event()
    shutdown_event = thread.Event()

    shutdown_state.set_state(shutdown_event)

    shutdown_event.set()

    search_encounter_thread = thread.Thread(target=search_encounter_func, daemon=True)

    time.sleep(1)
    startup_time = 11.5
    search_encounter_thread.start()
    shiny_is_found = False

    # while not shiny_is_found and not is_exiting:
    while not shiny_is_found:

        with shutdown_event:
            if shutdown_event.is_set():
                break

        duration = 0
        time.sleep(0.3)

        start_time, is_encounter = encounter_started(p1, p2)
        if is_encounter:
            pause_event.set()
            pause_state.set_state(pause_event)
            # search_encounter_thread.join()

        while is_encounter and not shiny_is_found and duration < startup_time:

            with shutdown_event:
                if shutdown_event.is_set():
                    break

            # if duration > startup_time - 2:
            #     print("No shiny this time.")
            # else:
            shiny_is_found = find_sparkles(habitat)
            end_time = time.time()
            duration = end_time - start_time

        if duration > startup_time:
            controls.switch_tab()
            time.sleep(0.1)
            flee_encounter(window_width, window_height)
            pause_event.clear()  # Resumes search_encounter_func
            pause_state.set_state(pause_event)
            # time.sleep(3)
            # controls.switch_tab()
    if shiny_is_found:
        # pause_state.set_state(True)
        # t1_2.join()
        # controls.switch_tab()
        print("Congratulations! You found a shiny!")
        time.sleep(1)
        # controls.switch_tab()
        # keyboard.remove_all_hotkeys()
        # exit()


def flee_encounter(window_width, window_height):
    x, y = controls.run_btn_coords(window_width, window_height)

    while True:
        time.sleep(0.1)
        if pyautogui.pixelMatchesColor(x, y, (41, 148, 206)):
            controls.click_coord(x, y)
            print("Encounter ended. Search continues...")
            time.sleep(6)
            break


def set_window_focus():
    version_num = "0.9.11"
    window_name1 = f"DeSmuME {version_num} x64"
    window_name2 = "Paused"
    time.sleep(1)

    window = None
    try:
        window = pywindow.getWindowsWithTitle(window_name1)[0]
        time.sleep(0.1)
        print(window)
        # window.restore()
        window.activate()
        # window.minimize()
        time.sleep(1)
        return window
    except IndexError:
        try:
            window = pywindow.getWindowsWithTitle(window_name2)[0]
            print(window)
            window.activate()
            time.sleep(1)
            return window
        except IndexError:
            print(f'\nWindow named: "{window_name1}" or "{window_name2}" could not be found.')
    except pywindow.PyGetWindowException:
        window.minimize()
        window.maximize()
        window.restore()
        return window
