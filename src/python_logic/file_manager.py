import json
# import uuid
import os
from datetime import datetime


def is_file_empty(file_path):
    return os.path.getsize(file_path) == 0


def create_data(hunt_id, pokemon_name, hunt_mode, encounters, is_finished):
    with open("../data/data.json", "w") as f:
        # # Get the current datetime*
        current_datetime = datetime.now()

        # # Format the datetime as "YYYY-MM-DD HH:MM"
        formatted_datetime = current_datetime.strftime('%Y-%m-%d %H:%M')

        end_date = formatted_datetime if is_finished else ""

        x = {
            "entries": 1,
            "hunt_data": [
                {
                    "id": hunt_id,
                    "pokemon_name": pokemon_name,
                    "hunt_mode": hunt_mode,
                    "start_date": formatted_datetime,
                    "last_time_hunted_date": formatted_datetime,
                    "end_date": end_date,
                    "encounters": encounters,
                    "finished": is_finished
                }
            ]
        }
        # "encounters_today": 0
        # print(json.dumps(x, indent=2))
        json.dump(x, f, indent=2)


def load_hunt(hunt_index: int):
    file_path = "../data/data.json"

    if not is_file_empty(file_path):
        with open(file_path, "r") as f:
            data = json.load(f)
            # print(json.dumps(data, indent=2))

            hunt = data['hunt_data'][hunt_index]
            return hunt
    else:
        print("No save data available.")


def add_data_entry(hunt_id, pokemon_name, hunt_mode, encounters, is_finished):
    with open("../data/data.json", "r+") as f:
        data = json.load(f)
        # print(json.dumps(data, indent=2))

        formatted_datetime = get_date("%Y-%m-%d %H:%M")

        # print("Current time:", formatted_datetime)

        end_date = formatted_datetime if is_finished else ""

        data['entries'] += 1

        if type(data['hunt_data']) is list:
            data['hunt_data'].append({
                "id": hunt_id,
                "pokemon_name": pokemon_name,
                "hunt_mode": hunt_mode,
                "start_date": formatted_datetime,
                "last_time_hunted_date": formatted_datetime,
                "end_date": end_date,
                "encounters": encounters,
                "finished": is_finished
            })
        f.seek(0)
        json.dump(data, f, indent=2)


def save_hunt(hunt_id, pokemon_name, hunt_mode, encounters, is_finished):
    data_file = "../data/data.json"

    # print(is_file_empty(data_file))

    if is_file_empty(data_file):
        create_data(hunt_id, pokemon_name, hunt_mode, encounters, is_finished)
    else:
        with open(data_file, "r+") as f:
            data = json.load(f)
            # print(json.dumps(data, indent=2))

            formatted_datetime = get_date("%Y-%m-%d %H:%M")

            match_found = False
            for entry in data["hunt_data"]:
                if entry['id'] == hunt_id:
                    match_found = True
                    entry['last_time_hunted_date'] = formatted_datetime
                    if is_finished:
                        entry['end_date'] = formatted_datetime
                    entry['finished'] = is_finished
                    entry['encounters'] = encounters
                    break

            if match_found:
                f.seek(0)
                json.dump(data, f, indent=2)
            else:
                add_data_entry(hunt_id, pokemon_name, hunt_mode, encounters, is_finished)
    print("Hunt was saved!\n")
    # json.dump(data, f, indent=2)


# def delete_data_entry():
#     with open("../data/data.json", "r") as f:
#         data = json.load(f)
#         print(json.dumps(data, indent=2))
#
#         print(data["hunt_data"]["counter"])


def display_current_hunts():
    file_path = "../data/data.json"

    with open(file_path, "r") as f:
        data = json.load(f)

        print(
            "\nActive Pokémon hunts:"
            "\n==================================================================="
            "\n#      Pokémon         Start Date        Hunt Mode      Encounters"
            "\n==================================================================="
        )

        i = 1
        real_index = 0
        x = []

        for entry in data["hunt_data"]:
            if not entry['finished']:
                x.append({
                    f"{i}": real_index
                })

                print(f"{i:<6} {entry['pokemon_name']:12} {entry['start_date']:20}"
                      f" {entry['hunt_mode']:14} {entry['encounters']:<10}")
                i += 1
            real_index += 1

        return x


def display_all_hunts():
    with open("../data/data.json", "r") as f:
        data = json.load(f)

        print("\nPokémon hunt history:"
              "\n=========================================================")
        for entry in data["hunt_data"]:
            print(
                f"{'Id:':20} {entry['id']}"
                f"\n{'Pokemon:':20} {entry['pokemon_name']}"
                f"\n{'Hunt type:':20} {entry['hunt_mode']}"
                f"\n{'Start date:':20} {entry['start_date']}"
                f"\n{'Last active date:':20} {entry['last_time_hunted_date']}"
                f"\n{'End date:':20} {entry['end_date']}"
                f"\n{'Encounters:':20} {entry['encounters']}"
                # f"\n{'Encounters today:':20} {entry['encounters_today']}"
                f"\n{'Hunt finished:':20} {entry['finished']}"
                "\n---------------------------------------------------------"
            )


def get_date(time_format):
    # Get the current datetime
    current_datetime = datetime.now()

    # Format the datetime as "YYYY-MM-DD HH:MM"
    return current_datetime.strftime(time_format)
