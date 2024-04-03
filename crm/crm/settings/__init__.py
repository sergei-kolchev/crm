import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent

load_dotenv(BASE_DIR / ".env")

CRM_SETTINGS_PATH = os.getenv("CRM_SETTINGS_PATH", "PROD")

if CRM_SETTINGS_PATH == "DEV":
    from .dev import *  # noqa F403
else:
    from .prod import *  # noqa F403

from .base import *  # noqa F403
