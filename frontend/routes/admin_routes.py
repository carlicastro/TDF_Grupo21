"""
Rutas de administración - Panel admin básico, gestión de usuarios y reservas
"""

from flask import Blueprint, render_template, redirect, url_for, session, flash, request
from services.api_client import (
    obtener_todos_usuarios,
    obtener_todas_reservas,
    eliminar_usuario,
    eliminar_reserva,
    obtener_usuario_por_id,
    obtener_reserva_por_id,
)
from routes.auth_routes import validar_admin, validar_sesion

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/admin")
def admin():
    """Redirigir a dashboard de admin"""
    return redirect(url_for("admin.admin_dashboard"))


@admin_bp.route("/admin/dashboard")
def admin_dashboard():
    """Dashboard administrativo básico"""
    # Validación simple de admin
    check = validar_admin()
    if check:
        return check

    # Estadísticas básicas
    usuarios = obtener_todos_usuarios()
    reservas = obtener_todas_reservas()

    estadisticas = {
        "total_usuarios": len(usuarios),
        "total_reservas": len(reservas),
        "total_hospedajes": 0,  # No gestionamos hospedajes desde admin
        "reservas_recientes": reservas[-5:] if reservas else [],
    }

    return render_template("admin/dashboard.html", estadisticas=estadisticas)


@admin_bp.route("/admin/usuarios")
def usuarios_admin():
    """Gestión de usuarios (solo admin)"""
    # Validación simple de admin
    check = validar_admin()
    if check:
        return check

    usuarios = obtener_todos_usuarios()
    return render_template("admin/usuarios/index.html", usuarios=usuarios)


@admin_bp.route("/admin/usuarios/<int:id_usuario>")
def mostrar_usuario_admin(id_usuario):
    """Mostrar detalles de usuario (solo admin)"""
    # Validación simple de admin
    check = validar_admin()
    if check:
        return check

    usuario = obtener_usuario_por_id(id_usuario)
    if not usuario:
        flash("Usuario no encontrado", "error")
        return redirect(url_for("admin.usuarios_admin"))

    # Obtener estadísticas adicionales si están disponibles
    reservas_activas = 0  # Placeholder
    reservas_completadas = 0  # Placeholder
    reservas_recientes = []  # Placeholder

    return render_template(
        "admin/usuarios/show.html",
        usuario=usuario,
        reservas_activas=reservas_activas,
        reservas_completadas=reservas_completadas,
        reservas_recientes=reservas_recientes,
    )


@admin_bp.route("/admin/usuarios/eliminar/<int:id_usuario>", methods=["GET", "POST"])
def eliminar_usuario_admin(id_usuario):
    """Eliminar usuario (solo admin)"""
    # Validación simple de admin
    check = validar_admin()
    if check:
        return check

    if id_usuario == session.get("user_id"):
        flash("No puedes eliminar tu propio usuario", "error")
        return redirect(url_for("admin.usuarios_admin"))

    resultado = eliminar_usuario(id_usuario)

    if resultado.get("success"):
        flash("Usuario eliminado", "success")
    else:
        flash("Error al eliminar usuario", "error")

    return redirect(url_for("admin.usuarios_admin"))


@admin_bp.route("/admin/reservas")
def reservas_admin():
    """Gestión de reservas (solo admin)"""
    # Validación simple de admin
    check = validar_admin()
    if check:
        return check

    reservas = obtener_todas_reservas()
    return render_template("admin/reservas/index.html", reservas=reservas)


@admin_bp.route("/admin/reservas/<int:id_reserva>")
def mostrar_reserva_admin(id_reserva):
    """Mostrar detalles de reserva (solo admin)"""
    # Validación simple de admin
    check = validar_admin()
    if check:
        return check

    reserva = obtener_reserva_por_id(id_reserva)
    if not reserva:
        flash("Reserva no encontrada", "error")
        return redirect(url_for("admin.reservas_admin"))

    # Obtener información adicional del usuario si está disponible
    usuario_info = None
    if hasattr(reserva, "id_usuario"):
        usuario_info = obtener_usuario_por_id(reserva.id_usuario)

    return render_template(
        "admin/reservas/show.html", reserva=reserva, usuario_info=usuario_info
    )


@admin_bp.route("/admin/reservas/eliminar/<int:id_reserva>", methods=["GET", "POST"])
def eliminar_reserva_admin(id_reserva):
    """Eliminar reserva (solo admin)"""
    # Validación simple de admin
    check = validar_admin()
    if check:
        return check

    resultado = eliminar_reserva(id_reserva)

    if resultado.get("success"):
        flash("Reserva eliminada", "success")
    else:
        flash("Error al eliminar reserva", "error")

    return redirect(url_for("admin.reservas_admin"))


@admin_bp.route("/admin/logout")
def admin_logout():
    """Cerrar sesión de admin"""
    session.clear()
    flash("Sesión cerrada exitosamente", "success")
    return redirect(url_for("public.index"))
