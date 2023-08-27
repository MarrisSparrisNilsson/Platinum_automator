import json.decoder
import time
import threading as thread
import os
import pyautogui

from state_manager import WindowStateManager, HuntStateManager
import actions
import detection
import controls
import file_manager


def print_start_menu():
    menu_options = [
        "Resume hunt",
        "Start new hunt",
        "Practice hunt",
        "Show hunt history",
        "Quit"
    ]

    print("Menu:")
    for i in range(len(menu_options)):
        print(f"{i + 1}. {menu_options[i]}")


def select_menu_option():
    is_valid = False

    while not is_valid:
        try:
            print_start_menu()
            option = int(input("#: "))

            is_valid = True
            match option:
                case 1:
                    try:
                        hunt = select_hunt()
                        # print(hunt)
                        hunt_id = hunt['id']
                        pokemon_name = hunt['pokemon_name']
                        hunt_mode = hunt['hunt_mode']
                        encounters = hunt['encounters']
                        HuntStateManager.get_instance().set_hunt_state(hunt_id=hunt_id, pokemon_name=pokemon_name, hunt_mode=hunt_mode, encounters=encounters)

                        return load_action(hunt_mode)
                    except json.decoder.JSONDecodeError:
                        print("No save data available.")
                case 2 | 3:
                    pokemon_name = input("Which Pokémon are you hunting?: ")
                    if option == 2:
                        HuntStateManager.get_instance().set_hunt_state(pokemon_name=pokemon_name)
                    else:
                        HuntStateManager.get_instance().set_hunt_state(pokemon_name=pokemon_name, is_practice=True)
                    return select_action()

                case 4:
                    file_manager.display_all_hunts()
                    input("Next (enter):")
                    is_valid = False

                case 5:
                    exit()
                case _:
                    if is_valid:
                        is_valid = False
                    print("Invalid option, try again.")
        except EOFError:
            print("End of file.")
        except ValueError:
            exit()


def select_hunt():
    x = file_manager.display_current_hunts()
    while True:
        res = input("\nPlease select a hunt to resume (#): ")

        for item in x:
            for k in item.keys():
                if k == res:
                    return file_manager.load_hunt(item[k])
        print("Invalid selection, try again.")


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
        {"Pokeradar": None},
        {"Fishing": actions.fishing_hunt},
        {"Fossil": None},
        {"Safari zone": None},
        {"Soft-Reset": actions.soft_reset_hunt},
        {"Egg": None},
        {"Regular": actions.regular_hunt}
    ]

    for mode in options:
        for k in mode.keys():
            if k == hunt_mode:
                print(f"Beginning {hunt_mode} hunt!")
                return thread.Thread(target=mode[k], daemon=True)


def select_action():
    is_valid = False

    while not is_valid:
        try:
            display_actions_menu()

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
                    HuntStateManager.get_instance().set_hunt_mode("Fishing")
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
                    HuntStateManager.get_instance().set_hunt_mode("Soft-Reset")
                    return thread.Thread(target=actions.soft_reset_hunt, daemon=True)
                case 6:
                    # print("Beginning Egg hunt!")
                    print("Egg hunt coming soon.")
                    return None
                case 7:
                    print("Beginning Regular hunt!")
                    HuntStateManager.get_instance().set_hunt_mode("Regular")
                    return thread.Thread(target=actions.regular_hunt, daemon=True)

                case _:
                    if is_valid:
                        is_valid = False
                    print("This option is not available, try again")
        except EOFError:
            print("End of file.")


def test_function():
    # detection.set_window_focus()

    # file_manager.read_data()
    print_start_menu()

    # file_manager.display_all_hunts()
    # file_manager.create_data()

    # window_width, window_height = WindowStateManager.get_instance().get_window_size()

    # get_mouse_coordinates()

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
