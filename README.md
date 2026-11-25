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

## 10. Referencia detallada de endpoints

Base URL local: `http://localhost:5000`.

Los endpoints de autenticación, usuarios y ventas devuelven un objeto con `status`, `message` y `data`. Los endpoints de productos y reportes devuelven directamente el objeto o arreglo de datos. Los errores JWT usan el formato de Flask-JWT-Extended (`msg`).

En las tablas, `—` indica que no aplica. Los endpoints `GET` no reciben cuerpo JSON.

### 10.1 Registrar usuario

**Resumen:** crea una cuenta de usuario. La contraseña se guarda como hash.  
**Método y ruta:** `POST /auth/registro`  
**Autorización:** no requiere token.

| Nombre | Ubicación | Tipo | Requerido | Descripción | Ejemplo |
|---|---|---|---|---|---|
| `Content-Type` | Header | string | Sí | Tipo del cuerpo | `application/json` |
| `nombre` | Body | string | Sí | Nombre, máximo 50 caracteres | `"Ana"` |
| `apellido` | Body | string | Sí | Apellido, máximo 50 caracteres | `"López"` |
| `correo_electronico` | Body | string | Sí | Correo único, máximo 100 caracteres | `"ana@example.com"` |
| `contrasena` | Body | string | Sí | Contraseña de hasta 72 bytes | `"ClaveSegura123"` |
| `fecha_nacimiento` | Body | string (date) | Sí | Formato `AAAA-MM-DD` | `"2002-05-15"` |
| `telefono` | Body | string | No | Máximo 20 caracteres | `"8112345678"` |
| `direccion` | Body | string | No | Máximo 255 caracteres | `"Monterrey"` |
| `nickname` | Body | string | No | Máximo 50 caracteres | `"ana"` |
| `imagen` | Body | string (Base64) o null | No | Imagen codificada en Base64 | `"/9j/4AAQ..."` |

**Request:**

```json
{
  "nombre": "Ana",
  "apellido": "López",
  "correo_electronico": "ana@example.com",
  "contrasena": "ClaveSegura123",
  "fecha_nacimiento": "2002-05-15",
  "telefono": "8112345678",
  "direccion": "Monterrey",
  "nickname": "ana"
}
```

**Responses:**

- `201 Created` — usuario registrado.

  ```json
  {
    "status": "success",
    "message": "Usuario registrado correctamente",
    "data": {
      "id_usuario": 12,
      "nombre": "Ana",
      "apellido": "López",
      "correo_electronico": "ana@example.com"
    }
  }
  ```

- `400 Bad Request` — campos faltantes o inválidos.

  ```json
  {
    "status": "error",
    "message": "Falta el campo nombre",
    "data": null
  }
  ```

- `409 Conflict` — el correo ya está registrado.

  ```json
  {
    "status": "error",
    "message": "El correo electrónico ya está registrado",
    "data": null
  }
  ```

- `500 Internal Server Error` — error de MySQL.

  ```json
  {
    "status": "error",
    "message": "Error de MySQL. Revisa la conexión y el esquema; consulta la consola.",
    "data": null
  }
  ```

**Errores y validaciones:** `fecha_nacimiento` debe ser una fecha válida; el correo debe incluir `@`; la contraseña admite hasta 72 bytes; el usuario no puede enviar `status` al registrarse. Si se envía imagen, debe ser Base64 válido y no exceder el límite del campo BLOB.

**cURL:**

```powershell
curl.exe -i -X POST "http://localhost:5000/auth/registro" -H "Content-Type: application/json" -d '{"nombre":"Ana","apellido":"López","correo_electronico":"ana@example.com","contrasena":"ClaveSegura123","fecha_nacimiento":"2002-05-15"}'
```

### 10.2 Iniciar sesión

**Resumen:** valida las credenciales y genera un token JWT.  
**Método y ruta:** `POST /auth/login`  
**Autorización:** no requiere token.

| Nombre | Ubicación | Tipo | Requerido | Descripción | Ejemplo |
|---|---|---|---|---|---|
| `Content-Type` | Header | string | Sí | Tipo del cuerpo | `application/json` |
| `correo_electronico` | Body | string | Sí | Correo registrado | `"ana@example.com"` |
| `contrasena` | Body | string | Sí | Contraseña de la cuenta | `"ClaveSegura123"` |

