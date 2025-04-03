import pytest
import requests

@pytest.fixture(scope="module")
def base_url():
    # A URL base do seu servidor local
    return "http://localhost:8030/ief-suporte/car-etl/v1/process_status"

def test_car_etl_disponivel_status200(base_url):
    
    response = requests.get(base_url)
    assert response.status_code == 200
    
# 
def test_car_etl_proxima_atualizacao_menor7dias(base_url):
    
    response = requests.get(base_url)
    response_data = response.json()
    time_next_schedule = response_data["task_info"][0]["time_next_schedule"]
    if "day" in time_next_schedule:
        days_until_next_schedule = int(time_next_schedule.split(" ")[0])
        assert days_until_next_schedule <= 7, f"A próxima execução é em mais de 7 dias: {days_until_next_schedule} dias."


