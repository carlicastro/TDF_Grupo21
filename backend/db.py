import os
import mysql.connector

def get_connection():
    """
    Conectar a la base de datos usando mysql.connector
    """
    # Obtener credenciales de variables de entorno o valores por defecto
    DB_USER = os.getenv('DB_USER', 'root')
    DB_PASS = os.getenv('DB_PASS', '')
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_NAME = os.getenv('DB_NAME', 'hotel_db')
    
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME
    )