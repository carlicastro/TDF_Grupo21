"""
Rutas públicas - Solo páginas estáticas accesibles sin autenticación
"""

from flask import Blueprint, render_template, redirect, url_for, session
from services.api_client import obtener_hospedajes

public_bp = Blueprint('public', __name__)

# Pre: Petición HTTP válida
# Post: Muestra página de inicio con hospedajes destacados
@public_bp.route('/')
def index():
    """Página de inicio con hospedajes destacados"""
    try:
        hospedajes = obtener_hospedajes()[:6]  # Solo los primeros 6
        return render_template('public/index.html', hospedajes=hospedajes)
    except Exception as e:
        # Si hay error con API, mostrar página sin hospedajes
        return render_template('public/index.html', hospedajes=[])

# Pre: Petición HTTP válida
# Post: Muestra página "Acerca de nosotros"
@public_bp.route('/nosotros')
def nosotros():
    """Página sobre nosotros"""
    return render_template('public/nosotros.html')

# Pre: Petición HTTP válida
# Post: Muestra página de servicios
@public_bp.route('/servicios')
def servicios():
    """Página de servicios"""
    return render_template('public/service.html')

# Pre: Petición HTTP válida
# Post: Muestra galería de imágenes
@public_bp.route('/galeria')
def galeria():
    """Página de galería"""
    return render_template('public/galeria.html')

# Pre: Petición HTTP válida
# Post: Muestra página de contacto
@public_bp.route('/contacto')
def contacto():
    """Página de contacto"""
    return render_template('public/contacto.html')

# Pre: Petición HTTP válida
# Post: Muestra página de preguntas frecuentes
@public_bp.route('/preguntas-frecuentes')
def preguntas_frecuentes():
    """Página de preguntas frecuentes"""
    return render_template('public/faq.html')

# Pre: Petición HTTP válida
# Post: Muestra página de preguntas frecuentes (alias)
@public_bp.route('/faq')
def faq():
    """Alias para preguntas frecuentes"""
    return render_template('public/faq.html')

# Pre: Petición HTTP válida
# Post: Muestra página de testimonios
@public_bp.route('/testimonios')
def testimonios():
    """Página de testimonios"""
    return render_template('public/testimonial.html')

# Pre: Petición HTTP válida
# Post: Muestra página de términos y condiciones
@public_bp.route('/terminos')
def terminos():
    """Página de términos y condiciones"""
    return render_template('public/terms.html')