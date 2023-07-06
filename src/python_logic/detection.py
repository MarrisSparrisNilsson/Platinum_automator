# import keyboard
import pygetwindow as pywindow
import pyautogui
import time
import math
# import os
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


def find_sparkles(window_width, window_height, habitat_name):
    try:
        # screenshot = pyautogui.screenshot(region=(850, 100, 850, 1000))
        # screenshot = pyautogui.screenshot(region=(850, 700, 850, 400))
        # screenshot.save("../images/test/shiny_area.png")

        # sparkles_list = ["cave", "eterna_forest_day", "snow_day", "snow_evening", "water_day"]
        # sparkles_list_len = len(sparkles_list)

        shutdown_event = ShutdownStateManager.get_instance().get_state()

        if shutdown_event is not None:
            return

        # x = 1250, y = 950
        # x = 1152, y = 887
        # x = 1342, y = 928
        # x = 1414, y = 881
        # x = 1154, y = 887

        # x = 931, y = 385
        # x = 1179, y = 283
        # x = 861, y = 759
        # x = 1567, y = 443

        # x: 1262, y: 906

        x1 = int(window_width * 0.2630359212050985)
        y1 = int(window_height * 0.27670250896057347)

        x2 = int(window_width * 0.36993047508690613)
        y2 = int(window_height * 0.6336917562724015)

        x3 = int(window_width * 0.45712630359212053)
        y3 = int(window_height * 0.2623655913978495)

        x4 = int(window_width * 0.3579142526071842)
        y4 = int(window_height * 0.1013620071684588)

        x5 = int(window_width * 0.45654692931633833)
        y5 = int(window_height * 0.5684587813620071)

        time.sleep(2)
        print("Searching for sparkles...")
        start_time = time.time()
        shiny_p1 = pyautogui.pixel(x1, y1)
        shiny_p2 = pyautogui.pixel(x2, y2)
        shiny_p3 = pyautogui.pixel(x3, y3)
        shiny_p4 = pyautogui.pixel(x4, y4)
        shiny_p5 = pyautogui.pixel(x5, y5)

        duration = 0
        while duration < 2:

            # if not pyautogui.pixelMatchesColor(x1, y1, (shiny_p1[0], shiny_p1[1], shiny_p1[2])):
            if not pyautogui.pixelMatchesColor(x1, y1, shiny_p1):
                print(f"P1: {pyautogui.pixel(x1, y1)}, {shiny_p1}")
                return True
            elif not pyautogui.pixelMatchesColor(x2, y2, shiny_p2):
                print(f"P2: {pyautogui.pixel(x2, y2)}, {shiny_p2}")
                return True
            elif not pyautogui.pixelMatchesColor(x3, y3, shiny_p3):
                print(f"P3: {pyautogui.pixel(x3, y3)}, {shiny_p3}")
                return True
            elif not pyautogui.pixelMatchesColor(x4, y4, shiny_p4):
                print(f"P4: {pyautogui.pixel(x4, y4)}, {shiny_p4}")
                return True
            elif not pyautogui.pixelMatchesColor(x5, y5, shiny_p5):
                print(f"P5: {pyautogui.pixel(x5, y5)}, {shiny_p5}")
                return True
            end_time = time.time()
            duration = end_time - start_time
        # else:
        #     return False
        # folder_dir = f"../images/sparkles/{habitat_name}"
        # counter = 1
        # for image in os.listdir(folder_dir):
        #
        #     print(f"Looking for shiny {counter}")
        #     counter += 1
        #     if image.endswith(".png"):
        #         # sparkles = pyautogui.locateOnScreen(f"../images/sparkles/other/indoor.png",
        #         sparkles = pyautogui.locateOnScreen(f"{folder_dir}/{image}",
        #                                             region=(800, 100, 950, 1000),
        #                                             # region=(850, 700, 850, 400),
        #                                             confidence=0.75)
        #         # confidence=0.9)
        #         if sparkles:
        #             print(f"Coords: {pyautogui.center(sparkles)}")
        #             pyautogui.moveTo(pyautogui.center(sparkles))
        #             pyautogui.screenshot(region=(800, 100, 920, 960)).save("../images/test/detected_sparkle.png")
        #             print(f"Sparkles was found for the {habitat_name} habitat, matching {image}!")
        #             return True

        # print(f"Sparkles was not found in {habitat_name}.")
        print("No shiny this time")
        return False
    except OSError:
        print("Incorrect image source.")
        quit()


