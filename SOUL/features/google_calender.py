from __future__ import print_function
import datetime
import pytz
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from main import speak


# Constants
MONTHS = ["january", "february", "march", "april", "may", "june",
          "july", "august", "september", "october", "november", "december"]
DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
DAY_EXTENSIONS = ["rd", "th", "st", "nd"]

# Scopes for Google Calendar
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def authenticate_google():
    """
    Authenticate and return a Google Calendar API service instance.
    """
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    return service

def get_events(day, service):
    """
    Fetch and read aloud the events for a specific day.
    """
    date = datetime.datetime.combine(day, datetime.datetime.min.time())
    end_date = datetime.datetime.combine(day, datetime.datetime.max.time())
    utc = pytz.UTC
    date = date.astimezone(utc)
    end_date = end_date.astimezone(utc)

    events_result = service.events().list(
        calendarId='primary',
        timeMin=date.isoformat(),
        timeMax=end_date.isoformat(),
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    events = events_result.get('items', [])

    if not events:
        speak('No upcoming events found.')
    else:
        speak(f"You have {len(events)} events on this day.")

        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'])

            if 'T' in start:
                start_time = start.split("T")[1].split("+")[0]
                hour = int(start_time.split(":")[0])
                minute = start_time.split(":")[1]
                am_pm = "am" if hour < 12 else "pm"
                hour = hour if hour <= 12 else hour - 12
                start_time_formatted = f"{hour}:{minute}{am_pm}"
            else:
                start_time_formatted = "All day"

            speak(f"{event['summary']} at {start_time_formatted}")

def get_date(text):
    """
    Parse a date from text.
    """
    today = datetime.date.today()

    if "today" in text:
        return today

    day = -1
    day_of_week = -1
    month = -1
    year = today.year

    for word in text.split():
        word = word.lower()
        if word in MONTHS:
            month = MONTHS.index(word) + 1
        elif word in DAYS:
            day_of_week = DAYS.index(word)
        elif word.isdigit():
            day = int(word)
        else:
            for ext in DAY_EXTENSIONS:
                if word.endswith(ext):
                    try:
                        day = int(word[:-len(ext)])
                    except:
                        pass

    if month < today.month and month != -1:
        year += 1

    if month == -1 and day != -1:
        if day < today.day:
            month = today.month + 1
        else:
            month = today.month

    if month == -1 and day == -1 and day_of_week != -1:
        current_day_of_week = today.weekday()
        dif = day_of_week - current_day_of_week
        if dif < 0:
            dif += 7
            if "next" in text:
                dif += 7
        return today + datetime.timedelta(days=dif)

    if month != -1 and day != -1:
        try:
            return datetime.date(year=year, month=month, day=day)
        except ValueError:
            return None

    return None
