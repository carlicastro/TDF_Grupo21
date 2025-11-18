from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = 'usuario'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False) 
    rol = db.Column(db.String(20), nullable=False, default='user') 
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)

    reservas = db.relationship('Reserva', backref='usuario_obj', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'email': self.email,
            'rol': self.rol
        }

class Hospedaje(db.Model):
    __tablename__ = 'hospedaje'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    capacidad = db.Column(db.Integer, nullable=False)
    precio = db.Column(db.Float, nullable=False)
    foto = db.Column(db.String(255), nullable=True) 
    disponibilidad = db.Column(db.Boolean, default=True)
    tipo = db.Column(db.String(50), nullable=False) 

    reservas = db.relationship('Reserva', backref='hospedaje_obj', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'precio': self.precio,
            'tipo': self.tipo,
            'disponibilidad': self.disponibilidad
        }

class Reserva(db.Model):
    __tablename__ = 'reserva'

    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    id_hospedaje = db.Column(db.Integer, db.ForeignKey('hospedaje.id'), nullable=False)
    
    checkin = db.Column(db.Date, nullable=False)
    checkout = db.Column(db.Date, nullable=False)
    cant_personas = db.Column(db.Integer, nullable=False)
    importe_total = db.Column(db.Float, nullable=False)
    estado = db.Column(db.String(20), default='pendiente')

def to_dict(self):
        return {
            'id': self.id,
            'id_usuario': self.id_usuario,
            'id_hospedaje': self.id_hospedaje,
            'usuario_nombre': self.usuario_obj.nombre if self.usuario_obj else None,
            'hospedaje_nombre': self.hospedaje_obj.nombre if self.hospedaje_obj else None,
            'estado': self.estado,
            'total': self.importe_total
        }