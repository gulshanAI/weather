from django.urls import path
from . import views

urlpatterns = [
    path('weather/', views.WeatherAPIView.as_view(), name='weather-api'),
    path('update/', views.UpdateSelfAPI.as_view(), name='update-weather-api'),
    # path('update/', views.Anaylitics.as_view(), name='update-weather-api'),
]
