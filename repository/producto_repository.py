from DB import Database
from utils import serializar, imagen

class Productorepository:
    @staticmethod
    def obtener_productos():
        return Productorepository.consultar()
    @staticmethod
    def obtener_producto(id_producto):
        filas = Productorepository.consultar(id_producto)
        return filas[0] if filas else None
    @staticmethod
    def consultar(id_producto=None):
        conn = Database().connect()
        try:
            with conn.cursor(dictionary=True) as cur:
                cur.execute('SELECT * FROM productos' + (' WHERE id_producto = %s' if id_producto is not None else ''), (id_producto,) if id_producto is not None else ())
                return [serializar(r) for r in cur.fetchall()]
        finally: conn.close()
    @staticmethod
    def guardar(datos, id_producto=None):
        campos = list(datos)
        valores = [imagen(datos[k]) if k == 'imagen' else datos[k] for k in campos]
        conn = Database().connect()
        try:
            with conn.cursor() as cur:
                if id_producto is None:
                    cur.execute(f"INSERT INTO productos ({', '.join(campos)}) VALUES ({', '.join(['%s']*len(campos))})", valores)
                    id_producto = cur.lastrowid
                else:
                    cur.execute(f"UPDATE productos SET {', '.join(k+' = %s' for k in campos)} WHERE id_producto = %s", valores+[id_producto])
            conn.commit()
            return id_producto
        except Exception:
            conn.rollback()
            raise
        finally: conn.close()
from DB import Database
from utils import serializar, imagen


class Productorepository:

    @staticmethod
    def obtener_productos():
        return Productorepository.consultar()

    @staticmethod
    def obtener_producto(id_producto):
        filas = Productorepository.consultar(id_producto)
        return filas[0] if filas else None

    @staticmethod
    def consultar(id_producto=None):
        conn = Database().connect()

        try:
            with conn.cursor(dictionary=True) as cur:
                sql = """
                    SELECT id_producto, codigo, descripcion, precio,
                           existencias, estatus, unidades, imagen, status
                    FROM productos
                """

                parametros = ()

                if id_producto is not None:
                    sql += " WHERE id_producto = %s"
                    parametros = (id_producto,)

                cur.execute(sql, parametros)

                return [
                    serializar(fila)
                    for fila in cur.fetchall()
                ]

        finally:
            conn.close()

    @staticmethod
    def guardar(datos, id_producto=None):
        # Los campos recibidos ya fueron validados por el servicio.
        campos = list(datos)

        valores = [
            imagen(datos[campo])
            if campo == "imagen"
            else datos[campo]
            for campo in campos
        ]

        conn = Database().connect()

        try:
            with conn.cursor() as cur:
                if id_producto is None:
                    columnas = ", ".join(campos)
                    marcadores = ", ".join(["%s"] * len(campos))

                    sql = f"""
                        INSERT INTO productos ({columnas})
                        VALUES ({marcadores})
                    """

                    cur.execute(sql, valores)
                    id_producto = cur.lastrowid

                else:
                    asignaciones = ", ".join(
                        f"{campo} = %s"
                        for campo in campos
                    )

                    sql = f"""
                        UPDATE productos
                        SET {asignaciones}
                        WHERE id_producto = %s
                    """

                    cur.execute(
                        sql,
                        valores + [id_producto]
                    )

            conn.commit()
            return id_producto

        except Exception:
            conn.rollback()
            raise

        finally:
            conn.close()
            