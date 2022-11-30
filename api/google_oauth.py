import os
from dotenv import load_dotenv
from oauthlib.oauth2 import WebApplicationClient
import requests
import json

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os.path
import base64
import email
from bs4 import BeautifulSoup

load_dotenv()
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

class GoogleOAuth:

    domainDict = {}

    def __init__(self):
        self.GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
        self.GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
        self.GOOGLE_DISCOVERY_URL = ("https://accounts.google.com/.well-known/openid-configuration")
        self.client = WebApplicationClient(self.GOOGLE_CLIENT_ID)
    
    def getOAuthClient(self):
        return self.client
    
    def getGoogleOAuthConfig(self):
        return requests.get(self.GOOGLE_DISCOVERY_URL).json()
    
    def login(self, base_url):
        google_provider_cfg = self.getGoogleOAuthConfig()
        authorization_endpoint = google_provider_cfg["authorization_endpoint"]
        request_uri = self.client.prepare_request_uri(
            authorization_endpoint,
            redirect_uri=base_url + "/callback",
            scope=["openid", "email", "profile"],
        )
        return request_uri
    
    def loginCallback(self, url, base_url, code):
        google_provider_cfg = self.getGoogleOAuthConfig()
        token_endpoint = google_provider_cfg["token_endpoint"]
        token_url, headers, body = self.client.prepare_token_request(
            token_endpoint,
            authorization_response=url,
            redirect_url=base_url,
            code=code
        )
        token_response = requests.post(
            token_url,
            headers=headers,
            data=body,
            auth=(self.GOOGLE_CLIENT_ID, self.GOOGLE_CLIENT_SECRET),
        )
        self.client.parse_request_body_response(json.dumps(token_response.json()))
        userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
        uri, headers, body = self.client.add_token(userinfo_endpoint)
        userinfo_response = requests.get(uri, headers=headers, data=body)
        if userinfo_response.json().get("email_verified"):
            unique_id = userinfo_response.json()["sub"]
            user_name = userinfo_response.json()["given_name"]
            user_email = userinfo_response.json()["email"]
            user_picture = userinfo_response.json()["picture"]
        else:
            return False, (None)
        return True, (unique_id, user_name, user_email, user_picture)

    def addToDictionary(self, s):
        angle = s.split('<')
        rate = angle[1].split('@')
        domain = rate[1].split('.')
        domainName = domain[0]
        if(domainName in self.domainDict):
            self.domainDict[domainName]+=1
        else:
            self.domainDict[domainName]=1

    def getDomainList(self):
        creds = None
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('/Users/indrasaikiranvalluru/Desktop/OrganizeGmail/api/credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)

        service = build('gmail', 'v1', credentials=creds)

        result = service.users().messages().list(userId='me').execute()

        result = service.users().messages().list(maxResults=200, userId='me').execute()
        messages = result.get('messages')
        print(type(messages))

        for msg in messages:
            txt = service.users().messages().get(userId='me', id=msg['id']).execute()
            try:
                payload = txt['payload']
                headers = payload['headers']

                for d in headers:
                    if d['name'] == 'Subject':
                        subject = d['value']
                    if d['name'] == 'From':
                        sender = d['value']

                parts = payload.get('parts')[0]
                data = parts['body']['data']
                data = data.replace("-","+").replace("_","/")
                decoded_data = base64.b64decode(data)

                soup = BeautifulSoup(decoded_data , "lxml")
                body = soup.body()
                self.addToDictionary(sender)

                print("From: ", sender)

                print('\n')
            
            except :

                pass
        return self.domainDict