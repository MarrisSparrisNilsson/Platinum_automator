# import keyboard
import pygetwindow as pywindow
import pyautogui
import time
import math
import threading as thread

import controls
from state_manager import ShutdownStateManager, PauseStateManager, WindowStateManager, HuntStateManager


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
    while duration < 2.2:  # Sparkles duration
        if check_shutdown_state():
            return

        if not pyautogui.pixelMatchesColor(x1, y1, shiny_p1):
            #  print(f"P1: {pyautogui.pixel(x1, y1)}, {shiny_p1}")
            pyautogui.moveTo(x1, y1)
            return True
        elif not pyautogui.pixelMatchesColor(x2, y2, shiny_p2):
            #  print(f"P2: {pyautogui.pixel(x2, y2)}, {shiny_p2}")
            pyautogui.moveTo(x2, y2)
            return True
        elif not pyautogui.pixelMatchesColor(x3, y3, shiny_p3):
            #  print(f"P3: {pyautogui.pixel(x3, y3)}, {shiny_p3}")
            pyautogui.moveTo(x3, y3)
            return True
        elif not pyautogui.pixelMatchesColor(x4, y4, shiny_p4):
            #  print(f"P4: {pyautogui.pixel(x4, y4)}, {shiny_p4}")
            pyautogui.moveTo(x4, y4)
            return True
        elif not pyautogui.pixelMatchesColor(x5, y5, shiny_p5):
            #  print(f"P5: {pyautogui.pixel(x5, y5)}, {shiny_p5}")
            pyautogui.moveTo(x5, y5)
            return True
        end_time = time.time()
        duration = end_time - start_time
        # print(duration)

    print("No shiny this time...☹️")
    return False


def find_exclamation_mark(cast):
    window_width, window_height = WindowStateManager.get_instance().get_window_size()

    exc_p_left = (int(window_width * 0.23608247422680412), int(window_height * 0.40771028037383180))
    exc_p_middle_down = (int(window_width * 0.24690721649484537), int(window_height * 0.42757009345794394))
    exc_p_middle_up = (int(window_width * 0.24690721649484537), int(window_height * 0.40303738317757010))
    exc_p_right = (int(window_width * 0.25721649484536080), int(window_height * 0.40537383177570090))

    dialog_p1 = (int(window_width * 0.032474226804123714), int(window_height * 0.802570093457944))
    dialog_p2 = (int(window_width * 0.4747422680412371), int(window_height * 0.9217289719626168))

    start_p = pyautogui.pixel(dialog_p2[0], dialog_p2[1])

    while True:
        pause_event = PauseStateManager.get_instance().get_state()
        if pause_event is not None:
            if not pause_event.is_set():
                break

        if check_shutdown_state():
            return

        # Pixels matching the red exclamation mark
        exclamation_mark_found = is_exclamation_mark(exc_p_left, exc_p_middle_down, exc_p_middle_up, exc_p_right)

        no_fish = False
        if not exclamation_mark_found:
            no_fish = dialog_is_open(dialog_p1, dialog_p2, start_p)

        if exclamation_mark_found:
            print("Exclamation found❗")
            cast[0] = 0
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
            cast[0] += 1
            print(f"No fish this time. ({cast[0]})")
            return


def is_exclamation_mark(exc_p_left: (int, int), exc_p_middle_down: (int, int), exc_p_middle_up: (int, int), exc_p_right: (int, int)):
    if (pyautogui.pixelMatchesColor(exc_p_left[0], exc_p_left[1], (255, 66, 0)) or
            pyautogui.pixelMatchesColor(exc_p_middle_down[0], exc_p_middle_down[1], (255, 66, 0)) or
            pyautogui.pixelMatchesColor(exc_p_middle_up[0], exc_p_middle_up[1], (255, 66, 0)) or
            pyautogui.pixelMatchesColor(exc_p_right[0], exc_p_right[1], (255, 66, 0))):
        return True
    else:
        return False


