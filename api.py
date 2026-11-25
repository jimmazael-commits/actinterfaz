import os, secrets
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from mysql.connector import Error, IntegrityError
from werkzeug.exceptions import HTTPException
from controllers.auth_controller import auth_bp
from controllers.usuario_controller import usuario_bp
from controllers.venta_controller import venta_bp
from controllers.producto_controller import producto_bp
from controllers.reporte_controller import reporte_bp

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY') or secrets.token_hex(32)
jwt = JWTManager(app)
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(usuario_bp)
app.register_blueprint(venta_bp)
app.register_blueprint(producto_bp)
app.register_blueprint(reporte_bp)

@app.errorhandler(ValueError)
def validacion(e): return jsonify(status='error', message=str(e), data=None), 400

@app.errorhandler(IntegrityError)
def integridad(e):
    code = 409 if e.errno == 1062 else 400
    return jsonify(status='error', message='Registro duplicado' if code == 409 else 'Datos incompatibles con la base de datos', data=None), code

@app.errorhandler(Error)
def error_bd(e):
    app.logger.exception('Error de MySQL')
    return jsonify(status='error', message='Error de MySQL. Revisa la conexión y el esquema; consulta la consola.', data=None), 500

@app.errorhandler(HTTPException)
def error_http(e): return jsonify(status='error', message=e.description, data=None), e.code

if __name__ == '__main__': app.run(debug=os.getenv('FLASK_DEBUG') == '1', port=5000)
