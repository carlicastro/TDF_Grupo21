# Hotel API Documentation# API Documentation - Hotel Management System# Hotel Management API# 🏨 Hotel Management API Documentation



Base URL: http://localhost:5000



## Authentication## Base URL

Uses Flask sessions. Login stores credentials in server session.

```

User Roles:

- admin: Full accesshttp://localhost:5000## Información General## Información General

- cliente: Limited access to own data

```

## USUARIOS



### POST /usuarios/login

Login user## Authentication

```json

{Uses Flask sessions. After login, credentials are stored in server session.- **Base URL:** `http://localhost:5000`**Base URL:** `http://localhost:5000`  

  "email": "usuario@email.com",

  "password": "contraseña123"

}

```**User Roles:**- **Versión:** 1.0  **Versión:** 1.0  

Response 200:

```json- `admin`: Full access to all endpoints

{

  "success": true,- `cliente`: Limited access to own reservations and data- **Tecnologías:** Flask, MySQL, Python 3.x**Tecnologías:** Flask, MySQL, Python 3.x  

  "message": "Login exitoso",

  "user": {

    "id": 1,

    "nombre": "Juan Pérez",## USUARIOS- **Autenticación:** Sesiones Flask**Autenticación:** Sesiones Flask

    "email": "juan@email.com",

    "rol": "cliente"

  }

}### POST `/usuarios/login`

