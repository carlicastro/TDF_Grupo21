"""
Cliente API para conectar con el backend del hotel
Funciones básicas para comunicación con el backend
"""

import requests
from flask import session

# Configuración del API Backend
API_BASE = "http://localhost:8080"


def make_request(method, url, **kwargs):
    """Hacer request al backend manteniendo las cookies de sesión"""
    # Enviar cookies directamente desde la sesión Flask del frontend
    cookies_to_send = session.get("backend_cookies", {}).copy()
    cookies_to_send.update(
        {
            "user_id": str(session.get("user_id", "")),
            "user_rol": session.get("user_rol", ""),
            "user_nombre": session.get("user_nombre", ""),
            "logged_in": str(session.get("logged_in", "")),
        }
    )

    # Filtrar cookies vacías
    cookies_to_send = {k: v for k, v in cookies_to_send.items() if v}

    # Hacer el request con cookies
    response = requests.request(method, url, cookies=cookies_to_send, **kwargs)

    return response


# ===== HOSPEDAJES =====


def obtener_hospedajes():
    """Obtener todos los hospedajes"""
    try:
        response = make_request("GET", f"{API_BASE}/hospedajes")
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        return []


def obtener_hospedaje(id_hospedaje):
    """Obtener hospedaje específico"""
    try:
        response = make_request("GET", f"{API_BASE}/hospedajes/{id_hospedaje}")
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        return None


def obtener_hospedaje_por_id(id_hospedaje):
    """Obtener hospedaje por ID (alias para obtener_hospedaje)"""
    return obtener_hospedaje(id_hospedaje)


def crear_hospedaje(datos_hospedaje):
    """Crear nuevo hospedaje (solo admin)"""
    try:
        response = make_request(
            "POST", f"{API_BASE}/hospedajes/", json=datos_hospedaje, timeout=10
        )

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


def actualizar_hospedaje(id_hospedaje, datos_hospedaje):
    """Actualizar hospedaje existente (solo admin)"""
    response = make_request(
        "PUT", f"{API_BASE}/hospedajes/{id_hospedaje}", json=datos_hospedaje
    )
    if response.status_code == 200:
        return {"success": True, "message": "Hospedaje actualizado"}
    return {"success": False, "message": "Error al actualizar hospedaje"}


def eliminar_hospedaje(id_hospedaje):
    """Eliminar hospedaje (solo admin)"""
    try:
        response = make_request("DELETE", f"{API_BASE}/hospedajes/{id_hospedaje}")

        if response.status_code == 200:
            return {"success": True, "message": "Hospedaje eliminado correctamente"}
        elif response.status_code == 404:
            return {"success": False, "message": "No se encontró la habitación"}
        elif response.status_code == 403:
            return {
                "success": False,
                "message": "No tienes permisos para eliminar habitaciones",
            }
        else:
            return {
                "success": False,
                "message": f"Error al eliminar habitación (Código: {response.status_code})",
            }
    except Exception as e:
        return {"success": False, "message": f"Error de conexión: {e}"}


# ===== USUARIOS =====


def login_usuario(email, password):
    """Iniciar sesión y mantener cookies del backend"""
    try:
        response = requests.request(
            "POST",
            f"{API_BASE}/usuarios/login",
            json={"email": email, "password": password},
        )

        if response.status_code == 200:
            # Procesar respuesta exitosa del backend
            session["backend_cookies"] = response.cookies.get_dict()
            backend_data = response.json()

            # Normalizar la respuesta para que siempre tenga 'success'
            if backend_data and "user" in backend_data:
                return {
                    "success": True,
                    "message": backend_data.get("message", "Login exitoso"),
                    "user": backend_data["user"],
                }
            elif backend_data and "id" in backend_data:
                # Si el backend devuelve directamente los datos del usuario
                return {
                    "success": True,
                    "message": "Login exitoso",
                    "user": backend_data,
                }
            else:
                return {
                    "success": True,
                    "message": "Login exitoso",
                    "user": backend_data or {},
                }
        elif response.status_code == 401:
            return {"success": False, "message": "Credenciales incorrectas"}
        else:
            return {
                "success": False,
                "message": f"Error del servidor: {response.status_code}",
            }

    except Exception as e:
        return {"success": False, "message": "Error de conexión con el servidor"}


