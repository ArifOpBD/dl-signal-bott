import os
import time
import requests
from model import DLModel
from features import get_sequence

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send(msg):
    requests.post(
        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
        data={"chat_id": CHAT_ID, "text": msg}
    )

model = DLModel()

def analyze():
    seq = get_sequence()
    prob = model.predict(seq)

    if prob > 0.75:
        signal = "UP 📈" if sum(seq) > 0 else "DOWN 📉"

        return signal, prob

    return None, prob

while True:
    result = analyze()

    if result:
        signal, prob = result

        send(f"""
🤖 DEEP LEARNING SIGNAL

Signal: {signal}
Confidence: {round(prob*100,2)}%

🧠 Pattern detected from last 10 candles

⚠️ High-quality setup only
""")

    time.sleep(60)