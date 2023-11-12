from flask import Flask, redirect, url_for, render_template
from flask_discord import DiscordOAuth2Session, requires_authorization, Unauthorized
import json
import os


with open('config.json') as config_file:
    config_data = json.load(config_file)
    

app = Flask(__name__)

app.secret_key = b"random bytes representing flask secret key"

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "true"
app.config["DISCORD_CLIENT_ID"] = config_data['discord_client_id']
app.config["DISCORD_CLIENT_SECRET"] = config_data['discord_client_secret']
app.config["DISCORD_REDIRECT_URI"] = config_data['discord_redirect_url']
app.config["DISCORD_BOT_TOKEN"] = config_data['discord_bot_token']


    
discord = DiscordOAuth2Session(app)


@app.route("/login/")
def login():
    return discord.create_session()


@app.route("/callback")
def callback():
    discord.callback()
    user = discord.fetch_user()
    return redirect(url_for(".me"))


@app.errorhandler(Unauthorized)
def redirect_unauthorized(e):
    return redirect(url_for("login"))


@app.route("/me/")
@requires_authorization
def me():
    return render_template('me.html', user=discord.fetch_user())


if __name__ == "__main__":
    app.run(debug=True)