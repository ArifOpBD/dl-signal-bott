import random

PAIRS = ["EUR/USD OTC", "GBP/USD OTC", "USD/JPY OTC", "AUD/USD OTC", "USD/CAD OTC",
        "USD/CHF OTC", "NZD/USD OTC", "EUR/GBP OTC", "EUR/JPY OTC", "GBP/JPY OTC",
        "AUD/JPY OTC", "CAD/JPY OTC", "CHF/JPY OTC", "NZD/JPY OTC",
        "EUR/AUD OTC", "EUR/CAD OTC", "GBP/AUD OTC", "GBP/CAD OTC",
        "BTC/USD OTC", "ETH/USD OTC", "XAU/USD OTC", "NAS100 OTC",
        "SPX500 OTC", "UK100 OTC", "GER30 OTC""]

def get_signal():
    return {
        "pair": random.choice(PAIRS),
        "direction": random.choice(["BUY 📈", "SELL 📉"]),
        "risk": random.randint(20, 75)
    }