from datetime import date
from repository.usuario_repository import UsuarioRepository
from utils import entero, imagen

def validar_usuario(datos, registro=False):
    limites = {'nombre':50, 'apellido':50, 'correo_electronico':100, 'telefono':20, 'direccion':255, 'nickname':50}
    permitidos = set(limites) | {'fecha_nacimiento','imagen','status'}
    if registro: permitidos.add('contrasena')
    if not datos or set(datos) - permitidos: raise ValueError('Campos vacíos o desconocidos en usuario')
    if registro:
        for k in ('nombre','apellido','correo_electronico','contrasena','fecha_nacimiento'):
            if not datos.get(k): raise ValueError(f'Falta el campo {k}')
        if 'status' in datos: raise ValueError('El registro utiliza status=1 por defecto')
        if not isinstance(datos['contrasena'], str) or len(datos['contrasena'].encode()) > 72:
            raise ValueError('contrasena debe ser texto de hasta 72 bytes')
    for k,limite in limites.items():
        if k in datos:
            v = datos[k]
            if v is None and k not in ('nombre','apellido','correo_electronico'): continue
            if not isinstance(v,str) or not v.strip() or len(v)>limite: raise ValueError(f'{k} inválido: máximo {limite} caracteres')
    if 'correo_electronico' in datos and '@' not in datos['correo_electronico']: raise ValueError('correo_electronico inválido')
    if 'fecha_nacimiento' in datos:
        try: date.fromisoformat(datos['fecha_nacimiento'])
        except (TypeError,ValueError): raise ValueError('fecha_nacimiento debe usar AAAA-MM-DD')
    if 'status' in datos:
        entero(datos['status'],'status')
        if datos['status'] not in (0,1): raise ValueError('status debe ser 0 o 1')
    if 'imagen' in datos: imagen(datos['imagen'])

class UsuarioService:
    obtener_todos = staticmethod(UsuarioRepository.obtener_todos)
    obtener_por_id = staticmethod(UsuarioRepository.obtener_por_id)
    @staticmethod
    def actualizar_usuario(id_usuario, datos):
        validar_usuario(datos)
        if not UsuarioRepository.obtener_por_id(id_usuario): return False
        return UsuarioRepository.actualizar(id_usuario, datos)
