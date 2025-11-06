# Backend del Sistema de Hotel (Flask + MySQL)


## ✅ Características

- **Flask**: Servidor web 
- **MySQL**: Base de datos con SQLAlchemy + mysql-connector-python

## 🚀 Instalación y Uso

### 1. Crear entorno virtual e instalar dependencias

```bash
python -m venv .venv
source .venv/Scripts/activate    # Windows
pip install -r requirements.txt
```

### 2. Configurar base de datos MySQL

- Base de datos: `hotel_db`
- Usuario: `root` (sin contraseña por defecto)
- Ejecutar el archivo `schema.sql` para crear las tablas

### 3. Ejecutar el servidor

```bash
python app.py
```

El servidor estará disponible en: `http://127.0.0.1:5000`

## 📋 Endpoints API

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/test-db` | Test de conexión a la base de datos |
| GET | `/api/usuarios` | Obtener todos los usuarios |
| GET | `/api/hospedajes` | Obtener todos los hospedajes |
| GET | `/api/reservas` | Obtener todas las reservas (con JOIN) |

### Ejemplo de respuesta

```json
{
  "ok": true,
  "data": [
    {
      "id_usuario": 1,
      "nombre": "Juan Pérez",
      "email": "juan@email.com",
      "rol": "cliente"
    }
  ]
}
```

## 📁 Estructura del Proyecto

```text
backend/
├── app.py                 # Servidor Flask principal
├── models/
│   ├── __init__.py        # Importaciones del paquete
│   ├── usuario.py         # Funciones CRUD usuarios
│   ├── hospedajes.py      # Funciones CRUD hospedajes
│   └── reservas.py        # Funciones CRUD reservas
├── requirements.txt       # Dependencias Python
├── schema.sql            # Esquema de base de datos
├── database.dbml         # Diagrama de base de datos
└── .venv/                # Entorno virtual
```

## 🔧 Configuración (Variables de Entorno)

Por defecto usa estas credenciales:

- `DB_USER=root`
- `DB_PASS=` (vacío)
- `DB_HOST=localhost`
- `DB_NAME=hotel_db`

Para cambiar, define las variables de entorno antes de ejecutar.

## 📊 Base de Datos

El sistema maneja 3 tablas principales:

- **usuarios**: Clientes y administradores del sistema
- **hospedajes**: Habitaciones y propiedades disponibles
- **reservas**: Reservas realizadas por los usuarios

Ver `schema.sql` para el esquema completo.
