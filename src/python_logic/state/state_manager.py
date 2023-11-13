import threading
import uuid
import pyautogui
import pygetwindow as pywindow

from src.python_logic import file_manager
from src.python_logic.Enums import EncounterTimeout, HuntMode


class ShutdownStateManager:
    _instance = None
    _state: threading.Event = None
    _lock = threading.Lock()

    @staticmethod
    def get_instance():
        if ShutdownStateManager._instance is None:
            with ShutdownStateManager._lock:
                if ShutdownStateManager._instance is None:
                    ShutdownStateManager._instance = ShutdownStateManager()
        return ShutdownStateManager._instance

    def set_state(self, value):
        with ShutdownStateManager._lock:
            self._state = value

    def get_state(self):
        with ShutdownStateManager._lock:
            return self._state

    def check_shutdown_state(self):
        shutdown_event = self.get_state()
        if shutdown_event is not None:
            return True
        else:
            return False


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

    def get_main_state(self):
        with PauseStateManager._lock:
            return self._main_state

    def check_pause_state(self, pause_message: str, continue_message: str):
        pause_event = self.get_state()
        # If encounter is active
        if pause_event is not None:
            if not pause_event.is_set():
                if len(pause_message) > 0:
                    print(pause_message)
                pause_event.wait()  # Wait for encounter to finish

                if len(continue_message) > 0 and not ShutdownStateManager.get_instance().check_shutdown_state():
                    print(continue_message + "\n")
                return True
        return False


class WindowStateManager:
    _instance = None
    _window = None
    _window_size: (int, int) = (0, 0)
    _lock = threading.Lock()

    @staticmethod
    def get_instance():
        if WindowStateManager._instance is None:
            with WindowStateManager._lock:
                if WindowStateManager._instance is None:
                    WindowStateManager._instance = WindowStateManager()
        return WindowStateManager._instance

    def set_state(self):
        # Find window dynamically
        all_w = pywindow.getAllWindows()
        # print("Scanning open windows:")
        for i in range(len(all_w)):
            window = all_w[i]
            # print(window.title)
            window_u = str.upper(window.title)
            if window_u.find("DESMUME") != -1 or window_u.find("PAUSED") != -1:
                print(f"\n{window.title} was detected!")
                try:
                    window = pywindow.getWindowsWithTitle(window.title)[0]
                    self._window = window
                    self._window_size = (window.width, window.height)
                    print(self._window_size)
                    return
                except IndexError:
                    print("Something went wrong.")
                    exit()
        print("Desmume was not detected.")
        exit(-1)

    def get_window_size(self):
        return self._window_size

    def get_window(self):
        return self._window


class HuntStateManager:
    _instance = None
    _hunt_id: str = str(uuid.uuid4())
    _pokemon_name: str = ""
    _hunt_mode: str = ""
    _encounters: int = 0
    # _hunt_index: int
    _finished: bool = False
    _is_practice: bool = False
    _was_hunted_today: bool = False
    _encounter_timeout = 0
    _facing_direction = None
    _lock = threading.Lock()

    @staticmethod
    def get_instance():
        if HuntStateManager._instance is None:
            with HuntStateManager._lock:
                if HuntStateManager._instance is None:
                    HuntStateManager._instance = HuntStateManager()
        return HuntStateManager._instance

    def set_hunt_state(self, hunt_id=str(uuid.uuid4()), pokemon_name="Unknown", hunt_mode="", encounters=0, is_practice=False):
        with (HuntStateManager._lock):
            self._hunt_id = hunt_id
            self._pokemon_name = pokemon_name
            self._hunt_mode = hunt_mode
            self._encounter_timeout = EncounterTimeout.LEGENDARY.value if hunt_mode == HuntMode.SOFT_RESET.value else EncounterTimeout.REGULAR.value
            self._encounters = encounters
            self._is_practice = is_practice
            print(f"Beginning {hunt_mode} hunt!")

    def set_hunt_mode(self, hunt_mode):
        with HuntStateManager._lock:
            self._hunt_mode = hunt_mode
            self._encounter_timeout = EncounterTimeout.LEGENDARY.value if hunt_mode == HuntMode.SOFT_RESET.value else EncounterTimeout.REGULAR.value
            print(f"Beginning {hunt_mode} hunt!")

    def set_was_hunted_today(self, was_hunted_today=False):
        with HuntStateManager._lock:
            self._was_hunted_today = was_hunted_today

    def get_was_hunted_today(self):
        with HuntStateManager._lock:
            return self._was_hunted_today

    def set_facing_direction(self, _facing_direction):
        with HuntStateManager._lock:
            self._facing_direction = _facing_direction

    def get_facing_direction(self):
        with HuntStateManager._lock:
            return self._facing_direction

    def get_encounters(self):
        with HuntStateManager._lock:
            return self._encounters

    def get_encounter_timeout(self):
        with HuntStateManager._lock:
            return self._encounter_timeout

    def increment_encounters(self):
        with HuntStateManager._lock:
            self._encounters += 1

    def finish_hunt(self, is_finished=False):
        with HuntStateManager._lock:
            file_manager.save_hunt(self._hunt_id, self._pokemon_name, self._hunt_mode, self._encounters, self._is_practice, is_finished)


class DialogStateManager:
    _instance = None
    _start_pixel = (0, 0, 0)
    _dialog_point1: (int, int) = (0, 0)
    _dialog_point2: (int, int) = (0, 0)
    _lock = threading.Lock()

    @staticmethod
    def get_instance():
        if DialogStateManager._instance is None:
            with DialogStateManager._lock:
                if DialogStateManager._instance is None:
                    DialogStateManager._instance = DialogStateManager()
        return DialogStateManager._instance

    def set_dialog_pixels(self):
        with DialogStateManager._lock:
            window_width, window_height = WindowStateManager.get_instance().get_window_size()
            dialog_p1 = (int(window_width * 0.032474226804123714), int(window_height * 0.802570093457944))
            dialog_p2 = (int(window_width * 0.4747422680412371), int(window_height * 0.9217289719626168))

            start_p = pyautogui.pixel(dialog_p2[0], dialog_p2[1])
            self._start_pixel = start_p
            self._dialog_point1 = dialog_p1
            self._dialog_point2 = dialog_p2

    def get_dialog_pixels(self):
        with DialogStateManager._lock:
            return self._start_pixel, self._dialog_point1, self._dialog_point2
