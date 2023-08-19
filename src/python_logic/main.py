# External modules
# import os
# import time
# import random
# import keyboard
import threading as thread
# import pyautogui

# Local modules
import controls
import actions
import detection
import helpers


def main():
    helpers.print_welcome_message()

    action_thread = helpers.select_action()
    shutdown_thread = thread.Thread(target=actions.watch_exit, daemon=True)

    try:
        shutdown_thread.start()
        detection.set_window_focus()
        detection.find_pause_and_resume()
        action_thread.start()
        action_thread.join()

        controls.clear_movement()  # Stop moving

    except AttributeError:
        print("No action was provided")


if __name__ == '__main__':
    try:
        main()
        # helpers.test_function()

    except KeyboardInterrupt:
        print("\nSession ended.")
