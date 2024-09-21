import requests
from django.conf import settings
from rest_framework import status

def fetchWeatherApi(location):
    api_key = settings.WEATHER_API_KEY
    url = f"https://api.weatherapi.com/v1/current.json?key={api_key}&q={location}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json(), status.HTTP_200_OK
    except requests.exceptions.HTTPError as http_err:
        return {"error": str(http_err)}, response.status_code
    except requests.exceptions.RequestException as req_err:
        return {"error": "An error occurred while fetching weather data."}, status.HTTP_500_INTERNAL_SERVER_ERROR
