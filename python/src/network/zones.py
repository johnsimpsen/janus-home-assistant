import json
from pathlib import Path
import requests
import threading

file_path = Path(__file__).parent.parent.parent / "data" / "zones.json"

with open(file_path, 'r') as file:
    zone_data = json.load(file).get("zones")


def setup_all_zones():
    threads = []

    for i, zone in enumerate(zone_data):
        t = threading.Thread(target=setup_zone, args=(zone, i))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()


def setup_zone(current_zone, zone_number):
    current_zone_ip = current_zone.get("ip")
    print(current_zone)

    try:
        response = requests.post(
            url=f'http://{current_zone_ip}/setupDevices',
            json=current_zone,
            headers={"Content-Type": "application/json"},
            timeout=5
        )

        print("Zone number " + str(zone_number) + ":")
        print(response.text)

    except Exception as e:
        print(str(current_zone_ip) + " was unresponsive")

