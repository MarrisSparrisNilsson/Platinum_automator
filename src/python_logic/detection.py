# import keyboard
import pygetwindow as pywindow
import pyautogui
import time
import math
import os
import threading as thread

import controls
from state_manager import ShutdownStateManager, PauseStateManager


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
            # print(res)
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

            sparkles = None
            print(f"Looking for shiny {counter}")
            counter += 1
            if image.endswith(".png"):
                # sparkles = pyautogui.locateOnScreen(f"../images/sparkles/other/indoor.png",
                sparkles = pyautogui.locateOnScreen(f"{folder_dir}/{image}",
                                                    region=(800, 100, 950, 1000),
                                                    # region=(850, 700, 850, 400),
                                                    confidence=0.7)
            if sparkles:
                pyautogui.moveTo(pyautogui.center(sparkles))
                pyautogui.screenshot(region=(800, 100, 920, 960)).save("../images/test/detected_sparkle.png")
                print(f"Sparkles was found for the {habitat} habitat, matching {image}!")
                return True

        print(f"Sparkles was not found in {habitat}.")
        return False
    except OSError:
        print("Incorrect image source.")
        quit()


def get_mouse_coordinates():
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

    time.sleep(0.3)
    # print(f"Left_P_rgb: {pixel_one}\nRight_P_rgb: {pixel_two}")

    if pixel_one == (0, 0, 0) and pixel_two == (0, 0, 0):
        print("Encounter started!")
        start_time = time.time()

        return start_time, True
    else:
        return 0, False


def encounter_detection(window_width, window_height, habitat, search_encounter_func):
    p1, p2 = get_encounter_pixels(window_width, window_height)

    pause_state = PauseStateManager.get_instance()
    pause_event = thread.Event()

    search_encounter_thread = thread.Thread(target=search_encounter_func, daemon=True)
    search_encounter_thread.start()

    startup_time = 11.5
    shiny_is_found = False

    while not shiny_is_found:

        shutdown_event = ShutdownStateManager.get_instance().get_state()
        if shutdown_event is not None:
            break

        duration = 0

        start_time, is_encounter = encounter_started(p1, p2)
        if is_encounter:
            pause_event.clear()  # Pauses search_encounter_func
            pause_state.set_state(pause_event)

            controls.clear_movement()
            controls.switch_tab()
            time.sleep(3)

        while is_encounter and not shiny_is_found and duration < startup_time:

            shutdown_event = ShutdownStateManager.get_instance().get_state()
            if shutdown_event is not None:
                break

            if duration < 6:
                shiny_is_found = find_sparkles(habitat)

            end_time = time.time()
            duration = end_time - start_time

        if duration > startup_time:
            controls.switch_tab()
            time.sleep(0.1)
            flee_encounter(window_width, window_height)
            pause_event.set()  # Resumes search_encounter_func
            pause_state.set_state(pause_event)
            # time.sleep(3)
            # controls.switch_tab()
    if shiny_is_found:
        # controls.switch_tab()
        print("Congratulations! You found a shiny!")
        time.sleep(1)
        # controls.switch_tab()
    else:
        search_encounter_thread.join()


def flee_encounter(window_width, window_height):
    x, y = controls.run_btn_coords(window_width, window_height)

    while True:
        shutdown_event = ShutdownStateManager.get_instance().get_state()
        if shutdown_event is not None:
            break

        time.sleep(0.1)
        if pyautogui.pixelMatchesColor(x, y, (41, 148, 206)):
            controls.click_coord(x, y)
            print("Encounter ended. Search continues...\n")
            time.sleep(5)
            break


def get_window():
    version_num = "0.9.11"
    window_name1 = f"DeSmuME {version_num} x64"
    window_name2 = "Paused"

    try:
        window = pywindow.getWindowsWithTitle(window_name1)[0]
        return window
    except IndexError:
        try:
            window = pywindow.getWindowsWithTitle(window_name2)[0]
            return window
        except IndexError:
            print(f'\nWindow named: "{window_name1}" or "{window_name2}" could not be found.')
            exit()


def set_window_focus():
    window = get_window()
    try:
        window.activate()
    except pywindow.PyGetWindowException:
        print("Something went wrong when trying to activate the window")
        window.minimize()
        window.maximize()
        window.restore()

    time.sleep(1)
