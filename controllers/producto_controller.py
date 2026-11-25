from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from services.producto_service import productoservice as Servicio
from utils import objeto_json

producto_bp = Blueprint('productos', __name__)

@producto_bp.get('/productos')
def listar_productos(): return jsonify(Servicio.listar_productos()), 200

@producto_bp.get('/productos/<int:id_producto>')
def obtener_producto(id_producto):
    producto = Servicio.buscar_producto(id_producto)
    return (jsonify(producto),200) if producto is not None else (jsonify(message='Producto no encontrado'),404)

@producto_bp.post('/productos')
@jwt_required()
def crear_producto(): return jsonify(Servicio.guardar(objeto_json())),201

@producto_bp.put('/productos/<int:id_producto>')
@jwt_required()
def actualizar_producto(id_producto):
    producto = Servicio.guardar(objeto_json(),id_producto)
    return (jsonify(producto),200) if producto is not None else (jsonify(message='Producto no encontrado'),404)
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required

from services.producto_service import productoservice as Servicio
from utils import objeto_json


producto_bp = Blueprint("productos", __name__)


@producto_bp.get("/productos")
def listar_productos():
    productos = Servicio.listar_productos()
    return jsonify(productos), 200


@producto_bp.get("/productos/<int:id_producto>")
def obtener_producto(id_producto):
    producto = Servicio.buscar_producto(id_producto)

    if producto is None:
        return jsonify({
            "message": "Producto no encontrado"
        }), 404

    return jsonify(producto), 200


@producto_bp.post("/productos")
@jwt_required()
def crear_producto():
    datos = objeto_json()
    producto = Servicio.guardar(datos)

    return jsonify(producto), 201


@producto_bp.put("/productos/<int:id_producto>")
@jwt_required()
def actualizar_producto(id_producto):
    datos = objeto_json()

    producto = Servicio.guardar(
        datos,
        id_producto
    )

    if producto is None:
        return jsonify({
            "message": "Producto no encontrado"
        }), 404

    return jsonify(producto), 200