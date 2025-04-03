# Serviços de Suporte para o Sistema Florescer  

## Serviço com as aplicações:

#### 1. CAR-ETL: Aplicação robusta para gerenciar a obtenção do grande volume de dados CAR do SICAR  
#### 2. CAR-API: Aplicação para disponibilizar dados do CAR com elevado desempenho e disponibilidade contínua  
#### 3. PROJETO: Aplicação para criar projetos de recomposição da vegetação, alinhados às necessidades reais  


## Essencial
Este diretório apresenta a implementação da aplicação (CAR-ETL) para gerenciar a obtenção da base de dados espacial do estado de Minas Gerais dos dados públicos do Sistema Nacional de Cadastro Ambiental Rural (SICAR). Trata-se de uma automatização de uma série de tarefas, do download dos dados (no momento feita de forma manual no SICAR) em formato shapefile (extract), inserção desses dados num banco de dados Postgres (load), e execução de algumas operações espaciais (transform), como a obteção do potencial de regeneração natural (baseada em proximidade de polígonos com vegetação nativa, ainda não implementado). Esses dados podem ser acessados via endpoints da aplicação CAR-API. Além disso, o sistema inclui uma aplicação voltada para a criação de projetos de recomposição da vegetação. É utilizado o diagnóstico ambiental da área a ser recomposta como referência para criar os projetos.


## Tecnologias 

Python 3.11 + dependências (requirements.txt)  
Postegres 16 + Postgis 3.4


## Deploy
### Se conteinerização com Docker:  
Na raíz da projeto `suporte` executar o comando:
```
# Build e execução em background
docker-compose up --build -d 

# Acompanhar os logs da execução
docker-compose logs -f
```
Obs: O host definido nas variáveis de ambiente (arquivo .env) deve ser o mesmo do nome do serviço do banco de dados postgres no arquivo docker-compose.yml. Exemplo: `DB_HOST=suporte_postgres_service`.

### Se stand-alone (sem Docker):  
Na raíz da projeto `suporte` executar o comando:
```
sudo apt-get update && apt-get install
sudo apt-get install binutils libproj-dev gdal-bin

# recomenda-se criar um ambiente virtual (com venv, por exemplo) do Python 3.11
python3 -m venv .venv_suporte
source .venv_suporte/bin/activate

pip install -r requirements.txt

# depois de subir o banco de dados
python manage.py migrate

# executar com manage.py do Django
python manage.py runserver

# ou subir a aplicação no servidor gunicorn de forma explicita
gunicorn --workers 3 --bind 0.0.0.0:8030 core.wsgi:application
```
Obs: O host definido nas variáveis de ambiente (arquivo .env) deve ser localhost. Exemplo: `DB_HOST=localhost`.  



### Exemplo de arquivo de variáveis de ambiente (.env):

Exemplo para ambiente de desenvolvimento, evitar essas credenciais de DB em produção.

DB_HOST=suporte_postgres_service se fizer o deploy com docker-compose.yml.

DB_HOST=localhost se fizer o deploy stand-alone.

FOLDER_CAR deve apresentar um caminho válido para os dados zip do CAR, para testes pode-se utilizar a porção de dados de teste na raiz do projeto em: ./suporte/data/car_etl/folder_car

Para produção utilize DEBUG=False

```
DEBUG=True
DB_HOST=suporte_postgres_service
DB_PORT=5432
DB_PORT_DOCKER=5436
DB_NAME=suporte_db
DB_USER=postgres
DB_PASSWORD=
DB_SSLMODE=
DB_SCHEMA=public
DEFAULT_SCHEDULE=sat,weekly,22:00
FOLDER_CAR=./suporte-service/data/car_etl/folder_car
TEMA_CAR=AREA_IMOVEL,APPS,AREA_CONSOLIDADA,AREA_POUSIO,HIDROGRAFIA,RESERVA_LEGAL,SERVIDAO_ADMINISTRATIVA,USO_RESTRITO,VEGETACAO_NATIVA
GEOSERVER_SICAR_WFS_URL=https://geoserver.car.gov.br/geoserver/sicar/wfs
```

