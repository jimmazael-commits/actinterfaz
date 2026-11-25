from DB import Database
from utils import serializar

class reporte:
    @staticmethod
    def consultar(sql):
        conn = Database().connect()
        try:
            with conn.cursor(dictionary=True) as cur:
                cur.execute(sql)
                return [serializar(r) for r in cur.fetchall()]
        finally:
            conn.close()

    @staticmethod
    def obtener_ventas_por_caja():
        return reporte.consultar("""
            SELECT c.numero_caja, SUM(v.total) AS total_ventas,
                   COUNT(v.id_venta) AS cantidad_tickets
            FROM ventas v INNER JOIN cajas c ON c.id_caja = v.id_caja
            GROUP BY c.numero_caja ORDER BY c.numero_caja
        """)

    @staticmethod
    def obtener_ventas_por_producto():
        return reporte.consultar("""
            SELECT p.id_producto, p.descripcion, SUM(d.cantidad) AS cantidad_vendida,
                   SUM(d.importe) AS total_generado
            FROM detalle_venta d INNER JOIN productos p ON p.id_producto = d.id_producto
            GROUP BY p.id_producto, p.descripcion ORDER BY total_generado DESC
        """)
