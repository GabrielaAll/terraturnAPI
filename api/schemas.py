from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class UserCreate(BaseModel):
    nome: str
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    nome: str
    email: str
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class PropriedadeCreate(BaseModel):
    property_id_slug: str
    nome_propriedade: str
    municipio: str
    latitude: float
    longitude: float
    tamanho_hectares: float
    tipo_solo: Optional[str] = None
    priorities: List[str] = []

class AnaliseRequest(BaseModel):
    property_id: int
    cultura_candidata: str
