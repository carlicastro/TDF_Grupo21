"""
Funciones para manejar la tabla reservas
"""
from flask import Blueprint, jsonify, request, session
from db import get_connection

reservas_bp = Blueprint('reservas', __name__)

def verificar_admin():
    """
    Verifica si el usuario es admin mediante sesión o header
    """
    if session.get('user_rol') == 'admin':
        return True
    
    admin_session = request.headers.get('X-Admin-Session')
    if admin_session and admin_session.startswith('admin_'):
        return True
    
    return False

@reservas_bp.route("/", methods=["GET"])
def get_reservas():
    """Ver todas las reservas (solo admin)"""
    if not verificar_admin():
        return jsonify({'error': 'Acceso denegado. Solo administradores.'}), 403
    
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT r.*, u.nombre as usuario_nombre, h.nombre as hospedaje_nombre
        FROM reservas r
        LEFT JOIN usuarios u ON r.id_usuario = u.id_usuario
        LEFT JOIN hospedajes h ON r.id_hospedaje = h.id_hospedaje
        ORDER BY r.fecha_creacion DESC
    """)
    reservas = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(reservas)

@reservas_bp.route("/<int:reserva_id>", methods=["GET"])
def get_reserva_by_id(reserva_id):
    """Ver reserva específica"""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT r.*, u.nombre as usuario_nombre, h.nombre as hospedaje_nombre
        FROM reservas r
        LEFT JOIN usuarios u ON r.id_usuario = u.id_usuario
        LEFT JOIN hospedajes h ON r.id_hospedaje = h.id_hospedaje
        WHERE r.id_reserva = %s
    """, (reserva_id,))
    reserva = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if not reserva:
        return ("Reserva no encontrada", 404)
    return jsonify(reserva)

@reservas_bp.route("/usuario/<int:user_id>", methods=["GET"])
def get_reservas_usuario(user_id):
    """Ver reservas de un usuario específico"""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT r.*, h.nombre as hospedaje_nombre, h.tipo, h.descripcion
        FROM reservas r
        LEFT JOIN hospedajes h ON r.id_hospedaje = h.id_hospedaje
        WHERE r.id_usuario = %s
        ORDER BY r.fecha_creacion DESC
    """, (user_id,))
    reservas = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(reservas)

@reservas_bp.route("/", methods=["POST"])
def crear_reserva():
    """Crear nueva reserva (cualquier usuario logueado)"""
    if not session.get('logged_in'):
        return ("Debe estar logueado para hacer una reserva", 401)
    
    data = request.get_json()
    id_usuario = data.get('id_usuario')
    id_hospedaje = data.get('id_hospedaje')
    fecha_checkin = data.get('fecha_checkin')
    fecha_checkout = data.get('fecha_checkout')
    cant_personas = data.get('cant_personas')
    importe_total = data.get('importe_total', 0.00)
    estado = data.get('estado', 'confirmada')
    
    if not all([id_usuario, id_hospedaje, fecha_checkin, fecha_checkout, cant_personas]):
        return ("Todos los campos son requeridos", 400)
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO reservas (id_usuario, id_hospedaje, fecha_checkin, fecha_checkout, cant_personas, importe_total, estado)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (id_usuario, id_hospedaje, fecha_checkin, fecha_checkout, cant_personas, importe_total, estado))
    
    conn.commit()
    cursor.close()
    conn.close()
    return ("Reserva creada exitosamente", 201)

@reservas_bp.route("/<int:reserva_id>", methods=["DELETE"])
def eliminar_reserva(reserva_id):
    """Eliminar reserva (solo admin)"""
    if not verificar_admin():
        return jsonify({'error': 'Acceso denegado. Solo administradores.'}), 403
    
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id_reserva FROM reservas WHERE id_reserva = %s", (reserva_id,))
    if not cursor.fetchone():
        cursor.close()
        conn.close()
        return ("Reserva no encontrada", 404)
    
    cursor.execute("DELETE FROM reservas WHERE id_reserva = %s", (reserva_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return ("Reserva eliminada exitosamente", 200)