import json
import requests
import requests.exceptions
import threading
import re
import unicodedata

from src.config import ZONE_DATA_PATH, HTTP_TIMEOUT_SECONDS
from src.home.zone_models import ZoneData

with open(ZONE_DATA_PATH, 'r') as file:
    zone_data = json.load(file).get("zones")


zone_activation_data = {}  # track active zones (zone_number: bool), true if active
device_nickname_data = {}  # track device_nickname to its zone_number and device_number


def cleanup_nickname(nickname):
    """
    Returns a formatted string with its outer whitespace removed, special characters removed,
    and inner whitespace changed to a single underscore.
    :param nickname:
    :return: formatted nickname
    """

    nickname = unicodedata.normalize("NFKD", nickname)
    nickname = nickname.lower()
    nickname.strip()
    nickname = re.sub(r"[^\w\s]", "", nickname)  # remove special characters
    nickname = re.sub(r"\s+", "_", nickname)  # normalize white spaces into a single underscore
    return nickname.strip("_")


def setup_all_zones():
    """attempts to communicate with all zones located identified in data/zones.json"""
    threads = []

    for i, zone in enumerate(zone_data):
        t = threading.Thread(target=setup_zone, args=(zone, i))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()


def setup_zone(current_zone, zone_number):
    current_zone_ip = current_zone.get("ip")
    #print(current_zone)

    try:
        response = requests.post(
            url=f'http://{current_zone_ip}/setupDevices',
            json=current_zone,
            headers={"Content-Type": "application/json"},
            timeout=HTTP_TIMEOUT_SECONDS
        )

        print("Zone " + str(zone_number) + ": " + response.text)

        zone_activation_data[zone_number] = True  # mark zone as successfully activated

        for j, device in enumerate(current_zone["devices"]):
            nickname = cleanup_nickname(device["nickname"])
            device_nickname_data[nickname] = {
                "zone_number": zone_number,
                "device_number": j,
            }

    except requests.exceptions.ConnectTimeout:
        print(str(current_zone_ip) + " was unresponsive\n")
        zone_activation_data[zone_number] = False  # mark zone as not active

    except requests.exceptions.ConnectionError:
        print(str(current_zone_ip) + " refused the connection\n")
        zone_activation_data[zone_number] = False  # mark zone as not active


def validate_zone_data():
    """
    check zone data has all needed attributes and does not have duplicate nicknames
    :return: *True* if valid
    :raises ValueError:
    """

    ZoneData.model_validate({"zones": zone_data})

    nicknames = set()
    for i, zone in enumerate(zone_data):
        for j, device in enumerate(zone["devices"]):
            nickname = cleanup_nickname(device["nickname"])

            if nickname not in nicknames:  # check for duplicate nickname
                nicknames.add(nickname)
            else:
                raise ValueError(f"Duplicate device nickname: {nickname} on zone {i} device {j}")

    return True
