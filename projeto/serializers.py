from rest_framework_gis.serializers import GeoFeatureModelSerializer
from .models import Projeto

class ProjetoSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Projeto
        geo_field = 'geometry'
        fields = [
            'supressao_apos_2008', 'tipo_area', 'tamanho_imovel',
            'potencial_regeneracao_natural', 'dinamica_hidrica',
            'pedregosidade_solo', 'estrutura_ecossistema', 'condicoes_solo',
            'ocupacao_area', 'declividade', 'fatores_perturbacao', 'geometry'
        ]