def find_exclamation_mark():
    # Exclamation_mark_area: 800, 450, 150, 300 (Full wide screen)
    # Not even a nibble: 100, 1100, 800, 150 (Full wide screen)
    while True:
        try:
            shutdown_event = ShutdownStateManager.get_instance().get_state()
            pause_event = PauseStateManager.get_instance().get_state()

            if pause_event is not None:
                if not pause_event.is_set():
                    # print("Fishing is paused")
                    break
            # print("Fishing now continues")

            if shutdown_event is not None:
                break

            # screenshot = pyautogui.screenshot(region=(100, 1100, 900, 150))
            # screenshot.save("../images/test/fish_got_away_area.png")
            # time.sleep(0.15)
            exclamation_mark_found = pyautogui.locateCenterOnScreen("../images/fish_on.png",
                                                                    region=(800, 450, 150, 300), confidence=0.7)
            no_fish = pyautogui.locateCenterOnScreen("../images/no_fish.png",
                                                     region=(100, 1100, 800, 150), confidence=0.5)

            # fish_got_away = pyautogui.locateCenterOnScreen("../images/fish_got_away_area.png",
            #                                                region=(100, 1100, 900, 150), confidence=0.7)

            # print(exclamation_mark_found)
            if exclamation_mark_found:
                print("Exclamation found!")
                # controls.a_key()
                # time.sleep(0.0001)
                for i in range(5):
                    controls.a_key()
                    time.sleep(0.01)
                    print("A button was pressed!")
                controls.a_key()
                break
            elif no_fish:
                print("No fish this time.")
                for i in range(1):
                    time.sleep(0.1)
                    controls.a_key()
                break
            # elif fish_got_away:
            #     print("Fish got away.")
            #     # for i in range(2):
            #     #     time.sleep(0.01)
            #     controls.a_key()
            #     break

        except OSError:
            print("Incorrect image source.")


def get_mouse_coordinates():
    mouse = pyautogui.position()
    print(mouse)
    window = get_window()

    percent_w = mouse.x / window.width
    print(percent_w)
    percent_h = mouse.y / window.height
    print(percent_h)

    # x: 0.2630359212050985
    # y: 0.27670250896057347

    # x: 0.36993047508690613
    # y: 0.6336917562724015

    # x: 0.45712630359212053
    # y: 0.2623655913978495

    # x: 0.3479142526071842
    # y: 0.1813620071684588


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
            pause_event.clear()  # Pauses search_encounter_func (Set flag False)
            pause_state.set_state(pause_event)
            # print(f"Paused: {pause_event.is_set()}")

            controls.clear_movement()
            controls.switch_tab()
            time.sleep(2.5)

        while is_encounter and not shiny_is_found and duration < startup_time:

            shutdown_event = ShutdownStateManager.get_instance().get_state()
            if shutdown_event is not None:
                break

            if duration < 6:
                shiny_is_found = find_sparkles(window_width, window_height, habitat)

            end_time = time.time()
            duration = end_time - start_time

        if duration > startup_time:
            controls.switch_tab()
            time.sleep(0.1)
            flee_encounter(window_width, window_height)
            pause_event.set()  # Resumes search_encounter_func (Set flag True)
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
            time.sleep(4.5)
            break


def get_window():
    version_num = "0.9.11"
    window_name1 = f"DeSmuME {version_num} x64"
    window_name2 = "Paused"

    try:
        window = pywindow.getWindowsWithTitle(window_name1)[0]
        print(window)
        return window
    except IndexError:
        try:
            window = pywindow.getWindowsWithTitle(window_name2)[0]
            print(window)
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
