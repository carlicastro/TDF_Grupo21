"""
Funciones para manejar la tabla usuarios
"""
from sqlalchemy import text


def obtener_todos_usuarios(connection):
    """
    Obtener todos los usuarios
    """
    query = "SELECT * FROM usuarios"
    result = connection.execute(text(query))
    
    # Convertir resultado a lista simple
    usuarios = []
    for row in result:
        usuario = {
            'id_usuario': row[0],
            'nombre': row[1], 
            'email': row[2],
            'password': row[3],
            'telefono': row[4],
            'rol': row[5]
        }
        usuarios.append(usuario)
    
    return usuarios