import json
from pathlib import Path

file_path = Path(__file__).parent.parent.parent / "data" / "zones.json"

with open(file_path, 'r') as file:
    zone_data = json.load(file).get("zones")