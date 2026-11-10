from excepciones import ClienteInvalidoError

class Cliente:
    def __init__(self, identificacion: str, nombre: str, correo: str, telefono: str):
        self.identificacion = identificacion
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono

    @property
    def identificacion(self):
        return self._identificacion

    @identificacion.setter
    def identificacion(self, valor):
        # Convertimos a texto por si acaso ingresan números puros
        valor_str = str(valor).strip()
        
        # Validamos si tiene puntos o espacios
        if "." in valor_str or " " in valor_str:
            raise ClienteInvalidoError("Error: La cédula no puede contener puntos ni espacios.")
        
        # Validamos que sean solo números
        if not valor_str.isdigit():
            raise ClienteInvalidoError("Error: La cédula debe contener únicamente números.")
            
        self._identificacion = valor_str
        