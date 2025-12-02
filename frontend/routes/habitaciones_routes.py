"""
Rutas de habitaciones - Vista pública y administración
CRUD básico: Create, Read, Update, Delete
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from datetime import datetime
from services.api_client import (
    obtener_hospedajes, obtener_hospedaje, crear_hospedaje, actualizar_hospedaje, eliminar_hospedaje
)
from .user_routes import validar_admin

habitaciones_bp = Blueprint('habitaciones', __name__)

# Pre: Petición HTTP válida
# Post: Muestra lista de todas las habitaciones disponibles
@habitaciones_bp.route('/habitaciones')
def lista():
    """Ver todas las habitaciones disponibles"""
    hospedajes = obtener_hospedajes()
    return render_template('habitaciones/lista-habitaciones.html', hospedajes=hospedajes)

# Pre: Petición HTTP válida, id de habitación
# Post: Si existe muestra detalles, si no existe redirige a lista con error
@habitaciones_bp.route('/habitaciones/<int:id>')
def detalle(id):
    """Ver detalles de habitación"""
    hospedaje = obtener_hospedaje(id)
    if not hospedaje:
        flash("Habitación no encontrada", "error")
        return redirect(url_for('habitaciones.lista'))
    
    fecha_minima = datetime.now().date().strftime('%Y-%m-%d')
    puede_reservar = session.get('logged_in', False)
    
    return render_template('habitaciones/detalles-habitacion.html', 
                         hospedaje=hospedaje,
                         fecha_minima=fecha_minima,
                         puede_reservar=puede_reservar)

# ===== RUTAS ADMIN (para administradores) =====

# Pre: Usuario con permisos de administrador
# Post: Si es admin muestra lista, si no redirige a acceso denegado
@habitaciones_bp.route('/admin/habitaciones')
def admin_lista():
    """Lista de habitaciones (admin)"""
    check = validar_admin()
    if check:
        return check
    
    hospedajes = obtener_hospedajes()
    return render_template('admin/habitaciones/index.html', hospedajes=hospedajes)

# Pre: Usuario con permisos de administrador
# Post: Si GET muestra formulario, si POST válido crea habitación y redirige, si inválido muestra error
@habitaciones_bp.route('/admin/habitaciones/crear', methods=['GET', 'POST'])
def admin_crear():
    """Crear nueva habitación (solo admin)"""
    check = validar_admin()
    if check:
        return check
    
    if request.method == 'GET':
        return render_template('admin/habitaciones/create.html')
    
    # POST: Crear habitación simple
    nombre = request.form.get('nombre', '').strip()
    precio = request.form.get('precio', '')
    capacidad = request.form.get('capacidad', '')
    
    # Validación simple
    if not nombre or not precio or not capacidad:
        flash("Todos los campos son requeridos", "error")
        return render_template('admin/habitaciones/create.html')
    
    # Datos para crear
    disponible = request.form.get('disponibilidad')
    datos = {
        'nombre': nombre,
        'descripcion': request.form.get('descripcion', ''),
        'precio': float(precio),
        'capacidad': int(capacidad),
        'tipo': request.form.get('tipo', 'habitacion'),
        'foto': request.form.get('imagen_url', ''),
        'disponibilidad': 1 if disponible == 'on' else 0
    }
    
    # Crear habitación
    resultado = crear_hospedaje(datos)
    
    if resultado.get('success'):
        flash("Habitación creada exitosamente", "success")
        return redirect(url_for('habitaciones.admin_lista'))
    else:
        flash("Error al crear habitación", "error")
        return render_template('admin/habitaciones/create.html')

# Pre: Usuario con permisos de administrador, id de habitación válido
# Post: Si existe muestra detalles de habitación, si no existe redirige con error
@habitaciones_bp.route('/admin/habitaciones/<int:id>')
def admin_mostrar(id):
    """Ver detalles de habitación (solo admin)"""
    # Validación simple de admin
    check = validar_admin()
    if check:
        return check
    
    hospedaje = obtener_hospedaje(id)
    if not hospedaje:
        flash("Habitación no encontrada", "error")
        return redirect(url_for('habitaciones.admin_lista'))
    
    return render_template('admin/habitaciones/show.html', hospedaje=hospedaje)

# Pre: Usuario con permisos de administrador, id de habitación válido
# Post: Si GET muestra formulario de edición, si POST válido actualiza y redirige, si inválido muestra error
@habitaciones_bp.route('/admin/habitaciones/editar/<int:id>', methods=['GET', 'POST'])
def admin_editar(id):
    """Editar habitación (solo admin)"""
    # Validación simple de admin
    check = validar_admin()
    if check:
        return check
    
    hospedaje = obtener_hospedaje(id)
    if not hospedaje:
        flash("Habitación no encontrada", "error")
        return redirect(url_for('habitaciones.admin_lista'))
    
    if request.method == 'GET':
        return render_template('admin/habitaciones/edit.html', hospedaje=hospedaje)
    
    # POST: Actualizar habitación
    disponible = request.form.get('disponibilidad')
    datos = {
        'nombre': request.form.get('nombre'),
        'descripcion': request.form.get('descripcion'),
        'precio': float(request.form.get('precio', 0)),
        'capacidad': int(request.form.get('capacidad', 1)),
        'tipo': request.form.get('tipo', 'habitacion'),
        'foto': request.form.get('imagen_url', ''),
        'disponibilidad': 1 if disponible == 'on' else 0
    }
    
    resultado = actualizar_hospedaje(id, datos)
    
    if resultado.get('success'):
        flash("Habitación actualizada correctamente", "success")
        return redirect(url_for('habitaciones.admin_lista'))
    else:
        flash("Error al actualizar habitación", "error")
        return render_template('admin/habitaciones/edit.html', hospedaje=hospedaje)

# Pre: Usuario con permisos de administrador, id de habitación válido
# Post: Elimina habitación y redirige a lista con mensaje de resultado
@habitaciones_bp.route('/admin/habitaciones/eliminar/<int:id>', methods=['GET', 'POST'])
def admin_eliminar(id):
    """Eliminar habitación (solo admin)"""
    # Validación simple de admin
    check = validar_admin()
    if check:
        return check
    
    resultado = eliminar_hospedaje(id)
    
    if resultado.get('success'):
        flash("Habitación eliminada correctamente", "success")
    else:
        # Usar el mensaje específico del backend
        flash(resultado.get('message', 'Error al eliminar habitación'), "error")
    
    return redirect(url_for('habitaciones.admin_lista'))