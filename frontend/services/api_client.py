"""
Cliente API SIMPLE para conectar con el backend del hotel
SOLO con sesiones Flask - SIN JWT
"""

import requests
from flask import session, has_request_context

# Configuración del API Backend
API_BASE = "http://localhost:8080"

# Crear una sesión persistente para mantener cookies
api_session = requests.Session()

# Pre: Método HTTP válido, URL válida
# Post: Si exitoso retorna response, si error retorna None
def make_request(method, url, **kwargs):
    """Hacer request SIMPLE al backend manteniendo sesión"""
    try:
        response = api_session.request(method, url, **kwargs)
        return response
    except Exception as e:
        print(f"[API ERROR] Error en request: {e}")
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

# ===== USUARIOS =====

# Pre: Email y contraseña válidos
# Post: Diccionario con success, message y user si exitoso
def login_usuario(email, password):
    """Iniciar sesión SIMPLE con Flask sessions"""
    try:
        # Login simple sin JWT usando sesión persistente
        response = api_session.post(
            f"{API_BASE}/usuarios/login",
            json={"email": email, "password": password}
        )
        
        if response and response.status_code == 200:
            backend_data = response.json()
            
            if has_request_context():
                # Guardar SOLO en sesión Flask
                session.clear()
                session['logged_in'] = True
                session.permanent = True
                
                user_data = backend_data.get('user', {})
                session['user_id'] = user_data.get('id', '')
                session['user_nombre'] = user_data.get('nombre', '')
                session['user_email'] = user_data.get('email', '')
                session['user_rol'] = user_data.get('rol', 'cliente')
                
                print(f"[LOGIN SIMPLE] Usuario logueado: {user_data.get('nombre')}")
            
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
        print(f"[LOGIN ERROR] Error: {e}")
        return {'success': False, 'message': 'Error de conexión con el servidor'}

# Pre: Usuario logueado
# Post: Cierra sesión y limpia cookies, retorna True
def logout_usuario():
    """Cerrar sesión SIMPLE"""
    try:
        response = api_session.post(f"{API_BASE}/usuarios/logout")
        print(f"[LOGOUT] Respuesta: {response.status_code if response else 'Sin respuesta'}")
    except Exception as e:
        print(f"[LOGOUT ERROR] Error: {e}")
    
    # Limpiar sesión Flask y API
    if has_request_context():
        session.clear()
        print("[LOGOUT] Sesión Flask limpiada")
    
    # Limpiar cookies de la sesión API
    api_session.cookies.clear()
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
        response = make_request('GET', f"{API_BASE}/usuarios/")
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 403:
            return []
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
        print(f"Error obteniendo reservas: {e}")
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
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        return None

# ===== RESERVAS =====

# Pre: Datos de reserva válidos, usuario logueado
# Post: True si se crea exitosamente, False si error
def crear_reserva(datos_reserva):
    """Crear nueva reserva"""
    try:
        print(f"Enviando datos de reserva: {datos_reserva}")  # Debug
        response = make_request('POST', f"{API_BASE}/reservas/", json=datos_reserva)
        print(f"Respuesta del backend - Status: {response.status_code if response else 'None'}")  # Debug
        
        if response:
            if response.status_code == 201:
                print("DEBUG: Reserva creada exitosamente")
                return True
            else:
                try:
                    error_data = response.json()
                    print(f"Error del backend: {error_data}")
                except:
                    print(f"Error del backend (texto): {response.text}")
                return False
        else:
            print("DEBUG: No se recibió respuesta del backend")
            return False
            
    except Exception as e:
        print(f"Error creando reserva: {e}")
        return False

# Pre: Permisos de administrador
# Post: Lista de todas las reservas o lista vacía si error
def obtener_todas_reservas():
    """Obtener todas las reservas (solo para admin)"""
    try:
        response = make_request('GET', f"{API_BASE}/reservas/")
        if response.status_code == 200:
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

# Pre: ID de hospedaje válido
# Post: Lista de reservas del hospedaje o lista vacía si error
def obtener_reservas_hospedaje(id_hospedaje):
    """Obtener reservas de un hospedaje específico"""
    try:
        response = make_request('GET', f"{API_BASE}/hospedajes/{id_hospedaje}/reservas")
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        return []