"""
Rutas públicas - Solo páginas estáticas accesibles sin autenticación
"""

from flask import Blueprint, render_template, redirect, url_for

public_bp = Blueprint('public', __name__)

@public_bp.route('/')
def index():
    """Página de inicio con hospedajes destacados"""
    from services.api_client import obtener_hospedajes
    hospedajes = obtener_hospedajes()[:6]  # Solo los primeros 6
    return render_template('public/index.html', hospedajes=hospedajes)

@public_bp.route('/nosotros')
def nosotros():
    """Página sobre nosotros"""
    return render_template('public/nosotros.html')

@public_bp.route('/servicios')
def servicios():
    """Página de servicios"""
    return render_template('public/service.html')

@public_bp.route('/galeria')
def galeria():
    """Página de galería"""
    return render_template('public/galeria.html')

@public_bp.route('/contacto')
def contacto():
    """Página de contacto"""
    return render_template('public/contacto.html')

@public_bp.route('/preguntas-frecuentes')
def preguntas_frecuentes():
    """Página de preguntas frecuentes"""
    return render_template('public/faq.html')

@public_bp.route('/faq')
def faq():
    """Alias para preguntas frecuentes"""
    return render_template('public/faq.html')

@public_bp.route('/testimonios')
def testimonios():
    """Página de testimonios"""
    return render_template('public/testimonial.html')

@public_bp.route('/terminos')
def terminos():
    """Página de términos y condiciones"""
    return render_template('public/terms.html')