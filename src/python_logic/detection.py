# import keyboard
import pygetwindow as pywindow
import pytesseract
import pyautogui
# import cv2
import time
import math
import threading as thread

from src.python_logic import controls
from src.python_logic.states.GameView import GameViewStateManager
from src.python_logic.states.Window import WindowStateManager
from src.python_logic.states.Shutdown import ShutdownStateManager
from src.python_logic.states.Pause import PauseStateManager
from src.python_logic.states.Hunt import HuntStateManager


def find_pause_and_resume():
    try:
        res = pyautogui.locateCenterOnScreen("../images/paused.png", region=(0, 0, 210, 100), confidence=0.9)
        # if res is None:
        #     print("The game is up and running!")
        # else:
        pyautogui.click(res)
    except OSError:
        print("Incorrect image source.")
    except pyautogui.ImageNotFoundException:
        # print("The game is up and running!\n")
        pass


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

    GameViewStateManager.get_instance().set_dialog_pixels()
    direction = HuntStateManager.get_instance().get_facing_direction()

    x = 0
    y = 0
    try:
        move_dirs = ['w', 'a', 's', 'd']
        i = move_dirs.index(direction)
        x, y = exc_points[i]
        # pyautogui.moveTo(x, y)
    except ValueError:
        pass

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
                # pyautogui.moveTo(x, y)
                if exclamation_mark_found:
                    break
        else:
            exclamation_mark_found = is_exclamation_mark(x, y)

        no_fish = False
        if not exclamation_mark_found:
            no_fish = dialog_is_open()

        if exclamation_mark_found:
            print("\nExclamation found❗")
            cast[0] = 0
            encounter[0] += 1
            for i in range(5):
                pyautogui.keyDown('e')
                time.sleep(0.05)
                pyautogui.keyUp('e')
                print('\r', end=f"A button was pressed: {i + 1} times")

                time.sleep(0.0001)
            return
        elif no_fish:
            time.sleep(0.3)
            controls.b_button()
            cast[0] += 1
            print('\r', end=f"No fish this time. ({cast[0]})")
            return
    print()


def is_exclamation_mark(x, y):
    return True if pyautogui.pixelMatchesColor(x, y, (255, 66, 0)) else False


def dialog_is_open():
    start_p, dialog_p1, dialog_p2 = GameViewStateManager.get_instance().get_dialog_pixels()
    if (pyautogui.pixelMatchesColor(dialog_p1[0], dialog_p1[1], (255, 255, 255)) and
            not pyautogui.pixelMatchesColor(dialog_p2[0], dialog_p2[1], start_p)):
        return True
    else:
        return False


def use_selected_item():
    GameViewStateManager.get_instance().set_dialog_pixels()

    pyautogui.keyDown('b')
    pyautogui.keyUp('b')

    time.sleep(0.5)

    return False if dialog_is_open() else True


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
    # print(f"Left_P: {pixel_coord_one}\nRight_P: {pixel_coord_two}")
    pixel_one_is_black = pyautogui.pixelMatchesColor(pixel_coord_one[0], pixel_coord_one[1], (0, 0, 0))
    pixel_two_is_black = pyautogui.pixelMatchesColor(pixel_coord_two[0], pixel_coord_two[1], (0, 0, 0))

    time.sleep(0.1)
    if pixel_one_is_black and pixel_two_is_black:
        HuntStateManager.get_instance().increment_encounters()
        encounters = HuntStateManager.get_instance().get_total_encounters()
        print(f"\n\nEncounter #{encounters} started!👊💥")
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
        PauseStateManager.get_instance().check_main_pause_state()

        if ShutdownStateManager.get_instance().check_shutdown_state():
            return

        is_encounter = encounter_started(p1, p2)
        if is_encounter:
            pause_event.clear()  # Pauses search_encounter_func (Set flag False)
            pause_state.set_state(pause_event)  # Update pause state

            controls.clear_movement()  # Stops movement / button presses

            timeout = HuntStateManager.get_instance().get_encounter_timeout()
            # print(f"Waiting: {timeout} seconds.")

            time.sleep(timeout)  # Time of encounter intro

            if ShutdownStateManager.get_instance().check_shutdown_state():
                return

            shiny_is_found = find_sparkles()

            pokemon = HuntStateManager.get_instance().get_hunted_pokemon_name()

            result = was_target_pokemon_found()
            if result:
                HuntStateManager.get_instance().set_target_pokemon_found()
                HuntStateManager.get_instance().increment_target_encounters()
                target_encounters = HuntStateManager.get_instance().get_target_pokemon_encounters()
                print(f"{pokemon} #{target_encounters}!")

            if shiny_is_found:
                print(f"Congratulations! You found a shiny {f'{pokemon}' if result else ''}!✨")
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


