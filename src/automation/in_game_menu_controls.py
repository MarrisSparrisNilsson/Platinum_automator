import time

import pyautogui

from src.automation import controls
from src.core.enums import BagSlots, InGameMenuSlots, UtilityItems
from src.core.Game import game_context, normalize_pixel_coords, normalize_region
from src.definitions import SRC_DIR
from src.states.Pause import PauseStateManager
from src.states.Shutdown import ShutdownStateManager
from src.utils.helpers import is_target_string_found
from src.vision.game_ui_detector import (
    dialog_is_open,
    has_background_changed,
    is_same_object_showing,
)
from src.window.game_object_region_definitions import UI_ELEMENT_PIXELS, UI_ELEMENTS

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
                    i = search_bag_item(utility_slot_value, item.value.lower())

                    if item is UtilityItems.MAX_REPEL:
                        activate_repel()
                    elif utility_slot_value == BagSlots.KEY_ITEMS:
                        register_key_item(i, register)
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
def register_key_item(i: int, register: bool = True):
    if register:
        x, y = normalize_pixel_coords(
            UI_ELEMENT_PIXELS["registered_item"][0],
            UI_ELEMENT_PIXELS["registered_item"][1] + i * UI_ELEMENT_PIXELS["list_item_border_y_offset"],
        )
        if not pyautogui.pixelMatchesColor(x, y, (255, 255, 255)):
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

    # Pixel in the middle of the orange rectangle (on the height axis) of the top most menu.
    menu_p = normalize_pixel_coords(
        UI_ELEMENT_PIXELS["menu_action"][0],
        UI_ELEMENT_PIXELS["menu_action"][1] + menu_num.value * UI_ELEMENT_PIXELS["menu_action_offset"],
    )

    pyautogui.moveTo(menu_p)

    # Find menu action
    while True:
        time.sleep(0.1)
        if ShutdownStateManager.get_instance().is_shutting_down():
            return

        if pyautogui.pixelMatchesColor(menu_p[0], menu_p[1], (255, 107, 16)):
            break
        else:
            # Choose the fastest scroll action
            if menu_num.value > InGameMenuSlots.TRAINER_CARD.value:
                controls.up()
            else:
                controls.down()


@controls.require_desmume_focus
def save_in_game():
    save_box_x, save_box_y = normalize_pixel_coords(*UI_ELEMENT_PIXELS["save_box"])
    start_save_box = pyautogui.pixel(save_box_x, save_box_y)
    while True:
        if ShutdownStateManager.get_instance().is_shutting_down():
            return True

        controls.a_button()
        time.sleep(0.5)

        if pyautogui.pixelMatchesColor(save_box_x, save_box_y, start_save_box):
            print("Game is saved!")
            return True


@controls.require_desmume_focus
def search_bag_item(utility_item_slot: int, utility_name: str):

    # Utility item slot coordinates (Could be: ITEMS, TM, POKE BALLS, KEY ITEMS etc.)
    # Calculate the offset of the target item slot based on the value of utility_item_slot.
    utility_item_slot_offset = UI_ELEMENT_PIXELS["bag_section_slot_offset"] * utility_item_slot

    x, y = normalize_pixel_coords(
        UI_ELEMENT_PIXELS["bag_section_coord"][0] + utility_item_slot_offset,
        UI_ELEMENT_PIXELS["bag_section_coord"][1],
    )
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

    x1, y1 = normalize_pixel_coords(*UI_ELEMENT_PIXELS["item_icon"])

    utility_item_name_img_path = SRC_DIR / f"assets/images/local/item_name.png"
    last_utility_item_location = SRC_DIR / f"assets/images/local/last_item.png"

    direction_changed = False

    item_scroll_index = 0
    start = 0
    stop = 6
    loop_dir = 1

    # print("item_scroll_index:", item_scroll_index, "start:", start, "stop:", stop, "loop_dir:", loop_dir)

    while True:
        try:
            # time.sleep(0.05)
            # FIXME: INVESTIGATE IF WORD RECOGNITION IS A BETTER SUITE FOR THIS FUNCTION
            # FIXME: Image region should be dynamic to window screen resolution

            utility_item_location = SRC_DIR / f"assets/images/utility_items/{utility_name}.png"
            item_icon_region = normalize_region(region=UI_ELEMENTS["inventory_item"])

            pyautogui.screenshot(str(last_utility_item_location), item_icon_region)
            image_match = pyautogui.locateCenterOnScreen(str(utility_item_location), region=item_icon_region, confidence=0.95)
            if image_match:  # Utility item found
                print(f"{utility_name} was found!")
                for item_scroll_index in range(start, stop, loop_dir):
                    match_x, match_y = normalize_pixel_coords(
                        UI_ELEMENT_PIXELS["list_item_border"][0],
                        UI_ELEMENT_PIXELS["list_item_border"][1] + item_scroll_index * UI_ELEMENT_PIXELS["list_item_border_y_offset"],
                    )
                    # print(f"i={item_scroll_index}:", pyautogui.pixel(match_x, match_y))
                    if pyautogui.pixelMatchesColor(match_x, match_y, (255, 0, 0)):
                        # print("Border found")
                        break

                item_name_region = normalize_region(
                    region=(
                        UI_ELEMENTS["item_name"][0],
                        UI_ELEMENTS["item_name"][1] + item_scroll_index * UI_ELEMENT_PIXELS["list_item_border_y_offset"],
                        UI_ELEMENTS["item_name"][2] - (40 if utility_item_slot == 7 else 0),
                        UI_ELEMENTS["item_name"][3],
                    ),
                )
                pyautogui.screenshot(str(utility_item_name_img_path), item_name_region)

                if not is_target_string_found(
                    utility_name,
                    utility_item_name_img_path,
                    0.5,
                ):
                    print("String did not match.")
                    raise pyautogui.ImageNotFoundException
                return item_scroll_index

        except pyautogui.ImageNotFoundException:
            if ShutdownStateManager.get_instance().is_shutting_down():
                return

            start_p = pyautogui.pixel(x1, y1)

            if direction_changed:
                controls.up()
                if item_scroll_index > 2:
                    item_scroll_index -= 1
                # Given that loop dir has shifted
                start = item_scroll_index
                stop = -1  # Because of range exclusion

            else:
                controls.down()
                if item_scroll_index < 3:
                    item_scroll_index += 1
                # Given that loop dir has shifted
                start = item_scroll_index
                stop = 6

            # print("item_scroll_index:", item_scroll_index, "start:", start, "stop:", stop, "loop_dir:", loop_dir)

            # If the same item is showing, change scroll direction or terminate search
            # fmt: off
            if (is_same_object_showing(last_utility_item_location, item_icon_region) 
                and not has_background_changed(
                x1, y1, start_p,
            )):
                if direction_changed:
                    print("Could not find item.")
                    exit(2)
                direction_changed = True
                print("Bottom reached. Checking the top of the list again...")
                # Change loop order
                loop_dir *= -1


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


def check_repel_status():
    # time.sleep(0.2)
    if dialog_is_open():
        pause_encounter_pause_event = PauseStateManager.get_instance().get_encounter_pause_state()

        # Pause if not already paused
        if pause_encounter_pause_event.is_set():
            pause_encounter_pause_event.clear()  # Pauses encounter detection
        for i in range(3):
            time.sleep(0.1)
            controls.a_button()
        time.sleep(0.1)
        return True
    return False
