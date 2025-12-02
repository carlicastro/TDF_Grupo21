"""
Funciones de autenticación centralizadas
"""
from flask import session, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from db import get_connection

# Pre: Existe una sesión Flask activa
# Post: Retorna True si usuario está logueado, False en caso contrario
def esta_logueado():
    if session.get('logged_in') == True:
        return True
    return False

# Pre: Usuario debe estar logueado previamente
# Post: Retorna True si el usuario tiene rol admin, False en caso contrario
def es_admin():

    if session.get('user_rol') == 'admin':
        return True
    return False

# Pre: Request debe contener JSON con email y password válidos
# Post: Si credenciales correctas, sesión iniciada y retorna user data. Si incorrectas, retorna error
def login_usuario():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    if email == '' or password == '':
        return jsonify({'success': False, 'message': 'Faltan datos'}), 400
    if email is None or password is None:
        return jsonify({'success': False, 'message': 'Faltan datos'}), 400
    
    # Buscar usuario
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    
    # Verificar password
    if user != None:
        if check_password_hash(user['password'], password) == True:
            # Guardar en sesión
            session.clear()
            session['logged_in'] = True
            session['user_id'] = user['id_usuario']
            session['user_nombre'] = user['nombre']
            session['user_email'] = user['email']
            session['user_rol'] = user['rol'] or 'cliente'
            
            return jsonify({
                'success': True,
                'message': 'Login correcto',
                'user': {
                    'id': user['id_usuario'],
                    'nombre': user['nombre'],
                    'email': user['email'],
                    'rol': user['rol'] or 'cliente'
                }
            })
        else:
            return jsonify({'success': False, 'message': 'Password mal'}), 401
    else:
        return jsonify({'success': False, 'message': 'Email no existe'}), 401

# Pre: Sesión Flask existe (puede estar logueada o no)
# Post: Sesión completamente limpia, usuario deslogueado
def logout_usuario():
    # Cerrar sesión
    session.clear()
    return jsonify({'success': True, 'message': 'Sesión cerrada'})

# Pre: Request con JSON conteniendo nombre, email, password. Email no debe existir en BD
# Post: Si datos válidos, usuario creado en BD con rol cliente. Si email existe, retorna error
def registro_usuario():
    # Registrar usuario nuevo
    data = request.get_json()
    nombre = data.get('nombre')
    email = data.get('email')
    password = data.get('password')
    telefono = data.get('telefono', '')
    direccion = data.get('direccion', '')
    
    # Verificar campos obligatorios
    if nombre == '' or email == '' or password == '':
        return jsonify({'success': False, 'message': 'Faltan datos obligatorios'}), 400
    if nombre is None or email is None or password is None:
        return jsonify({'success': False, 'message': 'Faltan datos obligatorios'}), 400
    
    conn = get_connection()
    cursor = conn.cursor()
    
    # Ver si email ya existe
    cursor.execute("SELECT id_usuario FROM usuarios WHERE email = %s", (email,))
    usuario_existe = cursor.fetchone()
    if usuario_existe != None:
        cursor.close()
        conn.close()
        return jsonify({'success': False, 'message': 'Email ya existe'}), 409
    
    # Crear usuario
    password_hash = generate_password_hash(password)
    cursor.execute("""
        INSERT INTO usuarios (nombre, email, telefono, password, direccion, rol)
        VALUES (%s, %s, %s, %s, %s, 'cliente')
    """, (nombre, email, telefono, password_hash, direccion))
    
    conn.commit()
    nuevo_id = cursor.lastrowid
    cursor.close()
    conn.close()
    
    return jsonify({'success': True, 'message': 'Usuario creado', 'user_id': nuevo_id}), 201