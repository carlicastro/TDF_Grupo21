from flask import Flask, session, request, g
from db import get_connection
import os

from models.hospedajes import hospedajes_bp
from models.reservas import reservas_bp
from models.usuario import usuarios_bp

app = Flask(__name__)

app.secret_key = os.environ.get('SECRET_KEY', 'clave1855')

@app.before_request
def handle_auth_headers():
    """Maneja los headers de autenticación del frontend"""
    if 'user_id' in session:
        del session['user_id']
    if 'user_rol' in session:
        del session['user_rol']
    if 'admin_authenticated' in session:
        del session['admin_authenticated']
    
    if request.headers.get('X-Admin-Session') == 'true':
        session['user_id'] = request.headers.get('X-User-ID', '1')
        session['user_rol'] = request.headers.get('X-User-Role', 'admin')
        session['admin_authenticated'] = True
        print(f"[AUTH] Headers recibidos - User: {session['user_id']}, Role: {session['user_rol']}")

app.register_blueprint(hospedajes_bp, url_prefix="/hospedajes")
app.register_blueprint(reservas_bp, url_prefix="/reservas")
app.register_blueprint(usuarios_bp, url_prefix="/usuarios")

@app.route('/health')
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
            'status': 'healthy',
            'database': 'connected',
            'message': 'API funcionando correctamente'
        }
    except Exception as e:
        return {
            'status': 'unhealthy', 
            'database': 'error',
            'message': str(e)
        }, 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
