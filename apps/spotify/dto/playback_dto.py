from typing import TypedDict


class AlbumCover(TypedDict):
    url: str
    width: int
    height: int


class Album(TypedDict):
    name: str
    cover: AlbumCover


class PlaybackResult(TypedDict):
    repeat_state: str
    track_id: str
    track_name: str
    album: Album
    artist: list[str]


class PlaybackError(TypedDict):
    error: str
