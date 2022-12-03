import os
from flask import Flask, redirect, request, url_for, render_template, g
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from api.google_oauth import GoogleOAuth
from api.gmail_utils import GmailUtils
from api.user import User
import json

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
login_manager = LoginManager()
login_manager.init_app(app)

oauth = GoogleOAuth()

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route("/")
def index():
    if current_user.is_authenticated:
        gmail_utils = GmailUtils(current_user.gid)
        email_counts = gmail_utils.getEmails()
        dataToHTML = []
        dropDownList = []
        for element in email_counts:
            dataToHTML.append(
                {
                    "tag": element,
                    "num": email_counts[element]
                }
            )
            dropDownList.append(element)
        return render_template("dashboard.html", topTags=dataToHTML, dropdownlist=dropDownList, picture=current_user.picture)
    else:
        return render_template("login.html")

@app.route("/delete")
def delete():
    orgToDelete = request.args.get("orgs")
    gmail_utils = GmailUtils(current_user.gid)
    gmail_utils.getEmails()
    gmail_utils.deleteEmails(orgToDelete)
    return redirect(url_for("index"))

@app.route("/login")
def login():
    request_uri = oauth.login(request.base_url)
    return redirect(request_uri)

@app.route("/login/callback")
def callback():
    email_verified, user_details = oauth.loginCallback(request.url, request.base_url, request.args.get("code"))
    if not email_verified:
        return "User email not available or not verified by Google.", 400
    (unique_id, user_name, user_email, user_picture) = user_details
    user = User(gid=unique_id, name=user_name, email=user_email, picture=user_picture)
    if not User.get(unique_id):
        User.create(unique_id, user_name, user_email, user_picture)
    login_user(user)
    return redirect(url_for("index"))

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(ssl_context="adhoc", debug=True)