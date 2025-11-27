"""
Frontend de Hotel - Sistema de Gestión de Reservas
Aplicación Flask organizada con Blueprints y Factory Pattern
"""

import os
from flask import Flask

# Importar blueprints
from routes.public_routes import public_bp
from routes.auth_routes import auth_bp
from routes.user_routes import user_bp
from routes.reservas_routes import reservas_bp
from routes.admin_routes import admin_bp
from routes.habitaciones_routes import habitaciones_bp

def create_app():
    """
    Factory para crear la aplicación Flask con configuración optimizada
    """
    app = Flask(__name__)
    
    # Configuración de la aplicación
    app.config.update(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'hotel_sistema_secreto_2024_dev_muy_largo_y_seguro'),
        DEBUG=True,
        TEMPLATES_AUTO_RELOAD=True,
        JSON_AS_ASCII=False,  # Para caracteres especiales en español
        SESSION_PERMANENT=False,  # No forzar permanente, decidir por request
        PERMANENT_SESSION_LIFETIME=14400,  # 4 horas en segundos (más tiempo)
        SESSION_COOKIE_SECURE=False,  # True en producción con HTTPS
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE='Lax',
        SESSION_REFRESH_EACH_REQUEST=True  # Refrescar sesión en cada request
    )
    
    # Context processor para hacer disponible la sesión en todos los templates
    @app.context_processor
    def inject_session():
        """Hacer variables de sesión disponibles en todos los templates"""
        from flask import session
        return {
            'logged_in': session.get('logged_in', False),
            'user_nombre': session.get('user_nombre', ''),
            'user_email': session.get('user_email', ''),
            'user_rol': session.get('user_rol', 'cliente'),
            'user_id': session.get('user_id', '')
        }
    
    # Middleware para mantener la sesión activa
    @app.before_request
    def make_session_permanent():
        """Asegurar que la sesión se mantenga activa sin invalidar"""
        from flask import session
        
        # Solo marcar como permanente si ya existe una sesión
        if session.get('logged_in'):
            session.permanent = True
        
        # No hacer verificaciones del backend aquí para evitar invalidaciones
    
    # Registrar blueprints
    app.register_blueprint(public_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(reservas_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(habitaciones_bp)
    
    # Manejadores de errores
    @app.errorhandler(404)
    def page_not_found(error):
        """Manejador personalizado para error 404"""
        from flask import render_template
        return render_template('public/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """Manejador personalizado para error 500"""
        from flask import render_template
        return render_template('public/404.html'), 500
    
    return app

# Crear la aplicación
app = create_app()

if __name__ == '__main__':
    # Configuración del servidor de desarrollo
    app.run(
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 3000)),
        debug=True,
        use_reloader=True
    )