import json.decoder
import time
import threading as thread
import os
import pyautogui

from state_manager import WindowStateManager, HuntStateManager
import actions
# import detection
# import controls
import encounter_methods
import file_manager
from Enums import HuntMode, WalkTypes, FishingTypes


def print_start_menu():
    menu_options = [
        "Continue latest hunt",
        "Resume hunt",
        "Start new hunt",
        "Practice hunt",
        "Show hunt history",
        "Quit"
    ]

    print("\nMenu:")
    for i in range(len(menu_options)):
        print(f"{i + 1}. {menu_options[i]}")


def select_menu_option():
    while True:
        try:
            print_start_menu()
            option = int(input("#: "))

            match option:
                case 1:
                    hunt = file_manager.load_latest_hunt()
                    print("\n---------------------------------------------------------")
                    file_manager.display_hunt(hunt)
                    ans = input("Do you want to continue this hunt? (y/n): ")
                    if ans == 'y' or ans == 'yes':
                        hunt_id = hunt['id']
                        pokemon_name = hunt['pokemon_name']
                        hunt_mode = hunt['hunt_mode']
                        encounters = hunt['encounters']
                        try:
                            is_practice = hunt['is_practice']
                        except KeyError:
                            is_practice = False

                        date_match: int = str(hunt['last_time_hunted_date']).find(file_manager.get_date("%Y-%m-%d"))
                        if date_match != -1:
                            HuntStateManager.get_instance().set_was_hunted_today(True)
                        HuntStateManager.get_instance().set_hunt_state(hunt_id, pokemon_name, hunt_mode, encounters, is_practice)

                        return load_action(hunt_mode)
                case 2:
                    hunt = select_hunt()
                    hunt_id = hunt['id']
                    pokemon_name = hunt['pokemon_name']
                    hunt_mode = hunt['hunt_mode']
                    encounters = hunt['encounters']
                    HuntStateManager.get_instance().set_hunt_state(hunt_id, pokemon_name, hunt_mode, encounters)

                    return load_action(hunt_mode)
                case 3 | 4:
                    pokemon_name = input("Which Pokémon are you hunting?: ")
                    if option == 2:
                        HuntStateManager.get_instance().set_hunt_state(pokemon_name=pokemon_name)
                    else:
                        HuntStateManager.get_instance().set_hunt_state(pokemon_name=pokemon_name, is_practice=True)
                    return select_action()

                case 5:
                    file_manager.display_all_hunts()
                    input("Next (enter):")
                case 6:
                    exit()
                case _:
                    print("Invalid option, try again.")
        except EOFError:
            print("End of file.")
        except json.decoder.JSONDecodeError:
            print("No save data available.")
        except TypeError:
            print("No save data available.")
        except KeyError:
            print("No save data available.")
        except ValueError:
            pass


def select_hunt():
    x = file_manager.display_current_hunts()
    while True:
        res = int(input("\nPlease select a hunt to resume (#): "))

        for item in x:
            for k in item.keys():
                if k == res:
                    return file_manager.load_hunt(item[k])
        print("Invalid selection, try again.")


