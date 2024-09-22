from django.shortcuts import render
import requests
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
from utils.api import fetchWeatherApi
from .models import City, WeatherInfo
from .serializers import CitySerializer

class WeatherAPIView(APIView):
    def get(self, request):
        location = request.query_params.get('location')
        if not location:
            ip_address = request.META.get('REMOTE_ADDR')
            if ip_address:
                ip_address = ip_address if ip_address != '127.0.0.1' else "Pune"
                location = ip_address
            else:
                return Response({"error": "Please provide a location."}, status=status.HTTP_400_BAD_REQUEST)
        weatherData, status_code = fetchWeatherApi(location)

        if status_code == status.HTTP_200_OK:
            city = weatherData['location']['name']
            country = weatherData['location']['country']
            city, created = City.objects.get_or_create(name=city, country=country)
            weatherInfo = WeatherInfo.updateOrCreateWeatherInfo(city, weatherData['current'])

            return Response({
                "city": city.name,
                "citySlug": city.slug,
                "country": city.country,
                "weather":weatherData
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

class AnalyticsAPI(APIView):
    def get(self, request):
        slug = request.query_params.get('slug')
        if not slug:
            return Response({"error": "Please provide a location."}, status=status.HTTP_400_BAD_REQUEST)

        city = City.objects.get(slug=slug)
        analytics = WeatherInfo.getDataIntervals(city)
        return Response(analytics)

class CityWeatherAPIView(APIView):
    def get(self, request):
        cities = City.objects.all()
        serializer = CitySerializer(cities, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
