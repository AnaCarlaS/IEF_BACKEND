from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from .views import home_suporte

urlpatterns = [
    path("ief-suporte/admin/", admin.site.urls),
    path("ief-suporte/", home_suporte, name='home-suporte'), 
    path("ief-suporte/", include("car_api.urls")),
    path("ief-suporte/", include("car_etl.urls")),
    path("ief-suporte/", include("projeto.urls")),
]  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
