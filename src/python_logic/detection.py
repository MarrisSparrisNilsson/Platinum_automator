# import keyboard
import pygetwindow as pywindow
import pyautogui
import time
import math
# import os
import threading as thread

import controls
from state_manager import ShutdownStateManager, PauseStateManager, WindowStateManager


# noinspection PyArgumentList
def find_pause_and_resume():
    # screenshot = pyautogui.screenshot(region=(0, 0, 210, 100))
    # screenshot.save("../images/test.png")

    # pyautogui.moveTo(res)
    try:
        res = pyautogui.locateCenterOnScreen("../images/paused.png", region=(0, 0, 210, 100), confidence=0.9)
        if res is None:
            print("The game is up and running!")
        else:
            pyautogui.click(res)
            # print(res)
    except OSError:
        print("Incorrect image source.")


# noinspection PyUnresolvedReferences
def find_sparkles():
    window_width, window_height = WindowStateManager.get_instance().get_window_size()

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

    # time.sleep(1)  # Seconds until Pokémon stands still
    shiny_p1 = pyautogui.pixel(x1, y1)
    shiny_p2 = pyautogui.pixel(x2, y2)
    shiny_p3 = pyautogui.pixel(x3, y3)
    shiny_p4 = pyautogui.pixel(x4, y4)
    shiny_p5 = pyautogui.pixel(x5, y5)

    duration = 0
    print("Searching for sparkles...")
    start_time = time.time()
    while duration < 1.6:  # Sparkles duration
        shutdown_event = ShutdownStateManager.get_instance().get_state()

        if shutdown_event is not None:
            return

        # if not pyautogui.pixelMatchesColor(x1, y1, (shiny_p1[0], shiny_p1[1], shiny_p1[2])):
        if not pyautogui.pixelMatchesColor(x1, y1, shiny_p1):
            print(f"P1: {pyautogui.pixel(x1, y1)}, {shiny_p1}")
            pyautogui.moveTo(x1, y1)
            return True
        elif not pyautogui.pixelMatchesColor(x2, y2, shiny_p2):
            print(f"P2: {pyautogui.pixel(x2, y2)}, {shiny_p2}")
            pyautogui.moveTo(x2, y2)
            return True
        elif not pyautogui.pixelMatchesColor(x3, y3, shiny_p3):
            print(f"P3: {pyautogui.pixel(x3, y3)}, {shiny_p3}")
            pyautogui.moveTo(x3, y3)
            return True
        elif not pyautogui.pixelMatchesColor(x4, y4, shiny_p4):
            print(f"P4: {pyautogui.pixel(x4, y4)}, {shiny_p4}")
            pyautogui.moveTo(x4, y4)
            return True
        elif not pyautogui.pixelMatchesColor(x5, y5, shiny_p5):
            print(f"P5: {pyautogui.pixel(x5, y5)}, {shiny_p5}")
            pyautogui.moveTo(x5, y5)
            return True
        end_time = time.time()
        duration = end_time - start_time

    print("No shiny this time")
    return False


# noinspection PyArgumentList
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
            time.sleep(0.05)
            exclamation_mark_found = pyautogui.locateCenterOnScreen(image="../images/fish_on.png",
                                                                    region=(800, 450, 150, 300), confidence=0.7)
            no_fish = pyautogui.locateCenterOnScreen(image="../images/no_fish.png", region=(100, 1100, 800, 150),
                                                     confidence=0.5)
            print(exclamation_mark_found)
            print(no_fish)

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
    window_width, window_height = WindowStateManager.get_instance().get_window_size()

    percent_w = mouse.x / window_width
    print(percent_w)
    percent_h = mouse.y / window_height
    print(percent_h)

    # x: 0.2630359212050985
    # y: 0.27670250896057347

    # x: 0.36993047508690613
    # y: 0.6336917562724015

    # x: 0.45712630359212053
    # y: 0.2623655913978495

    # x: 0.3479142526071842
    # y: 0.1813620071684588


def get_encounter_pixels():
    window_width, window_height = WindowStateManager.get_instance().get_window_size()

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

    print(f"ROUNDED_W: {width}, ROUNDED_H: {height}")
    w1 = int(width / 4)
    w2 = int(width - (width / 4))
    h = int(height / 2)
    pixel_one = (w1, h)
    pixel_two = (w2, h)

    return pixel_one, pixel_two


# noinspection PyUnresolvedReferences
def encounter_started(pixel_coord_one, pixel_coord_two):
    # print(f"Left_P: {pixel_coord_one}\nRight_P: {pixel_coord_two}")
    x1, y1 = pixel_coord_one
    x2, y2 = pixel_coord_two

    pixel_one_rbg = pyautogui.pixel(x1, y1)
    pixel_two_rbg = pyautogui.pixel(x2, y2)

    time.sleep(0.1)

    if pixel_one_rbg == (0, 0, 0) and pixel_two_rbg == (0, 0, 0):
        print("\nEncounter started!")
        return True
    else:
        return False


def encounter_detection(search_encounter_func):
    p1, p2 = get_encounter_pixels()

    pause_state = PauseStateManager.get_instance()
    pause_event = thread.Event()

    search_encounter_thread = thread.Thread(target=search_encounter_func, daemon=True)
    search_encounter_thread.start()

    # startup_time = 11.5
    shiny_is_found = False

    while not shiny_is_found:

        shutdown_event = ShutdownStateManager.get_instance().get_state()
        if shutdown_event is not None:
            return

        is_encounter = encounter_started(p1, p2)
        if is_encounter:
            pause_event.clear()  # Pauses search_encounter_func (Set flag False)
            pause_state.set_state(pause_event)

            controls.clear_movement()  # Stops movement / button presses

            time.sleep(4)  # Time of encounter intro

            shutdown_event = ShutdownStateManager.get_instance().get_state()
            if shutdown_event is not None:
                return

            shiny_is_found = find_sparkles()

            if shiny_is_found:
                print("Congratulations! You found a shiny!")
                time.sleep(1)

                # Shiny test
                # shiny_is_found = False
                # flee_encounter()
                # pause_event.set()  # Resumes search_encounter_func (Set flag True)
                # pause_state.set_state(pause_event)
            else:
                flee_encounter()
                pause_event.set()  # Resumes search_encounter_func (Set flag True)
                pause_state.set_state(pause_event)


# noinspection PyUnresolvedReferences
def flee_encounter():
    x, y = controls.run_btn_coords()

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


def set_window_focus():
    WindowStateManager.get_instance().set_state()
    window = WindowStateManager.get_instance().get_window()
    print(f"{window}\n")
    try:
        window.activate()
    except pywindow.PyGetWindowException:
        print("Something went wrong when trying to activate the window")
        window.minimize()
        window.maximize()
        window.restore()

    time.sleep(1)
