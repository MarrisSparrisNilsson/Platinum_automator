import pyautogui
# import cv2
import time
import math
import threading as thread

from src.audio.sound_player import play_sound
from src.core.App import app_context
from src.database.repositories import PokemonHuntRepository as hunt_db
from src.automation import controls
from src.core.Game import game_context
from src.states.Shutdown import ShutdownStateManager
from src.states.Pause import PauseStateManager
from src.states.Hunt import HuntStateManager
from src.vision.battle_detector import was_target_pokemon_found, find_sparkles
from src.vision.game_ui_detector import dialog_is_open


def is_exclamation_mark(x, y):
    # TODO: Improve this function to capture/recognize the actual image of exclamation mark popup. Pixels could be inconsistent.
    return True if pyautogui.pixelMatchesColor(x, y, (255, 66, 0)) else False


def find_exclamation_mark(cast, encounter):
    (window_width, window_height) = app_context.window_size

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

    game_context.set_dialog_pixels()
    direction = HuntStateManager.get_instance().get_facing_direction()

    x = 0
    y = 0
    try:
        move_dirs = ['w', 'a', 's', 'd']
        i = move_dirs.index(direction)
        x, y = exc_points[i]
        pyautogui.moveTo(x, y)
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
        # Search in all the fishing directions if not specified
        if direction is None:
            for p in range(len(exc_points)):
                x, y = exc_points[p]
                exclamation_mark_found = is_exclamation_mark(x, y)
                if exclamation_mark_found:
                    break
        else:
            exclamation_mark_found = is_exclamation_mark(x, y)

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
        # No fish on the hook
        elif dialog_is_open():
            time.sleep(0.3)
            controls.b_button()
            cast[0] += 1
            print('\r', end=f"No fish this time. ({cast[0]})")
            return
    print()


def get_encounter_pixels():
    (window_width, window_height) = app_context.window_size

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
    pixel_one_is_black = pyautogui.pixelMatchesColor(pixel_coord_one[0], pixel_coord_one[1], (0, 0, 0))
    pixel_two_is_black = pyautogui.pixelMatchesColor(pixel_coord_two[0], pixel_coord_two[1], (0, 0, 0))

    time.sleep(0.1)
    if pixel_one_is_black and pixel_two_is_black:
        encounters = hunt_db.increment_encounters(HuntStateManager.get_instance().get_hunt_id())
        # HuntStateManager.get_instance().increment_encounters()
        # encounters = HuntStateManager.get_instance().get_total_encounters()
        print(f"\n\nEncounter #{encounters} started!👊💥")
        return True
    else:
        return False


def encounter_detection(search_encounter_func, end_encounter_func, search_args=None):
    if not callable(search_encounter_func) and not callable(end_encounter_func):
        print("Missing encounter functions.")
        exit(-1)

    p1, p2 = get_encounter_pixels()

    pause_state = PauseStateManager.get_instance()
    pause_event = thread.Event()

    search_encounter_thread = thread.Thread(target=search_encounter_func, args=[search_args], daemon=True)
    search_encounter_thread.start()

    shiny_is_found = False

    while not shiny_is_found:
        PauseStateManager.get_instance().check_encounter_detection_pause_state()

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

            """
            NOTE: Using Tesseract (OCR) to read encountered pokemon name and verify with HuntStateManager._pokemon_name
                    if true then increment current hunted pokemon encounters by one.
            """
            pokemon = HuntStateManager.get_instance().get_hunted_pokemon_name()

            target_found = was_target_pokemon_found(pokemon)
            if target_found and not shiny_is_found:
                play_sound("Level-up.mp3")
                HuntStateManager.get_instance().set_target_pokemon_found()
                target_encounters = hunt_db.increment_target_encounters(HuntStateManager.get_instance().get_hunt_id())
                print(f"{pokemon} #{target_encounters}!")

            # Save after each encounter
            # HuntStateManager.get_instance().save_hunt()
            shiny_is_found = find_sparkles()

            if shiny_is_found:
                print(f"Congratulations! You found a shiny{f' {pokemon}' if target_found else ''}!✨")
                play_sound("shiny-pokemon.mp3")
                if target_found:
                    play_sound("Congratulations.mp3")
                    hunt_db.finish_hunt(HuntStateManager.get_instance().get_hunt_id())
                # HuntStateManager.get_instance().save_hunt(is_finished=True if target_found else False)
                time.sleep(1)

                on_off = False
                if on_off:
                    # --- Shiny tests (Commented/False by default) ---
                    shiny_is_found = False
                    end_encounter_func()
                    pause_event.set()  # Resumes search_encounter_func (Set flag True)
                    pause_state.set_state(pause_event)
                    # -----------------------------------------
            else:
                end_encounter_func()
                pause_event.set()  # Resumes search_encounter_func (Set flag True)
                pause_state.set_state(pause_event)
