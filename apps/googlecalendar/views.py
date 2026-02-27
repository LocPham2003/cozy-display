import json
from django.shortcuts import redirect
from django.http import JsonResponse
from django.conf import settings
from .helper import get_flow, get_calendar_list

REDIRECT_URI = 'http://127.0.0.1:8000/calendar/oauth/callback/'


def google_login(request):
    """Redirect the user to Google's OAuth consent screen."""
    flow = get_flow(REDIRECT_URI)
    authorization_url, state = flow.authorization_url(
        access_type='offline',   # gets a refresh token
        include_granted_scopes='true'
    )
    # Save state in session to verify later
    request.session['oauth_state'] = state
    return redirect(authorization_url)


def google_callback(request):
    """Handle the OAuth callback and save credentials to session."""
    flow = get_flow(REDIRECT_URI)
    flow.fetch_token(authorization_response=request.build_absolute_uri())

    credentials = flow.credentials
    # Save credentials to session
    request.session['credentials'] = {
        'token': credentials.token,
        'refresh_token': credentials.refresh_token,
        'token_uri': credentials.token_uri,
        'client_id': credentials.client_id,
        'client_secret': credentials.client_secret,
        'scopes': credentials.scopes
    }
    return redirect('calendar_list')


def calendar_list(request):
    """Fetch and return the user's calendar list."""
    # Check if user is authenticated
    if 'credentials' not in request.session:
        return redirect('google_login')

    credentials = request.session['credentials']
    calendars = get_calendar_list(credentials)
    return JsonResponse(calendars)