"""
Funciones para manejar la tabla usuarios + sistema de autenticación
"""
from flask import Blueprint, jsonify, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from db import get_connection

usuarios_bp = Blueprint('usuarios', __name__)

def verificar_admin():
    """
    Verifica si el usuario es admin mediante sesión o cookies
    """
    # Verificar por sesión Flask (cuando viene del navegador directamente)
    if session.get('user_rol') == 'admin':
        return True
    
    # Verificar por cookies (cuando viene del API client del frontend)
    user_rol_cookie = request.cookies.get('user_rol')
    if user_rol_cookie == 'admin':
        return True
    
    return False

# ===== RUTAS DE AUTENTICACIÓN =====

@usuarios_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({'success': False, 'message': 'Email y contraseña son requeridos'}), 400
    
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if user and check_password_hash(user['password'], password):
        session['user_id'] = user['id_usuario']
        session['user_name'] = user['nombre']
        session['user_email'] = user['email']
        session['user_rol'] = user['rol'] if user['rol'] else 'cliente'
        session['logged_in'] = True
        
        return jsonify({
            'success': True,
            'message': 'Login exitoso',
            'user': {
                'id': user['id_usuario'],
                'nombre': user['nombre'],
                'email': user['email'],
                'rol': user['rol'] if user['rol'] else 'cliente'
            }
        })
    else:
        return jsonify({'success': False, 'message': 'Email o contraseña incorrectos'}), 401

@usuarios_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'success': True, 'message': 'Sesión cerrada exitosamente'})

@usuarios_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    nombre = data.get('nombre')
    email = data.get('email')
    telefono = data.get('telefono', '')
    password = data.get('password')
    direccion = data.get('direccion', '')
    rol = data.get('rol', 'cliente')
    
    if not all([nombre, email, password]):
        return jsonify({'success': False, 'message': 'Nombre, email y contraseña son requeridos'}), 400
    
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id_usuario FROM usuarios WHERE email = %s", (email,))
    if cursor.fetchone():
        cursor.close()
        conn.close()
        return jsonify({'success': False, 'message': 'El email ya está registrado'}), 409
    
    hashed_password = generate_password_hash(password)
    cursor.execute("""
        INSERT INTO usuarios (nombre, email, telefono, password, direccion, rol)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (nombre, email, telefono, hashed_password, direccion, rol))
    
    conn.commit()
    user_id = cursor.lastrowid
    cursor.close()
    conn.close()
    
    return jsonify({'success': True, 'message': 'Usuario registrado exitosamente', 'user_id': user_id}), 201

# ===== RUTAS CRUD BÁSICAS =====

@usuarios_bp.route("/", methods=["GET"])
def get_usuarios():
    """Listar todos los usuarios (solo admin)"""
    if not verificar_admin():
        return jsonify({'error': 'Acceso denegado. Solo administradores.'}), 403
    
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id_usuario, nombre, email, telefono, rol, direccion, fecha_registro FROM usuarios")
    usuarios = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(usuarios)

@usuarios_bp.route("/<int:user_id>", methods=["GET"])
def get_usuario_by_id(user_id):
    """Ver usuario específico por ID"""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id_usuario, nombre, email, telefono, rol, direccion, fecha_registro FROM usuarios WHERE id_usuario = %s", (user_id,))
    usuario = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if not usuario:
        return ("Usuario no encontrado", 404)
    return jsonify(usuario)

@usuarios_bp.route("/<int:user_id>", methods=["DELETE"])
def eliminar_usuario(user_id):
    """Eliminar usuario (solo admin)"""
    if not verificar_admin():
        return jsonify({'error': 'Acceso denegado. Solo administradores.'}), 403
    
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id_usuario FROM usuarios WHERE id_usuario = %s", (user_id,))
    if not cursor.fetchone():
        cursor.close()
        conn.close()
        return ("Usuario no encontrado", 404)
    
    cursor.execute("DELETE FROM usuarios WHERE id_usuario = %s", (user_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return ("Usuario eliminado exitosamente", 200)

@usuarios_bp.route("/<int:user_id>/reservas", methods=["GET"])
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
