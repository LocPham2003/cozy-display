import base64
import json
import os
import time
import uuid
from urllib.parse import urlencode

import requests
from django.core.cache import cache
from django.http import JsonResponse, StreamingHttpResponse
from django.shortcuts import render, redirect
from dotenv import load_dotenv

from apps.spotify.constants import scope, authorize_url, token_url, curr_playback_key
from apps.spotify.helpers.playback_helper import get_playback, get_stream_data

load_dotenv()

redirect_uri = os.environ["SPOTIFY_REDIRECT_URI"]
client_id = os.environ["SPOTIFY_CLIENT_ID"]
client_secret = os.environ["SPOTIFY_CLIENT_SECRET"]


def index(request):
    return render(request, "spotify/index.html")


def login(request):
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

    access_token = request.session["spotify_credentials"]
    playback_data = get_playback(access_token)
    if "error" not in playback_data:
        cache.set(curr_playback_key, playback_data)
    return JsonResponse({"curr_playback_data": playback_data})


def cached_playback(request):
    return JsonResponse({"curr_playback_data": cache.get(curr_playback_key)})


def track_progress_stream(request):
    if "spotify_credentials" not in request.session:
        return redirect("spotify-login")

    def stream():
        while True:
            access_token = request.session["spotify_credentials"]
            stream_data = get_stream_data(access_token)
            yield json.dumps(stream_data) + "\n"
            time.sleep(1)

    return StreamingHttpResponse(stream())
