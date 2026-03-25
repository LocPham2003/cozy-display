import logging
import os

from django.conf import settings
from google_auth_oauthlib.flow import Flow

SCOPES = ["https://www.googleapis.com/auth/calendar"]
CREDENTIALS_FILE = os.path.join(settings.BASE_DIR, "credentials.json")
logger = logging.getLogger(__name__)


def get_flow(redirect_uri):
    """Create the OAuth flow instance."""
    flow = Flow.from_client_secrets_file(
        CREDENTIALS_FILE, scopes=SCOPES, redirect_uri=redirect_uri
    )
    return flow
