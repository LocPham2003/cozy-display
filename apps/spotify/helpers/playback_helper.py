import requests

from apps.spotify.dto.playback_dto import (
    PlaybackResult,
    PlaybackError,
    Album,
    AlbumCover,
)
from apps.spotify.dto.playback_stream import TrackProgress, TrackProgressData

playback_url = "https://api.spotify.com/v1/me/player"


def get_playback(access_token) -> PlaybackResult | PlaybackError:
    response = requests.get(
        playback_url,
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )

    if response.status_code == 200:
        playback_object = response.json()
        playback_item = playback_object.get("item")

        album_cover = AlbumCover(
            url=playback_item.get("album").get("images")[0].get("url"),
            width=playback_item.get("album").get("images")[0].get("width"),
            height=playback_item.get("album").get("images")[0].get("height"),
        )

        album = Album(
            name=playback_item.get("album").get("name"),
            cover=album_cover,
        )

        artists = []
        for artist_object in playback_item.get("artists"):
            artists.append(artist_object.get("name"))

        playback_result = PlaybackResult(
            repeat_state=playback_object.get("repeat_state"),
            track_id=playback_item.get("id"),
            track_name=playback_item.get("name"),
            album=album,
            artist=artists,
        )

        return playback_result
    elif response.status_code == 401:
        error = PlaybackError(error="Token expired, please login again")
    elif response.status_code == 204:
        error = PlaybackError(
            error="Playback is currently unavailable. Play something on spotify!"
        )
    else:
        error = PlaybackError(error="Something went wrong, please try again")

    return error


def get_stream_data(access_token) -> TrackProgress | PlaybackError:
    response = requests.get(
        playback_url,
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )

    if response.status_code == 200:
        playback_object = response.json()
        playback_item = playback_object.get("item")
        duration_ms = playback_item.get("duration_ms")
        progress_ms = playback_object.get("progress_ms")
        progress = round(progress_ms / duration_ms, 2)
        track_id = playback_item.get("id")

        track_progress_data = TrackProgressData(
            progress_ms=progress_ms,
            progress=progress,
            track_id=track_id,
        )

        return TrackProgress(track_progress=track_progress_data)
    elif response.status_code == 401:
        error = PlaybackError(error="Token expired, please login again")
    elif response.status_code == 204:
        error = PlaybackError(
            error="Playback is currently unavailable. Play something on spotify!"
        )
    else:
        error = PlaybackError(error="Something went wrong, please try again")

    return error
