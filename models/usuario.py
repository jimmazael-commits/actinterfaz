class Usuario:
    def __init__(
        self,
        id_usuario=None,
        nombre=None,
        apellido=None,
        correo_electronico=None,
        contrasena=None,
        telefono=None,
        direccion=None,
        imagen=None,
        nickname=None,
        fecha_nacimiento=None,
        status=1
    ):
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.apellido = apellido
        self.correo_electronico = correo_electronico
        self.contrasena = contrasena
        self.telefono = telefono
        self.direccion = direccion
        self.imagen = imagen
        self.nickname = nickname
        self.fecha_nacimiento = fecha_nacimiento
        self.status = status

    def a_diccionario(self):
        from utils import serializar
        return serializar({k:v for k,v in vars(self).items() if k != "contrasena"})