**Request:**

```json
{
  "correo_electronico": "ana@example.com",
  "contrasena": "ClaveSegura123"
}
```

**Responses:**

- `200 OK` — credenciales válidas.

  ```json
  {
    "status": "success",
    "message": "Inicio de sesión exitoso",
    "data": {
      "id_usuario": 12,
      "nombre": "Ana",
      "correo_electronico": "ana@example.com",
      "access_token": "<access_token>"
    }
  }
  ```

- `400 Bad Request` — falta un campo requerido.

  ```json
  {
    "status": "error",
    "message": "correo_electronico y contrasena son obligatorios",
    "data": null
  }
  ```

- `401 Unauthorized` — credenciales inválidas o cuenta inactiva.

  ```json
  {
    "status": "error",
    "message": "Credenciales inválidas",
    "data": null
  }
  ```

- `500 Internal Server Error` — error de MySQL; consulta el ejemplo de error `500` de la sección 10.1.

**Errores y validaciones:** ambos valores deben ser texto no vacío. La API no indica si falló el correo o la contraseña; responde con el mismo mensaje para credenciales inválidas.

**cURL:**

```powershell
curl.exe -i -X POST "http://localhost:5000/auth/login" -H "Content-Type: application/json" -d '{"correo_electronico":"ana@example.com","contrasena":"ClaveSegura123"}'
```

### 10.3 Listar usuarios

**Resumen:** devuelve los usuarios registrados sin incluir sus contraseñas.  
**Método y ruta:** `GET /usuarios`  
**Autorización:** requiere JWT.

| Nombre | Ubicación | Tipo | Requerido | Descripción | Ejemplo |
|---|---|---|---|---|---|
| `Authorization` | Header | string | Sí | Token Bearer obtenido en `/auth/login` | `Bearer <access_token>` |
| Parámetros | Path/Query | — | No | Este endpoint no recibe parámetros | — |
| Cuerpo | Body | — | No | No se envía JSON | — |

**Request:** no lleva cuerpo.

**Responses:**

- `200 OK` — lista de usuarios.

  ```json
  {
    "status": "success",
    "message": "Operación realizada correctamente",
    "data": [
      {
        "id_usuario": 12,
        "nombre": "Ana",
        "apellido": "López",
        "correo_electronico": "ana@example.com",
        "status": 1
      }
    ]
  }
  ```

- `401 Unauthorized` — token ausente, inválido o expirado.

  ```json
  {
    "msg": "Missing Authorization Header"
  }
  ```

- `500 Internal Server Error` — error al consultar MySQL; consulta el ejemplo de error `500` de la sección 10.1.

**Errores y validaciones:** incluye el token como `Authorization: Bearer <access_token>`. Los campos de imagen y fecha, cuando existen, se serializan como Base64 y formato ISO, respectivamente.

**cURL:**

```powershell
curl.exe -i "http://localhost:5000/usuarios" -H "Authorization: Bearer <access_token>"
```

### 10.4 Consultar usuario por ID

**Resumen:** devuelve un usuario específico sin exponer su contraseña.  
**Método y ruta:** `GET /usuarios/{id_usuario}`  
**Autorización:** requiere JWT.

| Nombre | Ubicación | Tipo | Requerido | Descripción | Ejemplo |
|---|---|---|---|---|---|
| `id_usuario` | Path | integer | Sí | Identificador del usuario | `12` |
| `Authorization` | Header | string | Sí | Token Bearer obtenido en `/auth/login` | `Bearer <access_token>` |
| Cuerpo | Body | — | No | No se envía JSON | — |

**Request:** `GET /usuarios/12`; no lleva cuerpo.

**Responses:**

- `200 OK` — usuario encontrado.

  ```json
  {
    "status": "success",
    "message": "Operación realizada correctamente",
    "data": {
      "id_usuario": 12,
      "nombre": "Ana",
      "apellido": "López",
      "correo_electronico": "ana@example.com",
      "status": 1
    }
  }
  ```

- `401 Unauthorized` — token ausente o inválido; usa el ejemplo de `401` de la sección 10.3.
- `404 Not Found` — no existe ese usuario.

  ```json
  {
    "status": "error",
    "message": "Usuario no encontrado",
    "data": null
  }
  ```

