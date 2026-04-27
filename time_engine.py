from datetime import datetime, timedelta

def execution_time():
    return datetime.utcnow() + timedelta(minutes=2)

def countdown(target):

    now = datetime.utcnow()
    sec = int((target - now).total_seconds())

    if sec < 0:
        return "00:00"

    return f"{sec//60:02d}:{sec%60:02d}"