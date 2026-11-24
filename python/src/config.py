from pathlib import Path

# DIRECTORIES AND PATHS

ROOT = Path(__file__).parent.parent
DATA_DIR = ROOT / "data"

VOSK_MODEL_PATH = DATA_DIR / "vosk-model-small-en-us-0.15"
ZONE_DATA_PATH = DATA_DIR / "zones.json"
GROUP_DATA_PATH = DATA_DIR / "groups.json"

# OTHER VARIABLES

DEBUG_MODE_ENABLED = True
HTTP_TIMEOUT_SECONDS = 5
