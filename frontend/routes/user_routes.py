"""
Rutas de usuario - Perfil y gestión personal
"""

from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from services.api_client import obtener_reservas_usuario

user_bp = Blueprint('user', __name__)

@user_bp.route('/perfil', methods=['GET', 'POST'])
def perfil():
    """Perfil de usuario - Lógica básica"""
    if not session.get('logged_in'):
        return redirect(url_for('auth.login'))
    
    return render_template('perfil/perfil.html')

@user_bp.route('/mis-reservas')
def mis_reservas():
    """Mis reservas del usuario logueado - Lógica básica"""
    if not session.get('logged_in'):
        return redirect(url_for('auth.login'))
    
    user_id = session.get('user_id')
    reservas = obtener_reservas_usuario(user_id)
    
    return render_template('perfil/mis_reservas.html', reservas=reservas)