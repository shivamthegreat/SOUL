import speech_recognition as sr
import pyttsx3
from soul.features import date_time
from soul.features import launch_app
from soul.features import website_open
from soul.features import weather
from soul.features import wikipedia
# from soul.features import news
from soul.features import send_email
from soul.features import google_search
from soul.features import google_calendar
from soul.features import note
from soul.features import system_stats
from soul.features import loc
from elevenlabs import generate, play, set_api_key

# IMPORTANT: Replace with your real API key
set_api_key("sk_19b742c77bc8fedf0bb696bec98d28b4de8e2af57b96ca4d")

# pyttxs or eleban  # <-- Removed invalid code (commented)

class SoulAssistant:
    def __init__(self):
        pass

    def mic_input(self):
        """
        Fetch input from mic
        return: user's voice input as text if true, false if fail
        """
        try:
            r = sr.Recognizer()
            with sr.Microphone() as source:
                print("Listening....")
                r.energy_threshold = 4000
                while True:
                    audio = r.listen(source)
                    try:
                        print("Recognizing...")
                        command = r.recognize_google(audio, language='en-in').lower()
                        print(f'You said: {command}')
                        return command
                    except:
                        print('Could not recognize, please try again...')
        except Exception as e:
            print(e)
            return False

    def tell_me_date(self):
        return date_time.date()

    def tell_time(self):
        return date_time.time()

    def launch_any_app(self, path_of_app):
        """
        Launch any windows application 
        :param path_of_app: path of exe 
        :return: True is success and open the application, False if fail
        """
        return launch_app.launch_app(path_of_app)

    def website_opener(self, domain):
        """
        This will open website according to domain
        :param domain: any domain, example "youtube.com"
        :return: True if success, False if fail
        """
        return website_open.website_opener(domain)

    def weather(self, city):
        """
        Return weather
        :param city: Any city of this world
        :return: weather info as string if True, or False
        """
        try:
            res = weather.fetch_weather(city)
        except Exception as e:
            print(e)
            res = False
        return res

    def tell_me(self, topic):
        """
        Tells about anything from wikipedia
        :param topic: any string is valid options
        :return: First 500 characters from wikipedia if True, False if fail
        """
        return wikipedia.tell_me_about(topic)

    # def news(self):
    #     """
    #     Fetch top news of the day from google news
    #     :return: news list of strings if True, False if fail
    #     """
    #     return news.get_news()

    def send_mail(self, sender_email, sender_password, receiver_email, msg):
        return send_email.mail(sender_email, sender_password, receiver_email, msg)

    def google_calendar_events(self, command):
        """
        Fetch events from Google Calendar based on the user's command.
        :param command: Command from user that is used to get the date
        """
        day = google_calendar.get_date(command)
        if day:
            events = google_calendar.get_events(day)  # Get events based on the day
            # Process or use the events as needed
            return events
        else:
            print("Unable to determine the date from the command.")
            return False

    def search_anything_google(self, command):
        google_search.google_search(command)

    def take_note(self, text):
        note.note(text)

    def system_info(self):
        return system_stats.system_stats()

    def location(self, location):
        current_loc, target_loc, distance = loc.loc(location)
        return current_loc, target_loc, distance

    def my_location(self):
        city, state, country = loc.my_location()
        return city, state, country

    def tts(self, text):
        """
        Text to Speech using ElevenLabs API
        :param text: Text to be converted to speech
        :return: True if successful, False if an error occurs
        """
        if not text:
            print("No text provided for TTS.")
            return False
        try:
            audio = generate(
                text=text,
                voice="Bella",  # Or any other voice you prefer
                model="eleven_multilingual_v2"
            )
            play(audio)
            return True
        except Exception as e:
            print(f"Error using ElevenLabs TTS: {e}")
            return False
