from DB import Database
from utils import serializar, imagen
from repository.procedimientos import ejecutar_sp


class UsuarioRepository:
    @staticmethod
    def consultar_procedimiento(nombre, parametros=(), uno=False):
        conn = Database().connect()

        try:
            with conn.cursor(dictionary=True) as cur:
                filas = ejecutar_sp(cur, nombre, parametros)

            if uno:
                return filas[0] if filas else None

            return filas
        finally:
            conn.close()

    @staticmethod
    def obtener_por_correo(correo):
        # AuthService necesita el hash sin serializar.
        return UsuarioRepository.consultar_procedimiento(
            "sp_usuario_por_correo",
            (correo,),
            uno=True
        )

    @staticmethod
    def obtener_por_id(id_usuario):
        usuario = UsuarioRepository.consultar_procedimiento(
            "sp_usuario_por_id",
            (id_usuario,),
            uno=True
        )

        return serializar(usuario)

    @staticmethod
    def obtener_todos():
        usuarios = UsuarioRepository.consultar_procedimiento(
            "sp_usuarios_listar"
        )

        return [serializar(usuario) for usuario in usuarios]

    @staticmethod
    def crear(datos):
        parametros = (
            datos.get("nombre"),
            datos.get("apellido"),
            datos.get("correo_electronico"),
            datos.get("contrasena"),
            datos.get("telefono"),
            datos.get("direccion"),
            datos.get("nickname"),
            datos.get("fecha_nacimiento"),
            imagen(datos.get("imagen"))
        )

        conn = Database().connect()

        try:
            with conn.cursor(dictionary=True) as cur:
                filas = ejecutar_sp(
                    cur,
                    "sp_usuario_crear",
                    parametros
                )

                id_usuario = filas[0]["id_usuario"]

            conn.commit()
            return id_usuario

        except Exception:
            conn.rollback()
            raise

        finally:
            conn.close()

    @staticmethod
    def actualizar(id_usuario, datos):
        permitidos = {
            "nombre",
            "apellido",
            "correo_electronico",
            "telefono",
            "direccion",
            "nickname",
            "fecha_nacimiento",
            "imagen",
            "status"
        }

        if not datos or set(datos) - permitidos:
            raise ValueError("Campos de usuario no permitidos")

        conn = Database().connect()

        try:
            with conn.cursor(dictionary=True) as cur:
                for campo, valor in datos.items():
                    if campo == "imagen":
                        valor = imagen(valor)
                    elif campo == "status":
                        # El procedimiento recibe texto o bytes.
                        valor = str(valor)

                    ejecutar_sp(
                        cur,
                        "sp_usuario_actualizar_campo",
                        (id_usuario, campo, valor)
                    )

            conn.commit()
            return True

        except Exception:
            conn.rollback()
            raise

        finally:
            conn.close()