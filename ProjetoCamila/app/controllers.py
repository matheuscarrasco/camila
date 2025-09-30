#projeto feito por: samuka-ang

from fastapi import APIRouter, HTTPException
from typing import List
from app.database import get_db_connection
from app.models import Dados, DadosCreate

router = APIRouter()

@router.get("/dados", response_model=List[Dados])
def get_dados():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM dados"
    
    try:
        cursor.execute(query)
        rows = cursor.fetchall()
        dados = [Dados(**row) for row in rows]
        return dados

    finally:
        cursor.close()
        connection.close()

@router.post("/dados", response_model=Dados)
def create_dado(dados: DadosCreate):
    connection = get_db_connection()
    cursor = connection.cursor()

    query = """
        INSERT INTO dados (variavel, valor)
        VALUES (%s, %s)
    """
    values = (dados.variavel, dados.valor)

    try:
        cursor.execute(query, values)
        connection.commit()
        return dados
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao inserir dados: {e}")
    finally:
        cursor.close()
        connection.close()
