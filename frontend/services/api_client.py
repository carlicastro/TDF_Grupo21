"""
Cliente API SIMPLE para conectar con el backend del hotel
SOLO con sesiones Flask - SIN JWT
"""

import requests
from flask import session, has_request_context

# Configuración del API Backend
API_BASE = "http://localhost:8080"

# Session para mantener cookies entre requests
import requests
session_api = requests.Session()

# Pre: Usuario debe estar logueado como admin en frontend
# Post: Si no está logueado en backend, hace login automático. Retorna True si exitoso
def ensure_admin_logged_in():
    """Asegurar que el admin esté logueado en el backend"""
    if not has_request_context():
        return False
        
    # Verificar si estamos logueados como admin en el frontend
    if not session.get('logged_in') or session.get('user_rol') != 'admin':
        return False
    
    # Intentar hacer login en el backend si es necesario
    try:
        # Probar si ya estamos autenticados en el backend
        test_response = session_api.get(f"{API_BASE}/usuarios/")
        if test_response.status_code == 200:
            return True  # Ya estamos autenticados
        
        # Si no estamos autenticados, hacer login
        email = session.get('user_email')
        if email:
            # Nota: No tenemos la contraseña guardada, esto es una limitación
            # En un sistema real usarías tokens o mantener la sesión activa
            return False
    except Exception as e:
        return False
    
    return False

# Pre: Método HTTP válido, URL válida
# Post: Si exitoso retorna response, si error retorna None
def make_request(method, url, **kwargs):
    """Hacer request SIMPLE al backend con sesión persistente"""
    try:
        # Usar la sesión persistente que mantiene las cookies
        response = session_api.request(method, url, **kwargs)
        return response
    except Exception as e:
        return None

# ===== HOSPEDAJES =====

# Pre: API disponible
# Post: Lista de hospedajes o lista vacía si error
def obtener_hospedajes():
    """Obtener todos los hospedajes"""
    try:
        response = make_request('GET', f"{API_BASE}/hospedajes/")
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        return []

# Pre: ID de hospedaje válido
# Post: Datos del hospedaje o None si no existe o error
def obtener_hospedaje(id_hospedaje):
    """Obtener hospedaje específico"""
    try:
        response = make_request('GET', f"{API_BASE}/hospedajes/{id_hospedaje}")
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        return None

# Pre: Datos de hospedaje válidos, permisos de admin
# Post: Diccionario con success y message indicando resultado
def crear_hospedaje(datos_hospedaje):
    """Crear nuevo hospedaje (solo admin)"""
    try:
        response = make_request('POST', f"{API_BASE}/hospedajes/", json=datos_hospedaje, timeout=10)
        
        if response.status_code == 201:
            return {"success": True, "message": "Hospedaje creado exitosamente"}
        elif response.status_code == 400:
            return {"success": False, "message": "Datos inválidos"}
        elif response.status_code == 401:
            return {"success": False, "message": "No autorizado"}
        elif response.status_code == 500:
            return {"success": False, "message": "Error interno del servidor"}
        else:
            return {"success": False, "message": f"Error HTTP {response.status_code}"}
            
    except requests.exceptions.ConnectionError:
        return {"success": False, "message": "No se pudo conectar con el backend"}
    except requests.exceptions.Timeout:
        return {"success": False, "message": "Timeout al conectar con el backend"}
    except Exception as e:
        return {"success": False, "message": f"Error inesperado: {str(e)}"}

# Pre: ID válido, datos de hospedaje válidos, permisos de admin
# Post: Diccionario con success y message indicando resultado
def actualizar_hospedaje(id_hospedaje, datos_hospedaje):
    """Actualizar hospedaje existente (solo admin)"""
    response = make_request('PUT', f"{API_BASE}/hospedajes/{id_hospedaje}", json=datos_hospedaje)
    if response.status_code == 200:
        return {"success": True, "message": "Hospedaje actualizado"}
    return {"success": False, "message": "Error al actualizar hospedaje"}

