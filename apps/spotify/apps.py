from django.apps import AppConfig
from django.core.cache import cache

from apps.spotify.constants import curr_playback_key


class SpotifyConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.spotify"

    def ready(self):
        cache.set(curr_playback_key, {})
