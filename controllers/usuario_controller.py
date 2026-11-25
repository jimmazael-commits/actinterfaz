from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from utils import objeto_json
from services.usuario_service import UsuarioService

usuario_bp = Blueprint('usuario_bp', __name__)

@usuario_bp.get("/usuarios")
@jwt_required()
def listar_usuarios():
    usuarios = UsuarioService.obtener_todos()
    return jsonify({"status": "success", "message": "Operación realizada correctamente", "data": usuarios}), 200

@usuario_bp.get("/usuarios/<int:id_usuario>")
@jwt_required()
def obtener_usuario(id_usuario):
    usuario = UsuarioService.obtener_por_id(id_usuario)
    if not usuario:
        return jsonify({"status": "error", "message": "Usuario no encontrado", "data": None}), 404
    return jsonify({"status": "success", "message": "Operación realizada correctamente", "data": usuario}), 200

@usuario_bp.put("/usuarios/<int:id_usuario>")
@jwt_required()
def actualizar_usuario(id_usuario):
    datos = objeto_json()
    exito = UsuarioService.actualizar_usuario(id_usuario, datos)
    if not exito:
        return jsonify({"status": "error", "message": "Usuario no encontrado o sin cambios", "data": None}), 404
    return jsonify({"status": "success", "message": "Usuario actualizado correctamente", "data": None}), 200