# Pre: ID de hospedaje válido, permisos de admin
# Post: Diccionario con success y message indicando resultado
def eliminar_hospedaje(id_hospedaje):
    """Eliminar hospedaje (solo admin)"""
    try:
        response = make_request('DELETE', f"{API_BASE}/hospedajes/{id_hospedaje}")
        
        if response.status_code == 200:
            return {"success": True, "message": "Hospedaje eliminado correctamente"}
        elif response.status_code == 404:
            return {"success": False, "message": "No se encontró la habitación"}
        elif response.status_code == 403:
            return {"success": False, "message": "No tienes permisos para eliminar habitaciones"}
        else:
            return {"success": False, "message": f"Error al eliminar habitación (Código: {response.status_code})"}
    except Exception as e:
        return {"success": False, "message": f"Error de conexión: {e}"}

#
# Pre: ID de hospedaje válido
# Post: Lista de fechas ocupadas como strings ['YYYY-MM-DD'] o lista vacía si error
def obtener_reservas_hospedaje(id_hospedaje):
    """Obtener fechas ocupadas de un hospedaje (solo fechas, sin datos personales)"""
    try:
        response = make_request('GET', f"{API_BASE}/hospedajes/{id_hospedaje}/disponibilidad")
        if response and response.status_code == 200:
            data = response.json()
            return data.get('fechas_ocupadas', [])
        return []
    except Exception as e:
        return []

# ===== USUARIOS =====

# Pre: Email y contraseña válidos
# Post: Diccionario con success, message y user si exitoso
def login_usuario(email, password):
    """Iniciar sesión SIMPLE - Solo verifica credenciales y guarda en sesión local"""
    try:
        # Verificar credenciales con el backend
        response = session_api.post(
            f"{API_BASE}/usuarios/login",
            json={"email": email, "password": password},
            timeout=10
        )
        
        if response and response.status_code == 200:
            backend_data = response.json()
            
            if has_request_context():
                # Guardar en sesión Flask del frontend
                session.clear()
                session['logged_in'] = True
                session.permanent = True
                
                user_data = backend_data.get('user', {})
                session['user_id'] = user_data.get('id', '')
                session['user_nombre'] = user_data.get('nombre', '')
                session['user_email'] = user_data.get('email', '')
                session['user_rol'] = user_data.get('rol', 'cliente')
            
            return {
                'success': True,
                'message': backend_data.get('message', 'Login exitoso'),
                'user': backend_data.get('user', {})
            }
        elif response and response.status_code == 401:
            return {'success': False, 'message': 'Credenciales incorrectas'}
        else:
            return {'success': False, 'message': f'Error del servidor: {response.status_code if response else "Sin respuesta"}'}
            
    except Exception as e:
        return {'success': False, 'message': 'Error de conexión con el servidor'}

# Pre: Usuario logueado
# Post: Cierra sesión Flask, retorna True
def logout_usuario():
    """Cerrar sesión SIMPLE"""
    try:
        session_api.post(f"{API_BASE}/usuarios/logout")
    except Exception as e:
        pass
    
    # Limpiar sesión Flask
    if has_request_context():
        session.clear()
    
    return True

# Pre: Datos de usuario válidos
# Post: Datos del usuario creado o None si error
def crear_usuario(datos_usuario):
    """Registrar nuevo usuario"""
    response = make_request('POST', f"{API_BASE}/usuarios/register", json=datos_usuario)
    if response.status_code == 201:
        return response.json()
    return None

