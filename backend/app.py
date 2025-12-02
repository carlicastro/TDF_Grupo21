from flask import Flask
import os

# Import blueprints
from models.hospedajes import hospedajes_bp
from models.reservas import reservas_bp
from models.usuario import usuarios_bp

# Crear la aplicación Flask
app = Flask(__name__)

# Configuración básica
app.secret_key = os.environ.get('SECRET_KEY', 'hotel_miracielo_2025')

# Registrar blueprints
app.register_blueprint(hospedajes_bp, url_prefix="/hospedajes") 
app.register_blueprint(reservas_bp, url_prefix="/reservas")
app.register_blueprint(usuarios_bp, url_prefix="/usuarios")

if __name__ == '__main__':
    print("=== INICIANDO BACKEND ===")
    app.run(debug=True, host='0.0.0.0', port=8080)
