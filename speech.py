import pyttsx3
import speech_recognition as sr

engine = pyttsx3.init()

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def take_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Listening...")
        recognizer.pause_threshold = 1
        audio = recognizer.listen(source)
    try:
        return recognizer.recognize_google(audio, language="en-in").lower()
    except:
        speak("Sorry, please repeat that.")
        return "None"