- `500 Internal Server Error` — error al consultar MySQL; consulta el ejemplo de error `500` de la sección 10.1.

**Errores y validaciones:** `id_usuario` debe ser un identificador entero reconocido por la ruta.

**cURL:**

```powershell
curl.exe -i "http://localhost:5000/usuarios/12" -H "Authorization: Bearer <access_token>"
```

### 10.5 Actualizar usuario

**Resumen:** modifica uno o más campos permitidos de un usuario.  
**Método y ruta:** `PUT /usuarios/{id_usuario}`  
**Autorización:** requiere JWT.

| Nombre | Ubicación | Tipo | Requerido | Descripción | Ejemplo |
|---|---|---|---|---|---|
| `id_usuario` | Path | integer | Sí | Identificador del usuario | `12` |
| `Authorization` | Header | string | Sí | Token Bearer obtenido en `/auth/login` | `Bearer <access_token>` |
| `nombre` | Body | string | No | Nombre, máximo 50 caracteres | `"Ana"` |
| `apellido` | Body | string | No | Apellido, máximo 50 caracteres | `"López"` |
| `correo_electronico` | Body | string | No | Correo, máximo 100 caracteres | `"ana@example.com"` |
| `telefono` | Body | string o null | No | Máximo 20 caracteres | `"8112345678"` |
| `direccion` | Body | string o null | No | Máximo 255 caracteres | `"Monterrey"` |
| `nickname` | Body | string o null | No | Máximo 50 caracteres | `"ana"` |
| `fecha_nacimiento` | Body | string (date) | No | Formato `AAAA-MM-DD` | `"2002-05-15"` |
| `imagen` | Body | string (Base64) o null | No | Imagen codificada en Base64 | `"/9j/4AAQ..."` |
| `status` | Body | integer | No | Estado: 0 o 1 | `1` |

**Request:**

```json
{
  "telefono": "8112345678",
  "direccion": "Monterrey"
}
```

**Responses:**

- `200 OK` — usuario actualizado.

  ```json
  {
    "status": "success",
    "message": "Usuario actualizado correctamente",
    "data": null
  }
  ```

- `400 Bad Request` — cuerpo vacío, campo desconocido o valor inválido.

  ```json
  {
    "status": "error",
    "message": "Campos vacíos o desconocidos en usuario",
    "data": null
  }
  ```

- `401 Unauthorized` — token ausente o inválido; usa el ejemplo de `401` de la sección 10.3.
- `404 Not Found` — el usuario no existe.

  ```json
  {
    "status": "error",
    "message": "Usuario no encontrado o sin cambios",
    "data": null
  }
  ```

- `500 Internal Server Error` — error de MySQL; consulta el ejemplo de error `500` de la sección 10.1.

**Errores y validaciones:** no se puede actualizar `contrasena` mediante este endpoint. El correo debe incluir `@`, la fecha debe ser ISO y `status` debe ser 0 o 1. Envía al menos un campo permitido.

**cURL:**

```powershell
curl.exe -i -X PUT "http://localhost:5000/usuarios/12" -H "Authorization: Bearer <access_token>" -H "Content-Type: application/json" -d '{"telefono":"8112345678","direccion":"Monterrey"}'
```

### 10.6 Listar productos

**Resumen:** devuelve los productos registrados.  
**Método y ruta:** `GET /productos`  
**Autorización:** no requiere token.

| Nombre | Ubicación | Tipo | Requerido | Descripción | Ejemplo |
|---|---|---|---|---|---|
| Parámetros | Path/Query | — | No | Este endpoint no recibe parámetros | — |
| Cuerpo | Body | — | No | No se envía JSON | — |

**Request:** no lleva cuerpo.

**Responses:**

- `200 OK` — arreglo de productos.

  ```json
  [
    {
      "id_producto": 1,
      "codigo": "PROD-001",
      "descripcion": "Producto de ejemplo",
      "precio": "25.50",
      "existencias": 20,
      "estatus": "activo",
      "unidades": "pieza",
      "imagen": null,
      "status": 1
    }
  ]
  ```

- `500 Internal Server Error` — error al consultar MySQL; consulta el ejemplo de error `500` de la sección 10.1.

**Errores y validaciones:** los precios se serializan como texto decimal y las imágenes, si existen, como Base64.

**cURL:**

