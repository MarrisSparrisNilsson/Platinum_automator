import pytest

from src.definitions import SRC_DIR
from src.utils.helpers import is_target_string_found


def test_is_target_string_found():
    utility_item_name_img_path = SRC_DIR / f"assets/images/local/item_name.png"
    print()
    print(str(utility_item_name_img_path))
    item_name = "Heart Scale"
    assert is_target_string_found(item_name, utility_item_name_img_path, 0.7)
