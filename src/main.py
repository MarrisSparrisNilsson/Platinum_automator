# External modules
import threading as thread
import time

# Local modules
from src.automation import actions, controls
from src.core.App import app_context
from src.database.database import initialize_db
from src.definitions import DEBUG_MODE, is_PyCharm
from src.sandbox import lab
from src.states.Shutdown import ShutdownStateManager
from src.UI.cli_ui import select_menu_option
from src.window.focus import find_pause_and_resume, set_window_focus


def main():
    print("\n=============== Welcome to the Platinum automator! ===============")
    try:
        app_context.set_window_state()
        initialize_db()
    except Exception as e:
        print(e)
        exit(-1)

    controls.console_focus(is_PyCharm)

    while True:
        if ShutdownStateManager.get_instance().is_shutting_down():
            return

        action_thread = select_menu_option()
        if action_thread is None:
            print("This action is currently unavailable❌")
            return

        shutdown_thread = thread.Thread(target=actions.watch_exit, name="___watch_exit_thread___", daemon=True)
        input("Press ENTER to start!")
        try:
            shutdown_thread.start()
            set_window_focus()
            time.sleep(1)
            find_pause_and_resume()
            # TODO: INVESTIGATE IF THIS IS NECESSARY, OR IF IT CAN BE REMOVED
            # if not DEBUG_MODE:
            # window_monitor_thread = thread.Thread(target=app_context.monitor_window, name="___monitor_window_thread___", daemon=True)
            # window_monitor_thread.start()
            action_thread.start()
            action_thread.join()  # Wait for action thread to finish it's work
            controls.clear_movement()  # Stop moving

        except AttributeError:
            print("No action was provided")


if __name__ == "__main__":
    try:
        # TODO: Refactor old JSON storage functions to new DB storage functions
        main()
        # test = {'hej': 1, 'da': 1}
        # print(list(test.keys())[0])
        # lab.experiment_function("This is an experimental function", False)
        # helpers.test_function(False)

    except KeyboardInterrupt:
        print("\nSession ended.")
