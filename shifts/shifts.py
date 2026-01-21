from datetime import datetime, timedelta


def get_current_working_shift():
    anchor_date = datetime(2026, 1, 1).date()

    now = datetime.utcnow()
    current_time = now.time()
    current_date = now.date()

    if current_time < datetime.strptime("04:30", "%H:%M").time():
        target_date = current_date - timedelta(days=1)
        period = "Ночь"
    elif current_time < datetime.strptime("11:30", "%H:%M").time():
        target_date = current_date
        period = "Утро"
    elif current_time < datetime.strptime("18:30", "%H:%M").time():
        target_date = current_date
        period = "День"
    else:
        target_date = current_date
        period = "Ночь"

    days_passed = (target_date - anchor_date).days
    cycle_day = days_passed % 5

    if period == "Утро":
        shift_number = (1 - cycle_day) % 5
    elif period == "День":
        shift_number = (2 - cycle_day) % 5
    else:
        shift_number = (3 - cycle_day) % 5

    return [int(shift_number), period, current_date.strftime("%d.%m.%y")]
