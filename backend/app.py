import os
from flask import Flask, jsonify
from sqlalchemy import create_engine, text

# Import model functions
from models import (
    obtener_todos_usuarios, obtener_todos_hospedajes, obtener_todas_reservas
)

# Crear la aplicación Flask
app = Flask(__name__)


def set_connection():
    """
    Conectar a la base de datos usando SQLAlchemy
    """
    # Obtener credenciales de variables de entorno o valores por defecto
    DB_USER = os.getenv('DB_USER', 'root')
    DB_PASS = os.getenv('DB_PASS', '')
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_NAME = os.getenv('DB_NAME', 'hotel_db')
    
    # Crear URL de conexión
    url = f"mysql+mysqlconnector://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
    engine = create_engine(url)
    
    # Test de conexión
    connection = engine.connect()
    return connection


def mostrar_registros(connection, query="SELECT * FROM usuarios;"):
    """
    Ejecutar consulta SQL simple
    """
    try:
        result = connection.execute(text(query))
        
        # Convertir resultado a lista simple
        registros = []
        for row in result:
            # Convertir cada fila a diccionario simple
            registro = {}
            for i, valor in enumerate(row):
                registro[f'columna_{i}'] = valor
            registros.append(registro)
        
        return registros
    except Exception as e:
        print(f"Error ejecutando consulta: {e}")
        raise


@app.route('/api/usuarios', methods=['GET'])
def listar_usuarios():
    connection = None
    try:
        connection = set_connection()
        usuarios = obtener_todos_usuarios(connection)
        return jsonify({'ok': True, 'data': usuarios}), 200
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 500
    finally:
        if connection:
            connection.close()


@app.route('/api/hospedajes', methods=['GET'])
def listar_hospedajes():
    connection = None
    try:
        connection = set_connection()
        hospedajes = obtener_todos_hospedajes(connection)
        return jsonify({'ok': True, 'data': hospedajes}), 200
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 500
    finally:
        if connection:
            connection.close()


@app.route('/api/reservas', methods=['GET'])
def listar_reservas():
    connection = None
    try:
        connection = set_connection()
        reservas = obtener_todas_reservas(connection)
        return jsonify({'ok': True, 'data': reservas}), 200
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 500
    finally:
        if connection:
            connection.close()


@app.route('/api/test-db', methods=['GET'])
def test_db():
    connection = None
    try:
        # Test de conexión usando el patrón set_connection
        connection = set_connection()
        # Creamos la query para ser ejecutada por la conexión
        query = "SELECT 1 as test, 'Conexión OK' as mensaje"
        result = mostrar_registros(connection, query)
        return jsonify({'ok': True, 'test': result}), 200
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 500
    finally:
        if connection:
            connection.close()


if __name__ == '__main__':
    app.run(debug=True)
