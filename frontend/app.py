from flask import Flask, render_template, send_from_directory
from dotenv import load_dotenv
import os

# Cargar .env en el directorio frontend
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

app = Flask(__name__, static_folder='static', template_folder='templates')

@app.route('/')
def index():
    # Index usa templates/index.html ya presente en la carpeta
    return render_template('index.html')

@app.route('/hospedaje/<int:id>')
def detalle_hospedaje(id):
    return render_template('hospedajes/detalle.html')

@app.route('/reservas/consultar')
def consultar():
    return render_template('reservas/consultar.html')

@app.route('/reservas/checkout')
def checkout():
    return render_template('reservas/checkout.html')

@app.route('/perfil')
def perfil():
    return render_template('perfil/mis_reservas.html')

# Ruta de ejemplo para servir assets si se necesita (Flask ya lo hace por defecto)
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory(os.path.join(app.root_path, 'static'), filename)

if __name__ == '__main__':
    debug = os.getenv('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=5001, debug=debug)
