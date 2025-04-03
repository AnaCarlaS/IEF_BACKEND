from django.urls import path
from .views import car_etl

urlpatterns = [
    path("car-etl/v1/", car_etl.urls),
]
