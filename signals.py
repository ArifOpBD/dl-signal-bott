import random

PAIRS = ["EUR/USD","GBP/USD","USD/JPY","AUD/USD","USD/CAD"]

def get_signal():
    return {
        "pair": random.choice(PAIRS),
        "direction": random.choice(["BUY 📈", "SELL 📉"]),
        "risk": random.randint(20, 75)
    }