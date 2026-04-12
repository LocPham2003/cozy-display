from apps.googlecalendar.utils import get_week_range
from .helper import get_calendar_service
from ..dto.EventDto import EventDto, EventObj


def get_weekly_event_list(credentials_dict, calendar_ids) -> EventObj:
    service = get_calendar_service(credentials_dict)
    time_min, time_max = get_week_range()
    all_events_list = []
    for calendar_id in calendar_ids:
        event_list = (
            service.events()
            .list(
                calendarId=calendar_id,
                timeMin=time_min,
                timeMax=time_max,
                singleEvents=True,
            )
            .execute()
        )
        all_events_list.append(event_list)

    event_dtos = __create_event_dtos(all_events_list)
    return {"events": event_dtos}


def __create_event_dtos(event_lists) -> list[EventDto]:
    event_dtos = []
    for event_list in event_lists:
        for event in event_list["items"]:
            event_display_name = event.get("organizer").get("displayName")
            event_start_time = event.get("start").get("dateTime")
            event_end_time = event.get("end").get("dateTime")
            event_dto = EventDto(
                etag=event.get("etag"),
                event_id=event.get("id"),
                summary=event.get("summary"),
                location=event.get("location"),
                display_name=event_display_name,
                start_time=event_start_time,
                end_time=event_end_time,
            )
            event_dtos.append(event_dto.__dict__)

    event_dtos.sort(key=lambda e: e["start_time"] or "")
    return event_dtos
