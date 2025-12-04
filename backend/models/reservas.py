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
    cursor.execute("""
        SELECT * FROM reservas 
        ORDER BY fecha_creacion DESC
    """)
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

# Pre: Usuario logueado, JSON con id_hospedaje, fechas válidas y cantidad personas
# Post: Si datos válidos, reserva creada en BD con estado confirmada. Si faltan datos, error 400
@reservas_bp.route("/", methods=["POST"])
def crear_reserva():
    """Crear reserva - SIMPLIFICADO para universidad"""
    data = request.get_json()
    
    # Obtener datos básicos
    user_id = data.get('id_usuario') or session.get('user_id') or 10  # Fallback a user_id 10
    hospedaje = data.get('id_hospedaje')
    checkin = data.get('fecha_checkin')
    checkout = data.get('fecha_checkout')
    personas = data.get('cant_personas')
    precio = data.get('importe_total', 0)
    
    # Validar datos mínimos
    if not hospedaje or not checkin or not checkout or not personas:
        return jsonify({"error": "Faltan datos obligatorios"}), 400
    
    try:
        # Guardar en base de datos
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO reservas (id_usuario, id_hospedaje, fecha_checkin, fecha_checkout, cant_personas, importe_total, estado)
            VALUES (%s, %s, %s, %s, %s, %s, 'confirmada')
        """, (user_id, hospedaje, checkin, checkout, personas, precio))
        
        conn.commit()
        nueva_reserva_id = cursor.lastrowid
        cursor.close()
        conn.close()
        
        print(f"[BACKEND] Reserva creada con ID: {nueva_reserva_id}")
        return jsonify({"success": True, "message": "Reserva creada", "id_reserva": nueva_reserva_id}), 201
        
    except Exception as e:
        print(f"[BACKEND ERROR] Error al crear reserva: {e}")
        return jsonify({"error": f"Error en BD: {str(e)}"}), 500

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