def logout_usuario():
    """Cerrar sesión y limpiar cookies"""
    try:
        response = make_request("POST", f"{API_BASE}/usuarios/logout")
    except:
        # Si hay error, aún así limpiar la sesión local
        pass

    # Limpiar cookies y sesión completamente
    session.pop("backend_cookies", None)
    session.clear()
    return True


def obtener_usuario_actual():
    """Obtener información del usuario actual desde el backend"""
    try:
        response = make_request("GET", f"{API_BASE}/health")
        if response.status_code == 200:
            # El backend no tiene endpoint específico para usuario actual,
            # pero podemos verificar si las cookies están funcionando
            return {"logged_in": True}
        return None
    except:
        return None


def crear_usuario(datos_usuario):
    """Registrar nuevo usuario"""
    response = make_request("POST", f"{API_BASE}/usuarios/register", json=datos_usuario)
    if response.status_code == 201:
        return response.json()
    return None


def obtener_todos_usuarios():
    """Obtener todos los usuarios (solo para admin)"""
    try:
        response = make_request("GET", f"{API_BASE}/usuarios")

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 403:
            return []
        else:
            return []
    except Exception as e:
        return []


def obtener_reservas_usuario(id_usuario):
    """Obtener reservas de un usuario"""
    try:
        response = make_request("GET", f"{API_BASE}/usuarios/{id_usuario}/reservas")
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        return []


def eliminar_usuario(id_usuario):
    """Eliminar usuario (solo admin)"""
    response = make_request("DELETE", f"{API_BASE}/usuarios/{id_usuario}")
    if response.status_code == 200:
        return {"success": True, "message": "Usuario eliminado"}
    return {"success": False, "message": "Error al eliminar usuario"}


def obtener_usuario_por_id(id_usuario):
    """Obtener usuario por ID (solo admin)"""
    try:
        response = make_request("GET", f"{API_BASE}/usuarios/{id_usuario}")
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        return None


# ===== RESERVAS =====


def crear_reserva(datos_reserva):
    """Crear nueva reserva"""
    try:
        response = make_request("POST", f"{API_BASE}/reservas", json=datos_reserva)
        if response.status_code == 201:
            return True
        # Puedes añadir más lógica de error si es necesario
        return False
    except Exception as e:
        # En caso de error de conexión o cualquier otra excepción
        print(f"Error al crear reserva: {e}")
        return False


def obtener_todas_reservas():
    """Obtener todas las reservas (solo para admin)"""
    try:
        response = make_request("GET", f"{API_BASE}/reservas")
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        return []


def eliminar_reserva(id_reserva):
    """Eliminar reserva (solo admin)"""

    response = make_request("DELETE", f"{API_BASE}/reservas/{id_reserva}")
    if response.status_code == 200:
        return {"success": True, "message": "Reserva eliminada"}
    return {"success": False, "message": "Error al eliminar reserva"}


def obtener_reserva_por_id(id_reserva):
    """Obtener reserva por ID (solo admin)"""
    try:
        response = make_request("GET", f"{API_BASE}/reservas/{id_reserva}")
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        return None


def obtener_reservas_hospedaje(id_hospedaje):
    """Obtener reservas de un hospedaje específico"""
    try:
        response = make_request("GET", f"{API_BASE}/hospedajes/{id_hospedaje}/reservas")
        if response.status_code == 200:
            return response.json()
        return []
    except Exception as e:
        return []


# ===== CLIENTE API GENÉRICO =====


class ApiClient:
    """Cliente API genérico para peticiones HTTP"""

    def __init__(self, base_url=API_BASE):
        self.base_url = base_url

    def post(self, endpoint, data):
        """Realizar petición POST"""
        try:
            response = make_request("POST", f"{self.base_url}{endpoint}", json=data)
            return response
        except Exception as e:
            return None

    def get(self, endpoint):
        """Realizar petición GET"""
        try:
            response = make_request("GET", f"{self.base_url}{endpoint}")
            return response
        except Exception as e:
            return None


# Instancia global del cliente API
api_client = ApiClient()
