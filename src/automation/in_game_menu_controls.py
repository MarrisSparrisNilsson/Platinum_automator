import time

import pyautogui

from src.automation import controls
from src.core.App import app_context
from src.core.enums import BagSlots, InGameMenuSlots, UtilityItems
from src.core.Game import game_context
from src.definitions import SRC_DIR
from src.states.Shutdown import ShutdownStateManager
from src.vision.game_ui_detector import (
    dialog_is_open,
    get_pixel_coords,
    has_background_changed,
)

# in_game_menu_pixels = {
#     {
#         "name": "Bag slot rectangle clear red",
#         "coordinate":
#     }
#
# }

utility_item_list = {
    f"{UtilityItems.NULL.value}": -1,
    f"{UtilityItems.REPEL.value}": BagSlots.ITEMS,
    f"{UtilityItems.SUPER_REPEL.value}": BagSlots.ITEMS,
    f"{UtilityItems.MAX_REPEL.value}": BagSlots.ITEMS,
    f"{UtilityItems.BIKE.value}": BagSlots.KEY_ITEMS,
    f"{UtilityItems.OLD_ROD.value}": BagSlots.KEY_ITEMS,
    f"{UtilityItems.GOOD_ROD.value}": BagSlots.KEY_ITEMS,
    f"{UtilityItems.SUPER_ROD.value}": BagSlots.KEY_ITEMS,
    f"{UtilityItems.POKERADAR.value}": BagSlots.KEY_ITEMS,
}


@controls.require_desmume_focus
def execute_inGame_menu_action(menu_num: InGameMenuSlots, utility_item: list[UtilityItems] = None, register: bool = True):
    controls.x_button()

    find_menu_action(menu_num)

    if ShutdownStateManager.get_instance().is_shutting_down():
        return

    controls.a_button()
    time.sleep(1)

    match menu_num:
        case InGameMenuSlots.BAG:
            if utility_item is not UtilityItems.NULL:
                for item in utility_item:
                    utility_slot_value: int = utility_item_list[f"{item.value}"]
                    search_bag_item(utility_slot_value, item.value.lower())

                    if item is UtilityItems.MAX_REPEL:
                        activate_repel()
                    elif utility_slot_value == BagSlots.KEY_ITEMS:
                        register_key_item(register)
                    time.sleep(0.5)
        case InGameMenuSlots.SAVE:
            save_in_game()
        case _:
            print("Input did not match any menu slots.")
    # Close bag and menu
    for i in range(5):
        controls.b_button()
        time.sleep(0.5)


@controls.require_desmume_focus
def register_key_item(register: bool = True):
    if register:
        w, h = app_context.window_size
        x = int(0.43195876288659796 * w)
        y = int(0.5070093457943925 * h)
        if pyautogui.pixelMatchesColor(x, y, (247, 148, 123)):
            print("Already registered")
        else:
            controls.a_button()
            controls.down()
            controls.a_button()
    else:  # Use item
        controls.a_button()
        controls.a_button()


@controls.require_desmume_focus
def find_menu_action(menu_num: InGameMenuSlots):
    # Menu start x: W * 0.3082474226804124
    # Menu start y: H * 0.10163551401869159

    # Menu end y: H * 0.9392523364485982

    # Menu Y: H * (0.24065420560747663 - 0.12967289719626168)

    window_width, window_height = app_context.window_size

    # Pixel in the middle of the orange rectangle (on the height axis) of the top most menu.
    menu_p = (
        int(window_width * 0.3092783505628866),
        int(window_height * (0.18574766355140188 + (menu_num.value * (0.24065420560747663 - 0.12967289719626168)))),
    )

    # menu_p = (int(window_width * 0.3077319587628866), int(window_height * 0.6285046728971962))
    # save_box_p = (int(window_width * 0.12061855670103093), int(window_height * 0.32710280373831774))
    # start_save_box = pyautogui.pixel(save_box_p[0], save_box_p[1])
    pyautogui.moveTo(menu_p)

    # Find menu action
    while True:
        time.sleep(0.1)
        if ShutdownStateManager.get_instance().is_shutting_down():
            return

        if pyautogui.pixelMatchesColor(menu_p[0], menu_p[1], (255, 107, 16)):
            # print("Menu action found.")
            break
        else:
            # Choose the fastest scroll action
            if menu_num.value > InGameMenuSlots.TRAINER_CARD.value:
                controls.up()
            else:
                controls.down()


