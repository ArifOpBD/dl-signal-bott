import os
import time
import requests
import json
from db import add_user, get_users

BOT_TOKEN = os.getenv("BOT_TOKEN")
URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

def send(chat_id, text, keyboard=None):
    data = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    }

    if keyboard:
        data["reply_markup"] = json.dumps(keyboard)

    requests.post(URL + "/sendMessage", data=data)

# /start system
def start(chat_id):
    add_user(chat_id)

    keyboard = {
        "keyboard": [
            ["📊 Auto Signal", "📈 Live Result"],
            ["💰 Money Management"],
            ["👥 VIP Group"]
        ],
        "resize_keyboard": True
    }

    send(chat_id,
        "🔥 *AUTO SIGNAL BOT*\n\n⚡ Fast | 🎯 Accurate | 💰 Smart Trading\n\nSelect an option below:",
        keyboard
    )

# broadcast signals
def broadcast(message):
    users = get_users()
    for u in users:
        send(u, message)

# Telegram updates
def get_updates(offset=None):
    return requests.get(URL + "/getUpdates", params={
        "timeout": 100,
        "offset": offset
    }).json()

# main loop
def run():
    offset = None

    while True:
        updates = get_updates(offset)

        for u in updates.get("result", []):
            offset = u["update_id"] + 1

            msg = u.get("message")
            if not msg:
                continue

            chat_id = msg["chat"]["id"]
            text = msg.get("text", "")

            if text == "/start":
                start(chat_id)

        time.sleep(60)

        # demo signal
        broadcast("📊 SIGNAL: EUR/USD → UP 📈")

run()