import os
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from config import settings

__all__ = [
    "get_gmail_service",
]


def get_gmail_service():
    creds = None
    if os.path.exists(settings.TOKEN_FILE_PATH):
        creds = Credentials.from_authorized_user_file(settings.TOKEN_FILE_PATH, settings.SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            client_config = {"installed": {
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": ["http://localhost"],
            }}
            flow = InstalledAppFlow.from_client_config(client_config, settings.SCOPES)
            creds = flow.run_local_server(port=0)
        with open(settings.TOKEN_FILE_PATH, "w") as f:
            f.write(creds.to_json())
    return build("gmail", "v1", credentials=creds)