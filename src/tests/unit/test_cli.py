import pytest
import questionary
from questionary import Choice


def test_select():
    menu_list = [
        "Hello there",
        "Whats up",
    ]
    selected = questionary.select("Hello", choices=menu_list)

    assert selected != ""
