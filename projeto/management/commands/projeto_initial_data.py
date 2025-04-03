import json
from pathlib import Path
from django.core.management.base import BaseCommand
from django.db import transaction
from django.conf import settings
from django.contrib.gis.geos import GEOSGeometry
from projeto.models import Bioma, Subdominio, Especie

class Command(BaseCommand):
    help = 'Importa dados de arquivos CSV e GeoJSON e substitui completamente as tabelas.'

    def handle(self, *args, **kwargs):
        
        self.stdout.write(self.style.SUCCESS('Iniciando importação de dados...'))
        bioma_file_path = Path(settings.DATA_DIR) / 'projeto/bioma.geojson'
        subdominio_file_path = Path(settings.DATA_DIR) / 'projeto/subdominio.geojson'
        especie_file_path = Path(settings.DATA_DIR) / 'projeto/especie.json'
        
        with transaction.atomic():
            Bioma.objects.all().delete()
            self._import_bioma(bioma_file_path)
        
        with transaction.atomic():
            Subdominio.objects.all().delete()
            self._import_subdominio(subdominio_file_path)
        
        with transaction.atomic():
            Especie.objects.all().delete()
            self._import_especie(especie_file_path)

        self.stdout.write(self.style.SUCCESS('Importação concluída com sucesso e dados substituídos!'))
    
    def _import_bioma(self, file_path):
        
        """Função auxiliar para importar dados de um arquivo GeoJSON"""
        
        try:
            with open(file_path, 'r', encoding='utf-8') as geojsonfile:
                data = json.load(geojsonfile)
                for feature in data['features']:
                    properties = feature['properties']
                    geometry = GEOSGeometry(json.dumps(feature['geometry']))
                    geometry.transform(4674)
                    Bioma.objects.create(
                        fid=properties['fid'],
                        bioma=properties['bioma'],
                        bioma_name=properties['bioma_name'],
                        bioma_code=properties['bioma_code'],
                        geometry=geometry,
                    )

            self.stdout.write(self.style.SUCCESS(f'Arquivo GeoJSON: {file_path} importado com sucesso.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erro ao importar do GeoJSON ({file_path}): {e}.'))
            raise  # Relevanta a exceção para garantir o rollback da transação

    def _import_subdominio(self, file_path):
        
        """Função auxiliar para importar dados de um arquivo GeoJSON"""
        
        try:
            with open(file_path, 'r', encoding='utf-8') as geojsonfile:
                data = json.load(geojsonfile)
                for feature in data['features']:
                    properties = feature['properties']
                    geometry = GEOSGeometry(json.dumps(feature['geometry']))
                    geometry.transform(4674)
                    Subdominio.objects.create(
                        fid=properties['fid'],
                        bioma=properties['bioma'],
                        subdominio=properties['subdominio'],
                        subdominio_code=properties['subdominio_code'],
                        bioma_name=properties['bioma_name'],
                        bioma_code=properties['bioma_code'],
                        geometry=geometry,
                    )

            self.stdout.write(self.style.SUCCESS(f'Arquivo GeoJSON: {file_path} importado com sucesso.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erro ao importar do GeoJSON ({file_path}): {e}.'))
            raise  # Relevanta a exceção para garantir o rollback da transação

    def _import_especie(self, file_path):
        
        """Função auxiliar para importar dados de um arquivo JSON"""
        
        try:
            with open(file_path, 'r', encoding='utf-8') as json_file:
                data = json.load(json_file)
                for item in data:
                    Especie.objects.create(
                        bioma=item['bioma'],
                        bioma_name=item['bioma_name'],
                        nome_cientifico=item['nome_cientifico'],
                        codigo=item['codigo'],
                        habito=item['habito'],
                        distribuicao=item['distribuicao'],
                        subdominio_list=item['subdominio_list'],
                        fisionomias=item['fisionomias'],
                        conservacao=item['conservacao'],
                        nomes_populares=item['nomes_populares'],
                        categorias_ecofisiologicas=item['categorias_ecofisiologicas'],
                    )
            self.stdout.write(self.style.SUCCESS(f'Arquivo JSON: {file_path} importado com sucesso.'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erro ao importar o JSON ({file_path}): {e}'))
            raise