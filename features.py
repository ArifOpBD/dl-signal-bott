def handle_menu(chat_id, text):

    if text == "📊 Auto Signal":
        return "📊 Auto Signal Active..."

    elif text == "💰 Money Management":
        return """
💰 MONEY MANAGEMENT

Risk:
• Low = 1%
• Medium = 2%
• High = 3%
"""

    elif text == "👨‍💻 Admin Contact":
        return "👨‍💻 Admin: @qxabir"

    elif text == "📈 Live Result":
        return "📈 Live system running..."

    return None