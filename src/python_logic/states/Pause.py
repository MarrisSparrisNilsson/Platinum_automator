import threading
from src.python_logic.states.Shutdown import ShutdownStateManager


class PauseStateManager:
    _instance = None
    _state: threading.Event = None
    _main_state: threading.Event = None
    _lock = threading.Lock()

    @staticmethod
    def get_instance():
        if PauseStateManager._instance is None:
            with PauseStateManager._lock:
                if PauseStateManager._instance is None:
                    PauseStateManager._instance = PauseStateManager()
        return PauseStateManager._instance

    def set_state(self, value):
        with PauseStateManager._lock:
            self._state = value

    def get_state(self):
        with PauseStateManager._lock:
            return self._state

    def set_main_state(self, value):
        with PauseStateManager._lock:
            self._main_state = value

    def get_main_pause_state(self):
        with PauseStateManager._lock:
            return self._main_state

    def check_main_pause_state(self):
        with PauseStateManager._lock:
            pause_main_event = self._main_state

            if pause_main_event is not None:
                if not pause_main_event.is_set():
                    print("========================================"
                          "\nEncounter detection: Paused🔴"
                          "\n========================================")
                    pause_main_event.wait()
                    if not ShutdownStateManager.get_instance().check_shutdown_state():
                        print("========================================"
                              "\nEncounter detection: Resumes▶️"
                              "\n========================================\n")
            return False

    def check_pause_state(self, pause_message="", continue_message=""):
        pause_event = self._state
        # If encounter is active
        if pause_event is not None:
            if not pause_event.is_set():
                if len(pause_message) > 0:
                    print(f"{pause_message}")
                pause_event.wait()  # Wait for encounter to finish

                if len(continue_message) > 0 and not ShutdownStateManager.get_instance().check_shutdown_state():
                    print(f"{continue_message}\n")
                return True
        return False
