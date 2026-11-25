class Venta:
    def __init__(
        self,
        id_venta=None,
        folio=None,
        id_usuario=None,
        id_caja=None,
        fecha_venta=None,
        total=None
    ):
        self.id_venta = id_venta
        self.folio = folio
        self.id_usuario = id_usuario
        self.id_caja = id_caja
        self.fecha_venta = fecha_venta
        self.total = total

    def a_diccionario(self):
        from utils import serializar
        return serializar({k:v for k,v in vars(self).items() if k != "contrasena"})
