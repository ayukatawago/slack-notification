import os

slack_api_token = os.environ.get("SLACK_API_TOKEN")
slack_trello_channel = os.environ.get("SLACK_TRELLO_CHANNEL")
slack_calendar_channel = os.environ.get("SLACK_CALENDAR_CHANNEL")

trello_api_key = os.environ.get("TRELLO_API_KEY")
trello_token = os.environ.get("TRELLO_TOKEN")
trello_board = os.environ.get("TRELLO_BOARD")

google_credential = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
target_calendars = os.environ.get("TARGET_CALENDARS")
calendar_colors = os.environ.get("CALENDAR_COLORS")