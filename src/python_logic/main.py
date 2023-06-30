# External modules
# import pyautogui
import pygetwindow as pywindow
import time
import random
import keyboard
# import multiprocessing as mp
import threading as thread

# Local modules
import controls
import actions
import detection


def main():
    print("--- Hello PyAutoGUI! ---")
    steps = random.randint(1, 10)
    print(f"Character is taking: {steps} steps")
    done = [False]

    t1 = thread.Thread(target=actions.lets_try_spinning, args=(done,), daemon=True)
    # t2 = thread.Thread(target=actions.watch_quit, daemon=True)

    # print("\nSwitching tab")
    set_window_focus()

    t1.start()
    done[0] = actions.watch_quit()

    # t2.start()

    t1.join()

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
          "\n4: Soft reset hunt"
          "\n5: Regular encounters"
          "\n======================="
          "\n\nOther automations:"
          "\n======================="
          "\n6: "
          "\n======================="
          "\n0: Quit")


def select_action():
    option = input("Enter your option (0-6: ")
    match option:
        case 0:
            print("Quitting")
        case 1:
            print("Running Pokeradar hunt")
        case 2:
            print("Running Fishing hunt")
        case 3:
            print("Running Fossil hunt")
        case 4:
            print("Running Soft reset hunt")
        case 5:
            print("Running Regular hunt")
        case 6:
            print("Running ... hunt")

        case _:
            print("This option is not available, try again")


def set_window_focus():
    version_num = "0.9.11"
    window_name1 = f"DeSmuME {version_num} x64"
    window_name2 = "Paused"
    time.sleep(1)

    try:
        window = pywindow.getWindowsWithTitle(window_name1)[0]
        window.activate()
        time.sleep(1)
        print(window)
    except IndexError:
        try:
            window = pywindow.getWindowsWithTitle(window_name2)[0]
            window.activate()
            time.sleep(1)
            print(window)
        except IndexError:
            print(f'\nWindow named: "{window_name1}" or "{window_name2}" could not be found.')


if __name__ == '__main__':
    # keyboard.on_press_key("esc", on_key_press)

    set_window_focus()
    detection.find_pause_and_resume()
    # main()
    # display_menu()
