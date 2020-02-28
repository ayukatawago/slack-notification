from main import app
from bot.slackbot import SlackBot
import config


@app.route('/')
def show_entries():
    message = 'Hello, World!'
    slack_bot = SlackBot(config.slack_api_token)
    slack_bot.post_message(channel="#todo", message=message)
    return message
