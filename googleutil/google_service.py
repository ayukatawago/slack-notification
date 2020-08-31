from datetime import datetime
from dateutil import relativedelta
from googleapiclient.discovery import build
from google.oauth2 import service_account


class GoogleCalendarService:
    scopes = ['https://www.googleapis.com/auth/calendar']

    def __init__(self, credentials, calendar_entry_list):
        self.credentials = service_account.Credentials.from_service_account_info(
            credentials,
            scopes=self.scopes
        )
        self.calendar_entry_list = calendar_entry_list
        # https://developers.google.com/calendar/v3/reference
        self.service = build('calendar', 'v3', credentials=self.credentials)

    def get_calendar_lists(self):
        calendar_list_entry = self.service.calendarList().list().execute()
        if calendar_list_entry['items'] is None:
            self.link_service_account()
            calendar_list_entry = self.service.calendarList().list().execute()
        return calendar_list_entry['items']

    def link_service_account(self):
        for calendar_entry in self.calendar_list_entry:
            self.service.calendarList().insert(body=calendar_entry).execute()

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
