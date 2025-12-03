"""
Funciones para manejar la tabla hospedajes
"""
from flask import Blueprint, jsonify, request
from datetime import timedelta
from db import get_connection
from .auth import es_admin

hospedajes_bp = Blueprint('hospedajes', __name__)

# Pre: Conexión a BD disponible
# Post: Retorna lista JSON de todos los hospedajes en la BD
@hospedajes_bp.route("/", methods=["GET"])
def get_hospedajes():
    # Ver todos los hospedajes
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM hospedajes")
    hospedajes = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(hospedajes)

# Pre: hospedaje_id debe ser un entero válido
# Post: Si ID existe, retorna hospedaje JSON. Si no existe, retorna error 404
@hospedajes_bp.route("/<int:hospedaje_id>", methods=["GET"])
def get_hospedaje_by_id(hospedaje_id):
    # Ver hospedaje específico por ID
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM hospedajes WHERE id_hospedaje = %s", (hospedaje_id,))
    hospedaje = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if not hospedaje:
        return ("Hospedaje no encontrado", 404)
    return jsonify(hospedaje)

# Pre: Usuario debe estar logueado como admin, JSON con nombre, precio y capacidad
# Post: Si es admin y datos válidos, hospedaje creado en BD. Si no es admin, error 403
@hospedajes_bp.route("/", methods=["POST"])
def crear_hospedaje():
    # Crear hospedaje nuevo (solo admin)
    if not es_admin():
        return jsonify({"error": "Solo administradores"}), 403
    
    data = request.get_json()
    
    nombre = data.get('nombre')
    descripcion = data.get('descripcion')
    precio = data.get('precio')
    capacidad = data.get('capacidad')
    foto = data.get('foto', '')
    
    # Validar datos básicos
    if not nombre or not precio or not capacidad:
        return jsonify({"error": "Faltan datos obligatorios"}), 400
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO hospedajes (nombre, descripcion, precio, capacidad, foto, disponibilidad, tipo)
        VALUES (%s, %s, %s, %s, %s, 1, 'habitacion')
    """, (nombre, descripcion, precio, capacidad, foto))
    
    conn.commit()
    cursor.close()
    conn.close()
    
    return jsonify({"success": True, "message": "Hospedaje creado"})

# Pre: Usuario admin, hospedaje_id válido, JSON con datos a actualizar
# Post: Si hospedaje existe y es admin, datos actualizados. Si no existe, error 404
@hospedajes_bp.route("/<int:hospedaje_id>", methods=["PUT"])
def actualizar_hospedaje(hospedaje_id):
    # Editar hospedaje (solo admin)
    if not es_admin():
        return jsonify({"error": "Solo administradores"}), 403
    
    data = request.get_json()
    
    conn = get_connection()
    cursor = conn.cursor()
    
    # Verificar que existe
    cursor.execute("SELECT * FROM hospedajes WHERE id_hospedaje = %s", (hospedaje_id,))
    if not cursor.fetchone():
        cursor.close()
        conn.close()
        return jsonify({"error": "Hospedaje no encontrado"}), 404
    
    # Actualizar datos simples
    nombre = data.get('nombre')
    precio = data.get('precio')
    capacidad = data.get('capacidad')
    
    if nombre:
        cursor.execute("UPDATE hospedajes SET nombre = %s WHERE id_hospedaje = %s", (nombre, hospedaje_id))
    if precio:
        cursor.execute("UPDATE hospedajes SET precio = %s WHERE id_hospedaje = %s", (precio, hospedaje_id))
    if capacidad:
        cursor.execute("UPDATE hospedajes SET capacidad = %s WHERE id_hospedaje = %s", (capacidad, hospedaje_id))
    
    conn.commit()
    cursor.close()
    conn.close()
    
    return jsonify({"success": True, "message": "Hospedaje actualizado"})

# Pre: Usuario admin logueado, hospedaje_id de hospedaje existente
# Post: Si hospedaje existe y es admin, hospedaje eliminado de BD. Si no existe, error 404
@hospedajes_bp.route("/<int:hospedaje_id>", methods=["DELETE"])
def eliminar_hospedaje(hospedaje_id):
    # Borrar hospedaje (solo admin)
    if not es_admin():
        return jsonify({"error": "Solo administradores"}), 403
    
    conn = get_connection()
    cursor = conn.cursor()
    
    # Verificar que existe
    cursor.execute("SELECT * FROM hospedajes WHERE id_hospedaje = %s", (hospedaje_id,))
    if not cursor.fetchone():
        cursor.close()
        conn.close()
        return jsonify({"error": "Hospedaje no existe"}), 404
    
    # Borrar
    cursor.execute("DELETE FROM hospedajes WHERE id_hospedaje = %s", (hospedaje_id,))
    conn.commit()
    cursor.close()
    conn.close()
    
    return jsonify({"success": True, "message": "Hospedaje eliminado"})

# Pre: hospedaje_id debe ser un entero válido
# Post: Retorna lista simple de fechas ocupadas
@hospedajes_bp.route("/<int:hospedaje_id>/disponibilidad", methods=["GET"])
def get_disponibilidad_hospedaje(hospedaje_id):
    """Ver fechas ocupadas - SIMPLE para estudiantes"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # SQL simple: obtener fechas de reservas confirmadas
    cursor.execute("""
        SELECT fecha_checkin, fecha_checkout
        FROM reservas 
        WHERE id_hospedaje = %s AND estado = 'confirmada'
    """, (hospedaje_id,))
    
    reservas = cursor.fetchall()
    cursor.close()
    conn.close()
    
    # Crear lista de fechas ocupadas (lógica simple)
    fechas_ocupadas = []
    for reserva in reservas:
        checkin = reserva[0]
        checkout = reserva[1]
        
        # Agregar día por día desde checkin hasta checkout
        fecha = checkin
        while fecha <= checkout:
            fechas_ocupadas.append(fecha.strftime('%Y-%m-%d'))
            fecha += timedelta(days=1)
    
    return jsonify({'fechas_ocupadas': fechas_ocupadas})
