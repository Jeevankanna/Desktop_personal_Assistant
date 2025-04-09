import requests
from config import API_KEYS

def get_weather():
    city = "Salem"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEYS['WEATHER']}&units=metric"
    response = requests.get(url).json()
    return f"The temperature in {city} is {response['main']['temp']}°C with {response['weather'][0]['description']}."
