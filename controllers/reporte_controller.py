from flask import Blueprint, jsonify
from services.reporte_service import reporteservice as reporte_service
from flask_jwt_extended import jwt_required


reporte_bp = Blueprint("reportes", __name__)


@reporte_bp.get("/reportes/ventas-por-caja")
@jwt_required()
def ventas_por_caja():
    try:
        reportes = reporte_service.listar_ventas_por_caja()
        resultado = reportes
        return jsonify(resultado), 200
    except Exception:
        raise


@reporte_bp.get("/reportes/ventas-por-producto")
@jwt_required()
def ventas_por_producto():
    try:
        reportes = reporte_service.listar_ventas_por_producto()
        resultado = reportes
        return jsonify(resultado), 200
    except Exception:
        raise