def display_actions_menu():
    action_list = [
        f"{HuntMode.POKERADAR.value} hunt",
        f"{HuntMode.FISHING.value} hunt",
        f"{HuntMode.FOSSIL.value} hunt",
        f"{HuntMode.SAFARI_ZONE.value} hunt",
        f"{HuntMode.SOFT_RESET.value} hunt",
        f"{HuntMode.EGG.value} hunt",
        f"{HuntMode.REGULAR.value} hunt"
    ]

    print(
        "Please select one of the following automation options:\n"
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


def load_action(hunt_mode):
    options = [
        {f"{HuntMode.POKERADAR.value}": None},
        {f"{HuntMode.FISHING.value}": actions.fishing_hunt},
        {f"{HuntMode.FOSSIL.value}": None},
        {f"{HuntMode.SAFARI_ZONE.value}": None},
        {f"{HuntMode.SOFT_RESET.value}": actions.soft_reset_hunt},
        {f"{HuntMode.EGG.value}": None},
        {f"{HuntMode.REGULAR.value}": actions.regular_hunt}
    ]

    for mode in options:
        for k in mode.keys():
            if k == hunt_mode:
                return thread.Thread(target=mode[k], daemon=True)


def select_action():
    while True:
        try:
            display_actions_menu()

            option = int(input("Enter your option (0-8): "))

            match option:
                case 0:
                    print("Program exited.")
                    exit()
                case 1:
                    # print(f"Beginning {HuntMode.POKERADAR.value} hunt!")
                    # print(f"{HuntMode.POKERADAR.value} hunt coming soon.")
                    return None
                case 2:
                    method, args = select_search_func(HuntMode.FISHING.value)
                    HuntStateManager.get_instance().set_hunt_mode(HuntMode.FISHING.value)

                    return thread.Thread(target=actions.fishing_hunt, args=[method, args], daemon=True)
                case 3:
                    # print(f"Beginning {HuntMode.FOSSIL.value} hunt!")
                    # print(f"{HuntMode.FOSSIL.value} hunt coming soon.")
                    return None
                case 4:
                    # print(f"Beginning {HuntMode.SAFARI_ZONE.value} hunt!")
                    # print(f"{HuntMode.SAFARI_ZONE.value} hunt coming soon.")
                    return None
                case 5:
                    # print(f"{HuntMode.SOFT_RESET.value} hunt coming soon.")
                    HuntStateManager.get_instance().set_hunt_mode(HuntMode.SOFT_RESET.value)
                    return thread.Thread(target=actions.soft_reset_hunt, daemon=True)
                case 6:
                    # print(f"Beginning {HuntMode.EGG.value} hunt!")
                    # print(f"{HuntMode.EGG.value} hunt coming soon.")
                    return None
                case 7:
                    method, args = select_search_func(HuntMode.REGULAR.value)
                    HuntStateManager.get_instance().set_hunt_mode(HuntMode.REGULAR.value)

                    return thread.Thread(target=actions.regular_hunt, args=[method, args], daemon=True)

                case _:
                    print("This option is not available, try again")
        except EOFError:
            print("End of file.")
        except ValueError:
            print("This hunt mode have no other search method.")


def select_search_func(hunt_mode):
    match hunt_mode:
        # case HuntMode.POKERADAR.value:
        case HuntMode.FISHING.value:
            fishing_methods = [
                {
                    "number": 1,
                    "description": f"{FishingTypes.REGULAR.value}",
                    "method": encounter_methods.fishing,
                    "args": None
                },
                {
                    "number": 2,
                    "description": f"{FishingTypes.FEEBAS.value}",
                    "method": None,
                    "args": None
                }
            ]
            search_methods = fishing_methods

        # case HuntMode.FOSSIL.value:
        # case HuntMode.SAFARI_ZONE.value:
        # case HuntMode.SOFT_RESET.value:
        # case HuntMode.EGG.value:
        case HuntMode.REGULAR.value:
            walk_methods = [
                {
                    "number": 1,
                    "description": f"{WalkTypes.RANDOM.value}",
                    "method": encounter_methods.walk_random,
                    "args": None
                },
                {
                    "number": 2,
                    "description": f"{WalkTypes.CIRCLES.value}",
                    "method": encounter_methods.lets_try_spinning,
                    "args": 1
                }
            ]
            search_methods = walk_methods
        case _:
            raise ValueError

    while True:
        try:
            num = 0
            print("Please select search method:")
            for option in search_methods:
                num += 1
                print(f"{option['number']}: {option['description']}")

            ans = int(input(f"Select option (1-{num}): "))

            method = search_methods[ans - 1]['method']
            args = search_methods[ans - 1]['args']

            if method is None:
                print("This method is currently unavailable, try again.\n")
            else:
                return method, args
        except IndexError:
            print("Invalid option.\n")


def test_function():
    print("Test function")
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
