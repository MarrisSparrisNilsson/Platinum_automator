import threading as thread
import time

from src.core.App import app_context
from src.states.Shutdown import ShutdownStateManager


# from src.UI import actions


def _worker_thread_function():
    while True:
        time.sleep(2)
        print("Doing some work.")


def _worker_isolated(shutdown_event):
    while not shutdown_event.is_set():
        time.sleep(0.01)
        print("Working...")

    print("Stopped")


def _worker_shared():
    # shutdown_event = ShutdownStateManager.get_instance().get_state()
    shutdown_event = app_context.shutdown_event
    print("id", id(shutdown_event))
    while not shutdown_event.is_set():
        time.sleep(0.01)
        print("Working...")

    print("Stopped")


# def test_threading():
#     shutdown_thread = thread.Thread(target=_worker_thread_function, daemon=True)
#
#     shutdown_thread.start()
#     shutdown_thread.join()
#
#     # Main execution
#     print("Program finished")


def test_shutdown_thread_isolated():
    shutdown_event = thread.Event()

    shutdown_thread = thread.Thread(
        target=_worker_isolated,
        args=(shutdown_event,)
    )

    print("")

    shutdown_thread.start()

    time.sleep(0.1)

    shutdown_event.set()

    shutdown_thread.join(timeout=1)

    assert not shutdown_thread.is_alive()


def test_shutdown_thread_shared():
    shutdown_event = app_context.shutdown_event

    print("\nid", id(shutdown_event))

    shutdown_event.clear()

    shutdown_thread = thread.Thread(target=_worker_shared, daemon=True)
    shutdown_thread.start()

    time.sleep(0.1)

    # app_context.shutdown_event.set()
    shutdown_event.set()

    shutdown_thread.join()

    assert not shutdown_thread.is_alive()
