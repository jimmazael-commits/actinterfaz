# API REST de Punto de Venta

## Datos del proyecto

- **Universidad:** Universidad Autónoma de Nuevo León
- **Facultad:** Facultad de Ciencias Físico Matemáticas
- **Materia:** Interfaz de programación de aplicaciones
- **Profesor:** Juan Alejandro Villarreal Mojica
- **Alumno:** Jaime Azael Garcia Lopez
- **Grupo:** 51
- **Avance:** 3er avance

## 1. Descripción

API REST para la administración de un punto de venta, desarrollada con Python, Flask y MySQL. Permite registrar usuarios, iniciar sesión con autenticación JWT, administrar productos, registrar ventas y consultar reportes.

Las contraseñas de los usuarios se almacenan mediante hash. Las operaciones de ventas y consultas de usuarios requieren autenticación.

## 2. Tecnologías

- **Python** y **Flask** para la API.
- **MySQL** para almacenar la información.
- **Flask-JWT-Extended** para autenticación mediante tokens JWT.
- **mysql-connector-python** para la conexión con MySQL.
- **bcrypt** para proteger las contraseñas.
- **Postman** (opcional) para probar los endpoints.

## 3. Requisitos

- Python 3.9 o superior.
- MySQL Server.
- `pip`.

## 4. Instalación y configuración

Desde PowerShell, en la carpeta del proyecto:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

### Base de datos

En MySQL Workbench, ejecuta los scripts en este orden:

1. `estructura_puntoventa_pia.sql`: crea la base `punto_venta` y sus tablas.
2. `stored_procedures.sql`: instala los procedimientos almacenados utilizados por la aplicación.

Para registrar ventas debe existir al menos una caja en la tabla `cajas`. Por ejemplo:

```sql
USE punto_venta;
INSERT INTO cajas (numero_caja, estatus) VALUES (1, 'activa');
```

### Variables de entorno

La aplicación lee la configuración de MySQL desde `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD` y `DB_NAME`. También puedes definir `JWT_SECRET_KEY` para mantener una clave JWT estable entre reinicios. Configúralas en PowerShell antes de iniciar la API:

```powershell
$env:DB_HOST = "localhost"
$env:DB_PORT = "3306"
$env:DB_USER = "tu_usuario_mysql"
$env:DB_PASSWORD = "tu_contrasena_mysql"
$env:DB_NAME = "punto_venta"
$env:JWT_SECRET_KEY = "reemplaza_por_una_clave_secreta"
```

No publiques contraseñas ni claves secretas en el repositorio. La aplicación lee variables de entorno; no carga automáticamente un archivo `.env`.

## 5. Ejecución

Con el entorno virtual activado y las variables configuradas:

```powershell
python api.py
```

La API queda disponible en `http://localhost:5000`.

## 6. Autenticación

Los endpoints protegidos requieren el token obtenido al iniciar sesión. En Postman, envíalo en el encabezado:

```text
Authorization: Bearer <access_token>
```

### Registro

`POST /auth/registro` — no requiere token.

```json
{
  "nombre": "Ana",
  "apellido": "López",
  "correo_electronico": "ana@example.com",
  "contrasena": "una-clave-segura",
  "fecha_nacimiento": "2002-05-15",
  "telefono": "8112345678",
  "direccion": "Monterrey",
  "nickname": "ana",
  "imagen": "<imagen en Base64, opcional>"
}
```

`fecha_nacimiento` debe tener formato `AAAA-MM-DD`. La imagen, si se envía, debe estar codificada en Base64.

### Inicio de sesión

`POST /auth/login` — no requiere token.

```json
{
  "correo_electronico": "ana@example.com",
  "contrasena": "una-clave-segura"
}
```

La respuesta exitosa incluye `access_token`.

## 7. Endpoints

| Método | Ruta | Función | Autenticación |
|---|---|---|---|
| `POST` | `/auth/registro` | Registrar un usuario | No |
| `POST` | `/auth/login` | Iniciar sesión y obtener JWT | No |
| `GET` | `/usuarios` | Listar usuarios | Sí |
| `GET` | `/usuarios/{id_usuario}` | Consultar un usuario | Sí |
| `PUT` | `/usuarios/{id_usuario}` | Actualizar campos de un usuario | Sí |
| `GET` | `/productos` | Listar productos | No |
| `GET` | `/productos/{id_producto}` | Consultar un producto | No |
| `POST` | `/productos` | Registrar un producto | Sí |
| `PUT` | `/productos/{id_producto}` | Actualizar campos de un producto | Sí |
| `POST` | `/ventas` | Registrar una venta | Sí |
| `GET` | `/reportes/ventas-por-caja` | Consultar ventas agrupadas por caja | Sí |
| `GET` | `/reportes/ventas-por-producto` | Consultar ventas agrupadas por producto | Sí |

### Productos

Para `POST /productos`, los campos obligatorios son `codigo`, `descripcion`, `precio`, `existencias`, `estatus` y `unidades`. `imagen` (Base64) y `status` (0 o 1) son opcionales.

```json
{
  "codigo": "PROD-001",
  "descripcion": "Producto de ejemplo",
  "precio": 25.5,
  "existencias": 20,
  "estatus": "activo",
  "unidades": "pieza"
}
```

En `PUT /productos/{id_producto}` envía únicamente los campos que quieras modificar.

### Usuarios

En `PUT /usuarios/{id_usuario}` se pueden actualizar campos como `nombre`, `apellido`, `correo_electronico`, `telefono`, `direccion`, `nickname`, `fecha_nacimiento`, `imagen` y `status`. La contraseña no se modifica mediante este endpoint.

### Ventas

`POST /ventas` recibe una caja y una lista de productos. El usuario se obtiene del token; si se incluye `id_usuario` en el cuerpo, debe coincidir con el token.

```json
{
  "id_caja": 1,
  "productos": [
    {
      "id_producto": 1,
      "cantidad": 2
    }
  ]
}
```

No repitas un producto en la lista: suma sus cantidades en un solo elemento. El precio y el total de la venta se calculan en el servidor.

### Reportes

- `GET /reportes/ventas-por-caja`: devuelve `numero_caja`, `total_ventas` y `cantidad_tickets`.
- `GET /reportes/ventas-por-producto`: devuelve `id_producto`, `descripcion`, `cantidad_vendida` y `total_generado`.

## 8. Base de datos

La base de datos `punto_venta` contiene estas tablas:

- **`usuarios`**: datos personales, correo, contraseña con hash, imagen y estado.
- **`cajas`**: número y estado de cada caja.
- **`productos`**: código, descripción, precio, existencias, unidades, imagen y estado.
- **`ventas`**: folio, usuario, caja, fecha y total.
- **`detalle_venta`**: productos, cantidades, precios e importes de cada venta.

Las consultas y operaciones de productos, usuarios, ventas y reportes utilizan procedimientos almacenados definidos en `stored_procedures.sql`.

## 9. Estructura del proyecto

```text
actinterfaz/
├── controllers/       # Rutas y manejo de peticiones HTTP
├── models/            # Modelos de datos
├── repository/        # Acceso a datos y procedimientos almacenados
├── services/          # Validaciones y lógica de negocio
├── api.py             # Creación y ejecución de la API Flask
├── config.py          # Configuración de conexión a MySQL
├── DB.py              # Conexión con la base de datos
├── utils.py           # Validación y serialización de datos
├── estructura_puntoventa_pia.sql
├── stored_procedures.sql
└── requirements.txt
```