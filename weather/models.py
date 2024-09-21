from django.db import models
from django.utils import timezone
from datetime import datetime
from datetime import timedelta
import pytz
from django.db.models import OuterRef, Subquery
from django.db.models.functions import TruncHour
from django.utils.text import slugify


class City(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(City, self).save(*args, **kwargs)

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
    lastUpdated = models.CharField(max_length=15)
    isExtreme = models.BooleanField(default=False)

    def __str__(self):
        return f"Weather data for {self.city.name} at {self.timestamp}"
    def save(self, *args, **kwargs):
        self.timestamp = timezone.localtime(self.timestamp)
        super(WeatherInfo, self).save(*args, **kwargs)
        
    @classmethod
    def updateOrCreateWeatherInfo(cls, city, weatherData):
        lastUpdatedStr = weatherData['last_updated']
        lastUpdated = datetime.strptime(lastUpdatedStr, '%Y-%m-%d %H:%M')
        lastUpdated = lastUpdated.replace(minute=0, second=0, microsecond=0)
        lastUpdated = lastUpdated.strftime("%Y-%m-%d %H:%M")

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
    def getDataIntervals(cls, city):
        now = timezone.now()
        ist_timezone = pytz.timezone('Asia/Kolkata')
        now = now.astimezone(ist_timezone)
        startTime = now.replace(minute=0, second=0, microsecond=0)
        endTime = startTime - timedelta(hours=24)
        data =  cls.objects.filter(city=city, lastUpdated__range=(endTime, startTime)).order_by('lastUpdated')
        print(data)
        if data:
            averages = data.aggregate(
                temperature=models.Avg('temperature'),
                humidity=models.Avg('humidity'),
                windSpeed=models.Avg('windSpeed'),
                windDir=models.Avg('windDir'),
                condition=models.Avg('condition'),
                pressure=models.Avg('pressure'),
                feelsLike=models.Avg('feelsLike'),
                precipitation=models.Avg('precipitation'),
                cloud=models.Avg('cloud'),
                windChill=models.Avg('windChill'),
                heatIndex=models.Avg('heatIndex'),
                dewPoint=models.Avg('dewPoint'),
                visibility=models.Avg('visibility'),
                uv=models.Avg('uv'),
                gust=models.Avg('gust')
            )
            return {
                "report": list(data.values()),
                "average": averages
            }
        return {
            "report": [],
            "average": {}
        }

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
