#Este seria el main
"""
Fase 4 - Componente práctico: Prácticas simuladas
Curso: Programación (Código 213023)
Universidad Nacional Abierta y a Distancia (UNAD)
Sistema Integral de Gestión - Empresa Software FJ / Ruta Chipaque
"""

import logging
import sys
from datetime import datetime

# ==========================================
# 1. CONFIGURACIÓN DEL SISTEMA DE LOGS
# ==========================================
# Aquí configuramos el archivo donde se registrarán automáticamente 
# todos los eventos, advertencias y errores que ocurran durante la ejecución.
logging.basicConfig(
    filename='sistema_reservas_chipaque.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
    encoding='utf-8'
)


# ==========================================
# 2. SECCIÓN DE EXCEPCIONES PERSONALIZADAS
# ==========================================
# En esta sección creamos nuestros propios errores heredando de la clase Exception.
# Esto nos permite controlar situaciones específicas del negocio sin que el programa se caiga.

class ErrorSistemaReservas(Exception):
    """Excepción base general para todos los errores propios del sistema."""
    pass

class CupoAgotadoError(ErrorSistemaReservas):
    """Se valida y se lanza cuando el usuario intenta reservar más cupos de los disponibles."""
    def __init__(self, mensaje="Lo sentimos, el servicio seleccionado no tiene cupos disponibles."):
        super().__init__(mensaje)

class ServicioNoDisponibleError(ErrorSistemaReservas):
    """Se valida y se lanza cuando se intenta contratar un servicio que está inhabilitado."""
    def __init__(self, mensaje="El servicio seleccionado se encuentra temporalmente inhabilitado."):
        super().__init__(mensaje)

class ReservaInvalidaError(ErrorSistemaReservas):
    """Se valida y se lanza cuando hay datos incompletos, cantidades en cero o IDs malos."""
    def __init__(self, mensaje="Los datos proporcionados forzosamente para la reserva son inválidos."):
        super().__init__(mensaje)
        