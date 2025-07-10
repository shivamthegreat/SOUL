from SOUL import SOUL_ASSISSTANT
import re
import requests
import pygame
import sys
import os
import tempfile
from dotenv import load_dotenv
import requests
import pprint
import random
import wikipedia
import webbrowser
import datetime
import json
import speech_recognition as sr
import pywhatkit as kit
import smtplib
import datetime
import pyjokes
import pyautogui
import pywhatkit
import wolframalpha
import time
from pydub import AudioSegment
from pydub.playback import play
from SOUL.config import config
from PIL import Image
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QTimer, QTime, QDate, Qt
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from SOUL.features.tempvoice import play_audio_bytes
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtCore import QThread, pyqtSignal
from SOUL.features.tempvoice import text_to_speech
obj=SOUL_ASSISSTANT()
from SOUL.features import *
# ==============
# ================== IMPORT DONE ===========================================================================================================


def speak(text):
    """
    Use ElevenLabs to speak text aloud.
    """
    if not config.ELEVENLABS_API_KEY:
        print("❌ Error: API key not found. Please set ELEVENLABS_API_KEY in your .env file.")
        return
    success, audio = text_to_speech(text)
    if not success:
        print(f"❌ TTS Error: {audio}")
        return

    success, message = play_audio_bytes(audio)
    if not success:
        print(f"❌ Playback Error: {message}")
   

def startup():
    speak("Welcome back to SOUL, your personal assistant.")
    speak("Allow me to introduce myself, I am Soul a virtual artificial intelligence designed by the SOUL team.")
    speak("I am constantly learning and improving, so the more you use me, the better I will become at understanding your needs and preferences.")

def wish():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<=12:
        speak("Good Morning")
    elif hour>12 and hour<18:
        speak("Good afternoon")
    else:
        speak("Good evening")
    c_time = obj.tell_time()
    speak(f"Currently it is {c_time}")

class MainThread(QThread):
    def __init__(self):
        super(MainThread, self).__init__()

    def run(self):
        self.TaskExecution()

    def TaskExecution(self):
        startup()
        wish()
        while True:
            command = obj.mic_input()

            if re.search('date', command):
                date = obj.tell_me_date()
                print(date)
                speak(date)

            elif "time" in command:
                time_c = obj.tell_time()
                print(time_c)
                speak(f"Sir the time is {time_c}")

            elif re.search('launch', command):
                dict_app = {
                    'chrome': 'C:/Program Files/Google/Chrome/Application/chrome'
                }

                app = command.split(' ', 1)[1]
                path = dict_app.get(app)

                if path is None:
                    speak('Application path not found')
                    print('Application path not found')

                else:
                    speak('Launching: ' + app + 'for you sir!')
                    obj.launch_any_app(path_of_app=path)


            elif re.search('open', command):
                domain = command.split(' ')[-1]
                open_result = obj.website_opener(domain)
                speak(f'Alright sir !! Opening {domain}')
                print(open_result)

            elif re.search('weather', command):
                city = command.split(' ')[-1]
                weather_res = obj.weather(city=city)
                print(weather_res)
                speak(weather_res)

            elif re.search('tell me about', command):
                topic = command.split(' ')[-1]
                if topic:
                    wiki_res = obj.tell_me(topic)
                    print(wiki_res)
                    speak(wiki_res)
                else:
                    speak(
                        "Sorry sir. I couldn't load your query from my database.")

            elif 'search google for' in command:
                obj.search_anything_google(command)
            
            elif 'youtube' in command:
                video = command.split(' ')[1]
                speak(f"Okay sir, playing {video} on youtube")
                pywhatkit.playonyt(video)

def tell_me_about(topic):
    """Retrieve a Wikipedia summary about the topic"""
    try:
        summary = wikipedia.summary(topic, sentences=3)
        return True, summary

    except wikipedia.exceptions.PageError:
        return False, f"Sorry, the page for '{topic}' does not exist."

    except wikipedia.exceptions.DisambiguationError as e:
        options = ', '.join(e.options[:3])
        return False, (
            f"Multiple results found for '{topic}'. "
            f"Please be more specific. For example: {options}"
        )

    except wikipedia.exceptions.HTTPTimeoutError:
        return False, "The request to Wikipedia timed out. Please try again later."

    except Exception as e:
        return False, f"An error occurred: {str(e)}"

def main():




















    def showTime(self):
        current_time = QTime.currentTime()
        current_date = QDate.currentDate()
        label_time = current_time.toString('hh:mm:ss')
        label_date = current_date.toString(Qt.ISODate)
        self.ui.textBrowser.setText(label_date)
        self.ui.textBrowser_2.setText(label_time)
        self.ui.textBrowser_3.setText("SOUL")
        self.ui.textBrowser_4.setText("Assistant")  