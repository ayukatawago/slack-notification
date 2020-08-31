import json
from dateutil import parser
from googleutil.google_service import GoogleCalendarService
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
    credential = json.loads(config.google_credential)
    calendar_entry_list = []
    for calendar_id, color_id in zip(config.target_calendars.split(','), config.calendar_colors.split(',')):
        calendar_entry_list.append({'id': calendar_id,'color_id': color_id})

    service = GoogleCalendarService(credential, calendar_entry_list)

    calendar_lists = service.get_calendar_lists()

    for calendar in calendar_lists:
        events = service.get_events_today(calendar['id'])
        if len(events) == 0:
            print('no event')
            continue

        # notify to slack
        blocks = create_calendar_block(calendar['summary'])
        attachments = create_calendar_attachments(events, calendar['backgroundColor'])

        slack.post_attachment_message(
            channel=config.slack_calendar_channel,
            blocks=blocks,
            attachments=attachments
        )
