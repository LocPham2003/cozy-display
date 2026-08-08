from django.urls import path
from apps.spotify.views import views

urlpatterns = [
    path("", views.index, name="spotify-index"),
    path("login/", views.login, name="spotify-login"),
    path("callback/", views.callback, name="spotify-callback"),
    path("home/", views.home, name="spotify-home"),
    path("curr_playback/", views.curr_playback, name="curr_playback"),
    path("cached_playback/", views.cached_playback, name="cached_playback"),
    path("progress/", views.track_progress_stream, name="progress"),
]
