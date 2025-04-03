import json
from datetime import datetime
from urllib.parse import parse_qs
import uuid
from django.shortcuts import render
from django.contrib.gis.geos import GEOSGeometry
from django.http import JsonResponse
from rest_framework import status
from .models import Projeto, Bioma, Especie, Subdominio
from .serializers import ProjetoSerializer
from .utils import load_comb_diagnostico, load_detalhamento_metodos, load_trat_pertubacao
from .services import mapa_view

comb_dicts = load_comb_diagnostico()
detalhes_metodo = load_detalhamento_metodos()
trat_pertubacao = load_trat_pertubacao()


def projeto_template(request):
    return render(request, 'projeto_template.html')


def buscar_recomendacao(inputs):
    for item in comb_dicts:
        if all(item[key] == value for key, value in inputs.items()):
            return item["recomendacao"]
    return "Nenhuma recomendação encontrada para as condições fornecidas."


def projeto_html(request):
        
        request_body = request.body.decode('utf-8')
        form_data = parse_qs(request_body)
        json_payload = form_data.get('jsonPayload', [''])[0]  # O valor é uma lista, pegamos o primeiro item
        data = json.loads(json.loads(json_payload))
        print(data)
        card_metodo = data.pop('card_metodo')
        print(card_metodo)
        serializer = ProjetoSerializer(data=data)
        
        if serializer.is_valid():

            properties = serializer.data.get("properties")
            essencial_properties = {"supressao_apos_2008", "tipo_area", "tamanho_imovel",
                                    "potencial_regeneracao_natural", "dinamica_hidrica",
                                    "pedregosidade_solo", "estrutura_ecossistema"}
            filtered_properties = {k: properties[k] for k in essencial_properties if k in properties}
            list_metodo = [card_metodo] # buscar_recomendacao(filtered_properties).splitlines()

            filtered_detalhes_metodo = {m: detalhes_metodo[m] for m in list_metodo if m in detalhes_metodo}
            geometry_gleba = serializer.data.get("geometry")
            geometry_json = json.dumps(geometry_gleba)
            geometry_projeto = GEOSGeometry(geometry_json)

            map_html, center = mapa_view(geometry_gleba.get("coordinates"))

            subdominio_intersecao = (
                Subdominio.objects
                .filter(geometry__intersects=geometry_projeto)
                .values('subdominio', 'bioma_name')
                .first()
            )
            if subdominio_intersecao:
                especies = (
                    Especie.objects
                    .filter(subdominio_list__contains=[subdominio_intersecao['subdominio']])
                    .values('nome_cientifico', 'nomes_populares', 'habito', 'conservacao',
                            'categorias_ecofisiologicas', 'subdominio_list')
                )
            else:
                return JsonResponse({'error': 'A geometria (polígono) não intersecciona com MG.'}, status=status.HTTP_400_BAD_REQUEST)
            
            bioma_intersecoes = (
                Bioma.objects
                .filter(geometry__intersects=geometry_projeto)
                .values('bioma_name')
                .first()
            )
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
            trat_adicional = [trat_pertubacao[value] for value in properties["fatores_perturbacao"]]
            
            contexto = {
                "cadastro": cadastro,
                "diagnostico": data,
                "metodo_recomendado": list_metodo,
                "tratamento_adicional": trat_adicional,
                "metodo_detalhamento": list(filtered_detalhes_metodo.values()),
                "especies": especies,
                "map_html": map_html,
            }
            return render(request, 'projeto.html', contexto)
        
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

