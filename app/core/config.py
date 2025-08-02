import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.environ.get("MONGO_URI")
DB_NAME = os.environ.get("DB_NAME", "Miyan1")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")

try:
    ADMIN_ID = int(os.environ.get("ADMIN_ID"))
except (ValueError, TypeError):
    raise ValueError("ADMIN_ID environment variable must be set to a valid integer.")