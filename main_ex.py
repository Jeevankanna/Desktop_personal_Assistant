import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser as wb
import os
import random
import requests
import openai
from logging_config import logger  # Import logging configuration

# Initialize text-to-speech engine
engine = pyttsx3.init()

# OpenAI API Key (Replace with your key)
OPENAI_API_KEY = "YOUR_OPENAI_API_KEY"

# OpenWeather API Key (Replace with your key)
WEATHER_API_KEY = "YOUR_OPENWEATHER_API_KEY"

def speak(audio):
    logger.info(f"Speaking: {audio}")  # Logs spoken output
    engine.say(audio)
    engine.runAndWait()

def time():
    Time = datetime.datetime.now().strftime("%I:%M %p")
    speak(f"The current time is {Time}")
    print("The current time is ", Time)
    logger.info(f"Time requested: {Time}")

def date():
    today = datetime.datetime.now().strftime("%d %B %Y")
    speak(f"Today's date is {today}")
    print("Today's date is ", today)
    logger.info(f"Date requested: {today}")

def takecommand():
    logger.info("Listening for a command...")
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        query = r.recognize_google(audio, language="en-in")
        print(query)
        logger.info(f"User Command: {query}")  # Logs user input
        return query.lower()
    except Exception as e:
        logger.error(f"Speech recognition error: {e}")
        speak("Please say that again")
        return "None"

# Store Chat History
def save_chat_history(user_id, user_message, bot_response):
    cursor.execute("INSERT INTO chat_history (user_id, user_message, bot_response) VALUES (?, ?, ?)",
                   (user_id, user_message, bot_response))
    conn.commit()

def chat_with_ai(prompt, user_id=1):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    ai_response = response["choices"][0]["message"]["content"]
    
    save_chat_history(user_id, prompt, ai_response)  # Save to Database
    return ai_response

# Store & Retrieve Reminders
def set_reminder(event, time, user_id=1):
    cursor.execute("INSERT INTO reminders (user_id, event, reminder_time) VALUES (?, ?, ?)",
                   (user_id, event, time))
    conn.commit()
    return f"Reminder set for {event} at {time}."

def get_reminders(user_id=1):
    cursor.execute("SELECT event, reminder_time FROM reminders WHERE user_id=? AND status='Pending'", (user_id,))
    reminders = cursor.fetchall()
    
    if reminders:
        return [f"{event} at {reminder_time}" for event, reminder_time in reminders]
    return ["No active reminders."]

# Fetch Weather
def get_weather(city="Salem"):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()

        if response.status_code != 200 or "main" not in data:
            error_message = data.get("message", "Unknown error occurred.")
            return f"Sorry, I couldn't fetch the weather. Reason: {error_message}"

        temp = data["main"]["temp"]
        weather_desc = data["weather"][0]["description"]
        return f"The temperature in {city} is {temp}°C with {weather_desc}."

    except requests.exceptions.RequestException as e:
        return f"⚠️ Network error: {e}"

# Main Loop
if __name__ == "__main__":
    speak("JARVIS is now active!")
    while True:
        query = takecommand()

        if "time" in query:
            time()

        elif "date" in query:
            date()

        elif "who are you" in query:
            speak("I'm Jarvis created by Mr. JK and I'm a desktop voice assistant.")

        elif "wikipedia" in query:
            try:
                speak("Searching Wikipedia...")
                query = query.replace("wikipedia", "")
                result = wikipedia.summary(query, sentences=2)
                print(result)
                speak(result)
            except:
                speak("Can't find this page sir, please ask something else")

        elif "set a reminder" in query:
            speak("What is the event?")
            event = takecommand()
            speak("At what time?")
            reminder_time = takecommand()
            response = set_reminder(event, reminder_time)
            speak(response)

        elif "what are my reminders" in query:
            reminders = get_reminders()
            speak("Here are your active reminders:")
            for reminder in reminders:
                speak(reminder)

        elif "chat" in query:
            speak("What would you like to ask?")
            user_input = takecommand()
            response = chat_with_ai(user_input)
            speak(response)
            print(response)

        elif "weather" in query:
            weather_report = get_weather()
            speak(weather_report)
            print(weather_report)

        elif "offline" in query:
            speak("Going offline, Have a great day sir!")
            quit()
