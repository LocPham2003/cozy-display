import os

from django.http import JsonResponse
from django.shortcuts import render, redirect
from dotenv import load_dotenv
import base64
import requests
import uuid
from urllib.parse import urlencode
from apps.spotify.constants import scope

redirect_uri = os.environ["SPOTIFY_REDIRECT_URI"]
client_id = os.environ["SPOTIFY_CLIENT_ID"]

load_dotenv()


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
    url = "https://accounts.spotify.com/authorize?" + urlencode(params)
    return redirect(url)


def callback(request):
    code = request.GET.get("code")
    state = request.GET.get("state")

    if state is None:
        return redirect("/")

    client_secret = os.environ["SPOTIFY_CLIENT_SECRET"]

    credentials = base64.b64encode(f"{client_id}:{client_secret}".encode()).decode()

    response = requests.post(
        "https://accounts.spotify.com/api/token",
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
    print(request.session["spotify_credentials"])
    return redirect("top_tracks")


def top_tracks(request):
    if "spotify_credentials" not in request.session:
        return redirect("spotify-login")

    access_token = request.session["spotify_credentials"]
    url = "https://api.spotify.com/v1/me/top/artists"

    response = requests.get(
        url,
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )

    print(response.json())

    return JsonResponse({"top_tracks": []})
