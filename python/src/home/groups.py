import json

from src.config import GROUP_DATA_PATH
from src.home.group_models import GroupData
from src.home.zones import cleanup_nickname

with open(GROUP_DATA_PATH, 'r') as file:
    group_data = json.load(file).get("groups")


nickname_to_devices = {}  # track group_nickname to a list of devices (nickname: list[device])


def setup_all_groups():
    """ sets up all groups by putting their nicknames and associated list of devices in a dictionary"""
    for group in group_data:
        nickname = cleanup_nickname(group["nickname"])
        nickname_to_devices[nickname] = group["devices"]


def validate_group_data():
    """
    check group data has all needed attributes and does not have duplicate nicknames
    :return: *True* if valid
    :raises ValueError:
    """

    GroupData.model_validate({"groups": group_data})

    nicknames = set()
    for group in group_data:
        nickname = cleanup_nickname(group["nickname"])

        if nickname not in nicknames:  # check for duplicate nickname
            nicknames.add(nickname)

        else:
            raise ValueError(f"Duplicate group nickname: {nickname}")

    return True
