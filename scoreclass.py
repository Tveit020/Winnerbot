import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from email.message import EmailMessage
import base64
import mimetypes


class Scoreclass:
    def __init__(self):
        self.iterative_num = 7
        self.base_url = "https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard?dates="

        self.df_path = "wintracker.csv"
        self.df = []
        # self.email_add = {
        #     "Brandon": "Tveit020@gmail.com",
        #     "Dan": "hoydan@ymail.com",
        #     "Austin": "Keller.Austin@gmail.com",
        #     "Ingvild": "Ingvild.Smelvaer@gmail.com",
        # }
        self.email_add = {
            "Brandon": "definitelynotspam1776@gmail.com",
            "Dan": None,
            "Austin": None,
            "Ingvild": None,
        }
        self.week_num = 2
        self.SCOPES = [
            "https://www.googleapis.com/auth/gmail.readonly",
            "https://www.googleapis.com/auth/gmail.compose",
        ]
        # self.creds = self.email_sign_in()
        self.winner = None

    def email_sign_in(self):

        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        creds = None
        SCOPES = [
            "https://www.googleapis.com/auth/gmail.readonly",
            "https://www.googleapis.com/auth/gmail.compose",
        ]
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

    def add_attachment(self, mime_message, attachment_filename):
        type_subtype, _ = mimetypes.guess_type(attachment_filename)
        maintype, subtype = type_subtype.split("/")

        with open(attachment_filename, "rb") as fp:
            attachment_data = fp.read()

        mime_message.add_attachment(attachment_data, maintype, subtype)

        return mime_message

    def send_score_email(self, email_to="definitelynotspam1776@gmail.com"):
        """Create and insert a draft email with attachment.
        Print the returned draft's message and id.
        Returns: Draft object, including draft id and message meta data.

        L
        """
        if email_to is None:
            return

        if self.creds is None:
            self.creds = self.email_sign_in()
        try:
            # create gmail api client
            service = build("gmail", "v1", credentials=self.creds)
            mime_message = EmailMessage()

            # headers
            mime_message["To"] = email_to
            mime_message["From"] = "definitelynotspam1776@gmail.com"
            mime_message["Subject"] = f"Team Draft Scoreboard: Week {self.week_num}"

            name = self.find_person(email_to)

            # text
            if self.winner != "Brandon":
                mime_message.set_content(
                    f"Dear {name},\n\nThis is ScoreBot, your (un)reliable scorekeeper for the draft team league!\nWinner for the week is {self.winner}!\nCurrent standings after week {self.week_num} are found below.\nAlso, included the actual scores as a .csv file.  This can be opened in excel.\n\nScorebot out!"
                )
            else:
                mime_message.set_content(
                    f"Dear {name},\n\nGuess whos number 1 mothafuckassssssss!\nCurrent standings after week {self.week_num} are found below."
                )

            # attachment

            # guessing the MIME type
            mime_message = self.add_attachment(
                mime_message,
                "C:\\Users\\NOTveitB\\Documents\\Python\\Personal\\Scrub Internet\\Standings.png",
            )
            mime_message = self.add_attachment(
                mime_message,
                "C:\\Users\\NOTveitB\\Documents\\Python\\Personal\\Scrub Internet\\scoretracker.csv",
            )

            encoded_message = base64.urlsafe_b64encode(mime_message.as_bytes()).decode()

            create_message = {"raw": encoded_message}
            # pylint: disable=E1101
            send_message = (
                service.users()
                .messages()
                .send(userId="me", body=create_message)
                .execute()
            )
            print(f"Message sent successfully!")

        except HttpError as error:
            print(f"An error occurred: {error}")
            send_message = None
        return send_message

    def find_person(self, email_add):
        add_list = list(self.email_add.values())
        name_list = list(self.email_add)

        return name_list[add_list.index(email_add)]


if __name__ == "__main__":
    scoreclass = Scoreclass()
    scoreclass.send_score_email(email_to="Tveit020@gmail.com")
