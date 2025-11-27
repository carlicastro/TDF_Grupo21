# Frontend - Sistema de Reservas Hotel

Interfaz web desarrollada con Flask, templates Jinja2 y Bootstrap para el sistema de reservas hoteleras.

## 🏗️ Arquitectura

- **Framework**: Flask con Blueprints modulares
- **Templates**: Jinja2 con herencia de plantillas
- **CSS**: Bootstrap + estilos personalizados
- **JS**: jQuery + componentes interactivos
- **Comunicación**: Cliente HTTP al backend API

## 📁 Estructura

```
frontend/
├── app.py                  # Aplicación principal Flask
├── routes/                 # Rutas organizadas por módulos
│   ├── public_routes.py   # Páginas públicas (inicio, servicios)
│   ├── auth_routes.py     # Autenticación (login, registro)
│   ├── admin_routes.py    # Panel de administración
│   ├── reservas_routes.py # Sistema de reservas
│   ├── habitaciones_routes.py # Gestión de habitaciones
│   └── user_routes.py     # Perfil de usuario
├── services/
│   └── api_client.py      # Cliente HTTP al backend
├── templates/             # Plantillas HTML
│   ├── Components/        # Componentes reutilizables
│   ├── public/           # Páginas públicas
│   ├── auth/             # Autenticación
│   ├── admin/            # Panel admin
│   ├── perfil/           # Perfil usuario
│   └── reservas/         # Sistema reservas
├── static/               # Recursos estáticos
│   ├── css/             # Estilos
│   ├── js/              # JavaScript
│   ├── images/          # Imágenes
│   └── assets/          # Admin assets
└── requirements.txt
```

## 🚀 Instalación

```bash
# Instalar dependencias
pip install -r requirements.txt

# Variables de entorno (.env)
SECRET_KEY=tu_clave_secreta_frontend

# Ejecutar servidor
python app.py
```

## 🌐 Rutas Principales

### Públicas
- `/` - Página de inicio
- `/nosotros` - Sobre nosotros
- `/servicios` - Servicios del hotel
- `/galeria` - Galería de imágenes
- `/contacto` - Información de contacto

### Autenticación
- `/login` - Iniciar sesión
- `/registro` - Crear cuenta
- `/logout` - Cerrar sesión

### Habitaciones
- `/habitaciones` - Lista de habitaciones
- `/habitaciones/<id>` - Detalles de habitación

### Reservas
- `/reservar/<id>` - Realizar reserva
- `/confirmacion` - Confirmación de reserva

### Usuario
- `/perfil` - Perfil personal
- `/mis-reservas` - Historial de reservas

### Administración (Admin)
- `/admin` - Dashboard administrativo
- `/admin/usuarios` - Gestión de usuarios
- `/admin/reservas` - Gestión de reservas
- `/admin/habitaciones` - Gestión de habitaciones

## 🔧 Tecnologías

- **Flask 3.0.3** - Framework web
- **Requests 2.31.0** - Cliente HTTP
- **Python-dotenv 1.0.1** - Variables de entorno
- **Bootstrap** - Framework CSS
- **jQuery** - JavaScript
- **Jinja2** - Motor de plantillas

## 🔗 Comunicación Backend

El frontend comunica con el backend API mediante:
- **Base URL**: `http://localhost:8080`
- **Método**: HTTP requests con cookies de sesión
- **Autenticación**: Cookies automáticas
- **Cliente**: `services/api_client.py`

## 🎨 Características

- ✅ **Responsive Design** - Compatible con móviles
- ✅ **Sistema de Sesiones** - Autenticación segura
- ✅ **Validación Frontend** - Formularios validados
- ✅ **Navegación Intuitiva** - UX optimizada
- ✅ **Panel Admin** - Gestión completa
- ✅ **Templates Modulares** - Código reutilizable

## 🌐 Puerto

El frontend se ejecuta en **puerto 3000** por defecto.