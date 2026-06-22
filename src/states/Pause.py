import threading
from src.states.Shutdown import ShutdownStateManager


class PauseStateManager:
    _instance = None
    _state: threading.Event = None
    _encounter_detection_state: threading.Event = None
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
            self._encounter_detection_state = value

    def get_main_pause_state(self):
        return self._encounter_detection_state

    def check_encounter_detection_pause_state(self):
        with PauseStateManager._lock:
            encounter_detection_event = self._encounter_detection_state

            if encounter_detection_event is not None:
                if not encounter_detection_event.is_set():
                    print("\n========================================"
                          "\nEncounter automation: Paused🔴"
                          "\n========================================\n")
                    encounter_detection_event.wait()
                    if not ShutdownStateManager.get_instance().check_shutdown_state():
                        print("\n========================================"
                              "\nEncounter automation: Resumes▶️"
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
