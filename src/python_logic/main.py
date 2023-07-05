# External modules
# import pyautogui
import os
import time
import random
import keyboard
# import multiprocessing as mp
import threading as thread

import pyautogui

# Local modules
import controls
import actions
import detection


# from state_manager import ExitStateManager


def main():
    # print("--- Hello PyAutoGUI! ---")
    # steps = random.randint(1, 10)
    # print(f"Character is taking: {steps} steps")
    # done = [False]
    # shutdown_state = ExitStateManager.get_instance()
    # shutdown_state.set_state(False)

    # t1 = thread.Thread(target=actions.lets_try_spinning, args=(done,), daemon=True)
    # t2 = thread.Thread(target=actions.watch_quit, daemon=True)

    # print("\nSwitching tab")
    habitat = get_habitat()
    window = detection.set_window_focus()
    detection.find_pause_and_resume()
    # t1 = thread.Thread(target=actions.regular_hunt, args=(window, habitat,), daemon=True)
    t1 = thread.Thread(target=actions.watch_exit, daemon=True)

    t1.start()
    # actions.watch_exit()
    actions.regular_hunt(window, habitat)

    # t2.start()

    # t1.join()

    # watch_quit_process.start()
    # spinning_process.start()

    # controls.activate_run()
    # print(f"{i + 1}: {end - start}")

    # quit()


def walk_straight_down(steps=1):
    start = time.time()
    controls.down()
    time.sleep(0.25 * steps)
    keyboard.release('s')
    end = time.time()
    print(end - start)


def display_menu():
    print("\n### Welcome to the Platinum automator ###"
          "\nPlease select one of the following automation options:"
          "\n\nShiny hunting method:"
          "\n======================="
          "\n1: Pokeradar hunt"
          "\n2: Fishing hunt"
          "\n3: Fossil hunt"
          "\n4: Safari zone hunt"
          "\n5: Soft reset hunt"
          "\n6: Egg hunt"
          "\n7: Regular encounters"
          "\n======================="
          "\n\nOther automations:"
          "\n======================="
          "\n8: "
          "\n======================="
          "\n0: Quit")


def select_action():
    option = input("Enter your option (0-8: ")
    match option:
        case 0:
            print("Program exited.")
        case 1:
            print("Begin Pokeradar hunt!")
        case 2:
            print("Begin Fishing hunt!")
        case 3:
            print("Begin Fossil hunt!")
        case 4:
            print("Begin Safari zone hunt!")
        case 5:
            print("Begin Soft reset hunt!")
        case 6:
            print("Begin Egg hunt!")
        case 7:
            print("Begin Regular hunt!")
        case _:
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
        controls.console_focus()
        selected_habitat = input(f"Please select your current hunting habitat (1-{counter}): ")
        try:
            valid_habitat_name = habitat_types[int(selected_habitat) - 1]
            if valid_habitat_name:
                print(f"{valid_habitat_name.capitalize()} was selected")
                return valid_habitat_name
            else:
                print("No such habitat is listed. Try again")

        except ValueError:
            print("Enter a valid number dumbass...")
        except IndexError:
            print("Not a list option.")


if __name__ == '__main__':
    try:

        main()
        # test_function()

        # window = detection.set_window_focus()
        # print(window)
        # detection.find_pause_and_resume()
        # time.sleep(1)

        # detection.encounter_detection(window.width, window.height, habitat)

        # display_menu()
    except KeyboardInterrupt:
        print("\nSession ended.")
