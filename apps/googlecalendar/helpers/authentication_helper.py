import logging

from django.conf import settings
from google_auth_oauthlib.flow import Flow

logger = logging.getLogger(__name__)


def get_flow(redirect_uri):
    """Create the OAuth flow instance."""
    flow = Flow.from_client_secrets_file(
        settings.GOOGLE_CREDENTIALS_PATH, scopes=settings.GOOGLE_SCOPES, redirect_uri=redirect_uri
    )
    return flow
