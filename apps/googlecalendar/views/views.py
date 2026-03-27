from django.shortcuts import redirect, render
from django.http import JsonResponse

from apps.googlecalendar.constants import REDIRECT_URI
from apps.googlecalendar.helpers.calendar_helper import get_user_calendar_list
from apps.googlecalendar.helpers.event_helper import get_weekly_event_list
from apps.googlecalendar.helpers.authentication_helper import get_flow


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


def calendar_list(request):
    """Render the user's calendar list as an HTML page."""
    if "credentials" not in request.session:
        return redirect("google_login")

    credentials = request.session["credentials"]
    calendars = get_user_calendar_list(credentials)
    return render(
        request, "googlecalendar/calendar_list.html", {"calendars": calendars["items"]}
    )


def event_list(request):
    """Fetch and return the user's event list."""
    if "credentials" not in request.session:
        return redirect("google_login")

    credentials = request.session["credentials"]
    calendar_ids = request.POST.getlist("calendar_ids")
    events = get_weekly_event_list(credentials, calendar_ids)
    return JsonResponse(events)
