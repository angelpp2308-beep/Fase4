#Este seria el main
##
#Fase 4 - Componente práctico: Prácticas simuladas
#Curso: Programación (Código 213023)
#Universidad Nacional Abierta y a Distancia (UNAD)
#Sistema Integral de Gestión - Empresa Software FJ / Ruta Chipaque
##

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

# ==========================================
# 3. CLASE QUE MODELA EL SERVICIO (Ruta / Recurso)
# ==========================================
class RutaTransporte:
    """Modela la entidad de servicio con sus atributos, encapsulación y validaciones internas."""
    def __init__(self, codigo_ruta: str, origen: str, destino: str, cupos_totales: int, disponible: bool = True):
        self.codigo_ruta = codigo_ruta
        self.origen = origen
        self.destino = destino
        self.cupos_totales = cupos_totales
        self.cupos_ocupados = 0
        self.disponible = disponible

    @property
    def cupos_disponibles(self) -> int:
        """Propiedad protegida que calcula dinámicamente los cupos libres."""
        return self.cupos_totales - self.cupos_ocupados

    def reservar_cupos(self, cantidad: int):
        """
        Validaciones estrictas del servicio:
        - Valida si el servicio está disponible.
        - Valida que la cantidad a reservar sea mayor a cero.
        - Valida que no se exceda el límite de cupos (sobrecupo).
        """
        # Validación 1: Disponibilidad del servicio
        if not self.disponible:
            logging.warning(f"Intento de reserva en ruta no disponible: {self.codigo_ruta}")
            raise ServicioNoDisponibleError(f"La ruta {self.codigo_ruta} no está disponible.")
        
        # Validación 2: Cantidad lógica permitida
        if cantidad <= 0:
            raise ReservaInvalidaError("La cantidad a reservar debe ser mayor a cero.")

        # Validación 3: Control de cupos máximos
        if self.cupos_ocupados + cantidad > self.cupos_totales:
            logging.warning(f"Intento de sobrecupo en ruta {self.codigo_ruta}. Solicitados: {cantidad}")
            raise CupoAgotadoError(f"No hay suficientes cupos en la ruta {self.codigo_ruta}. Disponibles: {self.cupos_disponibles}")

        # Si pasa todas las validaciones, efectúa la ocupación
        self.cupos_ocupados += cantidad
        logging.info(f"Reserva exitosa de {cantidad} cupo(s) en la ruta {self.codigo_ruta}.")
        