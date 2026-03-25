import json
from django.shortcuts import redirect
from django.http import JsonResponse, HttpResponseRedirect

from apps.googlecalendar.constants import my_event_groups
from apps.googlecalendar.helpers.calendar_helper import get_user_calendar_list
from apps.googlecalendar.helpers.event_helper import get_weekly_event_list
from apps.googlecalendar.helpers.authentication_helper import get_flow

REDIRECT_URI = "http://127.0.0.1:8000/calendar/oauth/callback/"


def google_login(request):
    """Redirect the user to Google's OAuth consent screen."""
    flow = get_flow(REDIRECT_URI)
    authorization_url, state = flow.authorization_url(
        access_type="offline",  # gets a refresh token
        include_granted_scopes="true",
    )
    # Save state in session to verify later
    request.session["oauth_state"] = state
    return redirect(authorization_url)


def google_callback(request):
    """Handle the OAuth callback and save credentials to session."""
    flow = get_flow(REDIRECT_URI)
    flow.fetch_token(authorization_response=request.build_absolute_uri())

    credentials = flow.credentials
    # Save credentials to session
    request.session["credentials"] = {
        "token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "token_uri": credentials.token_uri,
        "client_id": credentials.client_id,
        "client_secret": credentials.client_secret,
        "scopes": credentials.scopes,
    }
    return redirect("calendar_list")


def calendar_list(request) -> JsonResponse | HttpResponseRedirect:
    """Fetch and return the user's calendar list."""
    # Check if user is authenticated
    if "credentials" not in request.session:
        return redirect("google_login")

    credentials = request.session["credentials"]
    calendars = get_user_calendar_list(credentials)
    filtered_calendars = []
    for calendar in calendars.get("items", []):
        if calendar.get("summary") in my_event_groups:
            filtered_calendars.append(calendar)
    return JsonResponse({"calendars": filtered_calendars})


def event_list(request):
    """Fetch and return the user's calendar list."""
    # Check if user is authenticated
    if "credentials" not in request.session:
        return redirect("google_login")

    credentials = request.session["credentials"]

    filtered_calendars = json.loads(calendar_list(request).getvalue())
    calendar_ids = []

    for calendar in filtered_calendars.get("calendars", []):
        calendar_ids.append(calendar.get("id"))

    events = get_weekly_event_list(credentials, calendar_ids)
    return JsonResponse(events)
