import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
ADMIN_IDS = [
    int(x)
    for x in os.getenv("ADMIN_IDS").split(",")
]

WEBHOOK_URL = os.getenv("WEBHOOK_URL")
WEBHOOK_PATH = os.getenv("WEBHOOK_PATH", "webhook")
PORT = int(os.getenv("PORT", 8080))