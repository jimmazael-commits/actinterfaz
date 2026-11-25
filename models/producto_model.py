from utils import serializar


class Producto:
    def __init__(
        self,
        id_producto=None,
        codigo=None,
        descripcion=None,
        precio=None,
        existencias=None,
        estatus=None,
        unidades=None,
        imagen=None,
        status=1
    ):
        self.id_producto = id_producto
        self.codigo = codigo
        self.descripcion = descripcion
        self.precio = precio
        self.existencias = existencias
        self.estatus = estatus
        self.unidades = unidades
        self.imagen = imagen
        self.status = status

    def a_diccionario(self):
        return serializar({
            "id_producto": self.id_producto,
            "codigo": self.codigo,
            "descripcion": self.descripcion,
            "precio": self.precio,
            "existencias": self.existencias,
            "estatus": self.estatus,
            "unidades": self.unidades,
            "imagen": self.imagen,
            "status": self.status
        })