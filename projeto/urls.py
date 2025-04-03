from django.urls import path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .views import CriarProjetoView
from .views_frontend import projeto_template, projeto_html

schema_view = get_schema_view(
    openapi.Info(
        title="API Projeto de Recomendação",
        default_version='v1',
        description="Documentação da API",
        # terms_of_service="",
        # contact=openapi.Contact(email="contact@myapi.com"),
        # license=openapi.License(name="MIT"),
    ),
    url='https://florescer.inovação.dev.br/ief-suporte/projeto/v1/create/',
    public=True,
)

urlpatterns = [
    path('projeto/v1/create/', CriarProjetoView.as_view(), name='projeto-create'),
    path('projeto/v1/create/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('projeto/v1/template/', projeto_template, name='projeto-template'),
    path('projeto/v1/template/projeto_html/', projeto_html, name='projeto-html'),
]
