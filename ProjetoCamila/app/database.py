import mysql.connector
from dotenv import load_dotenv
import os
import logging

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

def get_db_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

def save_to_database(data):
    connection = get_db_connection()
    cursor = connection.cursor()

    if "variavel" not in data or "valor" not in data:
        logging.error("Dados inválidos")
        return

    variavel = data["variavel"]
    valor = data["valor"]

    query = """
        INSERT INTO dados (variavel, valor)
        VALUES (%s, %s) 
    """
    values = (variavel, valor)

    try:
        cursor.execute(query, values)
        connection.commit()
        logging.info(f"Dados inseridos: {data}")
    except Exception as e:
        logging.error(f"Erro ao inserir dados: {e}")
    finally:
        cursor.close()
        connection.close()
