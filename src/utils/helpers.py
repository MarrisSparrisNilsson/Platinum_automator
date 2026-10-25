import json
import os
import threading
import time
from datetime import datetime

import keyboard
import pyautogui

from src.automation import controls
from src.core.App import app_context
from src.core.Game import game_context
from src.states.Pause import PauseStateManager
from src.states.Shutdown import ShutdownStateManager


def test_get_screen_pixels():
    controls.switch_tab()
    time.sleep(1)
    game_context.set_dialog_pixels()
    start_p, dialog_p1, dialog_p2 = game_context.get_dialog_pixels()
    # controls.switch_tab()
    time.sleep(2)
    print(start_p)
    time.sleep(2)
    capture_pixel_info(dialog_p2[0], dialog_p2[1])


def pin_point_location_on_screen(x, y):
    controls.switch_tab()
    print(x, y)
    pyautogui.moveTo(x, y)


def test_operation(perform_func, operation_string="N/A", end_message="N/A", args=None, run_once=True):
    if args is None:
        args = []
    if not callable(perform_func):
        print("No perform func was given.")
        exit(-1)

    pixel_key = "k"
    seconds = 2
    while True:
        print(f"In {seconds} seconds, Press {pixel_key} to {operation_string} when ready.")
        for i in range(seconds):
            print(f"{seconds - i}")
            time.sleep(1)
        controls.switch_tab()

        keyboard.wait(pixel_key)

        # ==========================================================
        perform_func(*args)
        # ==========================================================

        controls.switch_tab()
        res = input("Press Enter to repeat or -1 to quit: ")
        print(res)
        if res == "-1" or run_once:
            print(end_message)
            break


def capture_pixel_info(x: int = 0, y: int = 0):
    new_x = x
    new_y = y
    if new_x and new_y:
        pixel = pyautogui.pixel(new_x, new_y)
    else:
        mouse = pyautogui.position()
        print(mouse)
        new_x = int(mouse.x)
        new_y = int(mouse.y)
        pixel = pyautogui.pixel(new_x, new_y)

    app_context.set_window_state()

    window_width, window_width = app_context.window_size

    print(f"Pixel RGB: {pixel}")
    pyautogui.moveTo(new_x, new_y)

    percent_w = new_x / window_width
    print(f"W: {percent_w}")
    percent_h = new_y / window_width
    print(f"H: {percent_h}")


def get_habitat():
    while True:
        print("\nPlease select one of the following habitats:")
        counter = 0
        folder_dir = f"../assets/images/sparkles"
        habitat_types = []
        for habitat_type in os.listdir(folder_dir):
            print(f"{counter + 1}: {habitat_type.capitalize()}")
            habitat_types.append(habitat_type)
            counter += 1
        # time.sleep(0.2)

        try:
            selected_habitat = input(f"Please select your current hunting habitat (1-{counter}): ")
            valid_habitat_name = habitat_types[int(selected_habitat) - 1]
            if valid_habitat_name:
                print(f"{valid_habitat_name.capitalize()} was selected")
                return valid_habitat_name
            else:
                print("No such habitat is listed. Try again")

        except ValueError:
            print("\nPlease enter a valid number...")
        except IndexError:
            print("Not a list option.")
        except UnicodeDecodeError:
            print("\nInput was canceled.")


def record_steps(file_name):
    """
    Helper function to track movement keys
    :param file_name: Output file name of the tracked steps
    """
    start_time = time.time()
    with open(f"../resources/{file_name}.json", "r+") as f:
        data = json.load(f)
        data["location"] = 0
        json.dump(data, f, indent=2)
    while True:
        key = ""
        end_time = time.time()
        duration = end_time - start_time

        if duration > 0.2:
            if keyboard.is_pressed("w"):
                key = "w"
            elif keyboard.is_pressed("a"):
                key = "a"
            elif keyboard.is_pressed("s"):
                key = "s"
            elif keyboard.is_pressed("d"):
                key = "d"

        if not key == "":
            start_time = time.time()
            print(f"{key} was pressed")
            with open(f"../resources/{file_name}.json", "r+") as f:
                data = json.load(f)
                data["path"].append(key)

                f.seek(0)
                json.dump(data, f, indent=2)


def get_date(time_format="%Y-%m-%d") -> str:
    """
    :param time_format: Format the datetime as "YYYY-MM-DD HH:MM" or "%Y-%m-%d %H:%M"
    :return: Current local date string based on format
    """
    # Get the current datetime
    current_datetime = datetime.now()

    # Format the datetime as "YYYY-MM-DD HH:MM"
    return current_datetime.strftime(time_format)


def read_tiles(resource_path):
    try:
        # Open the file
        with open(resource_path, "r") as f:
            file = json.load(f)
            tiles = file["path"]
            return tiles
    except json.decoder.JSONDecodeError:
        print(f"Something went wrong with the resource file: {resource_path}")
        exit(-1)


def shutdown(shutdown_message="Shutting down"):
    # TODO: REFACTOR INTO NEW IMPLEMENTATION WITH APP_CONTEXT STATES
    pause_main_state = PauseStateManager.get_instance()
    pause_main_event = threading.Event()

    shutdown_state = ShutdownStateManager.get_instance()
    shutdown_event = threading.Event()

    pause_main_event.set()  # Get out of lock
    shutdown_event.clear()  # Reset the internal flag to false (Shutting down)

    pause_main_state.set_main_state(pause_main_event)
    shutdown_state.set_state(shutdown_event)

    print(shutdown_message)
    raise SystemExit(0)
