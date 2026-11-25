from repository.venta_repository import VentaRepository
from utils import entero
class VentaService:
    @staticmethod
    def realizar_venta(datos):
        entero(datos.get('id_caja'),'id_caja',1)
        productos = datos.get('productos')
        if not isinstance(productos,list) or not productos: raise ValueError('productos debe ser una lista no vacía')
        ids = set()
        for item in productos:
            if not isinstance(item,dict): raise ValueError('Cada producto debe ser un objeto')
            entero(item.get('id_producto'),'id_producto',1)
            entero(item.get('cantidad'),'cantidad',1)
            if item['id_producto'] in ids: raise ValueError('No repitas id_producto en la venta; suma sus cantidades')
            ids.add(item['id_producto'])
        return VentaRepository.registrar_venta(datos['id_usuario'],datos['id_caja'],productos), 'Venta registrada correctamente',201
