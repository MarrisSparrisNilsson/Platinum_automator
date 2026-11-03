"""
This test file is used to write test for the EMULATION WINDOW as well as IN-GAME OBSERVATIONS.

This may include INTEGRATION AND UNIT TESTS.
"""

import threading as thread

import pytest
from pygetwindow import Win32Window

from src.automation import controls
from src.automation.actions import watch_exit
from src.core.App import app_context
from src.window.focus import set_window_focus


@pytest.fixture
def window_state_init():
    app_context.set_window_state()

    return app_context.get_window()


@pytest.mark.integration
def test_window_state_init(window_state_init):
    window = window_state_init

    assert window is not None


@pytest.mark.integration
def test_set_window_focus(window_state_init):
    """
    Test will NOT pass in debug mode when DESMUME window CANNOT be IS_ACTIVE == TRUE
    """
    set_window_focus()

    window: Win32Window = app_context.get_window()

    desmume_app = "DESMUME" in window.title.upper() or "PAUSED" in window.title.upper()

    window_focus = desmume_app and window.isActive
    if window_focus:
        print("DESMUME got focus")
        controls.switch_tab()

    assert window_focus == True


# def test_window_focus_thread(window_state_init):


@pytest.mark.integration
def test_monitor_window_move(window_state_init):
    window: Win32Window = window_state_init
    start_left_pos = window.left
    start_top_pos = window.top

    # Use 'esc' button to exit the loop inside monitor_window to finish the test.
    esc_btn = thread.Thread(target=watch_exit, daemon=True)
    esc_btn.start()

    window = app_context.monitor_window()
    controls.switch_tab()

    assert (start_left_pos != window.left) or (start_top_pos != window.top)
