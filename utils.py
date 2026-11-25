import base64
from datetime import date, datetime
from decimal import Decimal, InvalidOperation
from flask import request

def objeto_json():
    datos = request.get_json(silent=True)
    if not isinstance(datos, dict):
        raise ValueError('Envía un objeto JSON válido con Content-Type: application/json')
    return datos

def serializar(row):
    if row is None: return None
    result = {}
    for k,v in row.items():
        if k == 'status': v = int.from_bytes(v, 'big') if isinstance(v, bytes) else int(v)
        elif isinstance(v, (bytes, bytearray)): v = base64.b64encode(v).decode()
        elif isinstance(v, (date, datetime)): v = v.isoformat()
        elif isinstance(v, Decimal): v = str(v)
        result[k] = v
    return result

def imagen(valor):
    if valor is None: return None
    if not isinstance(valor, str): raise ValueError('imagen debe ser texto Base64 o null')
    try: data = base64.b64decode(valor.split(',', 1)[-1], validate=True)
    except Exception: raise ValueError('imagen no contiene Base64 válido')
    if len(data) > 65535: raise ValueError('imagen supera el límite del campo BLOB (65535 bytes)')
    return data

def entero(v, campo, minimo=0):
    if isinstance(v, bool) or not isinstance(v, int) or v < minimo:
        raise ValueError(f'{campo} debe ser entero mayor o igual a {minimo}')
    return v

def precio(v):
    try: n = Decimal(str(v))
    except (InvalidOperation, ValueError): raise ValueError('precio inválido')
    if not n.is_finite() or n < 0 or n > Decimal('99999999.99') or n != n.quantize(Decimal('.01')):
        raise ValueError('precio debe tener máximo dos decimales y estar entre 0 y 99999999.99')
    return n
