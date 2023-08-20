# import keyboard
import pygetwindow as pywindow
import pyautogui
import time
import math
# import os
import threading as thread

import controls
from state_manager import ShutdownStateManager, PauseStateManager, WindowStateManager


def find_pause_and_resume():
    try:
        res = pyautogui.locateCenterOnScreen("../images/paused.png", region=(0, 0, 210, 100), confidence=0.9)
        if res is None:
            print("The game is up and running!")
        else:
            pyautogui.click(res)
    except OSError:
        print("Incorrect image source.")


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
    print("Searching for sparkles...🔎")
    start_time = time.time()
    while duration < 1.6:  # Sparkles duration
        shutdown_event = ShutdownStateManager.get_instance().get_state()

        if shutdown_event is not None:
            return

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

    print("No shiny this time...☹️")
    return False


def find_exclamation_mark():
    window_width, window_height = WindowStateManager.get_instance().get_window_size()

    exc_p_left = (int(window_width * 0.23608247422680412), int(window_height * 0.4077102803738318))
    exc_p_middle_down = (int(window_width * 0.24690721649484537), int(window_height * 0.42757009345794394))
    exc_p_middle_up = (int(window_width * 0.24690721649484537), int(window_height * 0.4030373831775701))
    exc_p_right = (int(window_width * 0.2572164948453608), int(window_height * 0.4053738317757009))

    no_fish_p1 = (int(window_width * 0.032474226804123714), int(window_height * 0.802570093457944))
    no_fish_p2 = (int(window_width * 0.4747422680412371), int(window_height * 0.9217289719626168))

    start_p = pyautogui.pixel(no_fish_p2[0], no_fish_p2[1])

    while True:
        pause_event = PauseStateManager.get_instance().get_state()

        if pause_event is not None:
            if not pause_event.is_set():
                break

        shutdown_event = ShutdownStateManager.get_instance().get_state()
        if shutdown_event is not None:
            return

        exclamation_mark_found = False
        no_fish = False

        # Pixels matching the red exclamation mark
        if (pyautogui.pixelMatchesColor(exc_p_left[0], exc_p_left[1], (255, 66, 0)) or
                pyautogui.pixelMatchesColor(exc_p_middle_down[0], exc_p_middle_down[1], (255, 66, 0)) or
                pyautogui.pixelMatchesColor(exc_p_middle_up[0], exc_p_middle_up[1], (255, 66, 0)) or
                pyautogui.pixelMatchesColor(exc_p_right[0], exc_p_right[1], (255, 66, 0))):
            exclamation_mark_found = True
        elif (pyautogui.pixelMatchesColor(
                no_fish_p1[0], no_fish_p1[1], (255, 255, 255)) and not pyautogui.pixelMatchesColor(
            no_fish_p2[0], no_fish_p2[1], start_p)):
            no_fish = True

        if exclamation_mark_found:
            print("\nExclamation found❗")
            for i in range(5):
                pyautogui.keyDown('e')
                time.sleep(0.05)
                pyautogui.keyUp('e')
                print(f"A button was pressed: {i + 1}")
                time.sleep(0.0001)
            return
        elif no_fish:
            time.sleep(0.3)
            controls.b_key()
            print("No fish this time.")
            return


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


def encounter_started(pixel_coord_one, pixel_coord_two):
    # print(f"Left_P: {pixel_coord_one}\nRight_P: {pixel_coord_two}")
    pixel_one_is_black = pyautogui.pixelMatchesColor(pixel_coord_one[0], pixel_coord_one[1], (0, 0, 0))
    pixel_two_is_black = pyautogui.pixelMatchesColor(pixel_coord_two[0], pixel_coord_two[1], (0, 0, 0))

    time.sleep(0.1)
    if pixel_one_is_black and pixel_two_is_black:
        print("\nEncounter started!👊💥")
        return True
    else:
        return False


def encounter_detection(search_encounter_func):
    p1, p2 = get_encounter_pixels()

    pause_state = PauseStateManager.get_instance()
    pause_event = thread.Event()

    search_encounter_thread = thread.Thread(target=search_encounter_func, daemon=True)
    search_encounter_thread.start()

    shiny_is_found = False

    while not shiny_is_found:

        shutdown_event = ShutdownStateManager.get_instance().get_state()
        if shutdown_event is not None:
            return

        is_encounter = encounter_started(p1, p2)
        if is_encounter:
            pause_event.clear()  # Pauses search_encounter_func (Set flag False)
            pause_state.set_state(pause_event)  # Update pause state

            controls.clear_movement()  # Stops movement / button presses

            time.sleep(4)  # Time of encounter intro

            shutdown_event = ShutdownStateManager.get_instance().get_state()
            if shutdown_event is not None:
                return

            shiny_is_found = find_sparkles()

            if shiny_is_found:
                print("Congratulations! You found a shiny!✨")
                time.sleep(1)

                # --- Shiny test (Commented by default) ---
                shiny_is_found = False
                flee_encounter()
                pause_event.set()  # Resumes search_encounter_func (Set flag True)
                pause_state.set_state(pause_event)
                # -----------------------------------------
            else:
                flee_encounter()
                pause_event.set()  # Resumes search_encounter_func (Set flag True)
                pause_state.set_state(pause_event)


def flee_encounter():
    x, y = controls.run_btn_coords()

    while True:
        shutdown_event = ShutdownStateManager.get_instance().get_state()
        if shutdown_event is not None:
            break

        time.sleep(0.1)
        if pyautogui.pixelMatchesColor(x, y, (41, 148, 206)):  # Blue run button
            controls.click_coord(x, y)
            w, h = WindowStateManager.get_instance().get_window_size()
            time.sleep(3.5)
            if pyautogui.pixelMatchesColor(int(w / 4), int(h / 2), (0, 0, 0)):  # Black screen
                print("Encounter ended. Search continues...\n")
                time.sleep(1.2)
                break
            else:
                print("Error: Unable to escape for some reason...")
                exit()


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
