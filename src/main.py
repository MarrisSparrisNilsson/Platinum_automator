# External modules
import threading as thread

# Local modules
from src.automation import actions, controls
from src.core.App import app_context
from src.database.database import initialize_db
from src.sandbox import lab
from src.UI.cli_ui import select_menu_option
from src.window.focus import find_pause_and_resume, set_window_focus


def main():
    initialize_db()
    print("\n=============== Welcome to the Platinum-automator ===============")
    controls.console_focus()

    app_context.set_window_state()

    window_monitor_thread = thread.Thread(target=app_context.monitor_window, daemon=True)
    window_monitor_thread.start()

    while True:
        action_thread = select_menu_option()
        if action_thread is None:
            print("This action is currently unavailable❌")
            return

        shutdown_thread = thread.Thread(target=actions.watch_exit, daemon=True)
        input("Press ENTER to start!")
        try:
            shutdown_thread.start()
            set_window_focus()
            find_pause_and_resume()
            action_thread.start()
            action_thread.join()
            controls.clear_movement()  # Stop moving

        except AttributeError:
            print("No action was provided")


if __name__ == "__main__":
    try:
        # TODO: Refactor old JSON storage functions to new DB storage functions
        # main()
        # test = {'hej': 1, 'da': 1}
        # print(list(test.keys())[0])
        lab.experiment_function("This is an experimental function", False)
        # helpers.test_function(False)

    except KeyboardInterrupt:
        print("\nSession ended.")
