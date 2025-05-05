from src.shiro.config import OPEN_WEATHER_URL, CITY
import requests


def format_weather(data):
    temperature = data['main']['temp']
    weather_desc = data['weather'][0]['description']
    humidity = data['main']['humidity']
    wind_speed = data['wind']['speed']

    return (f"Temperature: {temperature}°C\n"
            f"Condition: {weather_desc}\n"
            f"Humidity: {humidity}%\n"
            f"Wind Speed: {wind_speed} m/s")


def get_weather(open_weather_api_key):
    params = {
        'q': CITY,
        'appid': open_weather_api_key,
        'units': 'metric'
    }
    response = requests.get(OPEN_WEATHER_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        return format_weather(data)
    else:
        return f"Error: {response.status_code}"