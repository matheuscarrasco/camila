#projeto feito por: samuka-ang

import paho.mqtt.client as mqtt
import json
import mysql.connector
import logging
from dotenv import load_dotenv
import os

load_dotenv()

MQTT_HOST = os.getenv("MQTT_HOST", " 1ce4694cef1a4e389f05e446b6a52cc6.s1.eu.hivemq.cloud")
MQTT_PORT = int(os.getenv("MQTT_PORT", 8883))
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "#")
MQTT_USERNAME = os.getenv("MQTT_USERNAME", "smart40n1")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD", "iOTC39Mc1dLg")

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "camila")
    )

def save_to_database(data):
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        query = "INSERT INTO dados (variavel, valor) VALUES (%s, %s)"
        values = (data["variable"], data["value"])
        cursor.execute(query, values)
        connection.commit()
        logging.info("Dados inseridos no banco de dados com sucesso.")
    except mysql.connector.Error as err:
        logging.error(f"Erro ao salvar dados no banco de dados: {err}")
    finally:
        cursor.close()
        connection.close()

def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        logging.info(f"Mensagem recebida: {data}")
        save_to_database(data)
    except Exception as e:
        logging.error(f"Erro ao processar mensagem: {e}")

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logging.info("Conectado ao broker MQTT com sucesso!")
        client.subscribe(MQTT_TOPIC)
    else:
        logging.error(f"Falha ao conectar ao broker MQTT. Código de erro: {rc}")

def start_mqtt():
    client = mqtt.Client()
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    client.on_connect = on_connect
    client.on_message = on_message
    try:
        client.tls_set()
        client.connect(MQTT_HOST, MQTT_PORT, 60)
        client.loop_forever()
    except Exception as e:
        logging.error(f"Erro ao conectar ao broker MQTT: {e}")

if __name__ == "__main__":
    start_mqtt()
