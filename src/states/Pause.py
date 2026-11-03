import threading

import emoji

from src.states.Shutdown import ShutdownStateManager


class PauseStateManager:
    _instance = None
    _instance_lock = threading.Lock()

    def __init__(self):
        # Events are created once and shared across threads.
        self._search_encounter_pause_state = threading.Event()
        self._encounter_detection_pause_state = threading.Event()

    @classmethod
    def get_instance(cls):
        with cls._instance_lock:
            if cls._instance is None:
                cls._instance = cls()

            return cls._instance

    def get_search_encounter_pause_state(self) -> threading.Event:
        """Get the event controlling I/O operations to search encounters."""
        return self._search_encounter_pause_state

    def get_encounter_pause_state(self) -> threading.Event:
        """Get the event controlling encounter detection."""
        return self._encounter_detection_pause_state

    def check_encounter_detection_breakpoint(self):
        encounter_detection_event = self.get_encounter_pause_state()

        if not encounter_detection_event.is_set():
            print(
                "\n========================================"
                f"\nEncounter detection: Paused {emoji.emojize(':red_circle:')}"
                "\n========================================\n"
            )

            print(f"Thread: {threading.current_thread().name} is locked! {emoji.emojize(':locked:')}")
            encounter_detection_event.wait()
            print(f"Thread: {threading.current_thread().name} was unlocked! {emoji.emojize(':unlocked:')}")

            if not ShutdownStateManager.get_instance().is_shutting_down():
                print(
                    "\n========================================"
                    f"\nEncounter detection: Resumes {emoji.emojize(':play_button:')}"
                    "\n========================================\n"
                )

    def check_search_encounter_breakpoint(self, pause_message="", continue_message=""):
        search_encounter_pause_event = self.get_search_encounter_pause_state()
        # If encounter is active
        if not search_encounter_pause_event.is_set():
            if len(pause_message) > 0:
                print(f"{pause_message}")

            print(f"\nThread: {threading.current_thread().name} is locked! {emoji.emojize(':locked:')}")
            search_encounter_pause_event.wait()  # Wait for encounter to finish
            print(f"\nThread: {threading.current_thread().name} was unlocked! {emoji.emojize(':unlocked:')}")

            if len(continue_message) > 0 and not ShutdownStateManager.get_instance().is_shutting_down():
                print(f"{continue_message}\n")
            return True
        return False
