import requests

playback_url = "https://api.spotify.com/v1/me/player"


def get_playback(access_token):
    response = requests.get(
        playback_url,
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )

    if response.status_code == 200:
        playback_object = response.json()
        playback_item = playback_object.get("item")
        album = {
            "name": playback_item.get("album").get("name"),
            "cover": {
                "url": playback_item.get("album").get("images")[0].get("url"),
                "width": playback_item.get("album").get("images")[0].get("width"),
                "height": playback_item.get("album").get("images")[0].get("height"),
            },
        }
        repeat_state = playback_object.get("repeat_state")
        progress_ms = playback_object.get("progress_ms")
        duration_ms = playback_item.get("duration_ms")
        progress = progress_ms / duration_ms
        track_name = playback_item.get("name")
        track_id = playback_item.get("id")
        artists = []
        for artist_object in playback_item.get("artists"):
            artists.append(artist_object.get("name"))
        return {
            "currently_playing": {
                "repeat_state": repeat_state,
                "track_id": track_id,
                "track_name": track_name,
                "duration_ms": duration_ms,
                "progress_ms": progress_ms,
                "progress": progress,
                "album": album,
                "artist": artists,
            }
        }
    else:
        return {"currently_playing": None}


def get_stream_data(access_token):
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
        return {
            "currently_playing": {
                "progress_ms": progress_ms,
                "progress": progress,
                "track_id": track_id,
            },
        }
    elif response.status_code == 401:
        return {"error": "Token expired, please login again"}
    elif response.status_code == 204:
        return {"error": "Playback is currently unavailable. Play something on spotify!"}
