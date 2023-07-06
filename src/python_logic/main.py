# External modules
# import os
# import time
# import random
# import keyboard
import threading as thread
# import pyautogui

# Local modules
# import controls
import actions
import detection
import helpers


def main():
    helpers.print_welcome_message()

    action_thread = helpers.select_action()
    # print("--- Hello PyAutoGUI! ---")
    # steps = random.randint(1, 10)
    # print(f"Character is taking: {steps} steps")

    shutdown_thread = thread.Thread(target=actions.watch_exit, daemon=True)
    shutdown_thread.start()

    try:
        action_thread.start()
        detection.set_window_focus()
        detection.find_pause_and_resume()
        action_thread.join()
    except AttributeError:
        print("No action was provided")


if __name__ == '__main__':
    try:
        # print_welcome_message()
        # display_actions_menu()
        main()
        # helpers.test_function()
        # select_action()

    except KeyboardInterrupt:
        print("\nSession ended.")
