import os
import base64
import re
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from bs4 import BeautifulSoup

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
APPLICATION_NAME = 'Gmail API Python Extract From Email'
CREDENTIAL_FILE_NAME = ''  # Update this to your actual file path
CLIENT_SECRET_FILE = ''  # This should be where you store the OAuth credentials
QUERY_TERM = 'from:support@mittarv.com subject:"support"'


def get_oauth_credentials():
    creds = None
    if os.path.exists(CREDENTIAL_FILE_NAME):
        creds = Credentials.from_authorized_user_file(CREDENTIAL_FILE_NAME, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(CREDENTIAL_FILE_NAME, 'w') as token:
            token.write(creds.to_json())
    return creds

def list_messages_matching_query(service, user_id, query=''):
    try:
        response = service.users().messages().list(userId=user_id, q=query).execute()
        messages = []
        if 'messages' in response:
            messages.extend(response['messages'])

        while 'nextPageToken' in response:
            page_token = response['nextPageToken']
            response = service.users().messages().list(userId=user_id, q=query, pageToken=page_token).execute()
            messages.extend(response['messages'])

        return messages
    except HttpError as error:
        print(f'An error occurred: {error}')

def get_message(service, user_id, msg_id):
    try:
        message = service.users().messages().get(userId=user_id, id=msg_id).execute()
        return message
    except HttpError as error:
        print(f'An error occurred: {error}')

def is_useful(headers):
    for header in headers:
        if header['name'] == 'From' and header['value'].strip() == 'support@mittarv.com':
            return True
    return False

def get_code(msg):
    parts = msg['payload'].get('parts', [])
    for part in parts:
        data = part.get('body', {}).get('data')
        if data:
            decoded_bodydata = base64.urlsafe_b64decode(data)
            soup = BeautifulSoup(decoded_bodydata, features="html.parser")
            otp_match = re.search(r'The sign-in OTP for Mitt Arv is\s*(\d{6})', soup.get_text())
            if otp_match:
                return otp_match.group(1)
    return None

def main():
    creds = get_oauth_credentials()
    service = build('gmail', 'v1', credentials=creds)
    messages = list_messages_matching_query(service, "me", query=QUERY_TERM)
    if messages:
        msg = get_message(service, "me", 'messages',[])
        headers = msg['payload']['headers']
        if is_useful(headers):
            otp = get_code(msg)
            if otp:
                print(f"OTP: {otp}")
            else:
                print("OTP not found in the email.")
    else:
        print("No emails found with the specified query.")

if __name__ == '__main__':
    main()