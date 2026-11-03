import threading


class ShutdownStateManager:
    _instance = None
    _instance_lock = threading.Lock()

    def __init__(self):
        # Events are created once and shared across threads.
        self._state: threading.Event = threading.Event()

    @classmethod
    def get_instance(cls):
        with cls._instance_lock:
            if cls._instance is None:
                cls._instance = cls()

            return cls._instance

    def get_state(self):
        """Get shutdown event state"""
        return self._state

    def is_shutting_down(self):
        """Return True if shutdown event is initiated, else False."""
        shutdown_event = self.get_state()
        return shutdown_event.is_set()
