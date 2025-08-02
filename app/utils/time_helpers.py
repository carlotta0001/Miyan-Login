from datetime import datetime, timedelta

def calculate_expiry_date(count_str, type_str):
    try:
        count = int(count_str)
    except ValueError:
        return None

    now = datetime.utcnow()
    unit = type_str.lower()

    if unit in ["minute", "minutes"]:
        return now + timedelta(minutes=count)
    elif unit in ["hour", "hours"]:
        return now + timedelta(hours=count)
    elif unit in ["day", "days"]:
        return now + timedelta(days=count)
    elif unit in ["week", "weeks"]:
        return now + timedelta(weeks=count)
    else:
        return None