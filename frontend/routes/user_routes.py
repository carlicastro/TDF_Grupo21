"""
Rutas de usuario SIMPLES
"""

from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from services.api_client import obtener_reservas_usuario

user_bp = Blueprint('user', __name__)

# Pre: Sesión Flask activa
# Post: Si usuario logueado retorna None, si no logueado retorna redirect a login
def validar_sesion():
    # Validar que el usuario esté logueado
    if not session.get('logged_in'):
        flash('Debes estar logueado', 'error')
        return redirect(url_for('auth.login'))
    return None

# Pre: Sesión Flask activa
# Post: Si es admin retorna None, si no es admin retorna redirect apropiado
def validar_admin():
    # Validar que el usuario sea admin
    if not session.get('logged_in'):
        flash('Debes iniciar sesión', 'error')
        return redirect(url_for('auth.login'))
    if session.get('user_rol') != 'admin':
        flash('No tienes permisos', 'error')
        return redirect(url_for('public.index'))
    return None


# Pre: Usuario debe estar logueado
# Post: Si logueado, muestra página de perfil. Si no logueado, redirige a login
@user_bp.route('/perfil')
def perfil():
    # Perfil simple
    check = validar_sesion()
    if check:
        return check
    
    return render_template('perfil/perfil.html',
                         user_nombre=session.get('user_nombre'),
                         user_email=session.get('user_email'),
                         user_rol=session.get('user_rol'))

# Pre: Usuario debe estar logueado
# Post: Si logueado, muestra sus reservas. Si no logueado, redirige a login
@user_bp.route('/mis-reservas')
def mis_reservas():
    # Mis reservas
    check = validar_sesion()
    if check:
        return check
    
    user_id = session.get('user_id')
    reservas = obtener_reservas_usuario(user_id)
    
    return render_template('perfil/mis_reservas.html', 
                         reservas=reservas,
                         user_id=user_id,
                         user_nombre=session.get('user_nombre'),
                         user_email=session.get('user_email'),
                         user_rol=session.get('user_rol'))