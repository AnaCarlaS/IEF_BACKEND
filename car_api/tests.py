import pytest
import requests
import time

@pytest.fixture(scope="module")
def base_url():
    # A URL base do seu servidor local
    return "http://localhost:8030/ief-suporte/car-api/v1/car"

def test_car_api_car_existe_status200(base_url):
    
    cod_imovel = "MG-3146107-AE08B0C6BB1740059D746996B00FE0B8"
    response = requests.get(base_url, params={"cod_imovel": cod_imovel})
    assert response.status_code == 200
    
    area_imovel = response.json()["area_imovel"][0]
    
    expected_data = {
        "cod_imovel": "MG-3146107-AE08B0C6BB1740059D746996B00FE0B8",
        "num_area": 51.625,
        "municipio": "Ouro Preto"
    }
    assert area_imovel["properties"]["cod_imovel"] == expected_data["cod_imovel"]
    assert area_imovel["properties"]["num_area"] == expected_data["num_area"]
    assert area_imovel["properties"]["municipio"] == expected_data["municipio"]

def test_car_api_car_nao_existe_status404(base_url):
    
    cod_imovel_invalido = "INVALIDO-0000000000000000"
    response = requests.get(base_url, params={"cod_imovel": cod_imovel_invalido})
    assert response.status_code == 404
    
    expected_message = {"detail": f"Código do imóvel '{cod_imovel_invalido}' não encontrado."}
    assert response.json() == expected_message

def test_car_api_performance_menor_0ponto5s(base_url):
    
    start_time = time.time()
    
    cod_imovel = "MG-3146107-AE08B0C6BB1740059D746996B00FE0B8"
    response = requests.get(base_url, params={"cod_imovel": cod_imovel})
    
    elapsed_time = time.time() - start_time
    
    assert elapsed_time < 0.5, f"Teste de performance falhou, tempo {elapsed_time:.2f} segundos"