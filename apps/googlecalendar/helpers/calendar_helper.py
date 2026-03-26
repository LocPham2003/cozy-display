from .helper import get_calendar_service


def get_user_calendar_list(credentials_dict):
    """Fetch the list of calendars for the authenticated user."""
    service = get_calendar_service(credentials_dict)
    calendar_list = service.calendarList().list().execute()
    return calendar_list
