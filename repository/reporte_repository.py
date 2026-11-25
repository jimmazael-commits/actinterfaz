from DB import Database
from repository.procedimientos import ejecutar_sp
from utils import serializar


class reporte:
    @staticmethod
    def consultar_procedimiento(nombre):
        conn = Database().connect()

        try:
            with conn.cursor(dictionary=True) as cur:
                filas = ejecutar_sp(cur, nombre)
                return [serializar(fila) for fila in filas]

        finally:
            conn.close()

    @staticmethod
    def obtener_ventas_por_caja():
        return reporte.consultar_procedimiento(
            "sp_reporte_ventas_por_caja"
        )

    @staticmethod
    def obtener_ventas_por_producto():
        return reporte.consultar_procedimiento(
            "sp_reporte_ventas_por_producto"
        )
