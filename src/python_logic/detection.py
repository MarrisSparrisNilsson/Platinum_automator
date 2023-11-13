# import keyboard
import pygetwindow as pywindow
import pyautogui
import time
import math
import threading as thread

from src.python_logic import controls
from src.python_logic.state.state_manager import ShutdownStateManager, PauseStateManager, WindowStateManager, HuntStateManager, DialogStateManager


def find_pause_and_resume():
    try:
        res = pyautogui.locateCenterOnScreen("../images/paused.png", region=(0, 0, 210, 100), confidence=0.9)
        if res is None:
            print("The game is up and running!")
        else:
            pyautogui.click(res)
    except OSError:
        print("Incorrect image source.")
    except pyautogui.ImageNotFoundException:
        print("The game is up and running!")


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

    coords = [
        (x1, y1),
        (x2, y2),
        (x3, y3),
        (x4, y4),
        (x5, y5)
    ]

    # time.sleep(1)  # Seconds until Pokémon stands still
    shiny_p1 = pyautogui.pixel(x1, y1)
    shiny_p2 = pyautogui.pixel(x2, y2)
    shiny_p3 = pyautogui.pixel(x3, y3)
    shiny_p4 = pyautogui.pixel(x4, y4)
    shiny_p5 = pyautogui.pixel(x5, y5)

    shiny_p = [
        shiny_p1,
        shiny_p2,
        shiny_p3,
        shiny_p4,
        shiny_p5
    ]

    duration = 0
    print("Searching for sparkles...🔎")
    start_time = time.time()
    while duration < 2.2:  # Sparkles duration
        if ShutdownStateManager.get_instance().check_shutdown_state():
            return

        for i in range(len(shiny_p)):
            x, y = coords[i]
            if has_background_changed(x, y, shiny_p[i]):
                return True

        end_time = time.time()
        duration = end_time - start_time
        # print(duration)

    print("No shiny this time...☹️")
    return False


def has_background_changed(x, y, shiny_p):
    if not pyautogui.pixelMatchesColor(x, y, shiny_p):
        #  print(f"P: {pyautogui.pixel(x, y)}, {shiny_p}")
        pyautogui.moveTo(x, y)
        return True
    else:
        return False


def find_exclamation_mark(cast, encounter):
    window_width, window_height = WindowStateManager.get_instance().get_window_size()

    exc_p_middle_up = (int(window_width * 0.24690721649484537), int(window_height * 0.40303738317757010))
    exc_p_left = (int(window_width * 0.23608247422680412) + 1, int(window_height * 0.40771028037383180))
    # exc_p_surf_left = (int(window_width * 0.2381443298969072), int(window_height * 0.40186915887850466))
    exc_p_middle_down = (int(window_width * 0.24690721649484537), int(window_height * 0.42757009345794394))
    exc_p_right = (int(window_width * 0.25721649484536080), int(window_height * 0.40537383177570090))

    exc_points = [
        exc_p_middle_up,
        exc_p_left,
        exc_p_middle_down,
        exc_p_right
    ]

    DialogStateManager.get_instance().set_dialog_pixels()

    move_dirs = ['w', 'a', 's', 'd']
    direction = HuntStateManager.get_instance().get_facing_direction()
    if direction is not None:
        i = move_dirs.index(direction)
        x, y = exc_points[i]
        pyautogui.moveTo(x, y)

    while True:
        pause_event = PauseStateManager.get_instance().get_state()
        if pause_event is not None:
            if not pause_event.is_set():
                break

        if ShutdownStateManager.get_instance().check_shutdown_state():
            return

        # Pixels matching the red exclamation mark
        exclamation_mark_found = False
        if direction is None:
            for p in range(len(exc_points)):
                x, y = exc_points[p]
                exclamation_mark_found = is_exclamation_mark(x, y)
                if exclamation_mark_found:
                    break
        else:
            exclamation_mark_found = is_exclamation_mark(x, y)

        no_fish = False
        if not exclamation_mark_found:
            no_fish = dialog_is_open()

        if exclamation_mark_found:
            print("Exclamation found❗")
            cast[0] = 0
            encounter[0] += 1
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


def is_exclamation_mark(x, y):
    return True if pyautogui.pixelMatchesColor(x, y, (255, 66, 0)) else False


def dialog_is_open():
    start_p, dialog_p1, dialog_p2 = DialogStateManager.get_instance().get_dialog_pixels()
    if (pyautogui.pixelMatchesColor(dialog_p1[0], dialog_p1[1], (255, 255, 255)) and
            not pyautogui.pixelMatchesColor(dialog_p2[0], dialog_p2[1], start_p)):
        return True
    else:
        return False


def use_selected_item():
    DialogStateManager.get_instance().set_dialog_pixels()

    pyautogui.keyDown('b')
    pyautogui.keyUp('b')

    time.sleep(0.5)

    return False if dialog_is_open() else True


# TODO: Tesseract OCR
# def find_pokemon():


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

        if ShutdownStateManager.get_instance().check_shutdown_state():
            return

        is_encounter = encounter_started(p1, p2)
        if is_encounter:
            pause_event.clear()  # Pauses search_encounter_func (Set flag False)
            pause_state.set_state(pause_event)  # Update pause state

            controls.clear_movement()  # Stops movement / button presses

            timeout = HuntStateManager.get_instance().get_encounter_timeout()
            print(f"Waiting: {timeout} seconds.")

            time.sleep(timeout)  # Time of encounter intro

            if ShutdownStateManager.get_instance().check_shutdown_state():
                return

            shiny_is_found = find_sparkles()

            # TODO: Use Tesseract (OCR) to read encountered pokemon name and verify with HuntStateManager._pokemon_name
            #       if true then increment current hunted pokemon encounters by one.
            #       else increment "other encounters" by one.

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
            controls.switch_tab()
            print("Something went wrong when trying to activate the window")
            window.minimize()
            window.maximize()
            window.restore()

        time.sleep(1)
