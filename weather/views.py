from django.shortcuts import render

import requests
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
from utils.api import fetchWeatherApi
from .models import City, WeatherInfo


class WeatherAPIView(APIView):
    def get(self, request):
        location = request.query_params.get('location')
        if not location:
            return Response({"error": "Please provide a location."}, status=status.HTTP_400_BAD_REQUEST)
        weatherData, status_code = fetchWeatherApi(location)

        if status_code == status.HTTP_200_OK:
            city = weatherData['location']['name']
            country = weatherData['location']['country']
            city, created = City.objects.get_or_create(name=city, country=country)
            weatherInfo = WeatherInfo.updateOrCreateWeatherInfo(city, weatherData['current'])

            analytics = WeatherInfo.getDataIntervals(city)

            return Response({
                # "city": city.name,
                # "country": city.country,
                # "weather": weatherData,
                "analytics": analytics
            }, status=status_code)

        return Response(weatherData, status=status_code)

class UpdateSelfAPI(APIView):
    def get(self, request):
        cities = City.objects.all()
        updatedList = []
        for city in cities:
            cityStatus = {
                "city": city.name,
                "status": True
            }
            try:
                weatherData, status_code = fetchWeatherApi(city.name)
                if status_code == status.HTTP_200_OK:
                    weatherInfo = WeatherInfo.updateOrCreateWeatherInfo(city, weatherData['current'])
                else:
                    raise ValueError(f"Failed to fetch weather data for {city.name}. Status code: {status_code}")
            except Exception as e:
                cityStatus['status'] = False
                cityStatus['error'] = str(e)
                print(f"Error updating weather data for {city.name}: {str(e)}")
            updatedList.append(cityStatus)
        return Response({"updated": updatedList}, status=status.HTTP_200_OK)
