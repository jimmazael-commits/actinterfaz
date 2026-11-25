from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from services.auth_service import AuthService
from utils import objeto_json

auth_bp = Blueprint("auth", __name__)

@auth_bp.post('/registro')
def registro():
    datos = objeto_json()
    res, msg, code = AuthService.registrar_usuario(datos)
    return jsonify(status='success' if res is not None else 'error', message=msg, data=res), code

@auth_bp.post('/login')
def login():
    datos = objeto_json()
    correo, clave = datos.get('correo_electronico'), datos.get('contrasena')
    if not isinstance(correo, str) or not correo.strip() or not isinstance(clave, str) or not clave:
        raise ValueError('correo_electronico y contrasena son obligatorios')
    res, msg, code = AuthService.login(correo, clave)
    if res is not None:
        res['access_token'] = create_access_token(identity=str(res['id_usuario']))
    return jsonify(status='success' if res is not None else 'error', message=msg, data=res), code
