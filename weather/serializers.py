from rest_framework import serializers
from .models import City, WeatherInfo

class WeatherInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherInfo
        fields = ['temperature', 'humidity', 'windSpeed', 'condition', 'cloud',  'uv',  'icon', 'lastUpdated', 'windDir']

class CitySerializer(serializers.ModelSerializer):
    lastWeatherInfo = serializers.SerializerMethodField()


    class Meta:
        model = City
        fields = ['name', 'slug', 'lastWeatherInfo', 'country']

    def get_lastWeatherInfo(self, city):
        # Get the most recent weather info (ordered by 'lastUpdated')
        latest_weather = WeatherInfo.objects.filter(city=city).order_by('-lastUpdated').first()
        if latest_weather:
            return WeatherInfoSerializer(latest_weather).data
        return None