@controls.require_desmume_focus
def save_in_game():
    window_width, window_height = app_context.window_size
    save_box_p = (int(window_width * 0.12061855670103093), int(window_height * 0.32710280373831774))
    start_save_box = pyautogui.pixel(save_box_p[0], save_box_p[1])
    while True:
        if ShutdownStateManager.get_instance().is_shutting_down():
            return True

        controls.a_button()
        time.sleep(0.5)

        if pyautogui.pixelMatchesColor(save_box_p[0], save_box_p[1], start_save_box):
            print("Game is saved!")
            return True


@controls.require_desmume_focus
def search_bag_item(utility_item_slot: int, utility_name: str):
    # pyautogui.screenshot("../images/test_max_repel.png", region=(10, 690, 110, 120))

    # Utility item slot coordinates (Could be: ITEMS, TM, POKE BALLS, KEY ITEMS etc.)
    bag_section_coord_x = 0.023471457548536655
    bag_section_coord_y = 0.514185667752443
    # This value will calculate the offset of the target item slot based on the value of utility_item_slot.
    utility_item_slot_offset = 0.021443059982613734 * utility_item_slot
    x, y = get_pixel_coords(bag_section_coord_x + utility_item_slot_offset, bag_section_coord_y)
    pyautogui.moveTo(x, y)

    while True:
        if ShutdownStateManager.get_instance().is_shutting_down():
            return

        if pyautogui.pixelMatchesColor(x, y, (255, 0, 0)):
            break  # Bag slot located
        else:
            controls.left()
            time.sleep(0.3)

    # Middle pixel coordinates of item image box in bag. If these pixels remain after going up or
    # down in the list (having reached the top or bottom of the list), scroll direction will change.
    x1, y1 = get_pixel_coords(0.034536082474226806, 0.8761682242990654)

    direction_changed = False
    while True:
        try:
            # time.sleep(0.05)
            # FIXME: INVESTIGATE IF WORD RECOGNITION IS A BETTER SUITE FOR THIS FUNCTION
            # FIXME: Image region should be dynamic to window screen resolution
            utility_item_location = SRC_DIR / f"assets/images/utility_items/{utility_name}.png"
            match = pyautogui.locateCenterOnScreen(str(utility_item_location), region=(10, 690, 110, 120), confidence=0.95)
            if match:  # Utility item found
                # print("Item was found.")
                return

        except pyautogui.ImageNotFoundException:
            if ShutdownStateManager.get_instance().is_shutting_down():
                return

            start_p = pyautogui.pixel(x1, y1)

            if direction_changed:
                controls.up()
            else:
                controls.down()

            # If the same item is showing, change scroll direction or terminate search
            if not has_background_changed(x1, y1, start_p):
                if direction_changed:
                    print("Could not find item.")
                    exit(2)
                direction_changed = True


@controls.require_desmume_focus
def activate_repel():
    for _ in range(3):
        if ShutdownStateManager.get_instance().is_shutting_down():
            return
        time.sleep(0.2)
        controls.a_button()

    time.sleep(1)
    controls.b_button()


@controls.require_desmume_focus
def use_registered_key_item():
    game_context.set_dialog_pixels()
    controls.b_button()  # Get out of potential dialog block
    controls.y_button()  # Use registered item
    time.sleep(0.5)

    # If dialog is shown immediately after using the item, assume it's not used in an appropriate location
    if dialog_is_open():
        raise EnvironmentError()
