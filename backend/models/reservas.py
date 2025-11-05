"""
Funciones para manejar la tabla reservas
"""
from sqlalchemy import text


def obtener_todas_reservas(connection):
    """
    Obtener todas las reservas con nombres de usuario y hospedaje
    """
    query = """
        SELECT r.id_reserva, r.id_usuario, r.id_hospedaje, 
               r.fecha_checkin, r.fecha_checkout, r.cant_personas, 
               r.importe_total, r.estado,
               u.nombre as usuario_nombre, 
               h.nombre as hospedaje_nombre
        FROM reservas r
        LEFT JOIN usuarios u ON r.id_usuario = u.id_usuario
        LEFT JOIN hospedajes h ON r.id_hospedaje = h.id_hospedaje
    """
    result = connection.execute(text(query))
    
    # Convertir resultado a lista simple
    reservas = []
    for row in result:
        reserva = {
            'id_reserva': row[0],
            'id_usuario': row[1],
            'id_hospedaje': row[2],
            'fecha_checkin': row[3],
            'fecha_checkout': row[4], 
            'cant_personas': row[5],
            'importe_total': row[6],
            'estado': row[7],
            'usuario_nombre': row[8],
            'hospedaje_nombre': row[9]
        }
        reservas.append(reserva)
    
    return reservas