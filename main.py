# External modules
import threading as thread

# Local modules
from src.python_logic import controls, actions, detection, helpers, cli_ui
from src.python_logic.states.GameView import WindowStateManager

from src.database.database import engine
from src.database.models import Base
from src.python_logic.states.Hunt import HuntStateManager


def main():
    initialize_database()
    print("\n### Welcome to the Platinum automator ###")
    controls.console_focus()
    while True:
        action_thread = cli_ui.select_menu_option()
        if action_thread is None:
            print("This action is currently unavailable❌")
        else:
            shutdown_thread = thread.Thread(target=actions.watch_exit, daemon=True)
            input("Press ENTER to start!")
            try:
                WindowStateManager.get_instance().set_state()
                shutdown_thread.start()
                detection.set_window_focus()
                detection.find_pause_and_resume()
                action_thread.start()
                action_thread.join()
                controls.clear_movement()  # Stop moving

            except AttributeError:
                print("No action was provided")


def initialize_database():
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    try:
        # TODO: Refactor old JSON storage functions to new DB storage functions
        main()
        # initialize_database()
        # helpers.test_function(False)

    except KeyboardInterrupt:
        print("\nSession ended.")
