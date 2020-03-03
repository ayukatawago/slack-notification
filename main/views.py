import json
import config
from flask import Flask, request, make_response
from bot.slackbot import SlackBot

app = Flask(__name__)


@app.route('/')
def show_entries():
    message = 'Hello, World!'
    return message


@app.route("/slack/json_html", methods=["POST"])
def json_html():
    slack_client = SlackBot(config.slack_api_token)

    # Parse the request payload
    form_json = json.loads(request.form["payload"])

    val = form_json["actions"][0]["value"]

    message = "complete card_id:" + val
    response = slack_client.post_message("#todo", message)

    return make_response("", 200)
