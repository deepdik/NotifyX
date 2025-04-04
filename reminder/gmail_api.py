from googleapiclient.discovery import build
from google.oauth2 import service_account
from django.conf import settings


SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
SERVICE_ACCOUNT_FILE = settings.GMAIL_CREDENTIALS_FILE  # Path to JSON credentials


def get_gmail_service():
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    return build('gmail', 'v1', credentials=creds)


def check_reply_received(thread_id):
    service = get_gmail_service()
    results = service.users().messages().list(userId='me', q=f'threadId:{thread_id}').execute()
    messages = results.get('messages', [])
    return len(messages) > 1  # If more than one message exists in the thread, reply was received
