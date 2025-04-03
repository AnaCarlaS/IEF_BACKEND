import os
import pandas as pd
import geopandas as gpd
import json
from typing import Dict
from urllib.parse import urlencode
from django.contrib.gis.gdal import DataSource
from django.http import JsonResponse
from ninja import NinjaAPI
from .serializers import serialize_geojson
from .schemas import CarResponse, UpdateResponse
from .utils import car_dat_criacao_limite4mf


from django.conf import settings

os.environ["GDAL_HTTP_UNSAFESSL"] = "YES"
os.environ["GDAL_HTTP_TIMEOUT"] = "2"
os.environ["GDAL_HTTP_CONNECTTIMEOUT"] = "2"
os.environ["GDAL_HTTP_MAX_RETRY"] = "6"
os.environ["GDAL_HTTP_RETRY_DELAY"] = "1"

car_api = NinjaAPI(urls_namespace='car-api', version='1.0.0')

from car_etl.models import (
    AreaImovel1, Apps1, Apps2, Apps3, Apps4, Apps5, Apps6, Apps7,
    AreaConsolidada1, AreaConsolidada2, AreaPousio1, Hidrografia1,
    ReservaLegal1, ServidaoAdministrativa1, UsoRestrito1,
    VegetacaoNativa1, VegetacaoNativa2
)


cod_dat_criacao_limite4mf = car_dat_criacao_limite4mf()


@car_api.get("/car", response=CarResponse)
def car(request, cod_imovel: str):

    """
    Disponibiliza dados do CAR (Cadastro Ambiental Rural) oriundos do SICAR por código de imóvel (cod_imovel).

    Args:
        cod_imovel (str): Código do imóvel.

    Returns:
        dict: Feições do CAR: area_imovel, apps, area_consolidada, vegetacao_nativa, reserva_legal,
                              hidrografia, servidao_administrativa, uso_restrito, uso_restrito, area_pousio    
    """

    area_imovel_data = serialize_geojson(AreaImovel1, cod_imovel)
    if not area_imovel_data:
        return JsonResponse(
            {"detail": f"Código do imóvel '{cod_imovel}' não encontrado."},
            status=404
        )
    area_pousio_data = serialize_geojson(AreaPousio1, cod_imovel)
    hidrografia_data = serialize_geojson(Hidrografia1, cod_imovel)
    reserva_legal_data = serialize_geojson(ReservaLegal1, cod_imovel)
    servidao_administrativa_data = serialize_geojson(ServidaoAdministrativa1, cod_imovel)
    uso_restrito_data = serialize_geojson(UsoRestrito1, cod_imovel)

    apps_data = []
    for model in [Apps1, Apps2, Apps3, Apps4, Apps5, Apps6, Apps7]:
        data = serialize_geojson(model, cod_imovel)
        if data:
            apps_data.extend(data)
    
    area_consolidada_data = []
    for model in [AreaConsolidada1, AreaConsolidada2]:
        data = serialize_geojson(model, cod_imovel)
        if data:
            area_consolidada_data.extend(data)
    
    vegetacao_nativa_data = []
    for model in [VegetacaoNativa1, VegetacaoNativa2]:
        data = serialize_geojson(model, cod_imovel)
        if data:
            vegetacao_nativa_data.extend(data)
    
    response_data = {
        "area_imovel": area_imovel_data,
        "apps": apps_data,
        "area_consolidada": area_consolidada_data,
        "vegetacao_nativa": vegetacao_nativa_data,
        "reserva_legal": reserva_legal_data,
        "hidrografia": hidrografia_data,
        "servidao_administrativa": servidao_administrativa_data,
        "uso_restrito": uso_restrito_data,
        "area_pousio": area_pousio_data,
    }

    response_data = {k: v for k, v in response_data.items() if v}
    
    return JsonResponse(response_data, safe=False, status=200)


@car_api.get("/info_update") #, response=UpdateResponse)
def info_update(request, cod_imovel: str):

    """
    Datas de criação e atualização do CAR, oriundas do GeoServer do SICAR, por código de imóvel (cod_imovel)

    Args:
        cod_imovel (str): Código do imóvel.

    Returns:
        dict    
    """    
    # cql_filter = "cod_imovel IN ({})".format(",".join("'{}'".format(c) for c in cod_imoveis))
    # cod_imovel = "MG-3146107-B6490DFAF1C8422FA9F02B584C53286C"
    # GEOSERVER_SICAR_WFS_URL="https://geoserver.car.gov.br/geoserver/sicar/wfs"
    params = {
        "service": "WFS",
        "version": "1.1.0",
        "request": "GetFeature",
        "typeName": "sicar:sicar_imoveis_mg",
        "outputFormat": "application/json",
        "CQL_FILTER": f"cod_imovel='{cod_imovel}'",
        # "propertyName": "cod_imovel,status_imovel,dat_criacao,data_atualizacao,area,condicao,uf,municipio,cod_municipio_ibge,m_fiscal,tipo_imovel"
    }
    params_encode = urlencode(params, safe=":,()")
    
    wfs_url = f"{settings.GEOSERVER_SICAR_WFS_URL}?{params_encode}"
    try:
        wfs_data = DataSource(wfs_url)
    except:
        JsonResponse({'Falha': f'GeoServer do SICAR fora do ar...'}, status=500)
    layer = wfs_data[0]
    geometry = layer.get_geoms()[0]
    info_update_dict = {
        "cod_imovel": layer.get_fields("cod_imovel")[0],
        "ind_status": layer.get_fields("status_imovel")[0],
        "ind_tipo": layer.get_fields("tipo_imovel")[0],
        "dat_criacao": layer.get_fields("dat_criacao")[0].isoformat(),
        "data_atualizacao": layer.get_fields("data_atualizacao")[0].isoformat(),
        "des_condic": layer.get_fields("condicao")[0],
        "mod_fiscal": layer.get_fields("m_fiscal")[0],
        "num_area": layer.get_fields("area")[0],
        "municipio":layer.get_fields("municipio")[0],
        "geometry": geometry.json,
    }
    
    return info_update_dict

@car_api.get("/is_dat_limite_pra")#, response=Dict[str, float])
def is_dat_limite_pra(request, cod_imovel: str):

    """
    Datas de criação e atualização do CAR, oriundas do GeoServer do SICAR, por código de imóvel (cod_imovel)

    Args:
        cod_imovel (str): Código do imóvel.

    Returns:
        dict    
    """    
    imovel = AreaImovel1.objects.get(cod_imovel=cod_imovel)
    # print(cod_dat_criacao_limite4mf)
    if imovel.mod_fiscal < 4.0 or cod_imovel in cod_dat_criacao_limite4mf:
        return {'pode_solicitar_adesao_pra': 'sim', 'mod_fiscal': imovel.mod_fiscal}
    else:
        return {'pode_solicitar_adesao_pra': 'nao', 'mod_fiscal': imovel.mod_fiscal}
