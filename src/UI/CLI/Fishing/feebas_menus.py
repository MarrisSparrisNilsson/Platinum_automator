import questionary
from questionary import Choice

from src.core.enums import FeebasHuntConfig
from src.utils.helpers import shutdown


def feebas_hunt_configuration(fish_at_pos: int, tot_tiles: int, furthest_reached: int = 0) -> tuple[bool, int]:
    """
    Prints the hunt configuration options and returns hunt configurations based on user input.

    :param fish_at_pos: Current position on the tile path
    :param tot_tiles: Total fish-able tiles in the pond
    :return: Walk_to_pos (bool), fish_at_pos (int)
    """
    walk_to_pos = False
    new_fish_at_pos = 0
    pos_to_newPos = False

    selected = feebas_hunt_configuration_menu(fish_at_pos, tot_tiles, furthest_reached)

    match selected:
        case "quit":
            shutdown()
            exit()

        case FeebasHuntConfig.START:
            walk_to_pos = False
            new_fish_at_pos = 0

        case FeebasHuntConfig.CURRENT_POS:
            walk_to_pos = False
            new_fish_at_pos = fish_at_pos

        case FeebasHuntConfig.START_TO_POS:
            walk_to_pos = True
            new_fish_at_pos = fish_at_pos

        case FeebasHuntConfig.START_TO_FURTHEST:
            walk_to_pos = True
            new_fish_at_pos = furthest_reached

        case FeebasHuntConfig.POS_TO_NEW:
            new_pos = get_new_position(fish_at_pos, tot_tiles)
            if new_pos is not None:
                walk_to_pos = True
                new_fish_at_pos = new_pos
                pos_to_newPos = True

    # 1. Start walking/fishing from current tile position,
    # 2. or use current tile position as walking start point to new location.
    if (fish_at_pos == new_fish_at_pos and not walk_to_pos) or (walk_to_pos and pos_to_newPos):
        start_pos = fish_at_pos
    else:
        start_pos = 0

    return walk_to_pos, start_pos, new_fish_at_pos


def feebas_hunt_configuration_menu(fish_at_pos: int, tot_tiles: int, furthest_reached: int = 0) -> FeebasHuntConfig | None:
    next_pos = fish_at_pos + 1
    last_pos = tot_tiles - 1

    destination = str(next_pos) if next_pos == last_pos else f"{next_pos}-{last_pos}"

    choices = [Choice(title="Start fishing at tile 0", value=FeebasHuntConfig.START)]

    if fish_at_pos > 0:
        choices.extend(
            [
                Choice(title=f"Start fishing at tile {fish_at_pos}", value=FeebasHuntConfig.CURRENT_POS),
                Choice(title=f"Go from 0 to fish at {fish_at_pos}", value=FeebasHuntConfig.START_TO_POS),
            ]
        )
    if furthest_reached > 0:
        choices.append(
            Choice(
                title=f"Go from 0 to fish at furthest position reached today: {furthest_reached}",
                value=FeebasHuntConfig.START_TO_FURTHEST,
            )
        )

    if fish_at_pos < tot_tiles - 1:
        choices.append(Choice(title=f"Go from {fish_at_pos} to fish at <New_Pos> ({destination})", value=FeebasHuntConfig.POS_TO_NEW))

    choices.append(Choice(title="Quit", value="quit"))

    return questionary.select(f"Hunt Configuration\nCurrent tile: {fish_at_pos}", choices=choices).ask()


def get_new_position(start_pos: int, total_tiles: int) -> int | None:
    # Text validation logic
    def validate_position(text: str):
        try:
            val = int(text.strip())
            if val == -1:
                return True
            if start_pos < val < total_tiles:
                return True
            return "Position out of range."
        except ValueError:
            return "Please enter a valid number."

    # Ask the user
    answer = questionary.text(
        f"Pick a new start point ({start_pos + 1}-{total_tiles - 1}) or -1 to cancel:", validate=validate_position
    ).ask()

    if answer is None:
        return None

    option = int(answer.strip())

    if option == -1:
        return None

    return option


def select_start_shore_pos(start_positions: dict):
    choices = [str(k) for k in start_positions.keys()]

    selected_side = questionary.select(
        "Select a starting position from shore side (default all):",
        [Choice(title=c.upper(), value=c) for c in choices] + [Choice(title="ALL", value="all")],
        default="all",
    ).ask()

    if selected_side == "all":
        return "all"

    side = start_positions[selected_side]
    start_pos_choice = [str(i) for i, value in enumerate(side) if value == 3]
    orientation = "left to right" if selected_side == "top" else "top to bottom"
    position_message = (
        f"Select a start point by position index (seen from {orientation} {start_pos_choice[0]}-{start_pos_choice[-1]}):"
        f"\n({', '.join([str(idx) for idx in start_pos_choice])}):"
    )

    # Select position and validate input
    start_pos = int(questionary.text(position_message, validate=(lambda x: x in start_pos_choice)).ask())
    if start_pos == "":
        return None

    start_pos_coord = (0, start_pos) if selected_side == "top" else (start_pos, 0)
    print("Selected position:", start_pos_coord)
    return start_pos_coord
