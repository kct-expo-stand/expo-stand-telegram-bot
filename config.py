import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
SHEET_ENDPOINT = os.getenv("SHEET_ENDPOINT")
DB_NAME = "leads.db"
