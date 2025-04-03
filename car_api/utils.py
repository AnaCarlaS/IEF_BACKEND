import csv
from pathlib import Path
from django.conf import settings

def car_dat_criacao_limite4mf():
    with open(Path(settings.DATA_DIR) / 'car_api/car_dat_criacao_limite4mf.csv', 'r') as arquivo:
        leitor_csv = csv.reader(arquivo)
        cod_imovel = set([linha[0] for linha in leitor_csv])
    return cod_imovel