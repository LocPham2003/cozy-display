from datetime import datetime
from typing import TypedDict, List


class EventDto:
    def __init__(
        self,
        etag: str,
        event_id: str,
        summary: str,
        location: str,
        display_name: str,
        start_time: datetime,
        end_time: datetime,
    ):
        self.etag = etag
        self.id = event_id
        self.summary = summary
        self.location = location
        self.display_name = display_name
        self.start_time = start_time
        self.end_time = end_time


class EventObj(TypedDict):
    events: List[EventDto]
