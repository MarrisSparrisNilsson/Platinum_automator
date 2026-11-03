import math
import threading as thread

# import cv2
import time

import pyautogui

from src.audio.sound_player import play_sound
from src.automation import controls
from src.core.App import app_context
from src.database.repositories import PokemonHuntRepository as hunt_db
from src.states.Hunt import HuntStateManager
from src.states.Pause import PauseStateManager
from src.states.Shutdown import ShutdownStateManager
from src.vision.battle_detector import find_sparkles, was_target_pokemon_found


def is_exclamation_mark(x, y):
    # TODO: Improve this function to capture/recognize the actual image of exclamation mark popup. Pixels could be inconsistent.
    # Match against red exclamation mark color
    return True if pyautogui.pixelMatchesColor(x, y, (255, 66, 0)) else False


def find_exclamation_mark() -> bool:
    window_width, window_height = app_context.window_size

    exc_p_middle_up = (int(window_width * 0.25), int(window_height * 0.40887850477757010))
    exc_p_left = (int(window_width * 0.2396907216) + 1, int(window_height * 0.40771028037383180))
    # exc_p_surf_left = (int(window_width * 0.2381443298969072), int(window_height * 0.40186915887850466))
    exc_p_middle_down = (int(window_width * 0.25), int(window_height * 0.42757009345794394))
    exc_p_right = (int(window_width * 0.2603092784), int(window_height * 0.40537383177570090))

    exc_points = [
        exc_p_middle_up,
        exc_p_left,
        exc_p_middle_down,
        exc_p_right,
    ]

    direction = HuntStateManager.get_instance().get_facing_direction()

    x = 0
    y = 0
    try:
        move_dirs = ["w", "a", "s", "d"]
        i = move_dirs.index(direction)
        x, y = exc_points[i]
        pyautogui.moveTo(x, y)
    except ValueError:
        pass

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

    return exclamation_mark_found


def get_encounter_pixels():
    window_width, window_height = app_context.window_size

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


def encounter_detection(
    search_encounter_func,
    end_encounter_func,
    search_args=None,
    flee_from_shiny=False,
):
    if not callable(search_encounter_func) and not callable(end_encounter_func):
        print("Missing encounter functions.")
        exit(-1)

    p1, p2 = get_encounter_pixels()

    pause_manager = PauseStateManager.get_instance()
    # Pause current encounter_detection_thread until search_encounter_thread has started
    encounter_pause_event = pause_manager.get_encounter_pause_state()
    encounter_pause_event.clear()

    # Resume search function without any blocking
    pause_search_encounter_event = pause_manager.get_search_encounter_pause_state()
    pause_search_encounter_event.set()

    search_encounter_thread = thread.Thread(
        target=search_encounter_func, name="___search_encounter_thread___", args=[search_args], daemon=True
    )
    search_encounter_thread.start()

    shiny_is_found = False

    while not shiny_is_found:
        PauseStateManager.get_instance().check_encounter_detection_breakpoint()

        if ShutdownStateManager.get_instance().is_shutting_down():
            return

        is_encounter = encounter_started(p1, p2)
        if is_encounter:
            pause_search_encounter_event.clear()  # Pauses search_encounter_func

            controls.clear_movement()  # Stops movement / button presses

            timeout = HuntStateManager.get_instance().get_encounter_timeout()
            # print("\nWaiting:", timeout, "seconds.")

            time.sleep(timeout)  # Time of encounter intro

            if ShutdownStateManager.get_instance().is_shutting_down():
                return

            """
            NOTE: Using Tesseract (OCR) to read encountered pokemon name and verify with HuntStateManager._pokemon_name
                    if true then increment current hunted pokemon encounters by one.
            """
            hunt_manager = HuntStateManager.get_instance()
            pokemon_name = hunt_manager.get_hunted_pokemon_name()

            target_found = was_target_pokemon_found(pokemon_name)
            if target_found and not shiny_is_found:
                play_sound("Level-up.mp3")
                hunt_manager.set_target_pokemon_found()
                target_encounters = hunt_db.increment_target_encounters(hunt_manager.get_hunt_id())
                print(f"{pokemon_name} #{target_encounters}!")

            # Save after each encounter
            # HuntStateManager.get_instance().save_hunt()
            shiny_is_found = find_sparkles()

            if shiny_is_found:
                print(f"Congratulations! You found a shiny{f' {pokemon_name}' if target_found else ''}!✨")
                play_sound("shiny-pokemon.mp3")
                if target_found:
                    play_sound("Congratulations.mp3")
                    hunt_db.finish_hunt(hunt_manager.get_hunt_id())
                time.sleep(1)

                # --- Shiny tests (Commented/False by default) ---
                if not flee_from_shiny:
                    return  # Exit encounter_detection loop and function
                else:
                    shiny_is_found = False
                    print("Fleeing from shiny!🏃‍♂️💨")
                    time.sleep(1)
                # -----------------------------------------

            end_encounter_func()
            pause_search_encounter_event.set()  # Resumes search_encounter_func
