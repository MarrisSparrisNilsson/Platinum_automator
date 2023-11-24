import uuid
import threading

from src.python_logic.Enums import EncounterTimeout, HuntMode
from src.python_logic import file_manager


class HuntStateManager:
    _instance = None

    # Save data
    _hunt_id: str = str(uuid.uuid4())
    _pokemon_name: str = ""
    _hunt_mode: str = ""
    _hunt_method: str = ""
    _total_encounters: int = 0
    _target_pokemon_encounters: int = 0
    # _finished: bool = False
    _is_practice: bool = False

    # Hunt cache
    _was_hunted_today: bool = False
    _encounter_timeout = 0
    _facing_direction = None
    _target_pokemon_found = False
    _lock = threading.Lock()

    @staticmethod
    def get_instance():
        if HuntStateManager._instance is None:
            with HuntStateManager._lock:
                if HuntStateManager._instance is None:
                    HuntStateManager._instance = HuntStateManager()
        return HuntStateManager._instance

    def set_hunt_state(self, hunt_id=str(uuid.uuid4()), pokemon_name="Unknown", hunt_mode="", hunt_method="", total_encounters=0, target_pokemon_encounters=0, is_practice=False):
        with (HuntStateManager._lock):
            self._hunt_id = hunt_id
            self._pokemon_name = str(pokemon_name).upper()
            self._hunt_mode = hunt_mode
            self._hunt_method = hunt_method
            self._encounter_timeout = EncounterTimeout.LEGENDARY.value if hunt_mode == HuntMode.SOFT_RESET.value else EncounterTimeout.REGULAR.value
            self._total_encounters = total_encounters
            self._target_pokemon_encounters = target_pokemon_encounters
            self._is_practice = is_practice

    def get_hunt_mode(self):
        with HuntStateManager._lock:
            return self._hunt_mode

    def set_hunt_mode(self, hunt_mode, hunt_method=""):
        with HuntStateManager._lock:
            self._hunt_mode = hunt_mode
            self._hunt_method = hunt_method
            self._encounter_timeout = EncounterTimeout.LEGENDARY.value if hunt_mode == HuntMode.SOFT_RESET.value else EncounterTimeout.REGULAR.value

    def set_was_hunted_today(self, was_hunted_today=False):
        with HuntStateManager._lock:
            self._was_hunted_today = was_hunted_today

    def get_was_hunted_today(self):
        with HuntStateManager._lock:
            return self._was_hunted_today

    def get_hunted_pokemon_name(self):
        with HuntStateManager._lock:
            return self._pokemon_name

    def set_facing_direction(self, _facing_direction):
        with HuntStateManager._lock:
            self._facing_direction = _facing_direction

    def get_facing_direction(self):
        with HuntStateManager._lock:
            return self._facing_direction

    def set_target_pokemon_found(self):
        with HuntStateManager._lock:
            self._target_pokemon_found = True

    def get_target_pokemon_found(self):
        with HuntStateManager._lock:
            return self._target_pokemon_found

    def get_total_encounters(self):
        with HuntStateManager._lock:
            return self._total_encounters

    def get_target_pokemon_encounters(self):
        with HuntStateManager._lock:
            return self._target_pokemon_encounters

    def get_encounter_timeout(self):
        with HuntStateManager._lock:
            return self._encounter_timeout

    def increment_encounters(self):
        with HuntStateManager._lock:
            self._total_encounters += 1

    def increment_target_encounters(self):
        with HuntStateManager._lock:
            self._target_pokemon_encounters += 1

    def finish_hunt(self, is_finished=False):
        with HuntStateManager._lock:
            file_manager.save_hunt(self._hunt_id, self._pokemon_name, self._hunt_mode, self._hunt_method, self._total_encounters, self._target_pokemon_encounters, self._is_practice, is_finished)
