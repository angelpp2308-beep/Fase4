class SoftwareFJException(Exception):
    """Excepción base para todos los errores del sistema Software FJ."""
    pass

class ClienteInvalidoError(SoftwareFJException):
    """Se lanza cuando los datos del cliente no cumplen con las validaciones."""
    pass

class ServicioNoDisponibleError(SoftwareFJException):
    """Se lanza cuando se intenta contratar un servicio inactivo o no disponible."""
    pass

class ReservaInvalidaError(SoftwareFJException):
    """Se lanza cuando hay conflictos o datos incorrectos en una reserva."""
    pass