```

Login user

### POST /usuarios/logout

Logout user## Tabla de Contenido---



### POST /usuarios/register**Request:**

Register new user

```json```json

{

  "nombre": "María García",{

  "email": "maria@email.com",

  "password": "contraseña123",  "email": "usuario@email.com",1. [Autenticación](#autenticacion)## 📋 Índice

  "telefono": "+1234567890"

}  "password": "contraseña123"

```

}2. [Usuarios](#usuarios)

### GET /usuarios/

Get all users (Admin only)```



### GET /usuarios/<user_id>3. [Hospedajes](#hospedajes)1. [Autenticación](#autenticación)

Get user by ID (Admin or owner)

**Response 200:**

### PUT /usuarios/<user_id>

Update user (Admin or owner)```json4. [Reservas](#reservas)2. [Usuarios](#usuarios)



### DELETE /usuarios/<user_id>{

Delete user (Admin only)

  "success": true,5. [Estado del Sistema](#estado)3. [Hospedajes](#hospedajes)

## HOSPEDAJES

  "message": "Login exitoso",

### GET /hospedajes/

Get all accommodations (Public)  "user": {6. [Códigos de Respuesta](#codigos)4. [Reservas](#reservas)

```json

[    "id": 1,

  {

    "id_hospedaje": 1,    "nombre": "Juan Pérez",7. [Ejemplos de Uso](#ejemplos)5. [Sistema de Salud](#sistema-de-salud)

    "nombre": "Suite Presidencial",

    "descripcion": "Amplia suite con vista al mar",    "email": "juan@email.com",

    "precio": 350.00,

    "capacidad": 4,    "rol": "cliente"6. [Códigos de Estado](#códigos-de-estado)

    "foto": "suite-presidencial.jpg",

    "disponibilidad": 1,  }

    "tipo": "suite"

  }}## Autenticacion7. [Ejemplos de Uso](#ejemplos-de-uso)

]

``````



### GET /hospedajes/<hospedaje_id>

Get accommodation by ID (Public)

### POST `/usuarios/logout`

### POST /hospedajes/

Create accommodation (Admin only)Logout userLa API utiliza sesiones Flask. Después del login, las credenciales se almacenan en la sesión del servidor.---

```json

{

  "nombre": "Habitación Deluxe",

  "descripcion": "Habitación moderna con balcón",**Response 200:**

  "precio": 150.00,

  "capacidad": 2,```json

  "foto": "habitacion-deluxe.jpg",

  "tipo": "habitacion"{**Roles de Usuario:**## � Autenticación

}

```  "success": true,



### PUT /hospedajes/<hospedaje_id>  "message": "Sesión cerrada exitosamente"- `admin`: Acceso completo a todos los endpoints

Update accommodation (Admin only)

}

### DELETE /hospedajes/<hospedaje_id>

Delete accommodation (Admin only)```- `cliente`: Acceso limitado a sus propias reservas y datosLa API utiliza sesiones Flask para manejar la autenticación. Después del login exitoso, las credenciales se almacenan en la sesión del servidor.



## RESERVAS



### GET /reservas/### POST `/usuarios/register`

Get all reservations (Admin only)

```jsonRegister new user

[

  {## Usuarios### Roles de Usuario:

    "id_reserva": 1,

    "id_usuario": 2,**Request:**

    "id_hospedaje": 1,

    "fecha_inicio": "2024-02-15",```json- **admin**: Acceso completo a todos los endpoints

    "fecha_fin": "2024-02-18",

    "num_huespedes": 2,{

    "precio_total": 1050.00,

    "estado": "confirmada",  "nombre": "María García",### Autenticación- **cliente**: Acceso limitado a sus propias reservas y datos

    "fecha_creacion": "2024-01-20T14:30:00",

    "usuario_nombre": "Juan Pérez",  "email": "maria@email.com",

    "hospedaje_nombre": "Suite Presidencial"

  }  "password": "contraseña123",

]

```  "telefono": "+1234567890"



### GET /reservas/<reserva_id>}#### POST `/usuarios/login`- ✅ **Sistema de permisos** basado en roles (admin/empleado/cliente)### **Ejecutar el servidor**

Get reservation by ID (Admin or owner)

```

### GET /reservas/usuario/<user_id>

Get user reservations (Admin or owner)Iniciar sesión de usuario



### POST /reservas/**Response 201:**

Create reservation (Authenticated user)

```json```json- ✅ **Base de datos MySQL** con relaciones y integridad referencial```bash

{

  "id_hospedaje": 1,{

  "fecha_inicio": "2024-03-15",

  "fecha_fin": "2024-03-18",  "success": true,**Request Body:**

  "num_huespedes": 2

}  "message": "Usuario registrado exitosamente",

```

  "user_id": 5```json- ✅ **Arquitectura modular** con blueprints de Flaskcd backend

### PUT /reservas/<reserva_id>

Update reservation (Admin only)}



### DELETE /reservas/<reserva_id>```{

Delete reservation (Admin or owner)



## HEALTH

### GET `/usuarios/`  "email": "usuario@email.com",python app.py

### GET /health

Check server statusGet all users (Admin only)

```json

{  "password": "contraseña123"

  "status": "healthy",

  "database": "connected",### GET `/usuarios/<user_id>`

  "message": "API funcionando correctamente"

}Get user by ID (Admin or owner)}## 🛠️ Tecnologías Utilizadas```

```



## HTTP Codes

- 200: OK### PUT `/usuarios/<user_id>````

- 201: Created

- 400: Bad RequestUpdate user data (Admin or owner)

- 401: Unauthorized

- 403: Forbidden**Servidor:** http://localhost:5000

- 404: Not Found

- 500: Internal Server Error### DELETE `/usuarios/<user_id>`



## ExamplesDelete user (Admin only)**Response (200):**



Login and create reservation:

```bash

# Login## HOSPEDAJES```json- **Backend**: Python 3.13, Flask 3.0

curl -X POST http://localhost:5000/usuarios/login \

  -H "Content-Type: application/json" \

  -d '{"email": "juan@email.com", "password": "123456"}' \

  -c cookies.txt### GET `/hospedajes/`{



# Create reservationGet all accommodations (Public)

curl -X POST http://localhost:5000/reservas/ \

  -H "Content-Type: application/json" \  "success": true,- **Base de Datos**: MySQL 8.0---

  -d '{"id_hospedaje": 1, "fecha_inicio": "2024-03-15", "fecha_fin": "2024-03-18", "num_huespedes": 2}' \

  -b cookies.txt**Response 200:**

```

```json  "message": "Login exitoso",

Get accommodations:

```bash[

curl -X GET http://localhost:5000/hospedajes/

```  {  "user": {- **Autenticación**: Flask Sessions + Werkzeug Security



## Setup    "id_hospedaje": 1,



Environment variables:    "nombre": "Suite Presidencial",    "id": 1,

```

SECRET_KEY=tu_clave_secreta_muy_segura_123    "descripcion": "Amplia suite con vista al mar",

DB_HOST=localhost

DB_USER=root    "precio": 350.00,    "nombre": "Juan Pérez",- **ORM**: MySQL Connector Python (queries nativas)## 🔐 **AUTENTICACIÓN - `/usuarios`**

DB_PASSWORD=tu_password

DB_NAME=hotel_db    "capacidad": 4,

```

    "foto": "suite-presidencial.jpg",    "email": "juan@email.com",

Start server:

```bash    "disponibilidad": 1,

cd backend

python app.py    "tipo": "suite"    "rol": "cliente"- **Arquitectura**: Blueprints de Flask

```

  }

## Notes

1. Sessions handled by Flask]  }

2. Use cookies for session maintenance

3. Date format: YYYY-MM-DD```

4. Requires MySQL connection

5. All endpoints validate permissions}### **POST** `/usuarios/login`



Last updated: November 13, 2025### GET `/hospedajes/<hospedaje_id>`

Get accommodation by ID (Public)```



### POST `/hospedajes/`## 📦 Instalación y Configuración**Descripción:** Iniciar sesión  

Create new accommodation (Admin only)

#### POST `/usuarios/logout`

**Request:**

```jsonCerrar sesión**Body:**

{

  "nombre": "Habitación Deluxe",

  "descripcion": "Habitación moderna con balcón",

  "precio": 150.00,**Response (200):**### 1. Requisitos Previos```json

  "capacidad": 2,

  "foto": "habitacion-deluxe.jpg",```json

  "tipo": "habitacion"

}{```bash{

```

  "success": true,

### PUT `/hospedajes/<hospedaje_id>`

Update accommodation (Admin only)  "message": "Sesión cerrada exitosamente"# Python 3.11+  "email": "admin@test.com",



### DELETE `/hospedajes/<hospedaje_id>`}

Delete accommodation (Admin only)

```# MySQL 8.0+  "password": "admin123"

## RESERVAS



### GET `/reservas/`

Get all reservations (Admin only)#### POST `/usuarios/register`# Git}



**Response 200:**Registrar nuevo usuario

```json

[``````

  {

    "id_reserva": 1,**Request Body:**

    "id_usuario": 2,

    "id_hospedaje": 1,```json**Respuesta exitosa:**

    "fecha_inicio": "2024-02-15",

    "fecha_fin": "2024-02-18",{

    "num_huespedes": 2,

    "precio_total": 1050.00,  "nombre": "María García",### 2. Instalación```json

    "estado": "confirmada",

    "fecha_creacion": "2024-01-20T14:30:00",  "email": "maria@email.com",

    "usuario_nombre": "Juan Pérez",

    "hospedaje_nombre": "Suite Presidencial"  "password": "contraseña123",```bash{

  }

]  "telefono": "+1234567890"

```

}# Clonar repositorio  "success": true,

### GET `/reservas/<reserva_id>`

Get reservation by ID (Admin or owner)```



### GET `/reservas/usuario/<user_id>`git clone https://github.com/rafaelmallquii/TDF_Grupo21.git  "message": "Login exitoso",

Get user reservations (Admin or owner)

**Response (201):**

### POST `/reservas/`

Create new reservation (Authenticated user)```jsoncd TDF_Grupo21/backend  "user": {



**Request:**{

```json

{  "success": true,    "id": 1,

  "id_hospedaje": 1,

  "fecha_inicio": "2024-03-15",  "message": "Usuario registrado exitosamente",

  "fecha_fin": "2024-03-18",

  "num_huespedes": 2  "user_id": 5# Crear entorno virtual    "nombre": "Admin",

}

```}



### PUT `/reservas/<reserva_id>````python -m venv .venv    "email": "admin@test.com",

Update reservation status (Admin only)



### DELETE `/reservas/<reserva_id>`

Delete reservation (Admin or owner)### Gestión de Usuariossource .venv/bin/activate  # Linux/Mac    "rol": "admin"



## HEALTH



### GET `/health`#### GET `/usuarios/`.venv\Scripts\activate     # Windows  }

Check server status

Obtener todos los usuarios (Solo Admin)

**Response 200:**

```json}

{

  "status": "healthy",**Response (200):**

  "database": "connected",

  "message": "API funcionando correctamente"```json# Instalar dependencias```

}

```[



## HTTP Status Codes  {pip install -r requirements.txt



| Code | Description |    "id_usuario": 1,

|------|-------------|

| 200 | OK |    "nombre": "Juan Pérez",```### **POST** `/usuarios/logout`

| 201 | Created |

| 400 | Bad Request |    "email": "juan@email.com",

| 401 | Unauthorized |

| 403 | Forbidden |    "telefono": "+1234567890",**Descripción:** Cerrar sesión  

| 404 | Not Found |

| 500 | Internal Server Error |    "rol": "cliente",



## Examples    "fecha_registro": "2024-01-15T10:30:00"### 3. Configuración de Base de Datos**Respuesta:**



### Login and Create Reservation  }

```bash

# 1. Login]```bash```json

curl -X POST http://localhost:5000/usuarios/login \

  -H "Content-Type: application/json" \```

  -d '{"email": "juan@email.com", "password": "123456"}' \

  -c cookies.txt# Crear base de datos en MySQL{



# 2. Create reservation#### GET `/usuarios/<user_id>`

curl -X POST http://localhost:5000/reservas/ \

  -H "Content-Type: application/json" \Obtener usuario por ID (Admin o propietario)mysql -u root -p < schema.sql  "success": true,

  -d '{

    "id_hospedaje": 1,

    "fecha_inicio": "2024-03-15",

    "fecha_fin": "2024-03-18",#### PUT `/usuarios/<user_id>````  "message": "Sesión cerrada exitosamente"

    "num_huespedes": 2

  }' \Actualizar datos de usuario (Admin o propietario)

  -b cookies.txt

```}



### Get Accommodations#### DELETE `/usuarios/<user_id>`

```bash

curl -X GET http://localhost:5000/hospedajes/Eliminar usuario (Solo Admin)### 4. Variables de Entorno```

```



### Admin - View Reservations

```bash## Hospedajes```bash

# Login as admin

curl -X POST http://localhost:5000/usuarios/login \

  -H "Content-Type: application/json" \

  -d '{"email": "admin@hotel.com", "password": "admin123"}' \### GET `/hospedajes/`# Opcional - Por defecto usa configuración local### **POST** `/usuarios/register`

  -c admin_cookies.txt

Obtener todos los hospedajes (Público)

# View all reservations

curl -X GET http://localhost:5000/reservas/ \export SECRET_KEY="tu_clave_secreta_muy_segura_123"**Descripción:** Registrar nuevo usuario  

  -b admin_cookies.txt

```**Response (200):**



## Setup```jsonexport DB_HOST="localhost"**Body:**



### Environment Variables[

```bash

SECRET_KEY=tu_clave_secreta_muy_segura_123  {export DB_USER="root"```json

DB_HOST=localhost

DB_USER=root    "id_hospedaje": 1,

DB_PASSWORD=tu_password

DB_NAME=hotel_db    "nombre": "Suite Presidencial",export DB_PASSWORD="tu_password"{

```

    "descripcion": "Amplia suite con vista al mar",

### Start Server

```bash    "precio": 350.00,export DB_NAME="hotel_db"  "nombre": "Juan Pérez",

cd backend

python app.py    "capacidad": 4,

```

    "foto": "suite-presidencial.jpg",```  "email": "juan@test.com",

Server starts at `http://localhost:5000`

    "disponibilidad": 1,

## Notes

    "tipo": "suite"  "password": "123456",

1. Sessions handled automatically by Flask

2. Use cookies to maintain session  }

3. All endpoints validate permissions

4. Date format: `YYYY-MM-DD`]### 5. Ejecutar Servidor  "telefono": "123-456-7890",

5. API uses MySQL - check DB connection

```

---

*Last updated: November 13, 2025*```bash  "direccion": "Calle 123",

### GET `/hospedajes/<hospedaje_id>`

Obtener hospedaje por ID (Público)python app.py  "rol": "cliente"



### POST `/hospedajes/````}

Crear nuevo hospedaje (Solo Admin)

```

**Request Body:**

```jsonLa API estará disponible en `http://localhost:5000`

{

  "nombre": "Habitación Deluxe",---

  "descripcion": "Habitación moderna con balcón",

  "precio": 150.00,## 📚 Documentación de Endpoints

  "capacidad": 2,

  "foto": "habitacion-deluxe.jpg",## 👥 **USUARIOS - `/usuarios`** (Solo Admin)

  "tipo": "habitacion"

}### 🔧 Sistema

```

| Endpoint | Método | Descripción | Autenticación |### **GET** `/usuarios/`

### PUT `/hospedajes/<hospedaje_id>`

Actualizar hospedaje (Solo Admin)|----------|---------|-------------|---------------|**Descripción:** Listar todos los usuarios  



### DELETE `/hospedajes/<hospedaje_id>`| `/health` | GET | Estado del servidor y DB | 🌐 Público |**Permisos:** Solo administradores  

Eliminar hospedaje (Solo Admin)

**Respuesta:**

## Reservas

### 🏠 Hospedajes```json

### GET `/reservas/`

Obtener todas las reservas (Solo Admin)| Endpoint | Método | Descripción | Autenticación |[



**Response (200):**|----------|---------|-------------|---------------|  {

```json

[| `/hospedajes/` | GET | Lista todos los hospedajes | 🌐 Público |    "id_usuario": 1,

  {

    "id_reserva": 1,| `/hospedajes/<id>` | GET | Detalle de hospedaje | 🌐 Público |    "nombre": "Admin",

    "id_usuario": 2,

    "id_hospedaje": 1,| `/hospedajes/` | POST | Crear hospedaje | 🔐 Solo Admin |    "email": "admin@test.com",

    "fecha_inicio": "2024-02-15",

    "fecha_fin": "2024-02-18",| `/hospedajes/<id>` | PUT | Actualizar hospedaje | 🔐 Solo Admin |    "telefono": "123456789",

    "num_huespedes": 2,

    "precio_total": 1050.00,| `/hospedajes/<id>` | DELETE | Eliminar hospedaje | 🔐 Solo Admin |    "rol": "admin",

    "estado": "confirmada",

    "fecha_creacion": "2024-01-20T14:30:00",    "direccion": "Admin Street",

    "usuario_nombre": "Juan Pérez",

    "hospedaje_nombre": "Suite Presidencial"### 👤 Usuarios    "fecha_registro": "2024-01-01T00:00:00"

  }

]| Endpoint | Método | Descripción | Autenticación |  }

```

|----------|---------|-------------|---------------|]

### GET `/reservas/<reserva_id>`

Obtener reserva por ID (Admin o propietario)| `/usuarios/login` | POST | Iniciar sesión | 🌐 Público |```



### GET `/reservas/usuario/<user_id>`| `/usuarios/logout` | POST | Cerrar sesión | 🌐 Público |

Obtener reservas de un usuario (Admin o propietario)

| `/usuarios/register` | POST | Registrar usuario | 🌐 Público |### **GET** `/usuarios/{id}`

### POST `/reservas/`

Crear nueva reserva (Usuario autenticado)| `/usuarios/` | GET | Lista todos los usuarios | 🔐 Solo Admin |**Descripción:** Ver usuario específico  



**Request Body:**| `/usuarios/<id>` | GET | Detalle de usuario | 🌐 Público |**Ejemplo:** `/usuarios/1`

```json

{| `/usuarios/<id>` | DELETE | Eliminar usuario | 🔐 Solo Admin |

  "id_hospedaje": 1,

  "fecha_inicio": "2024-03-15",### **DELETE** `/usuarios/{id}`

  "fecha_fin": "2024-03-18",

  "num_huespedes": 2### 📋 Reservas**Descripción:** Eliminar usuario  

}

```| Endpoint | Método | Descripción | Autenticación |**Permisos:** Solo administradores  



### PUT `/reservas/<reserva_id>`|----------|---------|-------------|---------------|**Ejemplo:** `/usuarios/5`

Actualizar estado de reserva (Solo Admin)

| `/reservas/` | POST | Crear reserva | 🔑 Usuario logueado |

### DELETE `/reservas/<reserva_id>`

Eliminar reserva (Admin o propietario)| `/reservas/` | GET | Lista todas las reservas | 🔐 Solo Admin |---



## Estado| `/reservas/<id>` | GET | Detalle de reserva | 🔐 Solo Admin |



### GET `/health`| `/reservas/<id>` | DELETE | Eliminar reserva | 🔐 Solo Admin |## 🏨 **HOSPEDAJES - `/hospedajes`**

Verificar estado del servidor

| `/reservas/usuario/<id>` | GET | Reservas de usuario | 🔑 Usuario logueado |

**Response (200):**

```json### **GET** `/hospedajes/`

{

  "status": "healthy",## 🔐 Sistema de Autenticación**Descripción:** Ver todos los hospedajes  

  "database": "connected",

  "message": "API funcionando correctamente"**Permisos:** Público  

}

```### Roles de Usuario**Respuesta:**



## Codigos- **👑 admin**: Acceso completo a todos los endpoints```json



| Código | Descripción |- **👨‍💼 empleado**: Acceso a consultas y algunas operaciones[

|--------|-------------|

| 200 | OK - Solicitud exitosa |- **👤 cliente**: Acceso limitado a operaciones propias  {

| 201 | Created - Recurso creado |

| 400 | Bad Request - Datos inválidos |    "id_hospedaje": 1,

| 401 | Unauthorized - Sin autenticación |

| 403 | Forbidden - Sin permisos |### Login    "nombre": "Hotel Paradise",

| 404 | Not Found - Recurso no encontrado |

| 500 | Internal Server Error - Error del servidor |```json    "descripcion": "Hermoso hotel en la playa",



## EjemplosPOST /usuarios/login    "precio_por_noche": 150.00,



### Ejemplo 1: Login y crear reserva{    "capacidad": 4,



```bash    "email": "admin@hotel.com",    "ubicacion": "Cancún, México",

# 1. Login

curl -X POST http://localhost:5000/usuarios/login \    "password": "admin123"    "disponible": true

  -H "Content-Type: application/json" \

  -d '{"email": "juan@email.com", "password": "123456"}' \}  }

  -c cookies.txt

]

# 2. Crear reserva

curl -X POST http://localhost:5000/reservas/ \Response:```

  -H "Content-Type: application/json" \

  -d '{{

    "id_hospedaje": 1,

    "fecha_inicio": "2024-03-15",    "success": true,### **GET** `/hospedajes/{id}`

    "fecha_fin": "2024-03-18",

    "num_huespedes": 2    "message": "Login exitoso",**Descripción:** Ver hospedaje específico  

  }' \

  -b cookies.txt    "user": {**Permisos:** Público  

```

        "id": 3,**Ejemplo:** `/hospedajes/1`

### Ejemplo 2: Obtener hospedajes

        "nombre": "Administrador",

```bash

curl -X GET http://localhost:5000/hospedajes/        "email": "admin@hotel.com",### **POST** `/hospedajes/` (Solo Admin)

```

        "rol": "admin"**Descripción:** Crear hospedaje  

### Ejemplo 3: Admin - Ver reservas

    }**Permisos:** Solo administradores  

```bash

# Login como admin}**Body:**

curl -X POST http://localhost:5000/usuarios/login \

  -H "Content-Type: application/json" \``````json

  -d '{"email": "admin@hotel.com", "password": "admin123"}' \

  -c admin_cookies.txt{



# Ver todas las reservas### Registro  "nombre": "Hotel Nuevo",

curl -X GET http://localhost:5000/reservas/ \

  -b admin_cookies.txt```json  "descripcion": "Descripción del hotel",

```

POST /usuarios/register  "precio_por_noche": 200.50,

## Configuración

{  "capacidad": 6,

### Variables de Entorno

```bash    "nombre": "Juan Pérez",  "ubicacion": "Madrid, España",

SECRET_KEY=tu_clave_secreta_muy_segura_123

DB_HOST=localhost    "email": "juan@example.com",  "disponible": true

DB_USER=root

DB_PASSWORD=tu_password    "password": "password123",}

DB_NAME=hotel_db

```    "telefono": "123-456-789",```



### Iniciar Servidor    "direccion": "Calle Falsa 123"

```bash

cd backend}### **PUT** `/hospedajes/{id}` (Solo Admin)

python app.py

``````**Descripción:** Editar hospedaje  



El servidor se inicia en `http://localhost:5000`**Permisos:** Solo administradores  



## Notas## 📝 Ejemplos de Uso**Body:** (campos opcionales)



1. Las sesiones se manejan automáticamente por Flask```json

2. Usa cookies para mantener la sesión activa

3. Todos los endpoints validan permisos### Consultar Hospedajes (Público){

4. Formato de fecha: `YYYY-MM-DD`

5. La API usa MySQL - verificar conexión a BD```bash  "precio_por_noche": 180.00,



---curl -X GET http://localhost:5000/hospedajes/  "disponible": false



*Documentación actualizada: 13 de noviembre de 2025*```}

```

### Crear Hospedaje (Admin)

```bash### **DELETE** `/hospedajes/{id}` (Solo Admin)

# 1. Login como admin**Descripción:** Eliminar hospedaje  

curl -c cookies.txt -X POST http://localhost:5000/usuarios/login \**Permisos:** Solo administradores

  -H "Content-Type: application/json" \

  -d '{"email":"admin@hotel.com","password":"admin123"}'---



# 2. Crear hospedaje## 📅 **RESERVAS - `/reservas`**

curl -b cookies.txt -X POST http://localhost:5000/hospedajes/ \

  -H "Content-Type: application/json" \### **GET** `/reservas/` (Solo Admin)

  -d '{**Descripción:** Ver todas las reservas  

    "nombre": "Suite Presidencial",**Permisos:** Solo administradores  

    "descripcion": "Amplia suite con vista al mar",**Respuesta:**

    "precio": 350.00,```json

    "capacidad": 4,[

    "tipo": "suite",  {

    "foto": "suite.jpg",    "id_reserva": 1,

    "disponibilidad": 1    "id_usuario": 2,

  }'    "id_hospedaje": 1,

```    "fecha_inicio": "2024-12-20",

    "fecha_fin": "2024-12-25",

### Crear Reserva (Usuario)    "numero_huespedes": 3,

```bash    "estado": "confirmada",

# 1. Login como usuario    "fecha_reserva": "2024-12-10T10:30:00",

curl -c cookies.txt -X POST http://localhost:5000/usuarios/login \    "usuario_nombre": "Juan Pérez",

  -H "Content-Type: application/json" \    "hospedaje_nombre": "Hotel Paradise"

  -d '{"email":"juan@example.com","password":"cliente123"}'  }

]

# 2. Crear reserva```

curl -b cookies.txt -X POST http://localhost:5000/reservas/ \

  -H "Content-Type: application/json" \### **GET** `/reservas/{id}`

  -d '{**Descripción:** Ver reserva específica  

    "id_usuario": 5,**Ejemplo:** `/reservas/1`

    "id_hospedaje": 1,

    "fecha_checkin": "2025-12-20",### **GET** `/reservas/usuario/{user_id}`

    "fecha_checkout": "2025-12-22",**Descripción:** Ver reservas de un usuario  

    "cant_personas": 2,**Ejemplo:** `/reservas/usuario/2`

    "importe_total": 240.00

  }'### **POST** `/reservas/`

```**Descripción:** Crear nueva reserva  

**Permisos:** Usuario logueado  

## 🗂️ Estructura del Proyecto**Body:**

```json

```{

backend/  "id_usuario": 2,

├── app.py                 # Aplicación principal Flask  "id_hospedaje": 1,

├── db.py                  # Configuración de base de datos  "fecha_inicio": "2024-12-20",

├── schema.sql             # Esquema de base de datos  "fecha_fin": "2024-12-25",

├── requirements.txt       # Dependencias Python  "numero_huespedes": 2,

├── API_DOCUMENTATION.md   # Esta documentación  "estado": "confirmada"

├── postman_collection.json # Colección de Postman}

└── models/                # Modelos de datos```

    ├── __init__.py

    ├── usuario.py         # Autenticación y CRUD usuarios### **DELETE** `/reservas/{id}` (Solo Admin)

    ├── hospedajes.py      # CRUD hospedajes**Descripción:** Eliminar reserva  

    └── reservas.py        # CRUD reservas**Permisos:** Solo administradores

```

---

## 🎯 Características Técnicas

## ⚡ **ENDPOINTS AUXILIARES**

### Seguridad

- ✅ Contraseñas hasheadas con Werkzeug### **GET** `/health`

- ✅ Validación de sesiones en endpoints protegidos**Descripción:** Verificar estado del servidor y DB  

- ✅ Sanitización de inputs**Respuesta:**

- ✅ Validación de roles y permisos```json

{

### Base de Datos  "status": "healthy",

- ✅ Integridad referencial con Foreign Keys  "database": "connected",

- ✅ Índices para optimización de consultas  "message": "API funcionando correctamente"

- ✅ Constraints para validación de datos}

- ✅ Timestamps automáticos```



### API Design---

- ✅ Respuestas JSON consistentes

- ✅ Códigos de estado HTTP apropiados## 🔒 **SISTEMA DE PERMISOS**

- ✅ Mensajes de error descriptivos

- ✅ Endpoints RESTful### **Niveles de Acceso:**



## 👨‍💻 Credenciales de Prueba| **Rol** | **Descripción** | **Permisos** |

|---------|----------------|--------------|

| Usuario | Email | Password | Rol || `admin` | Administrador | ✅ Todo: CRUD completo en usuarios, hospedajes y reservas |

|---------|-------|----------|-----|| `empleado` | Empleado | 🔄 Funcionalidad futura |

| Administrador | admin@hotel.com | admin123 | admin || `cliente` | Cliente | 👀 Ver hospedajes, crear/ver sus propias reservas |

| Empleado | empleado@hotel.com | empleado123 | empleado || Sin login | Público | 👀 Solo ver hospedajes |

| Juan Pérez | juan@example.com | cliente123 | cliente |

| María Gómez | maria@example.com | maria123 | cliente |### **Verificación de Permisos:**

```python

## 🔍 Testing# Lógica simple en cada endpoint

if session.get('user_rol') != 'admin':

Todos los endpoints han sido verificados y probados:    return ("Solo administradores pueden...", 403)

```

- ✅ 17 endpoints funcionando correctamente

- ✅ Sistema de permisos validado---

- ✅ Operaciones CRUD completas

- ✅ Autenticación y autorización funcional## 🗄️ **ESTRUCTURA DE BASE DE DATOS**

- ✅ Manejo de errores apropiado

### **Tabla: usuarios**

## 📞 Soporte```sql

- id_usuario (INT, PK, AUTO_INCREMENT)

Para dudas o problemas:- nombre (VARCHAR(100))

- **Repository**: [TDF_Grupo21](https://github.com/rafaelmallquii/TDF_Grupo21)- email (VARCHAR(100), UNIQUE)

- **Issues**: Crear issue en GitHub- telefono (VARCHAR(20))

- **Email**: Contactar al equipo de desarrollo- password (VARCHAR(255)) -- Hash bcrypt

- direccion (TEXT)

---- rol (ENUM: 'admin', 'empleado', 'cliente')

- fecha_registro (TIMESTAMP)

**Desarrollado por Grupo 21 - TDF 2025** 🚀```

### **Tabla: hospedajes**
```sql
- id_hospedaje (INT, PK, AUTO_INCREMENT)
- nombre (VARCHAR(150))
- descripcion (TEXT)
- precio_por_noche (DECIMAL(10,2))
- capacidad (INT)
- ubicacion (VARCHAR(200))
- disponible (BOOLEAN)
```

### **Tabla: reservas**
```sql
- id_reserva (INT, PK, AUTO_INCREMENT)
- id_usuario (INT, FK)
- id_hospedaje (INT, FK)
- fecha_inicio (DATE)
- fecha_fin (DATE)
- numero_huespedes (INT)
- estado (ENUM: 'pendiente', 'confirmada', 'cancelada')
- fecha_reserva (TIMESTAMP)
```

---

## 🧪 **USUARIOS DE PRUEBA**

| **Email** | **Password** | **Rol** |
|-----------|--------------|---------|
| admin@test.com | admin123 | admin |
| empleado@test.com | emp123 | empleado |
| cliente1@test.com | cli123 | cliente |
| cliente2@test.com | cli123 | cliente |

---

## 📝 **CÓDIGOS DE ESTADO HTTP**

| **Código** | **Significado** | **Uso** |
|------------|----------------|---------|
| `200` | OK | Operación exitosa |
| `201` | Created | Recurso creado |
| `400` | Bad Request | Datos inválidos |
| `401` | Unauthorized | No autenticado |
| `403` | Forbidden | Sin permisos |
| `404` | Not Found | Recurso no encontrado |
| `409` | Conflict | Email duplicado |
| `500` | Internal Error | Error del servidor |

---

## 🔧 **EXAMPLES DE USO CON cURL**

### **1. Login como Admin**
```bash
curl -X POST http://localhost:5000/usuarios/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@test.com","password":"admin123"}' \
  -c cookies.txt
```

### **2. Ver todos los usuarios (requiere login admin)**
```bash
curl -X GET http://localhost:5000/usuarios/ \
  -b cookies.txt
```

### **3. Crear hospedaje**
```bash
curl -X POST http://localhost:5000/hospedajes/ \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "nombre": "Hotel Test",
    "descripcion": "Hotel de prueba",
    "precio_por_noche": 100.00,
    "capacidad": 4,
    "ubicacion": "Test City"
  }'
```

### **4. Ver hospedajes (público)**
```bash
curl -X GET http://localhost:5000/hospedajes/
```

### **5. Crear reserva**
```bash
curl -X POST http://localhost:5000/reservas/ \
  -H "Content-Type: application/json" \
  -b cookies.txt \
  -d '{
    "id_usuario": 2,
    "id_hospedaje": 1,
    "fecha_inicio": "2024-12-20",
    "fecha_fin": "2024-12-25",
    "numero_huespedes": 2
  }'
```

---

## 🏗️ **ARQUITECTURA DEL CÓDIGO**

```
backend/
├── app.py                 # 🚀 Aplicación principal Flask
├── db.py                  # 🔌 Conexión MySQL
├── schema.sql             # 📊 Estructura de BD
├── requirements.txt       # 📦 Dependencias
└── models/
    ├── __init__.py        # 📁 Inicializador
    ├── usuario.py         # 👤 CRUD + Auth usuarios
    ├── hospedajes.py      # 🏨 CRUD hospedajes
    └── reservas.py        # 📅 CRUD reservas
```

### **Filosofía del Código:**
- ✅ **Simple y directo** - Sin decoradores complejos
- ✅ **Lógica de estudiante** - Fácil de entender
- ✅ **Verificación directa** - `session.get('user_rol') != 'admin'`
- ✅ **API REST pura** - Sin frontend JavaScript innecesario
- ✅ **Respuestas simples** - Tuplas `("mensaje", código)`

---

## ⚠️ **NOTAS IMPORTANTES**

1. **Seguridad:** Las contraseñas se almacenan hasheadas con Werkzeug
2. **Sesiones:** Se usan sesiones Flask, no JWT
3. **CORS:** No implementado (agregar si se necesita frontend separado)
4. **Entorno:** Servidor de desarrollo (no usar en producción)
5. **Base de datos:** Configurar credenciales en `db.py`

---

## 🎯 **PRÓXIMOS PASOS**

- [ ] Implementar validaciones de fechas en reservas
- [ ] Agregar búsqueda de hospedajes por filtros
- [ ] Sistema de roles más detallado para empleados
- [ ] Endpoint para dashboard con estadísticas
- [ ] Implementar paginación en listados

---

**🚀 API Lista para usar! Sistema completo de hospedajes con autenticación y permisos.** ✨