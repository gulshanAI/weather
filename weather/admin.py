from django.contrib import admin
from .models import WeatherData, City, WeatherAlert, WeatherInfo

admin.site.register(WeatherData)
admin.site.register(City)
admin.site.register(WeatherAlert)
admin.site.register(WeatherInfo)
