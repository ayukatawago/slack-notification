import json
from flask import request, make_response
import config
from flaskr import app
from slackutil.slackbot import SlackBot
from trelloutil.trellowrapper import TrelloWrapper


@app.route("/")
def show_entries():
    message = 'Hello, World!'
    return message


@app.route("/slack/json_html", methods=["POST"])
def json_html():
    slack_client = SlackBot(config.slack_api_token)
    trello_client = TrelloWrapper(config.trello_api_key, config.trello_token)

    # Parse the request payload
    form_json = json.loads(request.form["payload"])

    print(json.dumps(form_json))
    card_id = form_json["actions"][0]["value"]
    channel_id = form_json["channel"]["id"]
    trello_client.complete_card(card_id)

    message = "complete card_id:" + card_id
    slack_client.post_message(channel_id, message)

    return make_response("", 200)
