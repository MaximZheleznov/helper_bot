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
    print(days_passed)
    cycle_day = days_passed % 5
    print(cycle_day)
    shift_numbers = [5, 4, 3, 2, 1]

    if period == "Утро":
        shift_number = shift_numbers[cycle_day % 5 - 1]
    elif period == "День":
        shift_number = shift_numbers[cycle_day % 5 - 2]
    else:
        shift_number = shift_numbers[cycle_day % 5 - 3]

    return [int(shift_number), period, current_date.strftime("%d.%m.%y")]
