import os
from flask import Flask, jsonify
from flask_migrate import Migrate
from models import db, Usuario, Hospedaje, Reserva # Import db and models
from datetime import date

app = Flask(__name__)

# --- Configuration ---
DB_USER = os.getenv('DB_USER', 'root')
DB_PASS = os.getenv('DB_PASS', '')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_NAME = os.getenv('DB_NAME', 'hotel_db')

app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+mysqlconnector://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# --- Extensions ---
db.init_app(app)
migrate = Migrate(app, db)

@app.route('/api/usuarios', methods=['GET'])
def listar_usuarios():
    try:
        usuarios = Usuario.query.all()
        return jsonify({'ok': True, 'data': [u.to_dict() for u in usuarios]}), 200
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 500

@app.route('/api/hospedajes', methods=['GET'])
def listar_hospedajes():
    try:
        hospedajes = Hospedaje.query.all()
        return jsonify({'ok': True, 'data': [h.to_dict() for h in hospedajes]}), 200
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 500

@app.route('/api/reservas', methods=['GET'])
def listar_reservas():
    try:
        reservas = Reserva.query.all()
        return jsonify({'ok': True, 'data': [r.to_dict() for r in reservas]}), 200
    except Exception as e:
        return jsonify({'ok': False, 'error': str(e)}), 500

@app.cli.command("seed")
def seed_db():
    """Seeds the database with test data."""
    print("Seeding database...")
    
    # 1. Users
    admin = Usuario(nombre="Admin", email="admin@test.com", password="123", rol="admin")
    user1 = Usuario(nombre="Juan", email="juan@test.com", password="123", rol="cliente")
    
    # 2. Hospedajes
    hotel = Hospedaje(nombre="Hotel Sol", capacidad=2, precio=100.0, tipo="Hotel", descripcion="Lindo hotel")
    
    db.session.add_all([admin, user1, hotel])
    db.session.commit()

    # 3. Reserva
    reserva = Reserva(
        id_usuario=user1.id,
        id_hospedaje=hotel.id,
        checkin=date(2025, 12, 1),
        checkout=date(2025, 12, 5),
        cant_personas=2,
        importe_total=400.0
    )
    db.session.add(reserva)
    db.session.commit()
    print("Database seeded successfully!")

if __name__ == '__main__':
    app.run(debug=True)