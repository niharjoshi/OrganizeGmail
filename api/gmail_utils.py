import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pandas as pd
import requests
import shutil
import json

class GmailUtils:

    def __init__(self, gid):
        self.gid = gid
        self.scopes = ["https://mail.google.com/"]
        self.creds_storage = "/tmp/"
        self.service = self.getGmailService()
        self.emails = pd.DataFrame(columns=["message_id", "sender_domain"])
    
    def getGmailService(self):
        creds = None
        creds_token = self.creds_storage + self.gid + ".json"
        creds_file = self.creds_storage + "credentials.json"
        shutil.copyfile("credentials/credentials.json", creds_file)
        if os.path.exists(creds_token):
            creds = Credentials.from_authorized_user_file(creds_token, self.scopes)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(creds_file, self.scopes)
                creds = flow.run_local_server(port=0)
            with open(creds_token, "w") as token:
                token.write(creds.to_json())
        try:
            service = build("gmail", "v1", credentials=creds)
            return service
        except HttpError as error:
            print(f"An error occurred while trying to access the Gmail API: {error}")

    def getEmails(self):
        current_email = pd.DataFrame(columns=["message_id", "sender_domain"])
        results = self.service.users().messages().list(userId="me").execute()
        messages = results.get("messages")
        for message in messages:
            message_id = message["id"]
            sender_domain = None
            message_data = self.service.users().messages().get(userId="me", id=message_id).execute()
            for header in message_data["payload"]["headers"]:
                if header["name"] == "From":
                    sender = header["value"].rsplit(" ", 1)
                    sender_domain = sender[-1][1:-1]
                    row = pd.Series({"message_id": message_id, "sender_domain": sender_domain})
                    current_email = pd.concat([current_email, row.to_frame().T], ignore_index=True)
                    break
        self.emails = current_email
        return self.emails["sender_domain"].value_counts().to_dict()

    def deleteEmails(self, sender_domain, date_range=None):
        if not date_range:
            print(sender_domain)
            mail_ids_to_delete = self.emails.loc[self.emails["sender_domain"] == sender_domain]
            mail_ids_to_delete = mail_ids_to_delete["message_id"].to_list()
            print(mail_ids_to_delete)
            for mail_id in mail_ids_to_delete:
                self.service.users().messages().delete(userId="me", id=mail_id).execute()
            self.getEmails()
