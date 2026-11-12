import threading as thread

# import cv2
import time

import pyautogui

from src.audio.sound_player import play_sound
from src.automation import controls
from src.core.App import app_context
from src.core.Game import normalize_pixel_coords
from src.database.repositories import PokemonHuntRepository as hunt_db
from src.states.Hunt import HuntStateManager
from src.states.Pause import PauseStateManager
from src.states.Shutdown import ShutdownStateManager
from src.vision.battle_detector import find_sparkles, was_target_pokemon_found
from src.window.game_object_region_definitions import UI_ELEMENT_PIXELS


def is_exclamation_mark(x, y) -> bool:
    # TODO: Improve this function to capture/recognize the actual image of exclamation mark popup. Pixels could be inconsistent.
    # Match against red exclamation mark color
    return pyautogui.pixelMatchesColor(x, y, (255, 66, 0))


def find_exclamation_mark() -> bool:
    exc_points = {
        "w": normalize_pixel_coords(*UI_ELEMENT_PIXELS["excl_middle_up"]),
        "a": normalize_pixel_coords(*UI_ELEMENT_PIXELS["excl_left"]),
        "s": normalize_pixel_coords(*UI_ELEMENT_PIXELS["excl_middle_down"]),
        "d": normalize_pixel_coords(*UI_ELEMENT_PIXELS["excl_right"]),
    }

    direction = HuntStateManager.get_instance().get_facing_direction()

    try:
        x, y = exc_points[direction]
        pyautogui.moveTo(x, y)
    except ValueError:
        direction = ""

    # Search in all the fishing directions if not specified
    if direction == "":
        for p in exc_points.values():
            x, y = p
            if is_exclamation_mark(x, y):
                return True
        return False
    else:
        return is_exclamation_mark(x, y)


def get_encounter_pixels() -> tuple[tuple[int, int], tuple[int, int]]:
    window_width, window_height = app_context.window_size

    pixel_one = (
        int(window_width * 0.25),
        int(window_height * 0.50),
    )

    pixel_two = (
        int(window_width * 0.75),
        int(window_height * 0.50),
    )

    return pixel_one, pixel_two


def has_encounter_started(pixel_one: tuple[int, int], pixel_two: tuple[int, int]):
    pixel_one_is_black = pyautogui.pixelMatchesColor(*pixel_one, (0, 0, 0))
    pixel_two_is_black = pyautogui.pixelMatchesColor(*pixel_two, (0, 0, 0))

    time.sleep(0.1)
    if pixel_one_is_black and pixel_two_is_black:
        encounters = hunt_db.increment_encounters(HuntStateManager.get_instance().get_hunt_id())

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

    hunt_manager = HuntStateManager.get_instance()
    pokemon_name = hunt_manager.get_hunted_pokemon_name()
    hunt_id = hunt_manager.get_hunt_id()
    timeout = hunt_manager.get_encounter_timeout()

    shiny_is_found = False

    while not shiny_is_found:
        PauseStateManager.get_instance().check_encounter_detection_breakpoint()

        if ShutdownStateManager.get_instance().is_shutting_down():
            return

        if has_encounter_started(p1, p2):
            pause_search_encounter_event.clear()  # Pauses search_encounter_func
            controls.clear_movement()  # Stops movement / button presses

            # print("\nWaiting:", timeout, "seconds.")
            time.sleep(timeout)  # Time of encounter intro

            if ShutdownStateManager.get_instance().is_shutting_down():
                return

            """
            NOTE: Using Tesseract (OCR) to read encountered pokemon name and verify with HuntStateManager._pokemon_name
                    if true then increment current hunted pokemon encounters by one.
            """

            target_found = was_target_pokemon_found(pokemon_name)
            if target_found and not shiny_is_found:
                play_sound("Level-up.mp3")
                hunt_manager.set_target_pokemon_found()
                target_encounters = hunt_db.increment_target_encounters(hunt_id)
                print(f"{pokemon_name} #{target_encounters}!")

            shiny_is_found = find_sparkles()

            if ShutdownStateManager.get_instance().is_shutting_down():
                return

            if shiny_is_found:
                print(f"Congratulations! You found a shiny{f' {pokemon_name}' if target_found else ''}!✨")
                play_sound("shiny-pokemon.mp3", volume=0.5)
                if target_found:
                    play_sound("Congratulations.mp3", volume=1, block=True)
                    hunt_db.finish_hunt(hunt_id)
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
