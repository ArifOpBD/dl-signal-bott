import os
import time
import requests
import json
from datetime import datetime, timedelta
from db import add_user, get_users

BOT_TOKEN = os.getenv("BOT_TOKEN")
URL = f"https://api.telegram.org/bot{BOT_TOKEN}"


# ---------------- SEND MESSAGE ----------------
def send(chat_id, text, keyboard=None):
    data = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    }

    if keyboard:
        data["reply_markup"] = json.dumps(keyboard)

    return requests.post(URL + "/sendMessage", data=data).json()


# ---------------- START SYSTEM ----------------
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


# ---------------- SIGNAL ENGINE ----------------
def generate_signal():
    import random

    pairs = ["EUR/USD", "GBP/USD", "USD/JPY", "AUD/USD"]

    return {
        "pair": random.choice(pairs),
        "direction": random.choice(["BUY 📈", "SELL 📉"]),
        "risk": random.randint(20, 70)
    }


# ---------------- TIME ENGINE ----------------
def get_execution_time():
    return datetime.utcnow() + timedelta(minutes=2)


def countdown(exec_time):
    now = datetime.utcnow()
    sec = int((exec_time - now).total_seconds())

    if sec < 0:
        return "00:00"

    return f"{sec//60:02d}:{sec%60:02d}"


# ---------------- BROADCAST ----------------
def broadcast(text):
    users = get_users()
    for u in users:
        send(u, text)


# ---------------- TELEGRAM POLLING ----------------
def get_updates(offset=None):
    return requests.get(URL + "/getUpdates", params={
        "timeout": 100,
        "offset": offset
    }).json()


# ---------------- MAIN LOOP ----------------
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

        # ---------------- LIVE SIGNAL ----------------
        sig = generate_signal()
        exec_time = get_execution_time()

        users = get_users()
        msg_ids = {}

        # send initial signal
        for u in users:
            res = send(u, f"""
🤖 LIVE SIGNAL

💰 {sig['pair']}
📈 {sig['direction']}

⏱ Execution: {exec_time.strftime('%H:%M UTC')}
🛡 Risk: {sig['risk']}/100

⏳ Countdown starting...
""")
            msg_ids[u] = res["result"]["message_id"]

        # ---------------- COUNTDOWN UPDATE ----------------
        for _ in range(10):

            cd = countdown(exec_time)

            for u in users:
                requests.post(URL + "/editMessageText", data={
                    "chat_id": u,
                    "message_id": msg_ids[u],
                    "text": f"""
🤖 LIVE SIGNAL

💰 {sig['pair']}
📈 {sig['direction']}

⏱ Execution: {exec_time.strftime('%H:%M UTC')}
⏳ Countdown: {cd}

🛡 Risk: {sig['risk']}/100
"""
                })

            time.sleep(10)

        time.sleep(5)


run()