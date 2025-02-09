import time
import os

import keyboard
# import keyboard
import pyautogui
from src.python_logic.Enums import UtilityItems
from src.python_logic.states.Window import WindowStateManager
from src.python_logic import controls


def test_function():
    # for i in range(10):
    # print(f"Progress: {i}/9")
    # print('\r', end=f"Progress: {i}/9")
    # time.sleep(0.3)
    # WindowStateManager.get_instance().set_state()
    # file_manager.record_steps()
    # test_operation(Egg.is_two_pokemon_inserted, "see pokemon Day-Care slot status", "Pixel capture ended.", run_once=False)

    print("hello", UtilityItems.MAX_REPEL.value.lower())

    #
    # if False:
    #     test_operation(capture_pixel_info, "get mouse coordinates", run_once=False)
    # else:
    #     w, h = WindowStateManager.get_instance().get_window_size()
    #     item = 3
    #     x = int((0.023471457548536655 + (0.021443059982613734 * item)) * w)
    #     y = int(0.499185667752443 * h)
    #     controls.switch_tab()
    #     pin_point_location_on_screen(x, y)

    # test_operation(pin_point_location_on_screen, "see exact pixel location", "Pixel spotter ended.", [x, y])
    # time.sleep(3)
    # controls.activate_repel()
    # detection.was_target_pokemon_found()

    # file_manager
    # detection.find_exclamation_mark()
    # screenshot = pyautogui.screenshot(region=(start_x, start_y, end_x, end_y))
    # screenshot.save("../images/test/exclamation_area.png")


def pin_point_location_on_screen(x, y):
    print(x, y)
    pyautogui.moveTo(x, y)


def test_operation(perform_func, operation_string="N/A", end_message="N/A", args=None, run_once=True):
    if args is None:
        args = []
    if not callable(perform_func):
        print("No perform func was given.")
        exit(-1)

    pixel_key = 'k'
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


def capture_pixel_info():
    mouse = pyautogui.position()
    print(mouse)
    WindowStateManager.get_instance().set_state()
    window_width, window_height = WindowStateManager.get_instance().get_window_size()

    pixel = pyautogui.pixel(int(mouse.x), int(mouse.y))
    print(f"Pixel rbg: {pixel}")

    percent_w = mouse.x / window_width
    print(f"W: {percent_w}")
    percent_h = mouse.y / window_height
    print(f"H: {percent_h}")


def get_habitat():
    while True:
        print("\nPlease select one of the following habitats:")
        counter = 0
        folder_dir = f"../images/sparkles"
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
