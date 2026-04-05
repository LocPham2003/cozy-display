from django.urls import path
from apps.spotify.views import views

urlpatterns = [
    path("", views.index, name="spotify-index"),
    path("login/", views.login, name="spotify-login"),
    path("callback/", views.callback, name="spotify-callback"),
    path("top_tracks/", views.top_tracks, name="top_tracks"),
]
