from repository.reporte_repository import reporte as reporte_repository

class reporteservice:
    @staticmethod
    def listar_ventas_por_caja():
        return reporte_repository.obtener_ventas_por_caja()

    @staticmethod
    def listar_ventas_por_producto():
        return reporte_repository.obtener_ventas_por_producto()
