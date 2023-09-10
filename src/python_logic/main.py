# External modules
import threading as thread

# Local modules
import controls
import actions
import detection
import helpers


def main():
    print("\n### Welcome to the Platinum automator ###")
    controls.console_focus()
    while True:
        action_thread = helpers.select_menu_option()
        if action_thread is None:
            print("This action is currently unavailable❌")
        else:
            shutdown_thread = thread.Thread(target=actions.watch_exit, daemon=True)
            input("Press ENTER to start!")
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
