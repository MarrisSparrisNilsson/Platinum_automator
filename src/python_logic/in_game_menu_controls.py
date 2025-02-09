import pyautogui
import time

from src.python_logic.states.Window import WindowStateManager
from src.python_logic.states.Shutdown import ShutdownStateManager
from src.python_logic.states.GameView import get_pixel_coords
from src.python_logic import controls
from src.python_logic.Enums import InGameMenuSlots, UtilityItems, BagSlots

w, h = WindowStateManager.get_instance().get_window_size()

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


def select_in_game_menu_action(menu_num: InGameMenuSlots, utility_item: UtilityItems = UtilityItems.NULL):
    controls.x_button()

    find_menu_action(menu_num)

    if ShutdownStateManager.get_instance().check_shutdown_state():
        return

    controls.a_button()
    time.sleep(1)

    match menu_num:
        case InGameMenuSlots.BAG:
            if utility_item is not UtilityItems.NULL:
                print(utility_item.value)
                utility_slot_value: int = utility_item_list[f"{utility_item.value}"]
                search_bag_item(utility_slot_value, utility_item.value.lower())
                if utility_item is UtilityItems.MAX_REPEL:
                    activate_repel()
        case InGameMenuSlots.SAVE:
            save_in_game()
        case _:
            print("Input did not match any menu slots.")


def find_menu_action(menu_num: InGameMenuSlots):
    # Menu start x: W * 0.3082474226804124
    # Menu start y: H * 0.10163551401869159

    # Menu end y: H * 0.9392523364485982

    # Menu Y: H * (0.24065420560747663 - 0.12967289719626168)

    window_width, window_height = WindowStateManager.get_instance().get_window_size()

    # Pixel in the middle of the orange rectangle (on the height axis) of the top most menu.
    menu_p = (int(window_width * 0.3077319587628866), int(window_height * (0.18574766355140188 + (menu_num.value * (0.24065420560747663 - 0.12967289719626168)))))

    # menu_p = (int(window_width * 0.3077319587628866), int(window_height * 0.6285046728971962))
    # save_box_p = (int(window_width * 0.12061855670103093), int(window_height * 0.32710280373831774))
    # start_save_box = pyautogui.pixel(save_box_p[0], save_box_p[1])
    pyautogui.moveTo(menu_p)

    # Find menu action
    while True:
        time.sleep(0.1)
        if ShutdownStateManager.get_instance().check_shutdown_state():
            return

        if pyautogui.pixelMatchesColor(menu_p[0], menu_p[1], (255, 107, 16)):
            print("Menu action found.")
            break
        else:
            # Choose the fastest scroll action
            if menu_num.value > InGameMenuSlots.TRAINER_CARD.value:
                controls.up()
            else:
                controls.down()


def save_in_game():
    window_width, window_height = WindowStateManager.get_instance().get_window_size()
    save_box_p = (int(window_width * 0.12061855670103093), int(window_height * 0.32710280373831774))
    start_save_box = pyautogui.pixel(save_box_p[0], save_box_p[1])
    while True:
        if ShutdownStateManager.get_instance().check_shutdown_state():
            return True

        controls.a_button()
        time.sleep(0.5)

        if pyautogui.pixelMatchesColor(save_box_p[0], save_box_p[1], start_save_box):
            print("Game is saved!")
            return True


def search_bag_item(utility_item_slot: int, utility_name: str):
    # pyautogui.screenshot("../images/test_max_repel.png", region=(10, 690, 110, 120))
    # w, h = WindowStateManager.get_instance().get_window_size()
    # p1 = int(0.02422680412371134 * w)
    # p2 = int(0.5467289719626168 * h)

    # Utility item slot coordinates (Could be: ITEMS, TM, POKE BALLS, KEY ITEMS etc.)
    bag_section_coord_x = 0.023471457548536655
    bag_section_coord_y = 0.499185667752443
    # This value will calculate the offset of the target item slot based on the value of utility_item_slot.
    utility_item_slot_offset = int(0.021443059982613734 * utility_item_slot)
    x, y = get_pixel_coords(bag_section_coord_x + utility_item_slot_offset, bag_section_coord_y)

    while True:
        if pyautogui.pixelMatchesColor(x, y, (255, 0, 0)):
            break  # Bag slot located
        else:
            controls.left()
            time.sleep(0.3)

    # Middle pixel coordinates of item image box in bag. If these pixels remain after going up or
    # down in the list (having reached the top or bottom of the list), scroll direction will change.
    x1, y1 = get_pixel_coords(0.034536082474226806, 0.8761682242990654)

    direction_changed = False
    bottom_reached = False
    while True:
        try:
            time.sleep(0.1)
            # FIXME: INVESTIGATE IF WORD RECOGNITION IS A BETTER SUITE FOR THIS FUNCTION
            match = pyautogui.locateCenterOnScreen(f"../images/utility_items/{utility_name}.png", region=(10, 690, 110, 120), confidence=0.95)
            if match:  # Utility item found
                print("Item was found.")
                return

        except pyautogui.ImageNotFoundException:
            if ShutdownStateManager.get_instance().get_state():
                return

            start_p = pyautogui.pixel(x1, y1)

            if direction_changed:
                controls.up()
            else:
                controls.down()

            # If the same item is showing, change scroll direction
            if not has_background_changed(x1, y1, start_p):
                direction_changed = True
                if bottom_reached:
                    print("Could not find item.")
                    exit(2)
                bottom_reached = True


def activate_repel():
    for i in range(3):
        time.sleep(0.2)
        controls.a_button()

    # Close bag and menu
    for i in range(5):
        controls.b_button()
        time.sleep(0.5)


def has_background_changed(x, y, pixel):
    if not pyautogui.pixelMatchesColor(x, y, pixel):
        #  print(f"P: {pyautogui.pixel(x, y)}, {shiny_p}")
        pyautogui.moveTo(x, y)
        return True
    else:
        return False
