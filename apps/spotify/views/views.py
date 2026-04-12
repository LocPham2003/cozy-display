import json
import os
import time
from unittest import skip

from django.http import JsonResponse, StreamingHttpResponse
from django.core.cache import cache
from apps.spotify.helpers.playback_helper import get_playback, get_stream_data
from django.shortcuts import render, redirect
from dotenv import load_dotenv
import base64
import requests
import uuid
from urllib.parse import urlencode
from apps.spotify.constants import scope, curr_playback_key

redirect_uri = os.environ["SPOTIFY_REDIRECT_URI"]
client_id = os.environ["SPOTIFY_CLIENT_ID"]

load_dotenv()

authorize_url = "https://accounts.spotify.com/authorize?"
token_url = "https://accounts.spotify.com/api/token"

# Data-specific url
playback_url = "https://api.spotify.com/v1/me/player"
top_artists = "https://api.spotify.com/v1/me/top/artists"
curr_playing_url = "https://api.spotify.com/v1/me/player/currently-playing"


def index(request):
    return render(request, "spotify/index.html")


def login():
    state = str(uuid.uuid4())

    response_type = "code"

    params = {
        "client_id": client_id,
        "response_type": response_type,
        "scope": scope,
        "redirect_uri": redirect_uri,
        "state": state,
    }
    url = authorize_url + urlencode(params)
    return redirect(url)


def callback(request):
    code = request.GET.get("code")
    state = request.GET.get("state")

    if state is None:
        return redirect("/")

    client_secret = os.environ["SPOTIFY_CLIENT_SECRET"]

    credentials = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()

    response = requests.post(
        token_url,
        data={
            "code": code,
            "redirect_uri": redirect_uri,
            "grant_type": "authorization_code",
        },
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Basic {credentials}",
        },
    )

    request.session["spotify_credentials"] = response.json().get("access_token")
    return redirect("spotify-home")


def home(request):
    return render(request, "spotify/home.html")


def curr_playback(request):
    if "spotify_credentials" not in request.session:
        return redirect("spotify-login")

    return JsonResponse({"curr_playback_data": cache.get(curr_playback_key)})


def track_progress_stream(request):
    if "spotify_credentials" not in request.session:
        return redirect("spotify-login")

    def stream():
        while True:
            access_token = request.session["spotify_credentials"]
            stream_data = get_stream_data(access_token)

            if stream_data.get("currently_playing") is not None:
                if not cache.get(curr_playback_key):
                    cache.set(curr_playback_key, get_playback(access_token))

                curr_playback_data = cache.get(curr_playback_key)
                if curr_playback_data.get("track_id") != stream_data.get("track_id"):
                    cache.set(curr_playback_key, get_playback(access_token))

                yield json.dumps(stream_data) + "\n"
            else:
                yield (
                    json.dumps({"status": "No track is playing, start one on Spotify!"})
                    + "\n"
                )

            time.sleep(1)

    return StreamingHttpResponse(stream())
