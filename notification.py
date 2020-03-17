from datetime import datetime
from dateutil import parser, relativedelta
import json
import os
import pickle
from trelloutil.trellowrapper import TrelloApiWrapper
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from slackutil.slackwrapper import SlackApiWrapper
from slackutil.slackbuilder import SlackBlockBuilder, SlackAttachmentBuilder, SlackElementsBuilder
import config

slack = SlackApiWrapper(config.slack_api_token)


def create_trello_block(list_name):
    block = SlackBlockBuilder()
    block.add_section("*Today's task in `{}`*".format(list_name))
    block.add_divider()
    return block.build()


def create_trello_attachments(cards):
    today = datetime.now()
    builder = SlackAttachmentBuilder()
    for card in cards:
        list_name = card.get_list().name
        task_name = "`{}` {}".format(list_name, card.name)
        due_date = card.due_date.astimezone().strftime("%Y/%m/%d")

        elements = SlackElementsBuilder()
        elements.add_button("complete", card.id, "primary")
        elements.add_button("postpone", card.id)

        item = SlackBlockBuilder()
        item.add_section(task_name)
        item.add_context(due_date)
        item.add_actions(elements.build())

        if card.due_date.astimezone().date() < today.date():
            color = "#ff9900"
        else:
            color = "#00c300"
        builder.add_item(item.build(), color)
    return builder.build()


def get_todo_cards(trello_list):
    today = datetime.now()
    trello_cards = list()
    open_cards = trello_list.list_cards("open")
    if len(open_cards) == 0:
        return trello_cards

    for card in open_cards:
        if (card.due_date != ''
                and card.due_date.date() <= today.date()
                and not card.is_due_complete):
            trello_cards.append(card)
    return trello_cards


def notify_trello_tasks():
    # get cards from Trello
    trello = TrelloApiWrapper(config.trello_api_key, config.trello_token)
    trello_board = trello.get_board_by_name(config.trello_board)
    open_lists = trello_board.list_lists("open")
    for trello_list in open_lists:
        trello_cards = get_todo_cards(trello_list)
        if len(trello_cards) == 0:
            continue

        # notify to slack
        blocks = create_trello_block(trello_list.name)
        attachments = create_trello_attachments(trello_cards)
        slack.post_attachment_message(
            channel=config.slack_trello_channel,
            blocks=blocks,
            attachments=attachments
        )


def create_calendar_block(calendar_name):
    block = SlackBlockBuilder()
    block.add_section("*Today's schedule in `{}`*".format(calendar_name))
    block.add_divider()
    return block.build()


def create_calendar_attachments(events, color):
    builder = SlackAttachmentBuilder()
    for event in events:
        print(event)
        event_name = event['summary']
        event_url = event['htmlLink']
        start_time = parser.parse(event['start']['dateTime']).strftime("%H:%M")
        end_time = parser.parse(event['end']['dateTime']).strftime("%H:%M")

        item = SlackBlockBuilder()
        item.add_section("<{}|{}>".format(event_url, event_name))
        item.add_context("from {} to {}".format(start_time, end_time))

        builder.add_item(item.build(), color)
    return builder.build()


def notify_google_calendar():
    SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            print(config.google_credential)
            flow = InstalledAppFlow.from_client_config(json.loads(config.google_credential), SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    today = datetime.utcnow()
    today_start = today.isoformat() + 'Z'
    today_end = (today + relativedelta.relativedelta(days=1) + relativedelta.relativedelta(minutes=-1)).isoformat() + 'Z'
    print(today_start)
    service = build('calendar', 'v3', credentials=creds)
    calendar_list = service.calendarList().list(pageToken=None).execute()
    for calendar_list_entry in calendar_list['items']:
        if calendar_list_entry['summary'] in config.target_calendars:
            print(calendar_list_entry)
            events = service.events().list(
                calendarId=calendar_list_entry['id'],
                timeMin=today_start,
                timeMax=today_end,
                maxResults=10,
                singleEvents=True,
                orderBy='startTime').execute()
            if len(events['items']) == 0:
                print('no events')
                continue
            # notify to slack
            blocks = create_calendar_block(calendar_list_entry['summary'])
            attachments = create_calendar_attachments(events['items'], calendar_list_entry['backgroundColor'])
            print(attachments)
            slack.post_attachment_message(
                channel=config.slack_calendar_channel,
                blocks=blocks,
                attachments=attachments
            )


if __name__ == '__main__':
    notify_trello_tasks()
    notify_google_calendar()
