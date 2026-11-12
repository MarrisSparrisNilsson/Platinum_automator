import json
import os
import time
from datetime import datetime

import keyboard
import questionary

from src.automation import controls
from src.states.Pause import PauseStateManager
from src.states.Shutdown import ShutdownStateManager


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
        do_repeat = questionary.confirm("You want to repeat?", default=False).ask()
        if not do_repeat or run_once:
            print(end_message)
            break


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
    :param time_format: Format the datetime as "YYYY-MM-DD HH:MM" using "%Y-%m-%d %H:%M"
    :return: Current local date string based on format
    """
    # Get the current datetime
    current_datetime = datetime.now()

    # Format the datetime as "YYYY-MM-DD HH:MM"
    return current_datetime.strftime(time_format)


def shutdown(shutdown_message="Shutting down"):
    # TODO: REFACTOR INTO NEW IMPLEMENTATION WITH APP_CONTEXT STATES
    pause_manager = PauseStateManager.get_instance()
    encounter_pause_event = pause_manager.get_encounter_pause_state()

    shutdown_manager = ShutdownStateManager.get_instance()
    shutdown_event = shutdown_manager.get_state()

    shutdown_event.set()  # Shutting down
    # time.sleep(0.2)  # Wait for encounter_pause_state print
    encounter_pause_event.set()  # Get out of encounter detection lock

    print(shutdown_message, "\n")
    raise SystemExit(0)
