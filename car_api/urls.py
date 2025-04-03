from django.urls import path
from .views import car_api

urlpatterns = [
    path("car-api/v1/", car_api.urls),
]
