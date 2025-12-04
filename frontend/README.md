# Frontend - Sistema Hotel 🌐

**Interfaz web con Flask + Bootstrap para gestión hotelera**

## 🚀 Inicio Rápido

```bash
# 1. Instalar dependencias  
pip install -r requirements.txt

# 2. Ejecutar
python app.py
```

**✅ Servidor corriendo en:** `http://localhost:3000`

## 📁 Estructura

```
frontend/
├── app.py              # 🚀 Servidor Flask principal
├── routes/             # 📍 Rutas modulares (Blueprints)
│   ├── public_routes.py    # 🌍 Páginas públicas
│   ├── auth_routes.py      # 🔐 Login/Registro
│   ├── user_routes.py      # 👤 Perfil usuario
│   ├── habitaciones_routes.py # 🏨 Habitaciones
│   ├── reservas_routes.py  # 📅 Reservas
│   └── admin_routes.py     # ⚙️ Panel admin
├── services/
│   └── api_client.py   # 🔗 Conexión al backend
├── templates/          # 🎨 HTML (Jinja2)
└── static/            # 📦 CSS, JS, imágenes
```

## 🔗 Rutas Principales

### 🌍 **Públicas**
- `/` - Inicio
- `/habitaciones` - Lista habitaciones  
- `/nosotros` - Información

### 🔐 **Autenticación**
- `/login` - Iniciar sesión
- `/registro` - Crear cuenta

### 👤 **Usuario**
- `/perfil` - Mi perfil
- `/mis-reservas` - Mis reservas
- `/reservar/<id>` - Hacer reserva

### ⚙️ **Admin** (solo administradores)
- `/admin` - Dashboard
- `/admin/habitaciones` - Gestionar habitaciones
- `/admin/usuarios` - Gestionar usuarios

## 🛠️ Tecnologías

- **Flask** - Framework web
- **Requests** - API calls al backend
- **Bootstrap** - UI responsivo
- **Jinja2** - Templates HTML

## 🔄 Comunicación

```
Frontend (Flask:3000) → Backend API (Flask:8080)
```

**API Client:** `services/api_client.py` maneja todas las llamadas HTTP