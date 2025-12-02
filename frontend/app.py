"""
Frontend de Hotel
"""

import os
from flask import Flask, session, render_template

# Importar blueprints
from routes.public_routes import public_bp
from routes.auth_routes import auth_bp
from routes.user_routes import user_bp
from routes.reservas_routes import reservas_bp
from routes.admin_routes import admin_bp
from routes.habitaciones_routes import habitaciones_bp

# Crear aplicación Flask
app = Flask(__name__)

# Configuración simple
app.secret_key = 'hotel_secreto_universidad'
app.config['DEBUG'] = True

def variables_sesion():
    """Variables simples para templates"""
    return {
        'logged_in': session.get('logged_in', False),
        'user_nombre': session.get('user_nombre', ''),
        'user_rol': session.get('user_rol', 'cliente')
    }

def page_not_found(error):
    """Error 404 simple"""
    return render_template('public/404.html'), 404

# Registrar funciones
app.context_processor(variables_sesion)
app.errorhandler(404)(page_not_found)

# Registrar blueprints
app.register_blueprint(public_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(user_bp)
app.register_blueprint(reservas_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(habitaciones_bp)

if __name__ == '__main__':
    print("=== INICIANDO FRONTEND ===")
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 3000)), debug=True)