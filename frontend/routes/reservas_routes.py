"""
Rutas de reservas - Proceso de reserva y confirmación básico
"""

from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from services.api_client import obtener_hospedaje, crear_reserva
from datetime import datetime

reservas_bp = Blueprint("reservas", __name__)


@reservas_bp.route("/reservar/<int:id_hospedaje>", methods=["GET", "POST"])
def reservar(id_hospedaje):
    """Hacer reserva básica"""

    # ------------------------------------------------------------------
    # CORRECCIÓN: Si no está logueado, guardar el intento de reserva si es POST,
    # y luego redirigir al login.
    if not session.get("logged_in"):
        if request.method == "POST":
            # Guardamos los datos del formulario POST antes de ir al login
            session["redirect_after_login"] = {
                "action": "procesar_reserva_directa",
                "hospedaje_id": id_hospedaje,
                "fecha_checkin": request.form.get("fecha_checkin"),
                "fecha_checkout": request.form.get("fecha_checkout"),
                "personas": request.form.get("cant_personas", 1),
            }
            flash("Debes iniciar sesión para completar la reserva", "info")

        # Redirigir al login
        return redirect(url_for("auth.login"))
    # ------------------------------------------------------------------

    hospedaje = obtener_hospedaje(id_hospedaje)
    if not hospedaje:
        return redirect(url_for("habitaciones.lista"))

    if request.method == "POST":
        fecha_checkin = request.form.get("fecha_checkin")
        fecha_checkout = request.form.get("fecha_checkout")
        cant_personas = request.form.get("cant_personas", 1)

        # Calcular noches y precio
        try:
            fi = datetime.strptime(fecha_checkin, "%Y-%m-%d")
            fo = datetime.strptime(fecha_checkout, "%Y-%m-%d")
            noches = max(1, (fo - fi).days)
        except:
            noches = 1

        precio_total = float(hospedaje.get("precio", 0)) * noches

        datos_reserva = {
            "id_usuario": session.get("user_id"),
            "id_hospedaje": int(id_hospedaje),
            "fecha_checkin": fecha_checkin,
            "fecha_checkout": fecha_checkout,
            "cant_personas": int(cant_personas),
            "importe_total": precio_total,
            "estado": "confirmada",
        }

        if crear_reserva(datos_reserva):
            # Guardar datos de reserva en sesión para mostrar confirmación
            session["ultima_reserva"] = {
                "hospedaje": hospedaje,
                "fecha_checkin": fecha_checkin,
                "fecha_checkout": fecha_checkout,
                "cant_personas": cant_personas,
                "noches": noches,
                "precio_total": precio_total,
            }
            return redirect(url_for("reservas.confirmacion"))
        else:
            flash("Error al crear la reserva", "error")

    return render_template("habitaciones/detalles-habitacion.html", hospedaje=hospedaje)


@reservas_bp.route("/crear-reserva", methods=["POST"])
def crear_reserva_route():
    """Crear nueva reserva desde formulario"""
    if not session.get("logged_in"):
        return redirect(url_for("auth.login"))

    id_hospedaje = request.form.get("id_hospedaje")
    fecha_checkin = request.form.get("fecha_checkin")
    fecha_checkout = request.form.get("fecha_checkout")
    cant_personas = request.form.get("cant_personas", 1)

    # Calcular precio
    hospedaje = obtener_hospedaje(int(id_hospedaje))
    if hospedaje:
        try:
            fi = datetime.strptime(fecha_checkin, "%Y-%m-%d")
            fo = datetime.strptime(fecha_checkout, "%Y-%m-%d")
            noches = max(1, (fo - fi).days)
            precio_total = float(hospedaje["precio"]) * noches
        except:
            precio_total = float(hospedaje["precio"])
    else:
        precio_total = 0

    datos_reserva = {
        "id_usuario": session.get("user_id"),
        "id_hospedaje": int(id_hospedaje),
        "fecha_checkin": fecha_checkin,
        "fecha_checkout": fecha_checkout,
        "cant_personas": int(cant_personas),
        "importe_total": precio_total,
        "estado": "confirmada",
    }

    if crear_reserva(datos_reserva):
        # Guardar datos de reserva en sesión para mostrar confirmación
        session["ultima_reserva"] = {
            "hospedaje": hospedaje,
            "fecha_checkin": fecha_checkin,
            "fecha_checkout": fecha_checkout,
            "cant_personas": cant_personas,
            "noches": noches,
            "precio_total": precio_total,
        }
        return redirect(url_for("reservas.confirmacion"))
    else:
        flash("Error al crear la reserva", "error")
        return redirect(url_for("habitaciones.lista"))


@reservas_bp.route("/confirmacion")
def confirmacion():
    """Página de confirmación de reserva"""
    if not session.get("logged_in"):
        return redirect(url_for("auth.login"))

    # Obtener datos de la última reserva
    ultima_reserva = session.get("ultima_reserva")
    if not ultima_reserva:
        flash("No hay datos de reserva para mostrar", "warning")
        return redirect(url_for("public.index"))

    # Limpiar datos de sesión después de mostrar
    session.pop("ultima_reserva", None)

    return render_template("reservas/confirmacion.html", reserva=ultima_reserva)
