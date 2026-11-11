# -*- coding: utf-8 -*-
"""
Fase 4 - Componente práctico: Prácticas simuladas
Curso: Programación (Código 213023)
Universidad Nacional Abierta y a Distancia (UNAD)
Estudiante: Kevin Antonio Martínez Huérfano
Programa: Ingeniería de Sistemas
"""

import logging
import sys
from datetime import datetime

logging.basicConfig(
    filename='sistema_reservas_chipaque.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
    encoding='utf-8'
)

class ErrorSistemaReservas(Exception):
    pass

class CupoAgotadoError(ErrorSistemaReservas):
    def __init__(self, mensaje="Lo sentimos, el servicio seleccionado no tiene cupos disponibles."):
        super().__init__(mensaje)

class ServicioNoDisponibleError(ErrorSistemaReservas):
    def __init__(self, mensaje="El servicio de transporte seleccionado se encuentra temporalmente inhabilitado."):
        super().__init__(mensaje)

class ReservaInvalidaError(ErrorSistemaReservas):
    def __init__(self, mensaje="Los datos proporcionados para la reserva son inválidos o incompletos."):
        super().__init__(mensaje)

class RutaTransporte:
    def __init__(self, codigo_ruta: str, origen: str, destino: str, cupos_totales: int, disponible: bool = True):
        self.codigo_ruta = codigo_ruta
        self.origen = origen
        self.destino = destino
        self.cupos_totales = cupos_totales
        self.cupos_ocupados = 0
        self.disponible = disponible

    @property
    def cupos_disponibles(self) -> int:
        return self.cupos_totales - self.cupos_ocupados

    def reservar_cupos(self, cantidad: int):
        if not self.disponible:
            logging.warning(f"Intento de reserva en ruta no disponible: {self.codigo_ruta}")
            raise ServicioNoDisponibleError(f"La ruta {self.codigo_ruta} ({self.origen} - {self.destino}) no está disponible.")
        
        if cantidad <= 0:
            raise ReservaInvalidaError("La cantidad de cupos a reservar debe ser mayor a cero.")

        if self.cupos_ocupados + cantidad > self.cupos_totales:
            logging.warning(f"Intento de sobrecupo en ruta {self.codigo_ruta}. Solicitados: {cantidad}, Disponibles: {self.cupos_disponibles}")
            raise CupoAgotadoError(f"No hay suficientes cupos en la ruta {self.codigo_ruta}. Disponibles: {self.cupos_disponibles}")

        self.cupos_ocupados += cantidad
        logging.info(f"Reserva exitosa de {cantidad} cupo(s) en la ruta {self.codigo_ruta} ({self.origen} - {self.destino}).")

class GestorReservas:
    def __init__(self):
        self.rutas = {}

    def agregar_ruta(self, ruta: RutaTransporte):
        self.rutas[ruta.codigo_ruta] = ruta

    def procesar_reserva(self, codigo_ruta: str, cantidad: int, id_usuario: str):
        print(f"\n[PROCESANDO] Usuario: {id_usuario} | Ruta: {codigo_ruta} | Cantidad: {cantidad}")
        logging.info(f"Iniciando procesamiento de reserva - Usuario: {id_usuario}, Ruta: {codigo_ruta}, Cantidad: {cantidad}")
        
        try:
            if not id_usuario or len(id_usuario) < 5:
                raise ValueError(f"Identificación de usuario inválida: '{id_usuario}'. Debe tener al menos 5 caracteres.")

            if codigo_ruta not in self.rutas:
                raise KeyError(f"La ruta con código '{codigo_ruta}' no se encuentra registrada en el sistema.")

            ruta = self.rutas[codigo_ruta]
            ruta.reservar_cupos(cantidad)

        except (ValueError, KeyError) as e:
            logging.error(f"Error de validación o clave en transacción de usuario {id_usuario}: {str(e)}")
            raise ReservaInvalidaError(f"Fallo estructural en la solicitud de reserva para {id_usuario}.") from e

        except CupoAgotadoError as e:
            logging.error(f"Error de cupo agotado: {str(e)}")
            print(f"  -> [ALERTA CAPTURADA]: {e}")
            return False

        except ServicioNoDisponibleError as e:
            logging.error(f"Error de servicio no disponible: {str(e)}")
            print(f"  -> [ALERTA CAPTURADA]: {e}")
            return False

        else:
            print(f"  -> [ÉXITO]: Reserva confirmada satisfactoriamente para el usuario {id_usuario}.")
            logging.info(f"Transacción finalizada con éxito para el usuario {id_usuario}.")
            return True

        finally:
            print(f"  -> [AUDITORÍA]: Cierre de ciclo operativo para usuario {id_usuario} a las {datetime.now().strftime('%H:%M:%S')}.")
            logging.info(f"Cierre de ciclo operativo completado para {id_usuario}.")

def ejecutar_simulaciones():
    print("==================================================")
    print(" INICIO DE SIMULACIONES - FASE 4 (UNAD)           ")
    print(" Sistema de Gestión de Transporte - Ruta Chipaque ")
    print("==================================================")

    gestor = GestorReservas()
    gestor.agregar_ruta(RutaTransporte("R001", "Bogotá", "Chipaque", 10, disponible=True))
    gestor.agregar_ruta(RutaTransporte("R002", "Villavicencio", "Chipaque", 5, disponible=True))
    gestor.agregar_ruta(RutaTransporte("R003", "Cáqueza", "Bogotá", 2, disponible=False))

    casos_prueba = [
        ("R001", 3, "100234", "Simulación 1: Reserva válida estándar"),
        ("R001", 7, "100589", "Simulación 2: Reserva válida que agota los cupos restantes de R001"),
        ("R001", 2, "100999", "Simulación 3: Intento de reserva con cupos agotados"),
        ("R002", 4, "102345", "Simulación 4: Reserva válida en ruta R002"),
        ("R002", 3, "103456", "Simulación 5: Intento de superar cupos totales en R002"),
        ("R003", 1, "104567", "Simulación 6: Intento de reserva en ruta inhabilitada (R003)"),
        ("R999", 2, "105678", "Simulación 7: Intento de reserva con código de ruta inexistente"),
        ("R002", 1, "123", "Simulación 8: Intento de reserva con ID de usuario inválido"),
        ("R002", 0, "107890", "Simulación 9: Intento de reserva con cantidad de cupos en cero"),
        ("R002", 1, "108901", "Simulación 10: Reserva válida final tras depuración")
    ]

    for idx, (ruta, cantidad, usuario, descripcion) in enumerate(casos_prueba, 1):
        print(f"\n--- {descripcion} ---")
        try:
            gestor.procesar_reserva(ruta, cantidad, usuario)
        except Exception as e:
            print(f"  -> [EXCEPCIÓN EXTERNA CAPTURADA]: {e}")
            logging.critical(f"Excepción no controlada en bloque principal: {str(e)}")

    print("\n==================================================")
    print(" FIN DE LAS 10 SIMULACIONES - REVISAR LOGS        ")
    print("==================================================")

if __name__ == "__main__":
    ejecutar_simulaciones()
