from repository.producto_repository import Productorepository as Repo
from utils import entero, precio, imagen


class productoservice:

    @staticmethod
    def listar_productos():
        return Repo.obtener_productos()

    @staticmethod
    def buscar_producto(id_producto):
        return Repo.obtener_producto(id_producto)

    @staticmethod
    def guardar(datos, id_producto=None):
        limites = {
            "codigo": 50,
            "descripcion": 255,
            "estatus": 20,
            "unidades": 20
        }

        permitidos = set(limites) | {
            "precio",
            "existencias",
            "imagen",
            "status"
        }

        if not isinstance(datos, dict) or not datos:
            raise ValueError(
                "Debes enviar un objeto JSON con datos del producto"
            )

        desconocidos = set(datos) - permitidos

        if desconocidos:
            raise ValueError(
                "Campos desconocidos: "
                + ", ".join(sorted(desconocidos))
            )

        # Al crear, estos campos son obligatorios.
        if id_producto is None:
            obligatorios = [
                "codigo",
                "descripcion",
                "precio",
                "existencias",
                "estatus",
                "unidades"
            ]

            for campo in obligatorios:
                if campo not in datos:
                    raise ValueError(
                        f"Falta el campo {campo}"
                    )

        # Validar campos de texto.
        for campo, longitud in limites.items():
            if campo in datos:
                valor = datos[campo]

                if (
                    not isinstance(valor, str)
                    or not valor.strip()
                    or len(valor) > longitud
                ):
                    raise ValueError(
                        f"{campo} debe ser texto no vacío "
                        f"de máximo {longitud} caracteres"
                    )

        datos = dict(datos)

        if "precio" in datos:
            datos["precio"] = precio(datos["precio"])

        if "existencias" in datos:
            entero(
                datos["existencias"],
                "existencias"
            )

        if "status" in datos:
            entero(datos["status"], "status")

            if datos["status"] not in (0, 1):
                raise ValueError(
                    "status debe ser 0 o 1"
                )

        if "imagen" in datos:
            imagen(datos["imagen"])

        if id_producto is not None:
            producto = Repo.obtener_producto(id_producto)

            if producto is None:
                return None

        id_guardado = Repo.guardar(
            datos,
            id_producto
        )

        return Repo.obtener_producto(id_guardado)