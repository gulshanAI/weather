from django.db import models
from django.utils import timezone
from datetime import datetime
from datetime import timedelta

class City(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name}, {self.country}"

class WeatherInfo(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    temperature = models.FloatField()
    humidity = models.FloatField()
    windSpeed = models.FloatField()
    windDir = models.CharField(max_length=100)
    condition = models.CharField(max_length=100) 
    pressure = models.FloatField()
    feelsLike = models.FloatField()
    precipitation = models.FloatField()
    cloud = models.FloatField()
    windChill = models.FloatField()
    heatIndex = models.FloatField()
    dewPoint = models.FloatField()
    visibility = models.FloatField()
    uv = models.FloatField()
    gust = models.FloatField()
    icon = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    lastUpdated = models.DateTimeField()
    isExtreme = models.BooleanField(default=False)

    def __str__(self):
        return f"Weather data for {self.city.name} at {self.timestamp}"

    @classmethod
    def updateOrCreateWeatherInfo(cls, city, weatherData):
        lastUpdatedStr = weatherData['last_updated']
        lastUpdated = datetime.strptime(lastUpdatedStr, '%Y-%m-%d %H:%M')
        
        weatherInfo, created = cls.objects.get_or_create(
            city=city,
            lastUpdated=lastUpdated,
            defaults={
                'temperature': weatherData['temp_c'],
                'humidity': weatherData['humidity'],
                'windSpeed': weatherData['wind_kph'],
                'windDir': weatherData['wind_dir'],
                'condition': weatherData['condition']['text'],
                'icon': weatherData['condition']['icon'],
                'pressure': weatherData['pressure_mb'],
                'feelsLike': weatherData['feelslike_c'],
                'precipitation': weatherData['precip_mm'],
                'cloud': weatherData['cloud'],
                'windChill': weatherData['windchill_c'],
                'heatIndex': weatherData['heatindex_c'],
                'dewPoint': weatherData['dewpoint_c'],
                'visibility': weatherData['vis_km'],
                'uv': weatherData['uv'],
                'gust': weatherData['gust_kph'],
            }
        )

        weatherInfo.isExtreme = weatherInfo.temperature > 35
        weatherInfo.save()

        return weatherInfo

    @classmethod
    def getDataIntervals(cls, city, intervalMin=15, totalHr=24):
        now = timezone.now()
        startTime = now - timedelta(hours=totalHr)
        numIntervals = (totalHr * 60) // intervalMin

        weather_records = cls.objects.filter(
            city=city,
            lastUpdated__range=[startTime, now]
        ).order_by('lastUpdated')

        intervals = []
        for i in range(numIntervals):
            interval_start = now - timedelta(minutes=intervalMin * (i + 1))
            interval_end = now - timedelta(minutes=intervalMin * i)

            records_in_interval = weather_records.filter(
                lastUpdated__gte=interval_start,
                lastUpdated__lt=interval_end
            )

            intervals.append({
                'interval_start': interval_start,
                'interval_end': interval_end,
                'data': records_in_interval
            })

        return intervals

class WeatherAlert(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    alertMessage = models.CharField(max_length=255)
    alertType = models.CharField(max_length=100)
    triggeredAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Alert for {self.city.name} at {self.triggeredAt}: {self.alertMessage}"

class WeatherData(models.Model):
    city = models.CharField(max_length=100)
    temperature = models.FloatField()
    humidity = models.FloatField()
    condition = models.CharField(max_length=100)
    wind_speed = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.city} - {self.temperature}°C"
