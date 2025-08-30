import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from email.message import EmailMessage
import base64

import mimetypes

# If modifying these scopes, delete the file token.json.
SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.compose",
]


def sign_in():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(
        "C:\\Users\\NOTveitB\\Documents\\Python\\Personal\\Scrub Internet\\access_key\\token.json"
    ):
        creds = Credentials.from_authorized_user_file(
            "C:\\Users\\NOTveitB\\Documents\\Python\\Personal\\Scrub Internet\\access_key\\token.json",
            SCOPES,
        )
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "C:\\Users\\NOTveitB\\Documents\\Python\\Personal\\Scrub Internet\\access_key\\credentials.json",
                SCOPES,
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(
            "C:\\Users\\NOTveitB\\Documents\\Python\\Personal\\Scrub Internet\\access_key\\token.json",
            "w",
        ) as token:
            token.write(creds.to_json())

    return creds


def send_score_email(email_to, week_number=2, credits=None):
    """Create and insert a draft email with attachment.
    Print the returned draft's message and id.
    Returns: Draft object, including draft id and message meta data.

    L
    """
    if credits is None:
        credits = sign_in()
    try:
        # create gmail api client
        service = build("gmail", "v1", credentials=credits)
        mime_message = EmailMessage()

        # headers
        mime_message["To"] = email_to
        mime_message["From"] = "definitelynotspam1776"
        mime_message["Subject"] = f"Team Draft Scoreboard: Week {week_number}"

        # text
        mime_message.set_content(
            f"Current standings after week {week_number} are found below!"
        )

        # attachment
        attachment_filename = "C:\\Users\\NOTveitB\\Documents\\Python\\Personal\\Scrub Internet\\Standings.png"
        # guessing the MIME type
        type_subtype, _ = mimetypes.guess_type(attachment_filename)
        maintype, subtype = type_subtype.split("/")

        with open(attachment_filename, "rb") as fp:
            attachment_data = fp.read()
        mime_message.add_attachment(attachment_data, maintype, subtype)

        encoded_message = base64.urlsafe_b64encode(mime_message.as_bytes()).decode()

        create_message = {"raw": encoded_message}
        # pylint: disable=E1101
        send_message = (
            service.users().messages().send(userId="me", body=create_message).execute()
        )
        print(f"Message sent successfully!")

    except HttpError as error:
        print(f"An error occurred: {error}")
        send_message = None
    return send_message


if __name__ == "__main__":
    creds = send_score_email("definitelynotspam1776@gmail.com")
