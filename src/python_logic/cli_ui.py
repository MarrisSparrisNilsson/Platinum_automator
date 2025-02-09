import json.decoder
import threading as thread

from src.python_logic import file_manager, actions
from src.python_logic.Enums import HuntMode
from src.python_logic.states.Hunt import HuntStateManager


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
                        hunt_method = hunt['hunt_method']
                        total_encounters = hunt['total_encounters']
                        target_pokemon_encounters = hunt['target_pokemon_encounters']
                        try:
                            is_practice = hunt['is_practice']
                        except KeyError:
                            is_practice = False

                        date_match: int = str(hunt['last_time_hunted_date']).find(file_manager.get_date("%Y-%m-%d"))
                        if date_match != -1:
                            HuntStateManager.get_instance().set_was_hunted_today(True)
                        HuntStateManager.get_instance().set_hunt_state(hunt_id, pokemon_name, hunt_mode, hunt_method, total_encounters, target_pokemon_encounters, is_practice)

                        return actions.load_action(hunt_mode, hunt_method)
                case 2:
                    hunt = select_hunt()
                    if hunt is None:
                        continue

                    hunt_id = hunt['id']
                    pokemon_name = hunt['pokemon_name']
                    hunt_mode = hunt['hunt_mode']
                    hunt_method = hunt['hunt_method']
                    total_encounters = hunt['total_encounters']
                    target_pokemon_encounters = hunt['target_pokemon_encounters']
                    try:
                        is_practice = hunt['is_practice']
                    except KeyError:
                        is_practice = False
                    HuntStateManager.get_instance().set_hunt_state(hunt_id, pokemon_name, hunt_mode, hunt_method, total_encounters, target_pokemon_encounters, is_practice)

                    return actions.load_action(hunt_mode, hunt_method)
                case 3 | 4:
                    pokemon_name = input("Which Pokémon are you hunting?: ")
                    if option == 3:
                        HuntStateManager.get_instance().set_hunt_state(pokemon_name=pokemon_name)
                    if option == 4:
                        HuntStateManager.get_instance().set_hunt_state(pokemon_name=pokemon_name, is_practice=True)
                    return select_action()

                case 5:
                    file_manager.display_all_hunts()
                    input("Next (enter):")
                case 6:
                    exit(0)
                case _:
                    print("Invalid option, try again.")
        except EOFError:
            print("End of file.")
        except json.decoder.JSONDecodeError:
            print("No save data available.")
        # except TypeError:
        #     print("No save data available.")
        # except KeyError:
        #     print("No save data available.")
        except ValueError:
            pass
        except FileExistsError:
            print("No save data available.")


def select_hunt():
    x = file_manager.display_current_hunts()
    while True:
        try:
            res = int(input("\nPlease select a hunt to resume or -1 to go back (#): "))
            if res == -1:
                return None

            for item in x:
                for k in item.keys():
                    if int(k) == res:
                        return file_manager.load_hunt(item[k])
            print("Invalid selection, try again.")
        except ValueError:
            print("Input is not a number, try again.")


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

    for i in range(len(action_list)):
        print(f"{i + 1}: {action_list[i]}")

    # "\n======================="
    # "\n\nOther automations:"
    # "\n======================="
    # "\n8: "
    print("======================="
          "\n0: Quit")


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
                    method, args, method_name = select_search_func(HuntMode.FISHING.value)
                    HuntStateManager.get_instance().set_hunt_mode(HuntMode.FISHING.value, method_name)

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
                    HuntStateManager.get_instance().set_hunt_mode(HuntMode.EGG.value)
                    return thread.Thread(target=actions.egg_hunt, daemon=True)
                    # return None
                case 7:
                    method, args, method_name = select_search_func(HuntMode.REGULAR.value)
                    HuntStateManager.get_instance().set_hunt_mode(HuntMode.REGULAR.value, method_name)

                    return thread.Thread(target=actions.regular_hunt, args=[method, args], daemon=True)

                case _:
                    print("This option is not available, try again")
        except EOFError:
            print("End of file.")
        except ValueError:
            print("This hunt mode have no other search method.")


def select_search_func(hunt_mode):
    while True:
        try:
            num = 0
            print("Please select any of the search methods:")
            methods = actions.action_types[hunt_mode]['methods']
            for method in methods:
                num += 1
                print(f"{method['number']}: {method['method_name']}")

            ans = int(input(f"Select an option (1-{num}): "))

            method = methods[ans - 1]['method']
            args = methods[ans - 1]['args']
            method_name = methods[ans - 1]['method_name']

            if method is None:
                print("This method is currently unavailable, try again.\n")
            else:
                return method, args, method_name
        except IndexError:
            print("Invalid option.\n")
        except ValueError:
            print("Invalid option.\n")


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
