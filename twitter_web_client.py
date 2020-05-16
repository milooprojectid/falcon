from os import getenv
from flask import Flask, render_template, request
from tweepy import OAuthHandler, API
from dotenv import load_dotenv
from modules.db.mongodb import MongoDB

app = Flask(__name__)

load_dotenv()

consumer_key = getenv('TW_CONSUMER_KEY')
consumer_secret = getenv('TW_CONSUMER_SECRET')

auth = OAuthHandler(consumer_key,
                    consumer_secret)


@app.route("/login")
def login():
    login_url = auth.get_authorization_url()

    return render_template("login.html", data=login_url)


@app.route("/callback")
def callback():
    verifier = request.args.get('oauth_verifier')

    token = auth.get_access_token(verifier)
    access_token = token[0]
    access_secret = token[1]

    data = {'consumer_key': consumer_key, 'consumer_secret': consumer_secret,
            'access_token': access_token, 'access_secret': access_secret}

    DB_NAME = getenv('DB_NAME')
    db = MongoDB()
    if db.connect_db(DB_NAME):
        db.select_col("environment")
        db.find_and_modify(data)
    else:
        db.insert_first_data(data)

    return f"{consumer_key}, {consumer_secret}\n{access_token}, {access_secret}"


if __name__ == "__main__":
    app.run(debug=True)