# Pre: Permisos de administrador
# Post: Lista de usuarios o lista vacía si no autorizado o error
def obtener_todos_usuarios():
    """Obtener todos los usuarios (solo para admin)"""
    try:
        # Si no tenemos una sesión autenticada, intentar hacer login como admin
        response = make_request('GET', f"{API_BASE}/usuarios/")
        
        if response and response.status_code == 401:
            # Necesitamos autenticarnos - hacer login como admin
            login_response = session_api.post(
                f"{API_BASE}/usuarios/login",
                json={"email": "admin@hotel.com", "password": "admin123"},
                timeout=10
            )
            
            if login_response and login_response.status_code == 200:
                # Reintentar obtener usuarios después del login
                response = make_request('GET', f"{API_BASE}/usuarios/")
        
        if response and response.status_code == 200:
            return response.json()
        else:
            return []
            
    except Exception as e:
        return []

# Pre: ID de usuario válido
# Post: Lista de reservas del usuario o lista vacía si error
def obtener_reservas_usuario(id_usuario):
    """Obtener reservas de un usuario"""
    try:
        if not id_usuario:
            return []
            
        url = f"{API_BASE}/usuarios/{id_usuario}/reservas"
        response = make_request('GET', url)
        
        if response and response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        return []

# Pre: ID de usuario válido, permisos de admin
# Post: Diccionario con success y message indicando resultado
def eliminar_usuario(id_usuario):
    """Eliminar usuario (solo admin)"""
    response = make_request('DELETE', f"{API_BASE}/usuarios/{id_usuario}")
    if response.status_code == 200:
        return {"success": True, "message": "Usuario eliminado"}
    return {"success": False, "message": "Error al eliminar usuario"}

# Pre: ID de usuario válido, permisos de admin
# Post: Datos del usuario o None si no existe o error
def obtener_usuario_por_id(id_usuario):
    """Obtener usuario por ID (solo admin)"""
    try:
        response = make_request('GET', f"{API_BASE}/usuarios/{id_usuario}")
        
        if response and response.status_code == 401:
            # Hacer login como admin
            session_api.post(
                f"{API_BASE}/usuarios/login",
                json={"email": "admin@hotel.com", "password": "admin123"},
                timeout=10
            )
            response = make_request('GET', f"{API_BASE}/usuarios/{id_usuario}")
        
        if response and response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        return None

# ===== RESERVAS =====

# Pre: Datos de reserva válidos, usuario logueado
# Post: True si se crea exitosamente, False si error
def crear_reserva(datos_reserva):
    """Crear nueva reserva - SIMPLE con Flask sessions"""
    try:
        # Asegurar que tenemos user_id de la sesión del frontend
        if has_request_context() and session.get('logged_in'):
            datos_reserva['id_usuario'] = session.get('user_id')
            
            response = requests.post(
                f"{API_BASE}/reservas/",
                json=datos_reserva,
                timeout=10
            )
        else:
            return False
        
        if response and response.status_code in [200, 201]:
            return True
        else:
            return False
            
    except Exception as e:
        return False

# Pre: Permisos de administrador
# Post: Lista de todas las reservas o lista vacía si error
def obtener_todas_reservas():
    """Obtener todas las reservas (solo para admin)"""
    try:
        response = make_request('GET', f"{API_BASE}/reservas/")
        
        if response and response.status_code == 401:
            # Hacer login como admin
            session_api.post(
                f"{API_BASE}/usuarios/login",
                json={"email": "admin@hotel.com", "password": "admin123"},
                timeout=10
            )
            response = make_request('GET', f"{API_BASE}/reservas/")
        
        if response and response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        return []

# Pre: ID de reserva válido, permisos de admin
# Post: Diccionario con success y message indicando resultado
def eliminar_reserva(id_reserva):
    """Eliminar reserva (solo admin)"""
    response = make_request('DELETE', f"{API_BASE}/reservas/{id_reserva}")
    if response.status_code == 200:
        return {"success": True, "message": "Reserva eliminada"}
    return {"success": False, "message": "Error al eliminar reserva"}

# Pre: ID de reserva válido, permisos de admin
# Post: Datos de la reserva o None si no existe o error
def obtener_reserva_por_id(id_reserva):
    """Obtener reserva por ID (solo admin)"""
    try:
        response = make_request('GET', f"{API_BASE}/reservas/{id_reserva}")
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        return None