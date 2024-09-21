from django.contrib import admin
from .models import WeatherData, City, WeatherAlert, WeatherInfo


class WeatherDisplay(admin.ModelAdmin):
    list_display = ['id', 'city', 'temperature', 'humidity',
                    'lastUpdated', 'isExtreme', 'timestamp']

admin.site.register(WeatherData)
admin.site.register(City)
admin.site.register(WeatherAlert)
admin.site.register(WeatherInfo, WeatherDisplay)
