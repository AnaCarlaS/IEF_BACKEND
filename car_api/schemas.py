from pydantic import BaseModel
from typing import List, Optional

class Geometry(BaseModel):
    type: str
    coordinates: List[List[List[float]]] 

class Properties(BaseModel):
    cod_imovel: str
    cod_tema: str
    nom_tema: str
    mod_fiscal: float
    num_area: Optional[float] = None
    ind_status: str
    ind_tipo: Optional[str] = None
    des_condic: str
    municipio: Optional[str] = None
    cod_estado: Optional[str] = None
    pk: int

class GeoJSON(BaseModel):
    type: str
    id: int
    properties: Properties
    geometry: Geometry


class CarResponse(BaseModel):
    area_imovel: List[GeoJSON]
    apps: List[GeoJSON]
    tema_n: List[GeoJSON]

class UpdateResponse(BaseModel):
    cod_imovel: str
    ind_status: str
    ind_tipo: str
    dat_criacao: str
    data_atualizacao: str
    des_condic: str
    mod_fiscal: float
    num_area: float
    municipio:str