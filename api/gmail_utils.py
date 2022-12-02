import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import pandas as pd

class GmailUtils:

    def __init__(self, gid):
        self.gid = gid
        self.scopes = ["https://mail.google.com/"]
        self.creds_storage = "/tmp/"
        self.service = self.getGmailService()
        self.emails = pd.DataFrame(columns=["message_id", "sender_name", "sender_domain"])
    
    def getGmailService(self):
        creds = None
        creds_token = self.creds_storage + self.gid + ".json"
        creds_file = self.creds_storage + "credentials.json"
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

    def getDomain(self,s):
        angle = s.split('<')
        rate = angle[1].split('@')
        domain = rate[1].split('.')
        return domain[0]

    def getEmails(self):
        current_email = pd.DataFrame(columns=["message_id", "sender_name", "sender_domain"])
        results = self.service.users().messages().list(userId="me").execute()
        messages = results.get("messages")
        domainDic = {}
        for message in messages:
            message_id = message["id"]
            sender_domain = None
            message_data = self.service.users().messages().get(userId="me", id=message_id).execute()
            for header in message_data["payload"]["headers"]:
                if header["name"] == "From":
                    sender = header["value"].rsplit(" ", 1)
                    if(len(sender) == 2):
                        sender_name = sender[0]
                        #print(sender)
                        #print(len(sender))
                        sender_domain = self.getDomain(sender[-1])
                        #print(sender_domain)
                        # row = pd.Series({"message_id": message_id, "sender_name": sender_name, "sender_domain": sender_domain})
                        # current_email = pd.concat([current_email, row.to_frame().T], ignore_index=True)
                        print(sender_name)
                        if(sender_domain.capitalize() in domainDic):
                            domainDic[sender_domain.capitalize()]+=1
                        else:
                            domainDic[sender_domain.capitalize()]=1
                        # sender_name = sender[0]
                        # sender_domain = sender[1][1:-1]
                    break
            
            
        self.emails = current_email
        #return self.emails
        return domainDic
