import os
import requests
import time
from db import add_user, get_users
from signals import get_signal
from time_engine import execution_time, countdown

BOT_TOKEN = os.getenv("BOT_TOKEN")
URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

def send(text):
    users = get_users()
    msg_ids = []

    for u in users:
        res = requests.post(URL+"/sendMessage", data={
            "chat_id": u,
            "text": text
        }).json()

        msg_ids.append((u, res["result"]["message_id"]))

    return msg_ids

def edit(chat_id, msg_id, text):
    requests.post(URL+"/editMessageText", data={
        "chat_id": chat_id,
        "message_id": msg_id,
        "text": text
    })

def run():

    offset = None

    while True:

        updates = requests.get(URL+"/getUpdates", params={
            "timeout": 100,
            "offset": offset
        }).json()

        for u in updates.get("result", []):

            offset = u["update_id"] + 1

            msg = u.get("message")
            if not msg:
                continue

            chat_id = msg["chat"]["id"]
            text = msg.get("text","")

            if text == "/start":
                add_user(chat_id)
                requests.post(URL+"/sendMessage", data={
                    "chat_id": chat_id,
                    "text": "🤖 Bot Activated! You will receive live signals."
                })

        # SIGNAL GENERATE
        sig = get_signal()
        exec_time = execution_time()

        users = get_users()
        msg_map = {}

        for u in users:
            res = requests.post(URL+"/sendMessage", data={
                "chat_id": u,
                "text": f"""
🤖 LIVE SIGNAL

💰 {sig['pair']}
📈 {sig['direction']}

⏱ Execution: {exec_time.strftime('%H:%M UTC')}
🛡 Risk: {sig['risk']}/100

⏳ Starting countdown...
"""
            }).json()

            msg_map[u] = res["result"]["message_id"]

        # LIVE COUNTDOWN UPDATE
        for _ in range(10):

            cd = countdown(exec_time)

            for u in users:
                edit(u, msg_map[u], f"""
🤖 LIVE SIGNAL

💰 {sig['pair']}
📈 {sig['direction']}

⏱ Execution: {exec_time.strftime('%H:%M UTC')}
⏳ Countdown: {cd}

🛡 Risk: {sig['risk']}/100
""")

            time.sleep(10)

        time.sleep(5)