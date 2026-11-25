from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils import objeto_json
from services.venta_service import VentaService

venta_bp = Blueprint('venta_bp', __name__)

@venta_bp.post("/ventas")
@jwt_required()
def registrar_venta():
    datos = objeto_json()
    if 'id_usuario' in datos and datos['id_usuario'] != int(get_jwt_identity()):
        raise ValueError('id_usuario debe coincidir con el usuario del token')
    datos['id_usuario'] = int(get_jwt_identity())
    res, msg, status_code = VentaService.realizar_venta(datos)
    if res is None:
        return jsonify({"status": "error", "message": msg, "data": None}), status_code
    return jsonify({"status": "success", "message": msg, "data": res}), status_code
