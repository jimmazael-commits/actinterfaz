from DB import Database
from repository.procedimientos import ejecutar_sp
from utils import imagen, serializar


class Productorepository:
    @staticmethod
    def obtener_productos():
        return Productorepository.consultar()

    @staticmethod
    def obtener_producto(id_producto):
        filas = Productorepository.consultar(id_producto)
        return filas[0] if filas else None

    @staticmethod
    def consultar(id_producto=None):
        conn = Database().connect()

        try:
            with conn.cursor(dictionary=True) as cur:
                if id_producto is None:
                    filas = ejecutar_sp(cur, "sp_productos_listar")
                else:
                    filas = ejecutar_sp(
                        cur,
                        "sp_producto_por_id",
                        (id_producto,)
                    )

                return [serializar(fila) for fila in filas]

        finally:
            conn.close()

    @staticmethod
    def guardar(datos, id_producto=None):
        conn = Database().connect()

        try:
            with conn.cursor(dictionary=True) as cur:
                if id_producto is None:
                    parametros = (
                        datos["codigo"],
                        datos["descripcion"],
                        datos["precio"],
                        datos["existencias"],
                        datos["estatus"],
                        datos["unidades"],
                        imagen(datos.get("imagen")),
                        datos.get("status", 1)
                    )
                    filas = ejecutar_sp(
                        cur,
                        "sp_producto_crear",
                        parametros
                    )
                    id_producto = filas[0]["id_producto"]

                else:
                    for campo, valor in datos.items():
                        if campo == "imagen":
                            valor = imagen(valor)
                        elif campo == "status":
                            valor = str(valor)

                        ejecutar_sp(
                            cur,
                            "sp_producto_actualizar_campo",
                            (id_producto, campo, valor)
                        )

            conn.commit()
            return id_producto

        except Exception:
            conn.rollback()
            raise

        finally:
            conn.close()