```powershell
curl.exe -i "http://localhost:5000/productos"
```

### 10.7 Consultar producto por ID

**Resumen:** devuelve un producto específico.  
**Método y ruta:** `GET /productos/{id_producto}`  
**Autorización:** no requiere token.

| Nombre | Ubicación | Tipo | Requerido | Descripción | Ejemplo |
|---|---|---|---|---|---|
| `id_producto` | Path | integer | Sí | Identificador del producto | `1` |
| Cuerpo | Body | — | No | No se envía JSON | — |

**Request:** `GET /productos/1`; no lleva cuerpo.

**Responses:**

- `200 OK` — objeto del producto. El formato es el mismo que un elemento del arreglo de la sección 10.6.
- `404 Not Found` — no existe ese producto.

  ```json
  {
    "message": "Producto no encontrado"
  }
  ```

- `500 Internal Server Error` — error al consultar MySQL; consulta el ejemplo de error `500` de la sección 10.1.

**Errores y validaciones:** el identificador debe corresponder a un producto existente.

**cURL:**

```powershell
curl.exe -i "http://localhost:5000/productos/1"
```

### 10.8 Registrar producto

**Resumen:** registra un producto nuevo.  
**Método y ruta:** `POST /productos`  
**Autorización:** requiere JWT.

| Nombre | Ubicación | Tipo | Requerido | Descripción | Ejemplo |
|---|---|---|---|---|---|
| `Authorization` | Header | string | Sí | Token Bearer obtenido en `/auth/login` | `Bearer <access_token>` |
| `Content-Type` | Header | string | Sí | Tipo del cuerpo | `application/json` |
| `codigo` | Body | string | Sí | Código único, máximo 50 caracteres | `"PROD-001"` |
| `descripcion` | Body | string | Sí | Descripción, máximo 255 caracteres | `"Producto de ejemplo"` |
| `precio` | Body | number | Sí | Precio no negativo, máximo dos decimales | `25.50` |
| `existencias` | Body | integer | Sí | Existencias no negativas | `20` |
| `estatus` | Body | string | Sí | Estatus, máximo 20 caracteres | `"activo"` |
| `unidades` | Body | string | Sí | Unidad, máximo 20 caracteres | `"pieza"` |
| `imagen` | Body | string (Base64) o null | No | Imagen del producto | `"/9j/4AAQ..."` |
| `status` | Body | integer | No | Estado: 0 o 1; por defecto 1 | `1` |

**Request:**

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

**Responses:**

- `201 Created` — producto creado. El cuerpo es el objeto del producto, como en la sección 10.6.
- `400 Bad Request` — datos faltantes o inválidos.

  ```json
  {
    "status": "error",
    "message": "precio debe tener máximo dos decimales y estar entre 0 y 99999999.99",
    "data": null
  }
  ```

- `401 Unauthorized` — token ausente o inválido; usa el ejemplo de `401` de la sección 10.3.
- `409 Conflict` — el código del producto ya existe.

  ```json
  {
    "status": "error",
    "message": "Registro duplicado",
    "data": null
  }
  ```

- `500 Internal Server Error` — error de MySQL; consulta el ejemplo de error `500` de la sección 10.1.

**Errores y validaciones:** las cadenas requeridas no deben estar vacías. `precio` acepta hasta dos decimales; `existencias` debe ser entero no negativo; `status` debe ser 0 o 1. La imagen Base64 debe ser válida y no superar 65 535 bytes.

**cURL:**

```powershell
curl.exe -i -X POST "http://localhost:5000/productos" -H "Authorization: Bearer <access_token>" -H "Content-Type: application/json" -d '{"codigo":"PROD-001","descripcion":"Producto de ejemplo","precio":25.5,"existencias":20,"estatus":"activo","unidades":"pieza"}'
```

### 10.9 Actualizar producto

**Resumen:** actualiza uno o más campos de un producto existente.  
**Método y ruta:** `PUT /productos/{id_producto}`  
**Autorización:** requiere JWT.

