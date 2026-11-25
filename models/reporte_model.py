class VentaPorCaja:
    def a_diccionario(self):
        from utils import serializar
        return serializar(vars(self))

    def __init__(self, numero_caja=None, total_ventas=None, cantidad_tickets=None):
        self.numero_caja = numero_caja
        self.total_ventas = total_ventas
        self.cantidad_tickets = cantidad_tickets


class VentaPorProducto:
    def a_diccionario(self):
        from utils import serializar
        return serializar(vars(self))

    def __init__(self, id_producto=None, descripcion=None,
                 cantidad_vendida=None, total_generado=None):
        self.id_producto = id_producto
        self.descripcion = descripcion
        self.cantidad_vendida = cantidad_vendida
        self.total_generado = total_generado
