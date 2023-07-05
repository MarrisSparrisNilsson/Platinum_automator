# External modules
import os
import time
# import random
import keyboard
import threading as thread
import pyautogui

# Local modules
import controls
import actions
import detection


def main():
    print_welcome_message()

    action_thread = select_action()
    # print("--- Hello PyAutoGUI! ---")
    # steps = random.randint(1, 10)
    # print(f"Character is taking: {steps} steps")

    detection.set_window_focus()
    detection.find_pause_and_resume()

    shutdown_thread = thread.Thread(target=actions.watch_exit, daemon=True)
    shutdown_thread.start()

    try:
        action_thread.start()
        action_thread.join()
    except AttributeError:
        print("No action was provided")


def walk_straight_down(steps=1):
    start = time.time()
    controls.down()
    time.sleep(0.25 * steps)
    keyboard.release('s')
    end = time.time()
    print(end - start)


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
                # print("Begin Fishing hunt!")
                print("Fishing hunt coming soon.")
                return None
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
    keyboard.press('s')
    time.sleep(2)
    pyautogui.keyUp('s')
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
        time.sleep(0.2)

        selected_habitat = input(f"Please select your current hunting habitat (1-{counter}): ")
        try:
            valid_habitat_name = habitat_types[int(selected_habitat) - 1]
            if valid_habitat_name:
                print(f"{valid_habitat_name.capitalize()} was selected")
                return valid_habitat_name
            else:
                print("No such habitat is listed. Try again")

        except ValueError:
            print("Please enter a valid number...")
        except IndexError:
            print("Not a list option.")


if __name__ == '__main__':
    try:
        # print_welcome_message()
        # display_actions_menu()
        main()
        # select_action()
        # test_function()

    except KeyboardInterrupt:
        print("\nSession ended.")
