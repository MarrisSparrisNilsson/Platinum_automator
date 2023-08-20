import time
import threading as thread
import os
import pyautogui

from state_manager import WindowStateManager
import actions
import detection
import controls


def print_welcome_message():
    print(
        "\n### Welcome to the Platinum automator ###"
        "\nPlease select one of the following automation options:"
    )


def display_actions_menu():
    action_list = [
        "Pokeradar hunt",
        "Fishing hunt",
        "Fossil hunt",
        "Safari zone hunt",
        "Soft-Reset hunt",
        "Egg hunt",
        "Regular hunt"
    ]

    print(
        "\nShiny hunting method:"
        "\n======================="
    )
    # i = int
    for i in range(len(action_list)):
        print(f"{i + 1}: {action_list[i]}")

    # "\n======================="
    # "\n\nOther automations:"
    # "\n======================="
    # "\n8: "
    print("======================="
          "\n0: Quit")


def select_action():
    is_valid = False

    while not is_valid:
        try:
            display_actions_menu()

            controls.console_focus()
            option = int(input("Enter your option (0-8): "))
            # print("")
            is_valid = True

            match option:
                case 0:
                    print("Program exited.")
                    exit()
                case 1:
                    # print("Beginning Pokeradar hunt!")
                    print("Pokeradar hunt coming soon.")
                    return None
                case 2:
                    print("Beginning Fishing hunt!")
                    # print("Fishing hunt coming soon.")
                    return thread.Thread(target=actions.fishing_hunt, daemon=True)
                case 3:
                    # print("Beginning Fossil hunt!")
                    print("Fossil hunt coming soon.")
                    return None
                case 4:
                    # print("Beginning Safari zone hunt!")
                    print("Safari zone hunt coming soon.")
                    return None
                case 5:
                    print("Beginning Soft-Reset hunt!")
                    # print("Soft-Reset hunt coming soon.")
                    return thread.Thread(target=actions.soft_reset_hunt, daemon=True)
                case 6:
                    # print("Beginning Egg hunt!")
                    print("Egg hunt coming soon.")
                    return None
                case 7:
                    print("Beginning Regular hunt!")
                    return thread.Thread(target=actions.regular_hunt, daemon=True)

                case _:
                    if is_valid:
                        is_valid = False
                    print("This option is not available, try again")
        except EOFError:
            print("End of file.")


def test_function():
    detection.set_window_focus()

    # window_width, window_height = WindowStateManager.get_instance().get_window_size()

    get_mouse_coordinates()

    # detection.find_exclamation_mark()
    # screenshot = pyautogui.screenshot(region=(start_x, start_y, end_x, end_y))
    # screenshot.save("../images/test/exclamation_area.png")


def get_mouse_coordinates():
    print("Mouse coordinates in:")

    time.sleep(1)
    seconds = 3
    for i in range(seconds):
        print(f"{seconds - i}")
        time.sleep(1)

    mouse = pyautogui.position()
    print(mouse)
    window_width, window_height = WindowStateManager.get_instance().get_window_size()

    pixel = pyautogui.pixel(mouse.x, mouse.y)
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
