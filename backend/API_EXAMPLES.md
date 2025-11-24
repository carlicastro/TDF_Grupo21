# API Usage Examples

This file contains practical examples of using the Hotel Management API.

## Quick Test Commands

### 1. Check API Health
```bash
curl http://localhost:5000/health
```

### 2. Get All Accommodations (Public)
```bash
curl http://localhost:5000/hospedajes/
```

### 3. Login as Admin
```bash
curl -X POST http://localhost:5000/usuarios/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@hotel.com", "password": "admin123"}' \
  -c admin_session.txt
```

### 4. Get All Users (Admin required)
```bash
curl http://localhost:5000/usuarios/ \
  -b admin_session.txt
```

### 5. Get All Reservations (Admin required)
```bash
curl http://localhost:5000/reservas/ \
  -b admin_session.txt
```

### 6. Login as Client
```bash
curl -X POST http://localhost:5000/usuarios/login \
  -H "Content-Type: application/json" \
  -d '{"email": "juan@example.com", "password": "cliente123"}' \
  -c client_session.txt
```

### 7. Create Reservation (Client)
```bash
curl -X POST http://localhost:5000/reservas/ \
  -H "Content-Type: application/json" \
  -d '{
    "id_hospedaje": 1,
    "fecha_inicio": "2024-12-01",
    "fecha_fin": "2024-12-05",
    "num_huespedes": 2
  }' \
  -b client_session.txt
```

### 8. Get Specific Accommodation
```bash
curl http://localhost:5000/hospedajes/1
```

### 9. Register New User
```bash
curl -X POST http://localhost:5000/usuarios/register \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Test User",
    "email": "test@example.com",
    "password": "password123",
    "telefono": "+1234567890"
  }'
```

### 10. Logout
```bash
curl -X POST http://localhost:5000/usuarios/logout \
  -b admin_session.txt
```

## Testing Workflow

### Complete Admin Workflow
```bash
#!/bin/bash

echo "=== Testing Admin Workflow ==="

# 1. Login as admin
echo "1. Admin login..."
curl -X POST http://localhost:5000/usuarios/login \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@hotel.com", "password": "admin123"}' \
  -c admin.cookies

# 2. Get all users
echo "2. Getting all users..."
curl http://localhost:5000/usuarios/ \
  -b admin.cookies

# 3. Get all reservations
echo "3. Getting all reservations..."
curl http://localhost:5000/reservas/ \
  -b admin.cookies

# 4. Create new accommodation
echo "4. Creating new accommodation..."
curl -X POST http://localhost:5000/hospedajes/ \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Test Suite",
    "descripcion": "Suite de prueba",
    "precio": 200.00,
    "capacidad": 2,
    "tipo": "suite"
  }' \
  -b admin.cookies

# 5. Logout
echo "5. Logout..."
curl -X POST http://localhost:5000/usuarios/logout \
  -b admin.cookies

echo "=== Admin workflow completed ==="
```

### Complete Client Workflow
```bash
#!/bin/bash

echo "=== Testing Client Workflow ==="

# 1. Register new user
echo "1. Registering new user..."
curl -X POST http://localhost:5000/usuarios/register \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Test Client",
    "email": "testclient@example.com",
    "password": "password123",
    "telefono": "+9876543210"
  }'

# 2. Login as client
echo "2. Client login..."
curl -X POST http://localhost:5000/usuarios/login \
  -H "Content-Type: application/json" \
  -d '{"email": "testclient@example.com", "password": "password123"}' \
  -c client.cookies

# 3. View accommodations
echo "3. Viewing accommodations..."
curl http://localhost:5000/hospedajes/

# 4. Create reservation
echo "4. Creating reservation..."
curl -X POST http://localhost:5000/reservas/ \
  -H "Content-Type: application/json" \
  -d '{
    "id_hospedaje": 1,
    "fecha_inicio": "2024-12-15",
    "fecha_fin": "2024-12-20",
    "num_huespedes": 2
  }' \
  -b client.cookies

# 5. View my reservations
echo "5. Viewing my reservations..."
curl http://localhost:5000/reservas/usuario/5 \
  -b client.cookies

# 6. Logout
echo "6. Logout..."
curl -X POST http://localhost:5000/usuarios/logout \
  -b client.cookies

echo "=== Client workflow completed ==="
```

## Error Handling Examples

### Authentication Errors
```bash
# Try to access protected endpoint without login
curl http://localhost:5000/usuarios/
# Expected: 403 Forbidden

# Try with wrong credentials
curl -X POST http://localhost:5000/usuarios/login \
  -H "Content-Type: application/json" \
  -d '{"email": "wrong@email.com", "password": "wrongpass"}'
# Expected: 401 Unauthorized
```

### Permission Errors
```bash
# Login as client
curl -X POST http://localhost:5000/usuarios/login \
  -H "Content-Type: application/json" \
  -d '{"email": "juan@example.com", "password": "cliente123"}' \
  -c client.cookies

# Try to access admin endpoint
curl http://localhost:5000/usuarios/ \
  -b client.cookies
# Expected: 403 Forbidden

# Try to create accommodation (admin only)
curl -X POST http://localhost:5000/hospedajes/ \
  -H "Content-Type: application/json" \
  -d '{"nombre": "Test Room", "precio": 100}' \
  -b client.cookies
# Expected: 403 Forbidden
```

### Resource Not Found
```bash
# Try to get non-existent user
curl http://localhost:5000/usuarios/999

# Try to get non-existent accommodation
curl http://localhost:5000/hospedajes/999
```

## PowerShell Commands (Windows)

### Admin Login (PowerShell)
```powershell
$headers = @{ "Content-Type" = "application/json" }
$body = @{
    email = "admin@hotel.com"
    password = "admin123"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:5000/usuarios/login" -Method POST -Headers $headers -Body $body
```

### Get Accommodations (PowerShell)
```powershell
Invoke-RestMethod -Uri "http://localhost:5000/hospedajes/" -Method GET
```

## Python Examples

### Using requests library
```python
import requests

# Login
login_data = {
    "email": "admin@hotel.com",
    "password": "admin123"
}
session = requests.Session()
response = session.post("http://localhost:5000/usuarios/login", json=login_data)
print(response.json())

# Get users (session maintained)
users_response = session.get("http://localhost:5000/usuarios/")
print(users_response.json())

# Create accommodation
accommodation_data = {
    "nombre": "Python Test Room",
    "descripcion": "Created from Python",
    "precio": 150.00,
    "capacidad": 2,
    "tipo": "habitacion"
}
create_response = session.post("http://localhost:5000/hospedajes/", json=accommodation_data)
print(create_response.json())

# Logout
logout_response = session.post("http://localhost:5000/usuarios/logout")
print(logout_response.json())
```

## Notes

1. All session cookies are automatically handled by curl with `-c` and `-b` flags
2. Admin credentials: `admin@hotel.com` / `admin123`
3. Client credentials: `juan@example.com` / `cliente123`
4. Date format: `YYYY-MM-DD`
5. Always check response status codes for error handling
6. Session expires when server restarts

Last updated: November 13, 2025