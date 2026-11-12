import threading
import uuid

from src.core.enums import EncounterTimeout, HuntMode


class HuntStateManager:
    """Thread-safe singleton holding the bot's hunt state."""

    _instance = None
    _instance_lock = threading.Lock()  # guards singleton creation only

    def __new__(cls, *args, **kwargs):
        # Even HuntStateManager() returns the shared instance.
        if cls._instance is None:
            with cls._instance_lock:
                if cls._instance is None:
                    inst = super().__new__(cls)
                    inst._init_state()  # initialized exactly once, under the lock
                    cls._instance = inst
        return cls._instance

    def _init_state(self):
        self._lock = threading.RLock()  # guards all state access

        # Save data
        self._hunt_id: str = str(uuid.uuid4())
        self._pokemon_name: str = ""
        self._hunt_mode: str = ""
        self._hunt_method: str = ""
        self._is_practice: bool = False

        # Hunt cache
        self._was_hunted_today: bool = False
        self._encounter_timeout = 0
        self._facing_direction: str = ""
        self._target_pokemon_found: bool = False

    @classmethod
    def get_instance(cls) -> "HuntStateManager":
        return cls()

    # ------------------------------------------------------------------
    # Internal helper (call only while holding self._lock)
    # ------------------------------------------------------------------
    @staticmethod
    def _timeout_for(hunt_mode):
        # fmt: off
        return (
            EncounterTimeout.LEGENDARY.value 
            if hunt_mode == HuntMode.SOFT_RESET.value 
            else EncounterTimeout.REGULAR.value
        )

    # ------------------------------------------------------------------
    # Hunt state (save data)
    # ------------------------------------------------------------------
    def get_hunt_state(self):
        with self._lock:
            return (
                self._hunt_id,
                self._pokemon_name,
                self._hunt_mode,
                self._hunt_method,
                self._is_practice,
            )

    def set_hunt_state(
        self,
        hunt_id=None,
        pokemon_name: str = None,
        hunt_mode: str = None,
        hunt_method: str = None,
        is_practice: bool = None,
    ):
        """Partial update: only fields that are passed (not None) are changed."""
        with self._lock:
            if hunt_id is not None:
                self._hunt_id = hunt_id
            if pokemon_name is not None:
                self._pokemon_name = str(pokemon_name).upper()
            if hunt_mode is not None:
                self._hunt_mode = hunt_mode
                self._encounter_timeout = self._timeout_for(hunt_mode)
            if hunt_method is not None:
                self._hunt_method = hunt_method
            if is_practice is not None:
                self._is_practice = is_practice

    def get_hunt_id(self):
        with self._lock:
            return self._hunt_id

    def get_hunted_pokemon_name(self):
        with self._lock:
            return self._pokemon_name

    def get_hunt_mode(self):
        with self._lock:
            return self._hunt_mode

    def set_hunt_mode(self, hunt_mode, hunt_method=""):
        with self._lock:
            self._hunt_mode = hunt_mode
            self._hunt_method = hunt_method
            self._encounter_timeout = self._timeout_for(hunt_mode)

    def get_encounter_timeout(self):
        with self._lock:
            return self._encounter_timeout

    # ------------------------------------------------------------------
    # Hunt cache
    # ------------------------------------------------------------------
    def set_was_hunted_today(self, was_hunted_today=False):
        with self._lock:
            self._was_hunted_today = was_hunted_today

    def get_was_hunted_today(self):
        with self._lock:
            return self._was_hunted_today

    def set_facing_direction(self, facing_direction: str):
        """Context for `find_exclamation_mark()` only; does not physically move."""
        with self._lock:
            self._facing_direction = facing_direction

    def get_facing_direction(self) -> str:
        with self._lock:
            return self._facing_direction

    def set_target_pokemon_found(self, found: bool = True):
        with self._lock:
            self._target_pokemon_found = found

    def get_target_pokemon_found(self) -> bool:
        with self._lock:
            return self._target_pokemon_found

    def reset_hunt_cache(self):
        """Clear per-run cache without touching the saved hunt data."""
        with self._lock:
            self._was_hunted_today = False
            self._facing_direction = ""
            self._target_pokemon_found = False

    @property
    def lock(self):
        """Hold this for multi-step read-modify-write sequences."""
        return self._lock
