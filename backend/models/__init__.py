"""
Paquete models para el backend
"""
from .usuario import obtener_todos_usuarios
from .hospedajes import obtener_todos_hospedajes
from .reservas import obtener_todas_reservas

__all__ = [
    'obtener_todos_usuarios',
    'obtener_todos_hospedajes',
    'obtener_todas_reservas'
]
