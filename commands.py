import webbrowser as wb
import os
import random
from speech import speak
from weather import get_weather
from reminder import set_reminder
from smart_home import control_smart_home
import speech_recognition as sr

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language="en-in")
        print(query)
    except Exception as e:
        print(e)
        speak("Please say that again")
        return "Try Again"

def execute_command(query):
    if "time" in query:
        from datetime import datetime
        speak(f"The time is {datetime.now().strftime('%I:%M %p')}")
    elif "date" in query:
        from datetime import datetime
        speak(f"Today's date is {datetime.now().strftime('%d %B %Y')}")
    elif "weather" in query:
        speak(get_weather())
    elif "set reminder" in query:
        speak("What is the event?")
        event = take_command()
        speak("At what time?")
        reminder_time = take_command()
        set_reminder(event, reminder_time)
    elif "turn on the lights" in query:
        control_smart_home("lights", "on")
    elif "turn off the lights" in query:
        control_smart_home("lights", "off")
    elif "open youtube" in query:
        wb.open("youtube.com")
    elif "search on chrome" in query:
        speak("What should I search?")
        search = take_command()
        wb.open(f"https://www.google.com/search?q={search}")
    elif "offline" in query:
        speak("Shutting down. Have a great day!")
        quit()
    else:
        speak("Sorry, I didn't understand that.")
