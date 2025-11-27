# Backend - API REST Hotel

API REST desarrollada con Flask para gestión de reservas hoteleras.

## 🚀 Instalación

```bash
# Instalar dependencias
pip install -r requirements.txt

# Configurar base de datos
mysql -u root -p
CREATE DATABASE hotel_db;
USE hotel_db;
SOURCE schema.sql;

# Variables de entorno (.env)
DATABASE_HOST=localhost
DATABASE_USER=root
DATABASE_PASSWORD=tu_password
DATABASE_NAME=hotel_db
SECRET_KEY=clave_secreta_muy_segura

# Ejecutar servidor
python app.py
```

## 📡 Endpoints

- `POST /usuarios/register` - Registro
- `POST /usuarios/login` - Autenticación  
- `GET /usuarios/` - Listar usuarios (admin)
- `GET /hospedajes/` - Listar hospedajes
- `GET /reservas/` - Listar reservas (admin)
- `POST /reservas/` - Crear reserva

## 🔧 Dependencias

- Flask 3.0.3
- Flask-CORS 4.0.1
- mysql-connector-python 9.0.0
- python-dotenv 1.0.1

## 🌐 Puerto

Servidor ejecutándose en **puerto 8080**
