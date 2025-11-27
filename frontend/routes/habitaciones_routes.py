"""
Rutas de habitaciones - Vista pública y administración
CRUD básico: Create, Read, Update, Delete
"""

from flask import Blueprint, render_template, redirect, url_for, session, flash, request
from services.api_client import (
    obtener_hospedajes, obtener_hospedaje, crear_hospedaje, actualizar_hospedaje, eliminar_hospedaje
)
from routes.auth_routes import validar_admin, validar_sesion

habitaciones_bp = Blueprint('habitaciones', __name__)

# ===== RUTAS PÚBLICAS (para usuarios) =====

@habitaciones_bp.route('/habitaciones')
def lista():
    """Ver todas las habitaciones disponibles"""
    hospedajes = obtener_hospedajes()
    return render_template('habitaciones/lista-habitaciones.html', hospedajes=hospedajes)

@habitaciones_bp.route('/habitaciones/<int:id>')
def detalle(id):
    """Ver detalles de una habitación específica"""
    hospedaje = obtener_hospedaje(id)
    if not hospedaje:
        flash("Habitación no encontrada", "error")
        return redirect(url_for('habitaciones.lista'))
    
    return render_template('habitaciones/detalles-habitacion.html', hospedaje=hospedaje)

# ===== RUTAS ADMIN (para administradores) =====

@habitaciones_bp.route('/admin/habitaciones')
def admin_lista():
    """Gestión de habitaciones (solo admin)"""
    # Validación simple de admin
    check = validar_admin()
    if check:
        return check
    
    hospedajes = obtener_hospedajes()
    return render_template('admin/habitaciones/index.html', hospedajes=hospedajes)

@habitaciones_bp.route('/admin/habitaciones/crear', methods=['GET', 'POST'])
def admin_crear():
    """Crear nueva habitación (solo admin)"""
    # Validación simple de admin
    check = validar_admin()
    if check:
        return check
    
    if request.method == 'GET':
        return render_template('admin/habitaciones/create.html')
    
    # POST: Crear habitación
    try:
        # Validar campos requeridos
        nombre = request.form.get('nombre', '').strip()
        precio = request.form.get('precio', '').strip()
        capacidad = request.form.get('capacidad', '').strip()
        
        if not nombre:
            flash("El nombre es requerido", "error")
            return render_template('admin/habitaciones/create.html')
            
        if not precio:
            flash("El precio es requerido", "error")
            return render_template('admin/habitaciones/create.html')
            
        if not capacidad:
            flash("La capacidad es requerida", "error")
            return render_template('admin/habitaciones/create.html')
        
        # Preparar datos para el backend
        datos = {
            'nombre': nombre,
            'descripcion': request.form.get('descripcion', ''),
            'precio': float(precio),
            'capacidad': int(capacidad),
            'tipo': request.form.get('tipo', 'habitacion'),
            'foto': request.form.get('foto', ''),
            'disponibilidad': 1 if request.form.get('disponibilidad') == '1' else 0
        }
        
        # Intentar crear hospedaje
        resultado = crear_hospedaje(datos)
        
        if resultado.get('success'):
            flash("Habitación creada correctamente", "success")
            return redirect(url_for('habitaciones.admin_lista'))
        else:
            error_msg = resultado.get('message', 'Error desconocido')
            flash(f"Error al crear habitación: {error_msg}", "error")
            return render_template('admin/habitaciones/create.html')
            
    except ValueError as e:
        flash("Error en los datos del formulario: valores inválidos", "error")
        return render_template('admin/habitaciones/create.html')
    except Exception as e:
        flash(f"Error inesperado: {str(e)}", "error")
        return render_template('admin/habitaciones/create.html')

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
    datos = {
        'nombre': request.form.get('nombre'),
        'descripcion': request.form.get('descripcion'),
        'precio': float(request.form.get('precio', 0)),
        'capacidad': int(request.form.get('capacidad', 1)),
        'tipo': request.form.get('tipo', 'simple'),
        'foto': request.form.get('foto', ''),
        'disponibilidad': 1 if request.form.get('disponibilidad') else 0
    }
    
    resultado = actualizar_hospedaje(id, datos)
    
    if resultado.get('success'):
        flash("Habitación actualizada correctamente", "success")
        return redirect(url_for('habitaciones.admin_lista'))
    else:
        flash("Error al actualizar habitación", "error")
        return render_template('admin/habitaciones/edit.html', hospedaje=hospedaje)

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