import time

from src.automation import controls, in_game_menu_controls
from src.core.enums import InGameMenuSlots, UtilityItems
from src.core.Game import game_context
from src.database.repositories import FeebasRepository as feebas_state
from src.encounter_methods.Fishing.Feebas.feebas_utils import (
    get_cleared_percentage,
    get_cleared_tiles,
    make_feebas_fishing_movement,
    non_cleared_tile_ranges,
    read_feebas_tile_map,
    read_tiles,
)
from src.encounter_methods.Fishing.Feebas.path_finder import find_feebas_path
from src.encounter_methods.Fishing.fishing import fishing
from src.states.Hunt import HuntStateManager
from src.states.Pause import PauseStateManager
from src.states.Shutdown import ShutdownStateManager
from src.UI.CLI.Fishing.feebas_menus import (
    feebas_hunt_configuration,
    select_start_shore_pos,
)
from src.utils.helpers import get_date, shutdown

if __name__ == "__main__":
    feebas_grid, shore_positions = read_feebas_tile_map()
    start_pos_coord = select_start_shore_pos(shore_positions)
    # find_feebas_path()


def feebas_fishing(encounters=2):
    """
    Start point is located in the top right corner of the lake
    where you fish and then use surf.

    Map goes through every fish-able water tile

    Walk 'i' steps and turn towards i+1, then fish twice (default).

    Steps:

    1: Fish x2

    2: Take step, (``Path[i]``)

    3: Turn towards next step if ``Path[i] != Path[i+1]``
    """

    game_context.set_dialog_pixels()

    # Steps are determined by direction and edge of a tile that the path crosses.
    tiles = read_tiles()

    time.sleep(0.2)  # Wait for encounter_pause_state print

    feebas_state.init_feebas_tracking()

    feebas_info = feebas_state.get_feebas_state()
    found_date = feebas_info["found_date"]
    todays_date = get_date()

    # If Feebas has been found today
    if found_date == todays_date:
        was_found_today = True
        fish_at_pos = feebas_info["found_at"]
        tile_ranges = get_cleared_tiles(feebas_info, len(tiles))
        print(f"FEEBAS was last seen at tile {fish_at_pos}❗\n")
    else:
        was_found_today = False
        # (New day)
        if not feebas_info["current_date"] == todays_date:
            feebas_info = feebas_state.reset_feebas_state(todays_date)
            print("\nNew day has begun!" "\nFarthest reached position has been set to 0\n")
            tile_ranges = [(0, len(tiles) - 1)]
        else:
            tile_ranges = get_cleared_tiles(feebas_info, len(tiles))

        fish_at_pos = feebas_info["latest_tile"]

    controls.switch_tab()
    print("Non-cleared tile ranges:", tile_ranges)
    print(f"Cleared percentage: {get_cleared_percentage(tile_ranges, len(tiles)):.2f}%")
    walk_to_pos, start_pos, new_fish_at_pos = feebas_hunt_configuration(
        fish_at_pos,
        len(tiles),
        feebas_info["furthest_tile_reached_today"],
    )
    controls.switch_tab()

    # Ensure player is turned in the right direction
    if start_pos == 0:
        controls.move(tiles[0], 0)
    else:
        HuntStateManager.get_instance().set_facing_direction(tiles[start_pos])  # Set initial facing direction

    # Register Good Rod and Max repel
    in_game_menu_controls.execute_inGame_menu_action(
        InGameMenuSlots.BAG,
        [
            UtilityItems.MAX_REPEL,
            UtilityItems.GOOD_ROD,
        ],
    )

    if ShutdownStateManager.get_instance().is_shutting_down():
        return

    # No backslash in f-string allowed
    new_line = "\n"
    line_separator = "================================================"
    if walk_to_pos:
        print(line_separator)

    # print("walk_to_pos:", walk_to_pos)
    for tile in range(start_pos, len(tiles)):  # <--------------------------------- Begin loop --------------------
        # On feebas found tile, break loop and continue fishing
        if tile == fish_at_pos and was_found_today:
            print(f">>> Continuing to look for Feebas at current tile: {tile}❗")
            break

        if walk_to_pos:
            print("\r", end=f"Traveling tiles: {tile}/{new_fish_at_pos}")

        else:
            tile_message = f"Fishing at tile: {tile}{new_line}"
            print(f"{line_separator}{new_line}{tile_message}")

        # =================================================================
        """
        NOTE 1: (IF) Start fishing if current position index is greater or equal to assigned position
                (new_fish_at_pos) and therefore is NOT assigned to walk anywhere (walk_to_pos=False)
        NOTE 2: (ELSE) Skip fishing as long as current position is less than assigned start position.
        """

        if tile >= new_fish_at_pos:
            # When tile is not start position
            if tile != start_pos and walk_to_pos:
                walk_to_pos = False  # Goal position reached
                print("\nFishing spot reached")

            fishing(encounters, True)
            # HACK: Can these two be moved inside fishing?
            time.sleep(3)

            non_cleared_tile_ranges(tile_ranges, tile)
            feebas_state.increment_tile_count_tracking(tile, tile_ranges)

            # Don't touch
            PauseStateManager.get_instance().check_search_encounter_breakpoint(
                "Fishing is paused▶️", "Fishing and walking now continues🎣🪝"
            )

            # If Feebas was found
            was_found_today = HuntStateManager.get_instance().get_target_pokemon_found()
            if was_found_today:
                feebas_state.update_feebas_found(tile)
                todays_date = get_date()
                break  # Break/Exit walking progression loop

        if ShutdownStateManager.get_instance().is_shutting_down():
            return

        # =================================================================
        if tile == 0:
            print("\nSurf time!")
            controls.surf()
            time.sleep(1.5)
        else:
            make_feebas_fishing_movement(tiles, tile, walk_to_pos)

        if ShutdownStateManager.get_instance().is_shutting_down():
            return
        # =================================================================

    # Feebas has been found (keep fishing)
    while was_found_today:
        if not todays_date == get_date("%Y-%m-%d"):
            print("\nTime is past midnight🌙" "\nGo back to start position and try again.")
            # TODO: Maybe just replace ShutdownStateManager with a keyboard.press("esc")?
            # Set the internal flag to True (Shutting down)
            ShutdownStateManager.get_instance().get_state().set()
            return
        else:
            fishing(1)

    shutdown_message = "\nAt the end of the path⛔" "\nNo Feebas found❌" "\nGo back to start position and try again!↩️"
    shutdown(shutdown_message)
    return
