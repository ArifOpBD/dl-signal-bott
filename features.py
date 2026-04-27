import random

def get_sequence():
    # simulate last 10 candles movement
    return [random.uniform(-1, 1) for _ in range(10)]