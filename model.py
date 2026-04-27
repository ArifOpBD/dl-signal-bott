def ai_filter(signal):

    risk = signal["risk"]

    # filter bad signals
    if risk > 75:
        return False

    return True