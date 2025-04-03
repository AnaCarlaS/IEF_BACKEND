import json
import time
from datetime import datetime
import uuid
from django.shortcuts import render
from django.contrib.gis.db.models.functions import Intersection, Area
from django.contrib.gis.geos import GEOSGeometry
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Projeto, Bioma, Especie, Subdominio
from .serializers import ProjetoSerializer
from .utils import load_comb_diagnostico, load_detalhamento_metodos, load_trat_pertubacao

from .services import normalize_polygon, get_bounds_and_center

comb_dicts = load_comb_diagnostico()
detalhes_metodo = load_detalhamento_metodos()
trat_pertubacao = load_trat_pertubacao()

def home_projeto(request):
    return render(request, 'home_projeto.html')

def buscar_recomendacao(inputs):
    for item in comb_dicts:
        if all(item[key] == value for key, value in inputs.items()):
            return item["recomendacao"]
    return "Nenhuma recomendação encontrada para as condições fornecidas."

class CriarProjetoView(APIView):
    
    @swagger_auto_schema(
        request_body=ProjetoSerializer,
        responses={200: ProjetoSerializer, 400: openapi.Response('Erro de envio dos dados.')},
        operation_description="Criação de um novo projeto de recomposição da vegetação.",
    )
    
    def post(self, request):
        start_time = time.time()  # Início do cronômetro

        # Inicializa um dicionário para armazenar os tempos de execução
        timing_data = {}

        serializer = ProjetoSerializer(data=request.data)
        
        if serializer.is_valid():
            # Tempo de validação do serializer
            timing_data['Serializer Validation'] = time.time() - start_time

            # Propriedades essenciais
            start_time = time.time()  # Reinicia o cronômetro
            properties = serializer.data.get("properties")
            essencial_properties = {"supressao_apos_2008", "tipo_area", "tamanho_imovel",
                                    "potencial_regeneracao_natural", "dinamica_hidrica",
                                    "pedregosidade_solo", "estrutura_ecossistema"}
            filtered_properties = {k: properties[k] for k in essencial_properties if k in properties}
            list_metodo = buscar_recomendacao(filtered_properties).splitlines()
            timing_data['Filter Properties and Recommendation'] = time.time() - start_time

            # Detalhamento do método
            start_time = time.time()
            filtered_detalhes_metodo = {m: detalhes_metodo[m] for m in list_metodo if m in detalhes_metodo}
            timing_data['Detalhamento do Método'] = time.time() - start_time

            # Geometria do projeto
            start_time = time.time()
            geometry_gleba = serializer.data.get("geometry")
            geometry_json = json.dumps(geometry_gleba)
            geometry_projeto = GEOSGeometry(geometry_json)

            polygon_coords = normalize_polygon(geometry_gleba.get("coordinates"))
            _, center = get_bounds_and_center(polygon_coords)
            timing_data['Convert Geometry'] = time.time() - start_time

            # Interseção com subdomínios
            start_time = time.time()
            subdominio_intersecao = (
                Subdominio.objects
                .filter(geometry__intersects=geometry_projeto)
                .values('subdominio', 'bioma_name')
                .first()
                # .annotate(intersecao=Intersection('geometry', geometry_projeto))
                # .annotate(area_intersecao=Area('intersecao'))
                # .order_by('-area_intersecao')
            )
            timing_data['Subdomínio Intersection'] = time.time() - start_time

            if subdominio_intersecao:
                start_time = time.time()
                especies = (
                    Especie.objects
                    .filter(subdominio_list__contains=[subdominio_intersecao['subdominio']])
                    .values('nome_cientifico', 'nomes_populares', 'habito', 'conservacao',
                            'categorias_ecofisiologicas', 'subdominio_list')
                )
                timing_data['Fetch Especies'] = time.time() - start_time
            else:
                return Response({'error': 'A geometria (polígono) não intersecciona com MG.'}, status=status.HTTP_400_BAD_REQUEST)
            
            # Interseção com biomas
            start_time = time.time()
            bioma_intersecoes = (
                Bioma.objects
                .filter(geometry__intersects=geometry_projeto)
                .values('bioma_name')
                .first()
            )
            timing_data['Bioma Intersection'] = time.time() - start_time
            
            start_time = time.time()
            data_hora = datetime.now()
            cadastro = {
                "codigo_projeto": uuid.uuid4().hex.upper(),
                "data": data_hora.strftime("%d/%m/%Y"),
                "hora": data_hora.strftime("%H:%M:%S"),
                "bioma_ibge": bioma_intersecoes['bioma_name'],
                "bioma_subdominio": subdominio_intersecao['bioma_name'],
                "subdominio": subdominio_intersecao['subdominio'],
                "centro_gleba": center,
            }
            timing_data['Prepare Cadastro'] = time.time() - start_time
            
            # Adicionais e recomendação final
            start_time = time.time()
            trat_adicional = [trat_pertubacao[value] for value in properties["fatores_perturbacao"]]
            recomendacao = {
                "cadastro": cadastro,
                "diagnostico": properties,
                "metodo_recomendado": list_metodo,
                "tratamento_adicional": trat_adicional,
                "metodo_detalhamento": list(filtered_detalhes_metodo.values()),
                "especies": especies,
            }
            
            timing_data['Prepare Recomendation'] = time.time() - start_time
            
            # Tempo total
            timing_data['Total Execution Time'] = sum(timing_data.values())

            # Imprime os tempos de execução
            print("\n--- Tempos de Execução ---")
            for task, duration in timing_data.items():
                print(f"{task}: {duration:.4f} segundos")
            
            # print(list(filtered_detalhes_metodo.values()))
            # print(filtered_detalhes_metodo)
            return Response(recomendacao, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

