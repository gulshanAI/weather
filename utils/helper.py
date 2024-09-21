# weather/utils.py

import requests
from weather.models import WeatherData
from django.conf import settings
from datetime import timedelta
from django.utils import timezone

def fetch_weather_data(city):
    api_key = "930963d12588462d95932059242109"
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}&aqi=no"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

def save_weather_data(city):
    data = fetch_weather_data(city)
    if data:
        weather = WeatherData(
            city=city,
            temperature=data['current']['temp_c'],
            humidity=data['current']['humidity'],
            condition=data['current']['condition']['text'],
            wind_speed=data['current']['wind_kph'],
        )
        weather.save()
    return weather

def calculate_temperature_trend(city):
    now = timezone.now()
    last_24_hours = now - timedelta(hours=24)
    data = WeatherData.objects.filter(city=city, timestamp__gte=last_24_hours)
    if data:
        avg_temp = sum([entry.temperature for entry in data]) / len(data)
        return avg_temp
    return None

def calculate_humidity_trend(city):
    now = timezone.now()
    last_24_hours = now - timedelta(hours=24)
    data = WeatherData.objects.filter(city=city, timestamp__gte=last_24_hours)
    if data:
        avg_humidity = sum([entry.humidity for entry in data]) / len(data)
        return avg_humidity
    return None

def check_extreme_weather(city):
    data = WeatherData.objects.filter(city=city).latest('timestamp')
    alerts = []

    if data.temperature > 40:
        alerts.append(f"Extreme heat in {city}: {data.temperature}°C")
    if data.wind_speed > 50:
        alerts.append(f"Extreme wind speed in {city}: {data.wind_speed} kph")

    return alerts