from typing import TypedDict


class TrackProgressData(TypedDict):
    progress_ms: int
    progress: float
    track_id: str


class TrackProgress(TypedDict):
    track_progress: TrackProgressData
