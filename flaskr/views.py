import json
from flask import request, make_response
import config
from flaskr import app
from slackutil.slackwrapper import SlackApiWrapper
from trelloutil.trellowrapper import TrelloApiWrapper


@app.route("/")
def show_entries():
    message = 'Hello, World!'
    return message


@app.route("/slack/json_html", methods=["POST"])
def json_html():
    slack_client = SlackApiWrapper(config.slack_api_token)
    trello_client = TrelloApiWrapper(config.trello_api_key, config.trello_token)

    # Parse the request payload
    form_json = json.loads(request.form["payload"])
    print(json.dumps(form_json))

    # complete task on Trello
    card_id = form_json["actions"][0]["value"]
    trello_client.complete_card(card_id)

    # update message on Slack
    channel_id = form_json["channel"]["id"]
    timestamp = form_json["container"]["message_ts"]
    attachment_id = form_json["container"]["attachment_id"]
    blocks = form_json["message"]["blocks"]
    attachments = form_json["message"]["attachments"]
    attachments.pop(int(attachment_id) - 1)

    if len(attachments) == 0:
        current_message = blocks[0]["text"]["text"]
        blocks[0]["text"]["text"] = "`COMPLETED` " + current_message

    slack_client.update_message(channel_id, timestamp, blocks, attachments)

    return make_response("", 200)
