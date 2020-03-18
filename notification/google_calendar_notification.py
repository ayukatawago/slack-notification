import os
import json
import pickle
from datetime import datetime
from dateutil import parser, relativedelta
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from slackutil.slackbuilder import SlackBlockBuilder, SlackAttachmentBuilder
from slackutil.slackwrapper import SlackApiWrapper
import config


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
    slack = SlackApiWrapper(config.slack_api_token)
    scopes = ['https://www.googleapis.com/auth/calendar.readonly']
    creds = None
    if os.path.exists('../token.pickle'):
        with open('../token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            print(config.google_credential)
            flow = InstalledAppFlow.from_client_config(json.loads(config.google_credential), scopes)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('../token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    today_start = datetime.utcnow()
    today_end = today_start + relativedelta.relativedelta(days=1) + relativedelta.relativedelta(minutes=-1)
    service = build('calendar', 'v3', credentials=creds)
    calendar_list = service.calendarList().list(pageToken=None).execute()
    for calendar_list_entry in calendar_list['items']:
        if calendar_list_entry['summary'] in config.target_calendars:
            print(calendar_list_entry)
            events = service.events().list(
                calendarId=calendar_list_entry['id'],
                timeMin=today_start.isoformat() + 'Z',
                timeMax=today_end.isoformat() + 'Z',
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