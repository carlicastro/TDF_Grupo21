import os
from flask import Flask, jsonify, request
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

# Import existing models
from models import db, Usuario, Hospedaje, Reserva
from datetime import date

app = Flask(__name__)

# --- Database Config ---
DB_USER = os.getenv('DB_USER', 'root')
DB_PASS = os.getenv('DB_PASS', '')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_NAME = os.getenv('DB_NAME', 'hotel_db')

app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+mysqlconnector://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['JWT_SECRET_KEY'] = 'key-super-secreta'
jwt = JWTManager(app)

db.init_app(app)
migrate = Migrate(app, db)

def admin_required(fn):
    @wraps(fn)
    @jwt_required() 
    def wrapper(*args, **kwargs):
        current_user_id = get_jwt_identity()
        user = Usuario.query.get(current_user_id)
        
        if not user or user.rol != 'admin':
            return jsonify({"msg": "Admins only!"}), 403
            
        return fn(*args, **kwargs)
    return wrapper

@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({"msg": "Missing email or password"}), 400
    
    if Usuario.query.filter_by(email=data['email']).first():
        return jsonify({"msg": "User already exists"}), 400

    hashed_password = generate_password_hash(data['password'])
    rol_asignado = 'admin' if data.get('rol') == 'admin' else 'cliente'
    new_user = Usuario(
        nombre=data.get('nombre'),
        email=data.get('email'),
        password=hashed_password,
        rol=rol_asignado
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"msg": "User created successfully"}), 201

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = Usuario.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        return jsonify({"msg": "Bad email or password"}), 401

    access_token = create_access_token(identity=str(user.id))  
     
    return jsonify({
        "msg": "Login success",
        "access_token": access_token,
        "user": user.to_dict()
    }), 200

@app.route('/api/usuarios', methods=['GET'])
@admin_required 
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
@jwt_required()
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