def dialog_is_open(dialog_p1, dialog_p2, start_p):
    if (pyautogui.pixelMatchesColor(dialog_p1[0], dialog_p1[1], (255, 255, 255)) and
            not pyautogui.pixelMatchesColor(dialog_p2[0], dialog_p2[1], start_p)):
        return True
    else:
        return False


def check_shutdown_state():
    shutdown_event = ShutdownStateManager.get_instance().get_state()
    if shutdown_event is not None:
        return True
    else:
        return False


def check_pause_state(pause_message: str, continue_message: str):
    pause_event = PauseStateManager.get_instance().get_state()
    # If encounter is active
    if pause_event is not None:
        if not pause_event.is_set():
            if len(pause_message) > 0:
                print(pause_message)
            pause_event.wait()  # Wait for encounter to finish

            if len(continue_message) > 0 and not check_shutdown_state():
                print(continue_message + "\n")
            return True
    return False


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

    # print(f"ROUNDED_W: {width}, ROUNDED_H: {height}")
    w1 = int(width / 4)
    w2 = int(width - (width / 4))
    h = int(height / 2)
    pixel_one = (w1, h)
    pixel_two = (w2, h)

    return pixel_one, pixel_two


def encounter_started(pixel_coord_one, pixel_coord_two):
    pause_main_event = PauseStateManager.get_instance().get_main_state()

    if pause_main_event is not None:
        if not pause_main_event.is_set():
            print("Encounter detection is paused.")
            pause_main_event.wait()
            print("Encounter detection now continues.")

    # print(f"Left_P: {pixel_coord_one}\nRight_P: {pixel_coord_two}")
    pixel_one_is_black = pyautogui.pixelMatchesColor(pixel_coord_one[0], pixel_coord_one[1], (0, 0, 0))
    pixel_two_is_black = pyautogui.pixelMatchesColor(pixel_coord_two[0], pixel_coord_two[1], (0, 0, 0))

    time.sleep(0.1)
    if pixel_one_is_black and pixel_two_is_black:
        HuntStateManager.get_instance().increment_encounters()
        encounters = HuntStateManager.get_instance().get_encounters()
        print(f"\nEncounter #{encounters} started!👊💥")
        return True
    else:
        return False


def encounter_detection(search_encounter_func, end_encounter_func, search_args=None):
    p1, p2 = get_encounter_pixels()

    pause_state = PauseStateManager.get_instance()
    pause_event = thread.Event()

    search_encounter_thread = thread.Thread(target=search_encounter_func, args=[search_args], daemon=True)
    search_encounter_thread.start()

    shiny_is_found = False

    while not shiny_is_found:

        if check_shutdown_state():
            return

        is_encounter = encounter_started(p1, p2)
        if is_encounter:
            pause_event.clear()  # Pauses search_encounter_func (Set flag False)
            pause_state.set_state(pause_event)  # Update pause state

            controls.clear_movement()  # Stops movement / button presses

            timeout = HuntStateManager.get_instance().get_encounter_timeout()
            print(f"Waiting: {timeout} seconds.")

            time.sleep(timeout)  # Time of encounter intro (Legendary encounter)
            # time.sleep(4)  # Time of encounter intro (Regular encounter)

            if check_shutdown_state():
                return

            shiny_is_found = find_sparkles()

            if shiny_is_found:
                print("Congratulations! You found a shiny!✨")
                HuntStateManager.get_instance().finish_hunt(is_finished=shiny_is_found)
                time.sleep(1)

                on_off = False
                if on_off:
                    # --- Shiny test (Commented/False by default) ---
                    shiny_is_found = False
                    end_encounter_func()
                    pause_event.set()  # Resumes search_encounter_func (Set flag True)
                    pause_state.set_state(pause_event)
                    # -----------------------------------------
            else:
                end_encounter_func()
                pause_event.set()  # Resumes search_encounter_func (Set flag True)
                pause_state.set_state(pause_event)


def set_window_focus():
    with thread.Lock():
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
