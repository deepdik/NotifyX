from google.auth.transport.requests import Request
from django.conf import settings
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import pickle
import os


SERVICE_ACCOUNT_FILE = str(settings.BASE_DIR) + settings.GMAIL_CREDENTIALS_FILE  # Path to JSON credentials
print(SERVICE_ACCOUNT_FILE)
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
REDIRECT_URI = 'http://localhost:8010/'  # This must match Google Console

def get_gmail_service():
    creds = None
    if os.path.exists(settings.GMAIL_TOKEN_FILE):
        with open(settings.GMAIL_TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                SERVICE_ACCOUNT_FILE,
                SCOPES,
                redirect_uri=REDIRECT_URI
            )
            # flow.run_console()
            creds = flow.run_local_server(port=8000)

        with open(settings.GMAIL_TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)

    return build('gmail', 'v1', credentials=creds)


def get_thread_id_from_custom_message_id(service, custom_message_id):
    query = f"rfc822msgid:{custom_message_id}"
    results = service.users().messages().list(userId='me', q=query).execute()
    messages = results.get('messages', [])
    if not messages:
        return None  # Not found

    message = service.users().messages().get(userId='me', id=messages[0]['id']).execute()
    return message.get('threadId')

def check_reply_received(mess_id, sender_email):
    service = get_gmail_service()
    thread_id = get_thread_id_from_custom_message_id(service, mess_id)

    try:
        # Get all messages in the thread
        thread = service.users().threads().get(userId='me', id=thread_id, format='metadata').execute()
        messages = thread.get('messages', [])

        for msg in messages:
            headers = msg.get('payload', {}).get('headers', [])
            from_header = next((h['value'] for h in headers if h['name'].lower() == 'from'), None)

            # Check if the 'From' address is NOT yours
            if from_header and sender_email.lower() not in from_header.lower():
                return True  # Reply from someone else
    except Exception as e:
        print(f"[GMAIL API ERROR] Failed to check reply: {e}")

    return False

# check_reply_received("", "")