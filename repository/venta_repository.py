import uuid
from decimal import Decimal

from DB import Database
from utils import serializar
from repository.procedimientos import ejecutar_sp


class VentaRepository:
    @staticmethod
    def registrar_venta(id_usuario, id_caja, productos):
        conn = Database().connect()

        try:
            conn.start_transaction()

            with conn.cursor(dictionary=True) as cursor:
                usuarios = ejecutar_sp(
                    cursor,
                    "sp_venta_validar_usuario",
                    (id_usuario,)
                )

                if not usuarios or not serializar(usuarios[0])["status"]:
                    raise ValueError(
                        "Usuario inexistente o dado de baja"
                    )

                cajas = ejecutar_sp(
                    cursor,
                    "sp_venta_validar_caja",
                    (id_caja,)
                )

                if not cajas:
                    raise ValueError("La caja no existe")

                total_venta = Decimal("0.00")
                detalles = []
                ids_procesados = set()

                # Mantener un orden consistente al bloquear productos.
                for item in sorted(
                    productos,
                    key=lambda item: item["id_producto"]
                ):
                    id_producto = item["id_producto"]
                    cantidad = item["cantidad"]

                    if id_producto in ids_procesados:
                        raise ValueError(
                            "No repitas productos; suma sus cantidades"
                        )

                    ids_procesados.add(id_producto)

                    if (
                        isinstance(cantidad, bool)
                        or not isinstance(cantidad, int)
                        or cantidad <= 0
                    ):
                        raise ValueError(
                            "cantidad debe ser un entero mayor que 0"
                        )

                    filas = ejecutar_sp(
                        cursor,
                        "sp_venta_obtener_producto",
                        (id_producto,)
                    )

                    if not filas:
                        raise ValueError(
                            f"El producto con ID {id_producto} no existe"
                        )

                    producto = filas[0]

                    if not serializar(
                        {"status": producto["status"]}
                    )["status"]:
                        raise ValueError("Producto dado de baja")

                    if producto["existencias"] < cantidad:
                        raise ValueError("Existencias insuficientes")

                    precio = Decimal(str(producto["precio"]))
                    importe = precio * cantidad
                    total_venta += importe

                    detalles.append(
                        (id_producto, cantidad, precio, importe)
                    )

                if not detalles:
                    raise ValueError(
                        "La venta debe incluir productos"
                    )

                if total_venta > Decimal("99999999.99"):
                    raise ValueError(
                        "El total excede la capacidad de DECIMAL(10,2)"
                    )

                folio = f"V-{uuid.uuid4().hex[:18].upper()}"

                filas = ejecutar_sp(
                    cursor,
                    "sp_venta_crear",
                    (folio, id_usuario, id_caja, total_venta)
                )

                id_venta = filas[0]["id_venta"]

                for detalle in detalles:
                    ejecutar_sp(
                        cursor,
                        "sp_venta_agregar_detalle",
                        (id_venta, *detalle)
                    )

            conn.commit()

            return {
                "id_venta": id_venta,
                "folio": folio,
                "total": str(total_venta)
            }

        except Exception:
            conn.rollback()
            raise

        finally:
            conn.close()