from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

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


