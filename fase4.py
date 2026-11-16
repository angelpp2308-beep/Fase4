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
        # Fase 4 - Componente práctico: Prácticas simuladas
# Curso: Programación (Código 213023)
# Universidad Nacional Abierta y a Distancia (UNAD)
# Sistema Integral de Gestión - Empresa Software FJ / Ruta Chipaque

import logging
import sys
from datetime import datetime

# ==========================================
# 1. CONFIGURACIÓN DEL SISTEMA DE LOGS
# ==========================================
logging.basicConfig(
    filename='sistema_reservas_chipaque.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
    encoding='utf-8'
)


# ==========================================
# 2. SECCIÓN DE EXCEPCIONES PERSONALIZADAS
# ==========================================
class ErrorSistemaReservas(Exception):
    """Excepción base general para todos los errores propios del sistema."""
    pass

class CupoAgotadoError(ErrorSistemaReservas):
    """Se lanza cuando el usuario intenta reservar más cupos de los disponibles."""
    def __init__(self, mensaje="Lo sentimos, el servicio seleccionado no tiene cupos disponibles."):
        super().__init__(mensaje)

class ServicioNoDisponibleError(ErrorSistemaReservas):
    """Se lanza cuando se intenta contratar un servicio que está inhabilitado."""
    def __init__(self, mensaje="El servicio seleccionado se encuentra temporalmente inhabilitado."):
        super().__init__(mensaje)

class ReservaInvalidaError(ErrorSistemaReservas):
    """Se lanza cuando hay datos incompletos, cantidades en cero o IDs erróneos."""
    def __init__(self, mensaje="Los datos proporcionados para la reserva son inválidos."):
        super().__init__(mensaje)


# ==========================================
# 3. CLASE QUE MODELA EL SERVICIO (Ruta)
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
        """Propiedad que calcula dinámicamente los cupos libres."""
        return self.cupos_totales - self.cupos_ocupados

    def reservar_cupos(self, cantidad: int):
        if not self.disponible:
            logging.warning(f"Intento de reserva en ruta no disponible: {self.codigo_ruta}")
            raise ServicioNoDisponibleError(f"La ruta {self.codigo_ruta} no está disponible.")
        
        if cantidad <= 0:
            raise ReservaInvalidaError("La cantidad a reservar debe ser mayor a cero.")

        if self.cupos_ocupados + cantidad > self.cupos_totales:
            logging.warning(f"Intento de sobrecupo en ruta {self.codigo_ruta}. Solicitados: {cantidad}")
            raise CupoAgotadoError(f"No hay suficientes cupos en la ruta {self.codigo_ruta}. Disponibles: {self.cupos_disponibles}")

        self.cupos_ocupados += cantidad
        logging.info(f"Reserva exitosa de {cantidad} cupo(s) en la ruta {self.codigo_ruta}.")


# ==========================================
# 4. GESTOR DE RESERVAS (Control y Transacciones)
# ==========================================
class GestorReservas:
    """Centraliza la lógica de transacciones aplicando try, except, else y finally."""
    def __init__(self):
        self.rutas = {}

    def registrar_ruta(self, ruta: RutaTransporte):
        self.rutas[ruta.codigo_ruta] = ruta

    def procesar_reserva(self, codigo_ruta: str, cantidad: int, id_usuario: int):
        print(f"\n--- Procesando reserva: Ruta {codigo_ruta} | Cantidad: {cantidad} | Usuario: {id_usuario} ---")
        logging.info(f"Iniciando transacción para usuario {id_usuario} en ruta {codigo_ruta}.")
        
        try:
            # Validación de integridad de datos externos
            if not isinstance(id_usuario, int) or id_usuario < 1000:
                raise ValueError("El ID de usuario ingresado no posee un formato válido.")
            
            if codigo_ruta not in self.rutas:
                raise KeyError(f"La ruta con código {codigo_ruta} no existe en el sistema.")

            ruta = self.rutas[codigo_ruta]
            ruta.reservar_cupos(cantidad)

        except (CupoAgotadoError, ServicioNoDisponibleError, ReservaInvalidaError) as e:
            print(f"[ALERTA DE NEGOCIO] {e}")
            logging.error(f"Error controlado de negocio: {e}")
        
        except (ValueError, KeyError) as ex:
            print(f"[ERROR DE SISTEMA / ENCADENADO] Fallo estructural detectado: {ex}")
            logging.critical(f"Excepción estructural capturada: {ex}")
            raise ReservaInvalidaError("Fallo crítico en los parámetros de entrada.") from ex
        
        else:
            print("[ÉXITO] ¡Reserva procesada y confirmada correctamente!")
            logging.info(f"Bloque else ejecutado con éxito para usuario {id_usuario}.")
        
        finally:
            print("[AUDITORÍA] Cierre de ciclo de transacción y liberación de buffer de datos.")
            logging.info(f"Finalizó ciclo de validación para ruta {codigo_ruta}.\n")


# ==========================================
# 5. BLOQUE DE PRÁCTICAS SIMULADAS (10 CASOS)
# ==========================================
if __name__ == "__main__":
    print("==================================================")
    print(" INICIANDO SIMULACIÓN DE RESERVAS - CHIPAQUE / UNAD ")
    print("==================================================")

    gestor = GestorReservas()

    # Configuración de rutas de prueba
    gestor.registrar_ruta(RutaTransporte("R001", "Bogotá", "Chipaque", 10, True))
    gestor.registrar_ruta(RutaTransporte("R002", "Cáqueza", "Bogotá", 5, True))
    gestor.registrar_ruta(RutaTransporte("R003", "Chipaque", "Villavicencio", 8, False)) # Inhabilitada

    # Ejecución de las 10 simulaciones requeridas por la rúbrica
    # 1. Reserva válida estándar
    gestor.procesar_reserva("R001", 3, 100234)
    
    # 2. Reserva válida límite
    gestor.procesar_reserva("R001", 7, 100589)
    
    # 3. Cupo agotado
    gestor.procesar_reserva("R001", 2, 100999)
    
    # 4. Reserva válida ruta 2
    gestor.procesar_reserva("R002", 4, 102345)
    
    # 5. Supera cupos totales
    gestor.procesar_reserva("R002", 3, 103456)
    
    # 6. Ruta no disponible
    gestor.procesar_reserva("R003", 1, 104567)
    
    # 7. Ruta inexistente (Excepción encadenada)
    gestor.procesar_reserva("R999", 2, 105678)
    
    # 8. Usuario inválido (Excepción encadenada)
    gestor.procesar_reserva("R002", 1, 123)
    
    # 9. Cantidad negativa o cero
    gestor.procesar_reserva("R002", 0, 107890)
    
    # 10. Reserva válida final
    gestor.procesar_reserva("R002", 1, 108901)

    print("\n==================================================")
    print(" SIMULACIÓN FINALIZADA CON ÉXITO. LOGS GENERADOS. ")
    print("==================================================")

