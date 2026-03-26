from datetime import date, datetime, timedelta, timezone


def get_week_range(d: date = None):
    """Return the (start, end) of the week containing the given date as RFC3339 timestamps.

    Defaults to today. Week runs Monday (00:00:00Z) to Sunday (23:59:59Z).
    """
    if d is None:
        d = date.today()
    start = d - timedelta(days=d.weekday())  # Monday
    end = start + timedelta(days=6)  # Sunday

    start_dt = datetime(
        start.year, start.month, start.day, 0, 0, 0, tzinfo=timezone.utc
    )
    end_dt = datetime(end.year, end.month, end.day, 23, 59, 59, tzinfo=timezone.utc)

    return start_dt.isoformat().replace("+00:00", "Z"), end_dt.isoformat().replace(
        "+00:00", "Z"
    )
