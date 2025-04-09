import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser as wb
import os
import random
import requests
import openai
from memory import remember_this, recall_memory, forget_everything  # Memory module
from screenshot import take_screenshot  # Screenshot module
import requests
import json
import os
import logging
import psutil
import subprocess
from plyer import notification

# Initialize text-to-speech engine
engine = pyttsx3.init()

#configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
# OpenAI API Key (Replace with your key)
DEEPSEEK_API_KEY = "sk-97da4d1d18aa41e29efb524ee253864f"

# OpenWeather API Key (Replace with your key)
WEATHER_API_KEY = "YOUR_OPENWEATHER_API_KEY"

MEMORY_FILE = "memory.json"
MEMORY_FILE_TXT = "memory.txt"

DB_FILE = "jarvis_data.json"
running_apps = {}

# speak configuration
def speak(audio):
    engine.say(audio)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.runAndWait()

#Time
def time():
    Time = datetime.datetime.now().strftime("%I:%M %p")
    speak(f"The current time is {Time}")
    print("The current time is ", Time)

#Date
def date():
    today = datetime.datetime.now().strftime("%d %B %Y")
    speak(f"Today's date is {today}")
    print("Today's date is ", today)

def wishme():
    print("Welcome back  Mr.JK")
    speak("Welcome back  Mr.JK")
    
    hour = datetime.datetime.now().hour
    if hour >= 4 and hour < 12:
        speak("Good Morning Sir!!")
    elif hour >= 12 and hour < 16:
        speak("Good Afternoon Sir!!")
    elif hour >= 16 and hour < 24:
        speak("Good Evening Sir!")
    else:
        speak("Good Night Sir, See You Tomorrow")

    speak("Jarvis at your service sir, please tell me how may I help you.")

def takecommand():
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
    
    return query.lower()

#set a Remainder
def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return {"chat_history": [], "reminders": []}

    with open(MEMORY_FILE, "r") as file:
        return json.load(file)

def save_memory(memory_data):
    with open(MEMORY_FILE, "w") as file:
        json.dump(memory_data, file, indent=4)

def save_chat(user_input, bot_response):
    memory = load_memory()
    memory["chat_history"].append({"user": user_input, "bot": bot_response})
    save_memory(memory)

def set_reminder(event, time):
    memory = load_memory()
    memory["reminders"].append({"event": event, "time": time})
    save_memory(memory)
    return f"Reminder set for {event} at {time}."

def chat_with_deepseek(prompt):
    """Communicates with DeepSeek AI API and returns a chat response."""
    url = "https://api.deepseek.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,  # Control randomness of response
        "max_tokens": 200  # Limit response length
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        response.raise_for_status()  # Raise HTTP errors
        data = response.json()
        
        # Validate API response structure
        if "choices" in data and len(data["choices"]) > 0 and "message" in data["choices"][0]:
            return data["choices"][0]["message"]["content"]
        else:
            logging.error("Unexpected API response format: %s", data)
            return "Error: Unexpected response from DeepSeek AI."
    except requests.exceptions.Timeout:
        logging.error("Request timed out.")
        return "Error: Request to DeepSeek API timed out."
    except requests.exceptions.RequestException as e:
        logging.error("Request error: %s", e)
        return f"Error: {str(e)}"
    except Exception as e:
        logging.error("Unexpected error: %s", e)
        return "Error: An unexpected issue occurred."
    
def remember_event(event):
    data = load_memory()
    data["events"].append(event)
    save_memory(data)

    # Also save to Notepad (memory.txt)
    with open(MEMORY_FILE_TXT, "a") as file:
        file.write(event + "\n")

    return f"I will remember this: {event}"

# Load data from JSON file
def load_data():
    if not os.path.exists(DB_FILE):  # If file doesn't exist, create a new one
        save_data({"user": {}, "reminders": [], "chat_history": []})
    
    with open(DB_FILE, "r") as file:
        return json.load(file)

# Save data to JSON file
def save_data(data):
    with open(DB_FILE, "w") as file:
        json.dump(data, file, indent=4)

# Function to update user preferences
def update_user(name, voice_type):
    data = load_data()
    data["user"]["name"] = name
    data["user"]["voice_type"] = voice_type
    save_data(data)

    
# Function to log chat history
def log_chat(user_message, bot_response):
    data = load_data()
    data["chat_history"].append({"user": user_message, "bot": bot_response})
    save_data(data)

