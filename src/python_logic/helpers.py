import keyboard
import time
import threading as thread
import os
import pyautogui

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
        "Soft reset hunt",
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
    window = detection.get_window()
    is_valid = False

    while not is_valid:
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
                # print("Begin Pokeradar hunt!")
                print("Pokeradar hunt coming soon.")
                return None
            case 2:
                print("Begin Fishing hunt!")
                # print("Fishing hunt coming soon.")
                habitat = get_habitat()
                return thread.Thread(target=actions.fishing_hunt, args=(window, habitat))
            case 3:
                # print("Begin Fossil hunt!")
                print("Fossil hunt coming soon.")
                return None
            case 4:
                # print("Begin Safari zone hunt!")
                print("Safari zone hunt coming soon.")
                return None
            case 5:
                # print("Begin Soft reset hunt!")
                print("Soft reset hunt coming soon.")
                return None
            case 6:
                # print("Begin Egg hunt!")
                print("Egg hunt coming soon.")
                return None
            case 7:
                print("Begin Regular hunt!")
                habitat = get_habitat()
                return thread.Thread(target=actions.regular_hunt, args=(window, habitat))

            case _:
                if is_valid:
                    is_valid = False
                print("This option is not available, try again")


def test_function():
    detection.set_window_focus()
    # detection.find_exclamation_mark()
    time.sleep(2)
    window = detection.get_window()
    # detection.get_mouse_coordinates()

    x1 = int(window.width * 0.2630359212050985)
    y1 = int(window.height * 0.27670250896057347)

    x2 = int(window.width * 0.36993047508690613)
    y2 = int(window.height * 0.6336917562724015)

    x3 = int(window.width * 0.45712630359212053)
    y3 = int(window.height * 0.2623655913978495)

    x4 = int(window.width * 0.3579142526071842)
    y4 = int(window.height * 0.1013620071684588)

    x5 = int(window.width * 0.45654692931633833)
    y5 = int(window.height * 0.5684587813620071)

    # width = "3452", height = "1395"

    list = [(x1, y1), (x2, y2), (x3, y3), (x4, y4), (x5, y5)]

    for i in range(len(list)):
        pyautogui.moveTo(list[i])
        time.sleep(3)


    # keyboard.press('s')
    # time.sleep(2)
    # pyautogui.keyUp('s')
    # pyautogui.keyDown('w')
    # pyautogui.keyUp('w')
    # keyboard.release('w')
    # keyboard.start_recording()


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
