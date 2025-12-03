"""
Rutas de administración - Panel admin básico, gestión de usuarios y reservas
"""

from flask import Blueprint, render_template, redirect, url_for, session, flash
from services.api_client import (
    obtener_todos_usuarios, obtener_todas_reservas,
    eliminar_usuario, eliminar_reserva, obtener_usuario_por_id, obtener_reserva_por_id
)
from .user_routes import validar_admin

admin_bp = Blueprint('admin', __name__)

# Pre: URL '/admin' solicitada
# Post: Redirige al dashboard de administración
@admin_bp.route('/admin')
def admin():
    # Redirigir a dashboard de admin
    return redirect(url_for('admin.admin_dashboard'))

# Pre: Usuario debe estar logueado como admin
# Post: Si es admin, muestra dashboard con usuarios y reservas. Si no, redirige con error
@admin_bp.route('/admin/dashboard')
def admin_dashboard():
    # Dashboard administrativo simple
    check = validar_admin()
    if check:
        return check
    
    usuarios = obtener_todos_usuarios()
    reservas = obtener_todas_reservas()
    
    return render_template('admin/dashboard.html', usuarios=usuarios, reservas=reservas)

# Pre: Usuario debe estar logueado como admin
# Post: Si es admin, muestra lista de usuarios. Si no, redirige con error
@admin_bp.route('/admin/usuarios')
def usuarios_admin():
    # Lista de usuarios
    check = validar_admin()
    if check:
        return check
    
    usuarios = obtener_todos_usuarios()
    return render_template('admin/usuarios/index.html', usuarios=usuarios)

# Pre: Usuario admin logueado, id_usuario válido
# Post: Si usuario existe, muestra detalles. Si no existe, redirige con mensaje de error
@admin_bp.route('/admin/usuarios/<int:id_usuario>')
def mostrar_usuario_admin(id_usuario):
    # Ver usuario
    check = validar_admin()
    if check:
        return check
    
    usuario = obtener_usuario_por_id(id_usuario)
    if not usuario:
        flash("Usuario no encontrado", "error")
        return redirect(url_for('admin.usuarios_admin'))
    
    return render_template('admin/usuarios/show.html', usuario=usuario)

# Pre: Usuario admin logueado, id_usuario válido diferente al propio
# Post: Si eliminación exitosa, redirige con éxito. Si falla, redirige con error
@admin_bp.route('/admin/usuarios/eliminar/<int:id_usuario>', methods=['GET', 'POST'])
def eliminar_usuario_admin(id_usuario):
    # Eliminar usuario (solo admin)
    # Validación simple de admin
    check = validar_admin()
    if check:
        return check
    
    if id_usuario == session.get('user_id'):
        flash("No puedes eliminar tu propio usuario", "error")
        return redirect(url_for('admin.usuarios_admin'))
    
    resultado = eliminar_usuario(id_usuario)
    
    if resultado.get('success'):
        flash("Usuario eliminado", "success")
    else:
        flash("Error al eliminar usuario", "error")
    
    return redirect(url_for('admin.usuarios_admin'))

# Pre: Usuario debe estar logueado como admin
# Post: Si es admin, muestra lista de reservas. Si no, redirige con error
@admin_bp.route('/admin/reservas')
def reservas_admin():
    # Lista de reservas
    check = validar_admin()
    if check:
        return check
    
    reservas = obtener_todas_reservas()
    return render_template('admin/reservas/index.html', reservas=reservas)

# Pre: Usuario admin logueado, id_reserva válido
# Post: Si reserva existe, muestra detalles. Si no existe, redirige con mensaje de error
@admin_bp.route('/admin/reservas/<int:id_reserva>')
def mostrar_reserva_admin(id_reserva):
    # Ver reserva
    check = validar_admin()
    if check:
        return check
    
    reserva = obtener_reserva_por_id(id_reserva)
    if not reserva:
        flash("Reserva no encontrada", "error")
        return redirect(url_for('admin.reservas_admin'))
    
    return render_template('admin/reservas/show.html', reserva=reserva)

# Pre: Usuario admin logueado, id_reserva válido
# Post: Si eliminación exitosa, redirige con éxito. Si falla, redirige con error
@admin_bp.route('/admin/reservas/eliminar/<int:id_reserva>', methods=['GET', 'POST'])
def eliminar_reserva_admin(id_reserva):
    # Eliminar reserva (solo admin)
    # Validación simple de admin
    check = validar_admin()
    if check:
        return check
    
    resultado = eliminar_reserva(id_reserva)
    
    if resultado.get('success'):
        flash("Reserva eliminada", "success")
    else:
        flash("Error al eliminar reserva", "error")
    
    return redirect(url_for('admin.reservas_admin'))