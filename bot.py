import os
import time
import requests
import json

from db import add_user, get_users
from signals import get_signal
from time_engine import execution_time, countdown
from model import ai_filter
from features import handle_menu

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    print("BOT_TOKEN missing")
    exit()

URL = f"https://api.telegram.org/bot{BOT_TOKEN}"


# ---------------- SEND ----------------
def send(chat_id, text, keyboard=None):
    try:
        data = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "Markdown"
        }

        if keyboard:
            data["reply_markup"] = json.dumps(keyboard)

        return requests.post(URL + "/sendMessage", data=data).json()

    except:
        return {}


# ---------------- EDIT ----------------
def edit(chat_id, msg_id, text):
    try:
        requests.post(URL + "/editMessageText", data={
            "chat_id": chat_id,
            "message_id": msg_id,
            "text": text
        })
    except:
        pass


# ---------------- START ----------------
def start(chat_id):
    add_user(chat_id)

    keyboard = {
        "keyboard": [
            ["📊 Auto Signal", "📈 Live Result"],
            ["💰 Money Management"],
            ["👨‍💻 Admin Contact"]
        ],
        "resize_keyboard": True
    }

    send(chat_id, "🤖 AI SIGNAL BOT STARTED 🚀", keyboard)


# ---------------- GET UPDATES ----------------
def get_updates(offset=None):
    try:
        return requests.get(URL + "/getUpdates", params={
            "timeout": 50,
            "offset": offset
        }).json()
    except:
        return {}


# ---------------- SIGNAL ----------------
def send_signal():

    try:
        sig = get_signal()

        if not ai_filter(sig):
            return

        exec_time = execution_time()
        users = get_users()
        msg_map = {}

        for u in users:

            res = send(u, f"""
🤖 AI SIGNAL

💰 {sig['pair']}
📈 {sig['direction']}

⏱ Execution: {exec_time.strftime('%H:%M UTC')}
🛡 Risk: {sig['risk']}/100
""")

            if "result" in res:
                msg_map[u] = res["result"]["message_id"]

        start_time = time.time()

        while time.time() - start_time < 90:

            cd = countdown(exec_time)

            for u in users:
                if u in msg_map:
                    edit(u, msg_map[u], f"""
🤖 AI SIGNAL

💰 {sig['pair']}
📈 {sig['direction']}

⏱ Execution: {exec_time.strftime('%H:%M UTC')}
⏳ Countdown: {cd}

🛡 Risk: {sig['risk']}/100
""")

            time.sleep(10)

    except Exception as e:
        print("Signal error:", e)


# ---------------- RUN ----------------
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
            else:
                reply = handle_menu(chat_id, text)
                if reply:
                    send(chat_id, reply)

        send_signal()

        time.sleep(3)


run()