def view_database():
    data = load_data()
    print("\n JARVIS DATABASE TRANSACTIONS \n")
    
    print("🔹 **User Data:**")
    print(f"  - Name: {data['user'].get('name', 'Not Set')}")
    print(f"  - Voice Type: {data['user'].get('voice_type', 'Not Set')}\n")

    print("🔹 **Reminders:**")
    if data["reminders"]:
        for index, reminder in enumerate(data["reminders"], start=1):
            print(f"  {index}. {reminder['event']} at {reminder['time']}")
    else:
        print("  - No reminders set.\n")

    print("🔹 **Chat History:**")
    if data["chat_history"]:
        for chat in data["chat_history"]:
            print(f"   You: {chat['user']}")
            print(f"   JARVIS: {chat['bot']}\n")
    else:
        print("  - No chat history found.\n")

    print(" End of Transactions ")

def recall_events():
    if not os.path.exists(MEMORY_FILE_TXT):
        return "I don't remember any events."

    with open(MEMORY_FILE_TXT, "r") as file:
        events = file.readlines()

    if not events:
        return "I don't remember any events."

    return "Here are the events I remember:\n" + "".join(events)

# Weather Function
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

 # Remove from tracking

def notify(title, message):
    notification.notify(
        title=title,
        message=message,
        app_name="JARVIS",
        timeout=5
    )

if __name__ == "__main__":
    wishme()
    while True:
        query = takecommand()

        if "time" in query:
            time()

        elif "date" in query:
            date()

        elif "who are you" in query:
            speak("I'm Jarvis created by Mr. JK and I'm a  Personal desktop voice assistant.")

        elif "how are you Jarvis " in query:
            speak("I'm fine sir, What about you?")

        elif "fine" in query or "good" in query:
            speak("Glad to hear that sir!!")

        elif "wikipedia" in query:
            try:
                speak("Searching Wikipedia...")
                wb.open("https://www.wikipedia.org/")
                print(result)
                speak(result)
            except:
                speak("Can't find this page sir, please ask something else")

        elif "open youtube" in query:
            speak("Opening Youtube")
            notify("Opening Application", "Launching Youtube...")
            wb.open("youtube.com")

        elif "open google" in query:
            speak("Opening Google")
            notify("Opening Application", "Launching google...")
            wb.open("google.com")

    
        elif "open notepad" in query:
            speak("Opening Notepad")
            notify("Opening Application", "Launching Notepad...")
            subprocess.Popen("notepad.exe")

        elif "play music" in query:
            song_dir = os.path.expanduser("C:\\music")
            songs = os.listdir(song_dir)
            if songs:
                os.startfile(os.path.join(song_dir, random.choice(songs)))
            else:
                speak("No music files found in the directory.")

        elif "search on chrome" in query:
            try:
                speak("What should I search?")
                search = takecommand()
                wb.open(f"https://www.google.com/search?q={search}")
            except:
                speak("Can't open now, please try again later.")

        elif "deepseek chat" in query or "ai chat" in query:
            speak("What would you like to ask?")
            user_input = takecommand()
            response = chat_with_deepseek(user_input)
            speak(response)
            print(response)

        elif "set a reminder" in query:
            speak("What should I remind you about?")
            event = takecommand()
            speak("At what time?")
            reminder_time = takecommand()
            response = set_reminder(event, reminder_time)
            speak(response)

        elif "what are my reminders" in query:
            memory = load_memory()
            if memory["reminders"]:
                speak("Here are your reminders:")
                for reminder in memory["reminders"]:
                    speak(f"{reminder['event']} at {reminder['time']}")
            else:
                speak("You have no active reminders.")

        elif "what is the weather" in query:
            weather_report = get_weather()
            speak(weather_report)
            print(weather_report)

        elif "remember Jarvis" in query:
            speak("What should I remember")
            data = takecommand()
            speak("You said me to remember that" + data)
            print("You said me to remember that " + str(data))
            remember = open("data.txt", "w")
            remember.write(data)
            remember.close()

        elif "Jarvis do you remember anything" in query:
            remember = open("data.txt", "r")
            speak("You told me to remember that" + remember.read())
            print("You told me to remember that " + str(remember))


        elif "forget everything" in query or "clear memory" in query:
            confirmation = forget_everything()
            speak(confirmation)

        elif "screenshot" in query or "take a screenshot" in query:
            result = take_screenshot()
            speak(result)
            print(result)

        elif "view database" in query or "show transactions" in query:
            view_database()  # This will display all stored transactions
    
        elif "offline" in query or "shut down"in query:
            speak("Going offline, Have a great day sir!")
            quit()
