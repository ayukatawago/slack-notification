import json
from datetime import datetime
from dateutil import relativedelta
from googleapiclient.discovery import build
from google.oauth2 import service_account
import config


class GoogleCalendarService:
    scopes = ['https://www.googleapis.com/auth/calendar']

    def __init__(self):
        self.credentials = service_account.Credentials.from_service_account_info(
            json.loads(config.google_credential),
            scopes=self.scopes
        )
        # https://developers.google.com/calendar/v3/reference
        self.service = build('calendar', 'v3', credentials=self.credentials)

    def get_calendar_lists(self):
        calendar_list_entry = self.service.calendarList().list().execute()
        if calendar_list_entry['items'] is None:
            self.link_service_account()
            calendar_list_entry = self.service.calendarList().list().execute()
        return calendar_list_entry['items']

    def link_service_account(self):
        for calendar_id, color_id in zip(config.target_calendars.split(','), config.calendar_colors.split(',')):
            calendar_list_entry = {
                'id': calendar_id,
                'color_id': color_id
            }
            self.service.calendarList().insert(body=calendar_list_entry).execute()

    def get_events_today(self, calendar_id):
        today_start = datetime.utcnow()
        today_end = today_start + relativedelta.relativedelta(days=1) + relativedelta.relativedelta(minutes=-1)
        events = self.service.events().list(
            calendarId=calendar_id,
            timeMin=today_start.isoformat() + 'Z',
            timeMax=today_end.isoformat() + 'Z',
            maxResults=10,
            singleEvents=True,
            orderBy='startTime').execute()
        return events['items']
