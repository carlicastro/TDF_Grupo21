# Backend - Sistema Hotel 🏨

**API REST simplificada con Flask para gestión de reservas hoteleras**

## 🚀 Inicio Rápido

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Base de datos MySQL
mysql -u root -p < schema.sql

# 3. Ejecutar
python app.py
```

**✅ Servidor corriendo en:** `http://localhost:8080`

## 📁 Estructura

```
backend/
├── app.py              # Servidor principal Flask
├── db.py               # Conexión MySQL
├── schema.sql          # Base de datos + datos prueba
└── models/
    ├── usuario.py      # CRUD usuarios + auth
    ├── hospedajes.py   # CRUD habitaciones
    ├── reservas.py     # CRUD reservas
    └── auth.py         # Login/logout
```

## 🔌 API Endpoints

### Usuarios
- `POST /usuarios/login` - Iniciar sesión
- `POST /usuarios/register` - Registrarse
- `GET /usuarios/{id}/reservas` - Ver reservas usuario

### Hospedajes
- `GET /hospedajes/` - Listar habitaciones
- `POST /hospedajes/` - Crear habitación (admin)

### Reservas  
- `POST /reservas/` - Crear reserva
- `GET /reservas/` - Listar todas (admin)

## 👤 Usuarios de Prueba

```
Admin: admin@hotel.com / admin123
Cliente: juan@example.com / cliente123
Tu usuario: rmallqui@fi.uba.ar / rmallqui@fi.uba.ar
```

## 🛠️ Tecnologías

- **Flask** - Framework web
- **MySQL** - Base de datos  
- **Sessions** - Autenticación
- **CORS** - API accesible desde frontend