'''
Tesseract Page Segmentation Modes (PSM):
    0 = Orientation and script detection (OSD) only.
    1 = Automatic page segmentation with OSD.
    2 = Automatic page segmentation, but no OSD, or OCR. (not implemented)
    3 = Fully automatic page segmentation, but no OSD. (Default)
    4 = Assume a single column of text of variable sizes.
    5 = Assume a single uniform block of vertically aligned text.
    6 = Assume a single uniform block of text.
    7 = Treat the image as a single text line.
    8 = Treat the image as a single word.
    9 = Treat the image as a single word in a circle.
   10 = Treat the image as a single character.
   11 = Sparse text. Find as much text as possible in no particular order.
   12 = Sparse text with OSD.
   13 = Raw line. Treat the image as a single text line,
         bypassing hacks that are Tesseract-specific.
'''


def was_target_pokemon_found():
    # Pokémon name coordinates:
    # (window.left + 9, int(window.height * 0.20327102803738317), int(window.width * 0.12474226804123711), int(window.height * (0.28085981308411217 - 0.20327102803738317))))
    window = WindowStateManager.get_instance().get_window()

    pokemon_name_img_path = "../images/local/pokemon_name.png"
    pyautogui.screenshot(pokemon_name_img_path, region=(
        window.left + 9, int(window.height * 0.20327102803738317), int(window.width * 0.12474226804123711), int(window.height * (0.28085981308411217 - 0.20327102803738317))))

    pokemon_name = HuntStateManager.get_instance().get_hunted_pokemon_name()

    reading_configs = ["--psm 7", "--psm 8"]
    largest_match_count = 0
    for i in range(len(reading_configs)):
        matching_chars = 0
        reading = pytesseract.image_to_string(pokemon_name_img_path, config=reading_configs[i])
        if reading == pokemon_name:
            return True
        # print(reading)
        i = 0
        while i < len(pokemon_name) and i < len(reading):
            if reading[i] == pokemon_name[i]:
                matching_chars += 1
            i += 1
        if matching_chars > largest_match_count:
            largest_match_count = matching_chars

    # If 50% of the words (that are in order) match, we confirm we found the target Pokémon
    return True if largest_match_count / len(pokemon_name) >= 0.5 else False

    # img = cv2.imread("../images/pokemon_name.png")
    # w, h, _ = img.shape
    #
    # boxes = pytesseract.image_to_boxes(img, config=read_name_config)
    #
    # string = ""
    # for box in boxes.splitlines():
    #     print(box)
    #     box = box.split(" ")
    #     print(box)
    #     string += box[0]
    #     img = cv2.rectangle(img, (int(box[1]), h - int(box[2])), (int(box[3]), h - int(box[4])), (255, 0, 0), 2)
    #
    # cv2.imshow("img", img)
    # cv2.waitKey(0)
    # pokemon_name = string
    # pokemon_name = pytesseract.image_to_string("../images/feebas_text.png", config=read_name_config)
    # print(pokemon_name)


def set_window_focus():
    with thread.Lock():
        window = WindowStateManager.get_instance().get_window()

        # print(f"{window}\n")
        try:
            window.activate()
        except pywindow.PyGetWindowException:
            controls.switch_tab()
            print("Something went wrong when trying to activate the window")
            window.minimize()
            window.maximize()
            window.restore()

        time.sleep(1)