| Nombre | Ubicación | Tipo | Requerido | Descripción | Ejemplo |
|---|---|---|---|---|---|
| `id_producto` | Path | integer | Sí | Identificador del producto | `1` |
| `Authorization` | Header | string | Sí | Token Bearer obtenido en `/auth/login` | `Bearer <access_token>` |
| `codigo` | Body | string | No | Código único, máximo 50 caracteres | `"PROD-001"` |
| `descripcion` | Body | string | No | Descripción, máximo 255 caracteres | `"Producto actualizado"` |
| `precio` | Body | number | No | Precio no negativo, máximo dos decimales | `27.00` |
| `existencias` | Body | integer | No | Existencias no negativas | `18` |
| `estatus` | Body | string | No | Estatus, máximo 20 caracteres | `"activo"` |
| `unidades` | Body | string | No | Unidad, máximo 20 caracteres | `"pieza"` |
| `imagen` | Body | string (Base64) o null | No | Imagen del producto | `null` |
| `status` | Body | integer | No | Estado: 0 o 1 | `1` |

**Request:**

```json
{
  "precio": 27.0,
  "existencias": 18
}
```

**Responses:**

- `200 OK` — producto actualizado; devuelve el producto actualizado.
- `400 Bad Request` — cuerpo vacío o campos inválidos.

  ```json
  {
    "status": "error",
    "message": "Debes enviar un objeto JSON con datos del producto",
    "data": null
  }
  ```

- `401 Unauthorized` — token ausente o inválido; usa el ejemplo de `401` de la sección 10.3.
- `404 Not Found` — no existe el producto.

  ```json
  {
    "message": "Producto no encontrado"
  }
  ```

- `409 Conflict` — el nuevo código ya pertenece a otro producto; usa el ejemplo de `409` de la sección 10.8.
- `500 Internal Server Error` — error de MySQL; consulta el ejemplo de error `500` de la sección 10.1.

**Errores y validaciones:** envía al menos un campo permitido. Los límites y formatos son los mismos que para registrar un producto.

**cURL:**

```powershell
curl.exe -i -X PUT "http://localhost:5000/productos/1" -H "Authorization: Bearer <access_token>" -H "Content-Type: application/json" -d '{"precio":27.0,"existencias":18}'
```

### 10.10 Registrar venta

**Resumen:** registra una venta, sus detalles y descuenta existencias. El precio se toma del producto en la base de datos.  
**Método y ruta:** `POST /ventas`  
**Autorización:** requiere JWT.

| Nombre | Ubicación | Tipo | Requerido | Descripción | Ejemplo |
|---|---|---|---|---|---|
| `Authorization` | Header | string | Sí | Token Bearer; determina el usuario de la venta | `Bearer <access_token>` |
| `Content-Type` | Header | string | Sí | Tipo del cuerpo | `application/json` |
| `id_caja` | Body | integer | Sí | ID de una caja existente | `1` |
| `productos` | Body | array | Sí | Lista no vacía de productos | `[{"id_producto":1,"cantidad":2}]` |
| `productos[].id_producto` | Body | integer | Sí | ID de producto existente y activo | `1` |
| `productos[].cantidad` | Body | integer | Sí | Cantidad mayor que cero y con existencias | `2` |
| `id_usuario` | Body | integer | No | Si se envía, debe coincidir con el token | `12` |

**Request:**

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

**Responses:**

- `201 Created` — venta registrada.

  ```json
  {
    "status": "success",
    "message": "Venta registrada correctamente",
    "data": {
      "id_venta": 25,
      "folio": "V-AB12CD34EF56GH78IJ",
      "total": "51.00"
    }
  }
  ```

- `400 Bad Request` — caja o producto inexistente, lista inválida, producto repetido o existencias insuficientes.

  ```json
  {
    "status": "error",
    "message": "Existencias insuficientes",
    "data": null
  }
  ```

- `401 Unauthorized` — token ausente o inválido; usa el ejemplo de `401` de la sección 10.3.
- `500 Internal Server Error` — error de MySQL; consulta el ejemplo de error `500` de la sección 10.1.

**Errores y validaciones:** `id_caja`, `id_producto` y `cantidad` deben ser enteros positivos. La lista `productos` debe tener al menos un elemento y no puede repetir IDs. Un producto dado de baja o sin existencias no se puede vender. `id_usuario` se obtiene del JWT.

**cURL:**

```powershell
curl.exe -i -X POST "http://localhost:5000/ventas" -H "Authorization: Bearer <access_token>" -H "Content-Type: application/json" -d '{"id_caja":1,"productos":[{"id_producto":1,"cantidad":2}]}'
```

