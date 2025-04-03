import pandas as pd
from django.conf import settings
from pathlib import Path

def load_comb_diagnostico():
    file_path = Path(settings.DATA_DIR) / 'projeto/combinacoes_metodos.csv'
    df = pd.read_csv(file_path)
    comb_dicts = df.to_dict(orient='records')
    return comb_dicts

# TODO: aparentemente não é necessário essa manobra de cache.
detalhes_metodo_cache = None
def load_detalhamento_metodos():

    global detalhes_metodo_cache
    
    if detalhes_metodo_cache is None:
        
        file_path = Path(settings.DATA_DIR) / 'projeto/detalhamento_metodos.xlsx'
        cronograma = pd.read_excel(file_path, sheet_name='cronograma')
        descricao = pd.read_excel(file_path, sheet_name='descricao')
        descricao = descricao.set_index(descricao['recomendacao'])
        def fun_etapas(recom_grup):
            etapas_detalhes = []
            for i, (etapa_i, etapa_grup) in enumerate(recom_grup.groupby('etapa', sort=False)):
                etapas_detalhes.append(
                    {
                        'etapa_num': i+1,
                        'etapa': etapa_grup.etapa.iloc[0],
                        'sub_etapa': [{
                            'etapa': row.etapa, 
                            'sub_etapa': row.sub_etapa,
                            'inicio': row.inicio, 
                            'fim': row.fim, 
                        } for row in etapa_grup.itertuples()]
                    }
                )
            return etapas_detalhes

        detalhes = {}
        for recom, recom_grup in cronograma.groupby('recomendacao', sort=False):
            detalhes[recom] = {
                'metodo': recom,
                'recomendacao_code': descricao.loc[recom]['recomendacao_code'],
                'titulo': descricao.loc[recom]['titulo'],
                'resumo': descricao.loc[recom]['resumo'],
                'card': descricao.loc[recom]['card'],
                'descricao': descricao.loc[recom]['descricao'],
                'atividades': descricao.loc[recom]['atividades'],
                'cronograma': fun_etapas(recom_grup)
            }
    return detalhes

def load_trat_pertubacao():
    return {
    "secas_prolongadas": "A recuperação em áreas afetadas por SECAS prolongadas exige a implementação de técnicas de conservação de água, como o plantio de cobertura do solo e até mesmo o uso de irrigação em periodos críticos de escasses hídrica, especificamente nos estágios iniciais de desenvolvimento de mudas..",
    "sujeito_incendios": "Em áreas propensas a INCÊNDIOS, é fundamental a criação de faixas de proteção contra fogo, como aceiros, pode ajudar a reduzir os riscos de incêndio. Práticas de manejo de combustíveis, como controle de vegetação e monitoramento de áreas de risco, também são essenciais.",
    "sujeito_geadas": "Em áreas afetadas por GEADAS, é recomendado o plantio de espécies nativas e adaptadas às condições climáticas regionais que possam resistir a baixas temperaturas. Além disso, a utilização de barreiras naturais ou artificiais contra o vento pode ajudar a reduzir os danos causados por geadas intensas.",
    "acesso_gado": "Para áreas com acesso de GADO, é importante a instalação de cercas ou barreiras físicas para impedir o acesso do gado à área de recuperação. Além disso, é recomendado o manejo adequado do gado nas áreas circundantes, promovendo o controle da pastagem e evitando o sobrepastoreio nas áreas de recuperação.",
    "gramineas_exoticas": "A presença de GRAMÍNEAS EXÓTICAS pode ser um fator competitivo para as espécies nativas. O manejo de gramíneas exóticas inclui sua remoção mecânica ou com o uso de herbicidas seletivos, seguido pelo plantio de espécies nativas que possam competir com essas gramíneas. O monitoramento constante é necessário para evitar que as gramíneas exóticas se espalhem novamente.",
    "arvores_exoticas": "A presença de ÁRVORES EXÓTICAS pode ser prejudicial à regeneração da vegetação nativa, pois elas podem competir por recursos e alterar as condições ambientais. O controle de árvores exóticas pode ser feito por meio da remoção manual ou mecânica das árvores invasoras. Além disso, deve-se realizar o monitoramento  para garantir que não haja rebrota de espécies exóticas."
}
