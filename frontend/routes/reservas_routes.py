"""
Rutas de reservas SIMPLES - Proyecto Universitario
"""

from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from services.api_client import obtener_hospedaje, crear_reserva
from datetime import datetime
from .user_routes import validar_sesion

reservas_bp = Blueprint('reservas', __name__)

# Pre: Usuario logueado, id_hospedaje válido
# Post: Si GET muestra formulario, si POST válido crea reserva y redirige, si inválido muestra error
@reservas_bp.route('/reservar/<int:id_hospedaje>', methods=['GET', 'POST'])
def reservar(id_hospedaje):
    # Hacer reserva
    check = validar_sesion()
    if check:
        return check
    
    hospedaje = obtener_hospedaje(id_hospedaje)
    if not hospedaje:
        flash('Hospedaje no encontrado', 'error')
        return redirect(url_for('habitaciones.lista'))

    if request.method == 'POST':
        fecha_checkin = request.form.get('fecha_checkin')
        fecha_checkout = request.form.get('fecha_checkout')
        cant_personas = request.form.get('cant_personas', 1)

        if not fecha_checkin or not fecha_checkout:
            flash('Selecciona las fechas', 'error')
            return redirect(url_for('habitaciones.detalle', id=id_hospedaje))

        # Calcular precio simple
        try:
            fi = datetime.strptime(fecha_checkin, '%Y-%m-%d')
            fo = datetime.strptime(fecha_checkout, '%Y-%m-%d')
            noches = max(1, (fo - fi).days)
            precio_total = float(hospedaje.get('precio', 0)) * noches
        except:
            flash('Fechas inválidas', 'error')
            return redirect(url_for('habitaciones.detalle', id=id_hospedaje))

        datos_reserva = {
            'id_usuario': session.get('user_id'),
            'id_hospedaje': id_hospedaje,
            'fecha_checkin': fecha_checkin,
            'fecha_checkout': fecha_checkout,
            'cant_personas': int(cant_personas),
            'importe_total': precio_total
        }

        if crear_reserva(datos_reserva):
            # Guardar datos para confirmación
            session['ultima_reserva'] = {
                'hospedaje': hospedaje,
                'fecha_checkin': fecha_checkin,
                'fecha_checkout': fecha_checkout,
                'cant_personas': cant_personas,
                'noches': noches,
                'precio_total': precio_total
            }
            flash("Reserva creada exitosamente", "success")
            return redirect(url_for('reservas.confirmacion'))
        else:
            flash("Error al crear la reserva", "error")

    fecha_minima = datetime.now().date().strftime('%Y-%m-%d')
    return render_template('habitaciones/detalles-habitacion.html', 
                         hospedaje=hospedaje, 
                         fecha_minima=fecha_minima)

# Pre: Usuario logueado, datos de reserva en sesión
# Post: Si hay reserva muestra confirmación, si no hay reserva redirige a inicio
@reservas_bp.route('/confirmacion')
def confirmacion():
    # Confirmación de reserva
    check = validar_sesion()
    if check:
        return check
    
    # Obtener datos de reserva
    ultima_reserva = session.get('ultima_reserva')
    if not ultima_reserva:
        flash("No hay reserva para confirmar", "warning")
        return redirect(url_for('public.index'))
    
    # Limpiar datos después de mostrar
    session.pop('ultima_reserva', None)
    
    return render_template('reservas/confirmacion.html', reserva=ultima_reserva)