### 10.11 Reporte de ventas por caja

**Resumen:** agrupa ventas por número de caja y calcula el total y la cantidad de tickets.  
**Método y ruta:** `GET /reportes/ventas-por-caja`  
**Autorización:** requiere JWT.

| Nombre | Ubicación | Tipo | Requerido | Descripción | Ejemplo |
|---|---|---|---|---|---|
| `Authorization` | Header | string | Sí | Token Bearer obtenido en `/auth/login` | `Bearer <access_token>` |
| Parámetros | Path/Query | — | No | Este endpoint no recibe parámetros | — |
| Cuerpo | Body | — | No | No se envía JSON | — |

**Request:** no lleva cuerpo.

**Responses:**

- `200 OK` — arreglo de resultados.

  ```json
  [
    {
      "numero_caja": 1,
      "total_ventas": "150.00",
      "cantidad_tickets": 3
    }
  ]
  ```

- `401 Unauthorized` — token ausente o inválido; usa el ejemplo de `401` de la sección 10.3.
- `500 Internal Server Error` — error al consultar MySQL; consulta el ejemplo de error `500` de la sección 10.1.

**Errores y validaciones:** no recibe filtros ni parámetros. Si no existen ventas, devuelve un arreglo vacío.

**cURL:**

```powershell
curl.exe -i "http://localhost:5000/reportes/ventas-por-caja" -H "Authorization: Bearer <access_token>"
```

### 10.12 Reporte de ventas por producto

**Resumen:** agrupa ventas por producto y calcula la cantidad vendida y el total generado.  
**Método y ruta:** `GET /reportes/ventas-por-producto`  
**Autorización:** requiere JWT.

| Nombre | Ubicación | Tipo | Requerido | Descripción | Ejemplo |
|---|---|---|---|---|---|
| `Authorization` | Header | string | Sí | Token Bearer obtenido en `/auth/login` | `Bearer <access_token>` |
| Parámetros | Path/Query | — | No | Este endpoint no recibe parámetros | — |
| Cuerpo | Body | — | No | No se envía JSON | — |

**Request:** no lleva cuerpo.

**Responses:**

- `200 OK` — arreglo de resultados.

  ```json
  [
    {
      "id_producto": 1,
      "descripcion": "Producto de ejemplo",
      "cantidad_vendida": 6,
      "total_generado": "150.00"
    }
  ]
  ```

- `401 Unauthorized` — token ausente o inválido; usa el ejemplo de `401` de la sección 10.3.
- `500 Internal Server Error` — error al consultar MySQL; consulta el ejemplo de error `500` de la sección 10.1.

**Errores y validaciones:** no recibe filtros ni parámetros. Si no existen ventas, devuelve un arreglo vacío.

**cURL:**

```powershell
curl.exe -i "http://localhost:5000/reportes/ventas-por-producto" -H "Authorization: Bearer <access_token>"
```

## 11. Errores generales

| Código | Significado | Ejemplo de respuesta |
|---|---|---|
| `400` | JSON, parámetros o valores inválidos; también datos incompatibles con la base | `{"status":"error","message":"<detalle>","data":null}` |
| `401` | Falta un token válido en una ruta protegida | `{"msg":"Missing Authorization Header"}` |
| `404` | No existe el recurso solicitado o la ruta no existe | El cuerpo depende del endpoint; revisa la respuesta de esa ruta |
| `409` | Conflicto por un valor único duplicado, como correo o código de producto | `{"status":"error","message":"Registro duplicado","data":null}` |
| `500` | Error de MySQL o del servidor | `{"status":"error","message":"Error de MySQL. Revisa la conexión y el esquema; consulta la consola.","data":null}` |

## 12. Pruebas con Postman

1. Inicia la API y configura `http://localhost:5000` como base URL.
2. Ejecuta `POST /auth/registro` para crear un usuario.
3. Ejecuta `POST /auth/login` y copia `data.access_token`.
4. En las peticiones protegidas, selecciona **Authorization > Bearer Token** y pega el token.
5. Prueba las rutas de usuarios, productos, ventas y reportes con los ejemplos de esta documentación.

## 13. Change log

| Fecha | Cambio |
|---|---|
| 2026-11-24 | Se documentaron los endpoints, sus parámetros, ejemplos y respuestas principales. |
