"""
Funciones para manejar la tabla hospedajes
"""
from sqlalchemy import text


def obtener_todos_hospedajes(connection):
    """
    Obtener todos los hospedajes
    """
    query = "SELECT * FROM hospedajes"
    result = connection.execute(text(query))
    
    # Convertir resultado a lista simple
    hospedajes = []
    for row in result:
        hospedaje = {
            'id_hospedaje': row[0],
            'nombre': row[1],
            'descripcion': row[2], 
            'tipo': row[3],
            'precio_noche': row[4],
            'ubicacion': row[5],
            'capacidad_max': row[6],
            'disponible': row[7]
        }
        hospedajes.append(hospedaje)
    
    return hospedajes