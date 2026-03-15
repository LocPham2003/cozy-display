import os
import json
import logging
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from django.conf import settings

SCOPES = ['https://www.googleapis.com/auth/calendar']
CREDENTIALS_FILE = os.path.join(settings.BASE_DIR, 'credentials.json')
logger = logging.getLogger(__name__)                   

def get_flow(redirect_uri):
    """Create the OAuth flow instance."""
    flow = Flow.from_client_secrets_file(
        CREDENTIALS_FILE,
        scopes=SCOPES,
        redirect_uri=redirect_uri
    )
    return flow


def get_calendar_service(credentials_dict):
    """Build and return a Google Calendar service instance."""
    credentials = Credentials(
        token=credentials_dict['token'],
        refresh_token=credentials_dict['refresh_token'],
        token_uri=credentials_dict['token_uri'],
        client_id=credentials_dict['client_id'],
        client_secret=credentials_dict['client_secret'],
        scopes=credentials_dict['scopes']
    )
    service = build('calendar', 'v3', credentials=credentials)
    return service


def get_calendar_list(credentials_dict):
    """Fetch the list of calendars for the authenticated user."""
    service = get_calendar_service(credentials_dict)
    calendar_list = service.calendarList().list().execute()
    return calendar_list