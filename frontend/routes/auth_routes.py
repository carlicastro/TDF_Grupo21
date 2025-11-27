"""
Rutas de autenticación - Login, registro y logout
"""

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash,
    jsonify,
)
from services.api_client import login_usuario, crear_usuario, eliminar_reserva

auth_bp = Blueprint("auth", __name__)


# Funciones simples de validación de sesión
def esta_logueado():
    """Verificar si el usuario está logueado"""
    return session.get("logged_in", False)


def es_admin():
    """Verificar si el usuario es admin"""
    if not esta_logueado():
        return False
    user_rol = session.get("user_rol") or session.get("rol")
    return user_rol == "admin"


def validar_sesion():
    """Validación simple para rutas que requieren login"""
    if not esta_logueado():
        flash("Debes iniciar sesión para acceder a esta página", "error")
        return redirect(url_for("auth.login"))
    return None


def validar_admin():
    """Validación simple para rutas que requieren admin"""
    check = validar_sesion()
    if check:
        return check
    if not es_admin():
        flash("No tienes permisos para acceder a esta página", "error")
        return redirect(url_for("public.index"))
    return None


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """Login de usuarios - Lógica básica"""
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if not email or not password:
            flash("Email y contraseña son requeridos", "error")
            return render_template("auth/login.html")

        resultado = login_usuario(email, password)

        if resultado and resultado.get("success"):
            user_data = resultado.get("user", {})

            # El backend ya maneja la sesión con cookies
            # Solo guardamos los datos básicos para el frontend
            session.permanent = True
            session["logged_in"] = True
            session["user_id"] = user_data.get("id")
            session["user_nombre"] = user_data.get("nombre")
            session["user_email"] = user_data.get("email")
            session["user_rol"] = user_data.get("rol", "cliente")

            flash(f"Bienvenido {user_data.get('nombre')}", "success")

            # Verificar si hay una redirección pendiente después del login
            redirect_data = session.pop("redirect_after_login", None)
            if (
                redirect_data
                and redirect_data.get("action") == "procesar_reserva_directa"
            ):
                flash("Ahora puedes completar tu reserva", "info")
                hospedaje_id = redirect_data.get("hospedaje_id")
                return redirect(
                    url_for(
                        "public.detalles_habitacion",
                        id=hospedaje_id,
                        fecha_checkin=redirect_data.get("fecha_checkin"),
                        fecha_checkout=redirect_data.get("fecha_checkout"),
                        personas=redirect_data.get("personas"),
                    )
                )

            if user_data.get("rol") == "admin":
                return redirect(url_for("admin.admin_dashboard"))
            else:
                return redirect(url_for("public.index"))
        else:
            error_msg = (
                resultado.get("message", "Error al iniciar sesión")
                if resultado
                else "Error de conexión"
            )
            flash(error_msg, "error")

    return render_template("auth/login.html")


@auth_bp.route("/registro", methods=["GET", "POST"])
def registro():
    """Registro de nuevos usuarios - Lógica básica"""
    if request.method == "POST":
        nombre = request.form.get("nombre")
        email = request.form.get("email")
        password = request.form.get("password")

        datos = {"nombre": nombre, "email": email, "password": password}

        resultado = crear_usuario(datos)
        if resultado:
            flash("Usuario registrado exitosamente", "success")
            return redirect(url_for("auth.login"))
        else:
            flash("Error al registrar usuario", "error")

    return render_template("auth/registro.html")


@auth_bp.route("/logout")
def logout():
    """Cerrar sesión - Lógica básica"""
    from services.api_client import logout_usuario

    logout_usuario()  # Esto limpia las cookies del backend y la sesión
    flash("Sesión cerrada exitosamente", "success")
    return redirect(url_for("public.index"))
