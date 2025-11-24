# Backend del Sistema de Hotel (Flask + MySQL + Autenticación)

API REST para sistema de gestión hotelera con Flask y MySQL.

## ✅ Características Principales

- **Flask**: Servidor web con sistema de autenticación por sesiones
- **MySQL**: Base de datos con SQLAlchemy + mysql-connector-python
- **Autenticación**: Sistema de login simple con sesiones Flask
- **Roles de Usuario**: Admin, Empleado, Cliente
- **Seguridad**: Contraseñas hasheadas con Werkzeug
- **API REST**: Endpoints para CRUD de usuarios, hospedajes y reservas

## 📚 Documentación

- **[📋 API Completa](API_DOCUMENTATION.md)** - Documentación detallada de todos los endpoints
- **[📮 Postman](postman_collection.json)** - Colección para testing de API

## 🔑 Credenciales de Prueba

| Usuario | Email | Password | Rol |
|---------|-------|----------|-----|
| Admin | `admin@hotel.com` | `admin123` | admin |
| Cliente | `juan@example.com` | `cliente123` | cliente |

### 1. Crear entorno virtual e instalar dependencias

## 🛠️ Endpoints Principales

```bash

### 🌐 Públicospython -m venv .venv

- `GET /hospedajes/` - Lista hospedajessource .venv/Scripts/activate    # Windows

- `POST /usuarios/login` - Loginpip install -r requirements.txt

- `POST /usuarios/register` - Registro```



### 🔐 Admin### 2. Configurar base de datos MySQL

- `POST /hospedajes/` - Crear hospedaje

- `GET /usuarios/` - Lista usuarios```sql

- `GET /reservas/` - Lista reservas# Crear base de datos

CREATE DATABASE hotel_db;

### 🔑 Autenticados

- `POST /reservas/` - Crear reserva# Ejecutar el esquema

- `GET /reservas/usuario/<id>` - Mis reservasmysql -u root -p hotel_db < schema.sql

```

## 📁 Estructura

### 3. Configurar variables de entorno (opcional)

```

backend/```bash

├── app.py                    # Aplicación principal# Copiar y modificar el archivo de ejemplo

├── db.py                     # Conexión DBcp .env.example .env

├── schema.sql                # Base de datos# Editar .env con tus credenciales de MySQL

├── requirements.txt          # Dependencias```

├── API_DOCUMENTATION.md      # Docs completas

├── postman_collection.json   # Tests Postman### 4. Ejecutar el servidor

└── models/                   # Modelos

    ├── usuario.py            # Autenticación```bash

    ├── hospedajes.py         # CRUD hospedajespython app.py

    └── reservas.py           # CRUD reservas```

```

El servidor estará disponible en: `http://127.0.0.1:5000`

## ✅ Estado

## 🧪 Pruebas del Sistema

- **17 endpoints** verificados y funcionando

- **Sistema de permisos** implementado### Probar autenticación

- **Autenticación** con Flask sessions```bash

- **CRUD completo** para todas las entidades# Ejecutar suite de pruebas automatizadas

python test_auth.py

---

# Generar nuevas contraseñas hasheadas

**Grupo 21 - TDF 2025** 🚀python generate_passwords.py
```

## 📋 Endpoints de Autenticación

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/login` | Iniciar sesión con email/password |
| POST | `/logout` | Cerrar sesión |
| POST | `/register` | Registrar nuevo usuario |
| GET | `/session-info` | Información del usuario logueado |
| GET | `/check-auth` | Verificar si está autenticado |
| GET | `/user/protected` | Ruta protegida para usuarios |
| GET | `/admin/protected` | Ruta protegida para administradores |

### Ejemplo de Login

```bash
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@hotel.com",
    "password": "admin123"
  }'
```

**Respuesta:**
```json
{
  "success": true,
  "message": "Login exitoso",
  "user": {
    "id": 1,
    "nombre": "Administrador",
    "email": "admin@hotel.com", 
    "rol": "admin"
  },
  "redirect_url": "/admin/dashboard"
}
```

## 📋 Endpoints de Datos

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/usuarios/` | Obtener todos los usuarios |
| GET | `/usuarios/<id>` | Obtener usuario por ID |
| POST | `/usuarios/` | Crear nuevo usuario |
| PUT | `/usuarios/<id>` | Actualizar usuario |
| DELETE | `/usuarios/<id>` | Eliminar usuario |
| GET | `/hospedajes/` | Obtener todos los hospedajes |
| GET | `/reservas/` | Obtener todas las reservas |

## 🔒 Sistema de Roles y Permisos

### Roles Disponibles
- **admin**: Acceso completo al sistema
- **empleado**: Gestión de reservas y hospedajes  
- **cliente**: Solo perfil personal y reservas propias

### Decoradores de Protección
```python
@login_required      # Requiere usuario logueado
@admin_required      # Requiere rol de administrador
```

### Redirecciones por Rol
- **Admin** → `/admin/dashboard`
- **Empleado** → `/admin/dashboard` 
- **Cliente** → `/perfil`

## 📁 Estructura del Proyecto

```text
backend/
├── app.py                    # Servidor Flask + autenticación
├── models/
│   ├── __init__.py
│   ├── usuario.py           # CRUD usuarios + auth
│   ├── hospedajes.py        # CRUD hospedajes  
│   └── reservas.py          # CRUD reservas
├── db.py                    # Conexión MySQL
├── schema.sql              # Schema + datos de prueba
├── requirements.txt        # Dependencias
├── generate_passwords.py   # Generar hashes
├── test_auth.py           # Pruebas del login
├── .env.example           # Variables de entorno
└── README.md              # Este archivo
```

## 🔧 Configuración

### Variables de Entorno (.env)
```bash
SECRET_KEY=tu_clave_secreta_muy_segura
DB_HOST=localhost
DB_USER=root  
DB_PASSWORD=tu_password_mysql
DB_NAME=hotel_db
DB_PORT=3306
```

### Configuración por Defecto
- Puerto: `5000`
- Host: `0.0.0.0` 
- Debug: `True`
- Sesiones: Archivos del sistema

## 📊 Base de Datos

### Tablas Principales
- **usuarios**: Autenticación y datos personales
- **hospedajes**: Habitaciones disponibles
- **reservas**: Reservas de clientes

### Relaciones
- `reservas.id_usuario` → `usuarios.id_usuario`
- `reservas.id_hospedaje` → `hospedajes.id_hospedaje`

## 🔄 Integración con Frontend

El backend está diseñado para integrarse con el frontend Flask en puerto 5001:

- **Backend**: `http://localhost:5000` (API + Auth)
- **Frontend**: `http://localhost:5001` (Templates + UI)

### Flujo de Autenticación
1. Frontend envía credenciales a `/login`
2. Backend valida y crea sesión
3. Redirección según rol del usuario
4. Frontend verifica sesión con `/session-info`

## 📝 Notas Importantes

- **Producción**: Cambiar `SECRET_KEY` en producción
- **Base de Datos**: Ejecutar `schema.sql` antes del primer uso  
- **Contraseñas**: Usar `generate_passwords.py` para crear hashes
- **Pruebas**: Ejecutar `test_auth.py` para verificar funcionamiento
