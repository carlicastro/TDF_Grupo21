from flask import Flask, session, request
from db import get_connection
import os

# Import blueprints
from models.hospedajes import hospedajes_bp
from models.reservas import reservas_bp
from models.usuario import usuarios_bp

# Crear la aplicación Flask
app = Flask(__name__)

# Configuración de sesiones - debe coincidir con el frontend
app.secret_key = os.environ.get(
    "SECRET_KEY", "hotel_sistema_secreto_2024_dev_muy_largo_y_seguro"
)


# Middleware para manejar autenticación por cookies (no headers)
@app.before_request
def handle_auth_cookies():
    """Maneja la autenticación basada en cookies de sesión del frontend"""
    # No limpiar la sesión - confiar en las cookies
    # Mantener compatibilidad con headers si es necesario (pero ya no limpiar sesiones)
    if request.headers.get("X-Admin-Session") == "true":
        session["user_id"] = request.headers.get("X-User-ID", "1")
        session["user_rol"] = request.headers.get("X-User-Role", "admin")
        session["admin_authenticated"] = True


# Registrar blueprints
app.register_blueprint(hospedajes_bp, url_prefix="/hospedajes")
app.register_blueprint(reservas_bp, url_prefix="/reservas")
app.register_blueprint(usuarios_bp, url_prefix="/usuarios")


# Ruta de salud del servidor
@app.route("/health")
def health_check():
    """
    Endpoint para verificar que el servidor está funcionando
    """
    try:
        # Probar conexión a la base de datos
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        cursor.fetchone()
        cursor.close()
        conn.close()

        return {
            "status": "healthy",
            "database": "connected",
            "message": "API funcionando correctamente",
        }
    except Exception as e:
        return {"status": "unhealthy", "database": "error", "message": str(e)}, 500


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
