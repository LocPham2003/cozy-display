from django.urls import path
from apps.googlecalendar.views import views

urlpatterns = [
    path("login/", views.google_login, name="google_login"),
    path("oauth/callback/", views.google_callback, name="google_callback"),
    path("calendar_list/", views.calendar_list, name="calendar_list"),
    path("event_list/", views.event_list, name="event_list"),
]
