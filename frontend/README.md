# Frontend - Proyecto Hospedajes

Estructura y cómo levantar el frontend (Flask + Jinja2)

Requisitos:
- Python 3.8+

Archivos añadidos:
- `requirements.txt` (Flask, python-dotenv)
- `.env` (variables de entorno para desarrollo)
- `app.py` (pequeña app Flask que sirve las plantillas existentes)

Pasos rápidos (desde la carpeta `frontend`):

1) Crear virtualenv (bash):

```bash
python -m venv .venv
source .venv/Scripts/activate   # en Git Bash/mingw64
# o en PowerShell: .venv\\Scripts\\Activate.ps1
# o en cmd: .venv\\Scripts\\activate.bat
```

2) Instalar dependencias:

```bash
pip install -r requirements.txt
```

3) Comprobar `.env` (ya existe un `.env` de ejemplo). Ajustar `API_BASE_URL` si tu backend corre en otro host/puerto.

4) Ejecutar la app Flask (opcional):

```bash
# desde la carpeta frontend y con el venv activado
python app.py
```

La app por defecto arranca en el puerto `5001` y sirve las plantillas que ya están en `templates/`.

Siguientes pasos sugeridos:
- Conectar llamadas desde las plantillas/JS al backend `API_BASE_URL`.
- Añadir manejo de sesiones/autenticación si se requiere.
