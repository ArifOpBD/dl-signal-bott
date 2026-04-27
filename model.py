def ai_filter(signal):

    if signal["risk"] > 80:
        return False

    return True