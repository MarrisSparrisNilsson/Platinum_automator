from src.database.repositories.FeebasRepository import get_feebas_state
from src.UI.CLI.cli_helpers import print_hunt_obj


def print_feebas_state():
    feebas_state = get_feebas_state()
    print_hunt_obj(feebas_state)
