import os
from dotenv import load_dotenv
from oauthlib.oauth2 import WebApplicationClient
import requests
import json

load_dotenv()

class GoogleOAuth:

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
