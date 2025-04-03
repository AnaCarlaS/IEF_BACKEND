import pytest
import requests
import time

@pytest.fixture(scope="module")
def base_url():
    return "http://localhost:8030/ief-suporte/projeto/v1/create/"

@pytest.fixture
def valid_payload():
    return {
        "supressao_apos_2008": "nao",
        "tipo_area": "reserva_legal",
        "tamanho_imovel": "menor4mf_agri_familiar",
        "potencial_regeneracao_natural": "baixo",
        "dinamica_hidrica": "nao_alaga",
        "pedregosidade_solo": "baixo",
        "estrutura_ecossistema": "florestal",
        "condicoes_solo": "sem_sinais_erosao",
        "ocupacao_area": "areas_abandonadas",
        "declividade": "entre_0a25",
        "fatores_perturbacao": [
            "secas_prolongadas", "sujeito_incendios", "sujeito_geadas",
            "acesso_gado", "gramineas_exoticas", "arvores_exoticas"
        ],
        "geometry": {
            "type": "MultiPolygon",
            "coordinates": [
                [[
                    [-43.5230909, -20.34917], [-43.52344648, -20.34891736],
                    [-43.52369913, -20.34886121], [-43.524036, -20.34872085],
                    [-43.52457872, -20.34865535], [-43.52456937, -20.34850563],
                    [-43.5242325, -20.34857113], [-43.52408278, -20.34852435],
                    [-43.5239705, -20.34851499], [-43.52384885, -20.34860856],
                    [-43.52360556, -20.34873957], [-43.52333419, -20.34870214],
                    [-43.52320319, -20.3488425], [-43.52320319, -20.34899221],
                    [-43.5230909, -20.34917]
                ]]
            ]
        }
    }

def test_create_projeto_status200(base_url, valid_payload):
    """Testa se a API retorna 200 para um payload válido."""
    response = requests.post(base_url, json=valid_payload)
    assert response.status_code == 200

    data = response.json()
    assert "cadastro" in data
    assert "diagnostico" in data
    assert "metodo_recomendado" in data

    expected_keys = ["codigo_projeto", "data", "hora", "bioma_ibge", "bioma_subdominio", "subdominio", "centro_gleba"]
    for key in expected_keys:
        assert key in data["cadastro"]

def test_create_projeto_payload_invalido_status400(base_url):
    """Testa se a API retorna 400 para um payload inválido."""
    payload_invalido = {"tipo_area": "reserva_legal"}  # Payload incompleto
    response = requests.post(base_url, json=payload_invalido)
    assert response.status_code == 400

def test_create_projeto_performance_menor_0ponto5s(base_url, valid_payload):
    """Testa se a API responde em menos de 0.5s."""
    start_time = time.time()
    response = requests.post(base_url, json=valid_payload)
    elapsed_time = time.time() - start_time

    assert elapsed_time < 0.5, f"Teste de performance falhou, tempo {elapsed_time:.2f} segundos"

