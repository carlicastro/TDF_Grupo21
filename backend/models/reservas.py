"""
Funciones para manejar la tabla reservas con sesiones Flask
"""
from flask import Blueprint, jsonify, request, session
from db import get_connection
from .auth import esta_logueado, es_admin

reservas_bp = Blueprint('reservas', __name__)

# Pre: Usuario debe estar logueado como admin
# Post: Si es admin, retorna lista JSON de todas las reservas. Si no es admin, error 403
@reservas_bp.route("/", methods=["GET"])
def get_reservas():
    # Ver todas las reservas (solo admin)
    if esta_logueado() == False:
        return jsonify({'error': 'Debes estar logueado'}), 401
    if es_admin() == False:
        return jsonify({'error': 'Solo para admin'}), 403
    
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM reservas ORDER BY fecha_creacion DESC")
    reservas = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(reservas)

# Pre: reserva_id debe ser un entero válido
# Post: Si reserva existe, retorna datos JSON. Si no existe, error 404
@reservas_bp.route("/<int:reserva_id>", methods=["GET"])
def get_reserva_by_id(reserva_id):
    # Ver una reserva
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM reservas WHERE id_reserva = %s", (reserva_id,))
    reserva = cursor.fetchone()
    cursor.close()
    conn.close()
    
    # Si no existe la reserva
    if reserva is None:
        return jsonify({"error": "No se encontró la reserva"}), 404
    
    return jsonify(reserva)

# Pre: Usuario logueado, user_id debe coincidir con el usuario de la sesión
# Post: Si es el mismo usuario, retorna sus reservas JSON. Si no coincide, error 403
@reservas_bp.route("/usuario/<int:user_id>", methods=["GET"])
def get_reservas_usuario(user_id):
    # Ver mis reservas
    if esta_logueado() == False:
        return jsonify({'error': 'Debes estar logueado'}), 401
    
    # Solo puedo ver mis propias reservas
    mi_id = session.get('user_id')
    if mi_id != user_id:
        return jsonify({'error': 'Solo puedes ver tus propias reservas'}), 403
    
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM reservas WHERE id_usuario = %s", (user_id,))
    mis_reservas = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return jsonify(mis_reservas)

# Pre: Usuario logueado, JSON con id_hospedaje, fechas válidas y cantidad personas
# Post: Si datos válidos, reserva creada en BD con estado confirmada. Si faltan datos, error 400
@reservas_bp.route("/", methods=["POST"])
def crear_reserva():
    # Hacer una reserva
    if esta_logueado() == False:
        return jsonify({'error': 'Debes estar logueado'}), 401
    
    data = request.get_json()
    
    # Datos básicos
    mi_id = session.get('user_id')
    hospedaje = data.get('id_hospedaje')
    checkin = data.get('fecha_checkin')
    checkout = data.get('fecha_checkout')
    personas = data.get('cant_personas')
    precio = data.get('importe_total', 0)
    
    # Validar que no falten datos
    if not hospedaje or not checkin or not checkout or not personas:
        return jsonify({"error": "Faltan datos obligatorios"}), 400
    
    # Guardar en base de datos
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO reservas (id_usuario, id_hospedaje, fecha_checkin, fecha_checkout, cant_personas, importe_total, estado)
        VALUES (%s, %s, %s, %s, %s, %s, 'confirmada')
    """, (mi_id, hospedaje, checkin, checkout, personas, precio))
    
    conn.commit()
    nueva_reserva_id = cursor.lastrowid
    cursor.close()
    conn.close()
    
    return jsonify({"success": True, "message": "Reserva creada", "id_reserva": nueva_reserva_id})

# Pre: Usuario admin logueado, reserva_id de reserva existente
# Post: Si reserva existe y es admin, reserva eliminada de BD. Si no existe, error 404
@reservas_bp.route("/<int:reserva_id>", methods=["DELETE"])
def eliminar_reserva(reserva_id):
    # Borrar una reserva (solo admin)
    if esta_logueado() == False:
        return jsonify({'error': 'Debes estar logueado'}), 401
    if es_admin() == False:
        return jsonify({'error': 'Solo para admin'}), 403
    
    conn = get_connection()
    cursor = conn.cursor()
    
    # Verificar si existe
    cursor.execute("SELECT * FROM reservas WHERE id_reserva = %s", (reserva_id,))
    reserva = cursor.fetchone()
    
    if reserva is None:
        cursor.close()
        conn.close()
        return jsonify({"error": "Reserva no existe"}), 404
    
    # Borrar reserva
    cursor.execute("DELETE FROM reservas WHERE id_reserva = %s", (reserva_id,))
    conn.commit()
    cursor.close()
    conn.close()
    
    return jsonify({"success": True, "message": "Reserva eliminada"})