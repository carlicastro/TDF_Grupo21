"""
Rutas de autenticación SIMPLES
"""

from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from services.api_client import login_usuario, crear_usuario, logout_usuario

auth_bp = Blueprint('auth', __name__)

# Pre: Petición HTTP válida
# Post: Si GET muestra formulario, si POST válido inicia sesión y redirige, si inválido muestra error
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Login simple"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not email or not password:
            flash("Email y contraseña requeridos", "error")
            return render_template('auth/login.html')
        
        resultado = login_usuario(email, password)
        
        if resultado and resultado.get('success'):
            user_data = resultado.get('user', {})
            flash(f"Bienvenido {user_data.get('nombre')}", "success")
            
            if user_data.get('rol') == 'admin':
                return redirect(url_for('admin.admin_dashboard'))
            else:
                return redirect(url_for('public.index'))
        else:
            flash('Error al iniciar sesión', "error")
    
    return render_template('auth/login.html')

# Pre: Petición HTTP válida
# Post: Si GET muestra formulario, si POST válido registra usuario y redirige a login, si inválido muestra error
@auth_bp.route('/registro', methods=['GET', 'POST'])
def registro():
    """Registro simple"""
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        password = request.form.get('password')
        
        datos = {'nombre': nombre, 'email': email, 'password': password}
        
        if crear_usuario(datos):
            flash("Usuario registrado", "success")
            return redirect(url_for('auth.login'))
        else:
            flash("Error al registrar", "error")
    
    return render_template('auth/registro.html')

# Pre: Usuario con sesión activa
# Post: Cierra sesión y redirige a inicio con mensaje de confirmación
@auth_bp.route('/logout')
def logout():
    """Cerrar sesión simple"""
    logout_usuario()
    flash("Sesión cerrada", "success")
    return redirect(url_for('public.index'))