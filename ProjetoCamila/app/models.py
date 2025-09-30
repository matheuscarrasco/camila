from pydantic import BaseModel
from datetime import datetime

class Dados(BaseModel):
    iddados: int
    variavel: str
    valor: str
    datahora: datetime

    class Config:
        orm_mode = True

class DadosCreate(BaseModel):
    variavel: str
    valor: str
  
