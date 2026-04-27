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
URL = f"https://api.telegram.org/bot{BOT_TOKEN}"


def send(chat_id, text, keyboard=None):

    data = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    }

    if keyboard:
        data["reply_markup"] = json.dumps(keyboard)

    return requests.post(URL+"/sendMessage", data=data).json()


def edit(chat_id, msg_id, text):

    requests.post(URL+"/editMessageText", data={
        "chat_id": chat_id,
        "message_id": msg_id,
        "text": text
    })


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

    send(chat_id, "🤖 AI SIGNAL BOT STARTED", keyboard)


def get_updates(offset=None):

    return requests.get(URL+"/getUpdates", params={
        "timeout": 100,
        "offset": offset
    }).json()


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
            text = msg.get("text","")

            if text == "/start":
                start(chat_id)
                continue

            reply = handle_menu(chat_id, text)

            if reply:
                send(chat_id, reply)

        # ---------------- SIGNAL SYSTEM ----------------

        sig = get_signal()

        if not ai_filter(sig):
            continue

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

            msg_map[u] = res["result"]["message_id"]

        # countdown loop
        for _ in range(10):

            cd = countdown(exec_time)

            for u in users:
                edit(u, msg_map[u], f"""
🤖 AI SIGNAL

💰 {sig['pair']}
📈 {sig['direction']}

⏱ Execution: {exec_time.strftime('%H:%M UTC')}
⏳ Countdown: {cd}

🛡 Risk: {sig['risk']}/100
""")

            time.sleep(10)

        time.sleep(5)


run()