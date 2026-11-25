from utils import serializar
from services.usuario_service import validar_usuario
import bcrypt
from repository.usuario_repository import UsuarioRepository

class AuthService:
    @staticmethod
    def registrar_usuario(datos):
        validar_usuario(datos, registro=True)
        datos = dict(datos)
        if UsuarioRepository.obtener_por_correo(datos.get('correo_electronico')):
            return None, "El correo electrónico ya está registrado", 409

        pwd_bytes = datos['contrasena'].encode('utf-8')
        salt = bcrypt.gensalt()
        datos['contrasena'] = bcrypt.hashpw(pwd_bytes, salt).decode('utf-8')

        id_usuario = UsuarioRepository.crear(datos)
        respuesta_data = {
            "id_usuario": id_usuario,
            "nombre": datos.get('nombre'),
            "apellido": datos.get('apellido'),
            "correo_electronico": datos.get('correo_electronico')
        }
        return respuesta_data, "Usuario registrado correctamente", 201

    @staticmethod
    def login(correo, contrasena):
        usuario = UsuarioRepository.obtener_por_correo(correo)
        if not usuario or not serializar({'status': usuario['status']})['status']:
            return None, "Credenciales inválidas", 401

        try:
            valida = bcrypt.checkpw(contrasena.encode('utf-8'), usuario['contrasena'].encode('utf-8'))
        except ValueError:
            valida = False
        if not valida:
            return None, "Credenciales inválidas", 401

        datos_usuario = {
            "id_usuario": usuario['id_usuario'],
            "nombre": usuario['nombre'],
            "correo_electronico": usuario['correo_electronico']
        }
        return datos_usuario, "Inicio de sesión exitoso", 200