### Exemplo de uso dos endpoints das aplicações

#### 1. Exemplos de uso dos endpoints da aplicação CAR-API:  

Dados do CAR, oriundos do SICAR, por código de imóvel (cod_imovel), com o endpoint car:  
https://florescer.inovação.dev.br/ief-suporte/car-api/v1/car?cod_imovel=MG-3146107-AE08B0C6BB1740059D746996B00FE0B8  

Dados da Área Imóvel do CAR atualizados, oriundas do GeoServer do SICAR, por código de imóvel (cod_imovel), com o endpoint info_update:  
https://florescer.inovação.dev.br/ief-suporte/car-api/v1/info_update?cod_imovel=MG-3146107-AE08B0C6BB1740059D746996B00FE0B8  

Verificação quanto a data limite de inscrição no CAR para solicitar adesão ao PRA, por código de imóvel (cod_imovel), com o endpoint is_dat_limite_pra:  
https://florescer.inovação.dev.br/ief-suporte/car-api/v1/is_dat_limite_pra?cod_imovel=MG-3146107-AE08B0C6BB1740059D746996B00FE0B8  

#### 2. Exemplos de uso dos endpoints da aplicação CAR-ETL:  

Modificar agendamento do processo ETL de atualização dos dados do CAR, com o endpoint modify_schedule:  
https://florescer.inovação.dev.br/ief-suporte/car-etl/v1/modify_schedule?days_of_week=sat&frequency=weekly&time_of_day=23:30  

Executar processo ETL de atualização dos dados do CAR agora, com o endpoint run_now:  
https://florescer.inovação.dev.br/ief-suporte/car-etl/v1/run_now  

Cancelar processo ETL de atualização dos dados do CAR, com o endpoint cancel_process:  
https://florescer.inovação.dev.br/ief-suporte/car-etl/v1/cancel_process?confirm=yes  

Ver status do processo ETL de atualização e status dos dados do CAR no banco de dados, com o endpoint process_status:  
https://florescer.inovação.dev.br/ief-suporte/car-etl/v1/process_status  

#### 3. Exemplos de uso dos endpoints da aplicação PROJETO:  

Criar projeto de recomposição da vegetação de acordo com o diagnóstico, com o endpoint create:  
https://florescer.inovação.dev.br/ief-suporte/projeto/v1/create/  

Demonstração de uma requisição com o fetch do JavaScript:  

```
const payload = {
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
    "fatores_perturbacao": ["secas_prolongadas", "sujeito_incendios",
    "sujeito_geadas", "acesso_gado", "gramineas_exoticas", "arvores_exoticas"],
    "geometry": {
    "type": "MultiPolygon",
    "coordinates": [ [ [ [ -43.5230909, -20.34917 ], [ -43.52344648, -20.34891736 ],
    [ -43.52369913, -20.34886121 ], [ -43.524036, -20.34872085 ], [ -43.52457872, -20.34865535 ],
    [ -43.52456937, -20.34850563 ], [ -43.5242325, -20.34857113 ], [ -43.52408278, -20.34852435 ],
    [ -43.5239705, -20.34851499 ], [ -43.52384885, -20.34860856 ], [ -43.52360556, -20.34873957 ],
    [ -43.52333419, -20.34870214 ], [ -43.52320319, -20.3488425 ], [ -43.52320319, -20.34899221 ],
    [ -43.5230909, -20.34917 ] ] ] ]
    }
};
const requestOptions = {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
};
fetch("https://florescer.inovação.dev.br/ief-suporte/projeto/v1/create/", requestOptions)
    .then((response) => response.text())
    .then((result) => console.log(result))
    .catch((error) => console.error(error));
```


Interface gráfica (template) para facilitar as execuções de teste de criar projeto de recomposição da vegetação, com o endpoint template:  
https://florescer.inovação.dev.br/ief-suporte/projeto/v1/template