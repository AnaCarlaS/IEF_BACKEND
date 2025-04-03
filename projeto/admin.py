from django.contrib.gis import admin
from .models import Projeto, Bioma, Subdominio, Especie

# Registrando o modelo Projeto
class ProjetoAdmin(admin.ModelAdmin):
    list_display = ('id', 'tipo_area', 'tamanho_imovel', 'potencial_regeneracao_natural', 'dinamica_hidrica',
                    'pedregosidade_solo', 'estrutura_ecossistema', 'condicoes_solo', 'ocupacao_area', 'declividade')
    search_fields = ('tipo_area', 'tamanho_imovel')
    list_filter = ('tipo_area', 'tamanho_imovel')
    gis_geometry_field = 'geometry'

# Registrando o modelo Bioma
class BiomaAdmin(admin.ModelAdmin):
    list_display = ('fid', 'bioma', 'bioma_name', 'bioma_code')
    search_fields = ('bioma', 'bioma_name')
    list_filter = ('bioma',)
    gis_geometry_field = 'geometry'

# Registrando o modelo Subdominio
class SubdominioAdmin(admin.ModelAdmin):
    list_display = ('fid', 'bioma', 'subdominio')
    search_fields = ('bioma', 'subdominio')
    list_filter = ('bioma',)
    gis_geometry_field = 'geometry'

# Registrando o modelo Especie
class EspecieAdmin(admin.ModelAdmin):
    list_display = ('nome_cientifico', 'nomes_populares', 'bioma', 'conservacao', 'categorias_ecofisiologicas')
    search_fields = ('nome_cientifico', 'nomes_populares', 'bioma', 'habito', 'subdominio_list',
                    'fisionomias', 'conservacao', 'categorias_ecofisiologicas')
    list_filter = ('bioma', 'habito', 'subdominio_list', 'fisionomias', 'conservacao', 'categorias_ecofisiologicas')

# Registrando as classes de administração no Django Admin
admin.site.register(Projeto, ProjetoAdmin)
admin.site.register(Bioma, BiomaAdmin)
admin.site.register(Subdominio, SubdominioAdmin)
admin.site.register(Especie, EspecieAdmin)
