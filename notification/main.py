from notification.google_calendar_notification import notify_google_calendar
from notification.trello_notification import notify_trello_tasks


if __name__ == '__main__':
    notify_trello_tasks()
    notify_google_calendar()
