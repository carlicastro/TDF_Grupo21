"""
Funciones para manejar la tabla hospedajes
"""
from flask import Blueprint, jsonify, request, session
from db import get_connection

hospedajes_bp = Blueprint('hospedajes', __name__)

@hospedajes_bp.route("/", methods=["GET"])
def get_hospedajes():
    """Ver todos los hospedajes"""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM hospedajes")
    hospedajes = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(hospedajes)

@hospedajes_bp.route("/<int:hospedaje_id>", methods=["GET"])
def get_hospedaje_by_id(hospedaje_id):
    """Ver hospedaje específico por ID"""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM hospedajes WHERE id_hospedaje = %s", (hospedaje_id,))
    hospedaje = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if not hospedaje:
        return ("Hospedaje no encontrado", 404)
    return jsonify(hospedaje)

@hospedajes_bp.route("/", methods=["POST"])
def crear_hospedaje():
    """Crear hospedaje (solo admin)"""
    print(f"[CREATE] Session: {dict(session)}")
    print(f"[CREATE] User rol: {session.get('user_rol')}")
    
    if session.get('user_rol') != 'admin':
        print(f"[CREATE] DENIED - Role: {session.get('user_rol')} != 'admin'")
        return ("Solo administradores pueden crear hospedajes", 403)
    
    data = request.get_json()
    print(f"[CREATE] Data received: {data}")
    
    nombre = data.get('nombre')
    descripcion = data.get('descripcion')
    precio = data.get('precio')
    capacidad = data.get('capacidad')
    foto = data.get('foto', '')
    disponibilidad = data.get('disponibilidad', 1)
    tipo = data.get('tipo', '')
    
    if not all([nombre, precio, capacidad]):
        print(f"[CREATE] VALIDATION ERROR - Missing fields")
        return ("Nombre, precio y capacidad son requeridos", 400)
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO hospedajes (nombre, descripcion, precio, capacidad, foto, disponibilidad, tipo)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (nombre, descripcion, precio, capacidad, foto, disponibilidad, tipo))
        
        conn.commit()
        cursor.close()
        conn.close()
        print(f"[CREATE] SUCCESS - Hospedaje creado: {nombre}")
        return ("Hospedaje creado exitosamente", 201)
    except Exception as e:
        print(f"[CREATE] DATABASE ERROR: {e}")
        return ("Error interno del servidor", 500)

@hospedajes_bp.route("/<int:hospedaje_id>", methods=["PUT"])
def actualizar_hospedaje(hospedaje_id):
    """Editar hospedaje (solo admin)"""
    if session.get('user_rol') != 'admin':
        return ("Solo administradores pueden editar hospedajes", 403)
    
    data = request.get_json()
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id_hospedaje FROM hospedajes WHERE id_hospedaje = %s", (hospedaje_id,))
    if not cursor.fetchone():
        cursor.close()
        conn.close()
        return ("Hospedaje no encontrado", 404)
    
    campos_actualizacion = []
    valores = []
    
    if 'nombre' in data:
        campos_actualizacion.append("nombre = %s")
        valores.append(data['nombre'])
    if 'descripcion' in data:
        campos_actualizacion.append("descripcion = %s")
        valores.append(data['descripcion'])
    if 'precio' in data:
        campos_actualizacion.append("precio = %s")
        valores.append(data['precio'])
    if 'capacidad' in data:
        campos_actualizacion.append("capacidad = %s")
        valores.append(data['capacidad'])
    if 'foto' in data:
        campos_actualizacion.append("foto = %s")
        valores.append(data['foto'])
    if 'disponibilidad' in data:
        campos_actualizacion.append("disponibilidad = %s")
        valores.append(data['disponibilidad'])
    if 'tipo' in data:
        campos_actualizacion.append("tipo = %s")
        valores.append(data['tipo'])
    
    if not campos_actualizacion:
        return ("No se proporcionaron campos para actualizar", 400)
    
    valores.append(hospedaje_id)
    query = f"UPDATE hospedajes SET {', '.join(campos_actualizacion)} WHERE id_hospedaje = %s"
    
    cursor.execute(query, valores)
    conn.commit()
    cursor.close()
    conn.close()
    return ("Hospedaje actualizado exitosamente", 200)

@hospedajes_bp.route("/<int:hospedaje_id>", methods=["DELETE"])
def eliminar_hospedaje(hospedaje_id):
    """Eliminar hospedaje (solo admin)"""
    if session.get('user_rol') != 'admin':
        return ("Solo administradores pueden eliminar hospedajes", 403)
    
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id_hospedaje FROM hospedajes WHERE id_hospedaje = %s", (hospedaje_id,))
    if not cursor.fetchone():
        cursor.close()
        conn.close()
        return ("Hospedaje no encontrado", 404)
    
    cursor.execute("DELETE FROM hospedajes WHERE id_hospedaje = %s", (hospedaje_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return ("Hospedaje eliminado exitosamente", 200)
