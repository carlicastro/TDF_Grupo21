"""
Usuarios - Sistema Hotel 
"""
from flask import Blueprint, jsonify, session
from db import get_connection
from .auth import esta_logueado, es_admin, login_usuario, logout_usuario, registro_usuario

usuarios_bp = Blueprint('usuarios', __name__)

# Pre: Request POST con JSON conteniendo email y password válidos
# Post: Si credenciales correctas, sesión iniciada y retorna user data. Si incorrectas, retorna error
@usuarios_bp.route('/login', methods=['POST'])
def login():
    # Login de usuario
    return login_usuario()

# Pre: Sesión Flask existe (puede estar logueada o no)
# Post: Sesión completamente limpia, usuario deslogueado
@usuarios_bp.route('/logout', methods=['POST'])
def logout():
    # Cerrar sesión
    return logout_usuario()

# Pre: Request POST con JSON conteniendo nombre, email, password. Email no debe existir en BD
# Post: Si datos válidos, usuario creado en BD con rol cliente. Si email existe, retorna error
@usuarios_bp.route('/register', methods=['POST'])
def registro():
    # Registrar usuario nuevo
    return registro_usuario()

# Pre: Usuario debe estar logueado como admin
# Post: Si es admin, retorna lista JSON de todos los usuarios. Si no es admin, error 403
@usuarios_bp.route("/", methods=["GET"])
def ver_todos_usuarios():
    # Ver todos los usuarios - solo admin
    if esta_logueado() == False:
        return jsonify({'error': 'Debes estar logueado'}), 401
    if es_admin() == False:
        return jsonify({'error': 'Solo para admin'}), 403
    
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id_usuario, nombre, email, telefono, rol, direccion FROM usuarios")
    todos = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(todos)

# Pre: user_id debe ser un entero válido
# Post: Si usuario existe, retorna datos JSON sin password. Si no existe, error 404
@usuarios_bp.route("/<int:user_id>", methods=["GET"])
def ver_usuario(user_id):
    # Ver un usuario
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT id_usuario, nombre, email, telefono, rol, direccion FROM usuarios WHERE id_usuario = %s", (user_id,))
    usuario = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if usuario == None:
        return jsonify({'error': 'No existe'}), 404
    return jsonify(usuario)

# Pre: Usuario admin logueado, user_id de usuario existente
# Post: Si usuario existe y es admin, usuario eliminado de BD. Si no existe, error 404
@usuarios_bp.route("/<int:user_id>", methods=["DELETE"])
def borrar_usuario(user_id):
    # Borrar usuario - solo admin
    if esta_logueado() == False:
        return jsonify({'error': 'Debes estar logueado'}), 401
    if es_admin() == False:
        return jsonify({'error': 'Solo para admin'}), 403
    
    conn = get_connection()
    cursor = conn.cursor()
    
    # Ver si existe
    cursor.execute("SELECT id_usuario FROM usuarios WHERE id_usuario = %s", (user_id,))
    usuario_existe = cursor.fetchone()
    if usuario_existe == None:
        cursor.close()
        conn.close()
        return jsonify({'error': 'No existe'}), 404
    
    # Borrar
    cursor.execute("DELETE FROM usuarios WHERE id_usuario = %s", (user_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'success': True, 'message': 'Usuario borrado'})

# Pre: user_id debe ser un entero válido de usuario existente
# Post: Si usuario existe, retorna lista JSON de sus reservas con datos del hotel. Si no existe, error 404
@usuarios_bp.route("/<int:user_id>/reservas", methods=["GET"])
def ver_reservas_usuario(user_id):
    # Ver reservas de usuario
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    # Verificar que el usuario existe
    cursor.execute("SELECT id_usuario FROM usuarios WHERE id_usuario = %s", (user_id,))
    usuario_existe = cursor.fetchone()
    if not usuario_existe:
        cursor.close()
        conn.close()
        return jsonify({'error': 'Usuario no existe'}), 404
    
    # Obtener reservas del usuario
    cursor.execute("""
        SELECT r.*, h.nombre as hotel_nombre
        FROM reservas r
        LEFT JOIN hospedajes h ON r.id_hospedaje = h.id_hospedaje
        WHERE r.id_usuario = %s
        ORDER BY r.fecha_creacion DESC
    """, (user_id,))
    mis_reservas = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return jsonify(mis_reservas)
