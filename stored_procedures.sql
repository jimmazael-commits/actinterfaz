USE punto_venta;

DELIMITER $$

-- USUARIOS

DROP PROCEDURE IF EXISTS sp_usuario_por_correo$$
CREATE PROCEDURE sp_usuario_por_correo(
    IN p_correo VARCHAR(100)
)
BEGIN
    -- Incluye el hash para que AuthService pueda validar el login.
    SELECT *
    FROM usuarios
    WHERE correo_electronico = p_correo;
END$$


DROP PROCEDURE IF EXISTS sp_usuario_por_id$$
CREATE PROCEDURE sp_usuario_por_id(
    IN p_id_usuario INT
)
BEGIN
    SELECT id_usuario, nombre, apellido, correo_electronico,
           telefono, direccion, nickname, fecha_nacimiento,
           status, imagen
    FROM usuarios
    WHERE id_usuario = p_id_usuario;
END$$


DROP PROCEDURE IF EXISTS sp_usuarios_listar$$
CREATE PROCEDURE sp_usuarios_listar()
BEGIN
    SELECT id_usuario, nombre, apellido, correo_electronico,
           telefono, direccion, nickname, fecha_nacimiento,
           status, imagen
    FROM usuarios;
END$$


DROP PROCEDURE IF EXISTS sp_usuario_crear$$
CREATE PROCEDURE sp_usuario_crear(
    IN p_nombre VARCHAR(50),
    IN p_apellido VARCHAR(50),
    IN p_correo VARCHAR(100),
    IN p_contrasena VARCHAR(255),
    IN p_telefono VARCHAR(20),
    IN p_direccion VARCHAR(255),
    IN p_nickname VARCHAR(50),
    IN p_fecha_nacimiento DATE,
    IN p_imagen BLOB
)
BEGIN
    INSERT INTO usuarios (
        nombre, apellido, correo_electronico, contrasena,
        telefono, direccion, nickname, fecha_nacimiento, imagen
    )
    VALUES (
        p_nombre, p_apellido, p_correo, p_contrasena,
        p_telefono, p_direccion, p_nickname,
        p_fecha_nacimiento, p_imagen
    );

    SELECT LAST_INSERT_ID() AS id_usuario;
END$$


-- Actualiza un campo por llamada.
-- Repository ejecutará todas las llamadas dentro de una transacción.
DROP PROCEDURE IF EXISTS sp_usuario_actualizar_campo$$
CREATE PROCEDURE sp_usuario_actualizar_campo(
    IN p_id_usuario INT,
    IN p_campo VARCHAR(50),
    IN p_valor BLOB
)
BEGIN
    CASE p_campo
        WHEN 'nombre' THEN
            UPDATE usuarios SET nombre = p_valor
            WHERE id_usuario = p_id_usuario;

        WHEN 'apellido' THEN
            UPDATE usuarios SET apellido = p_valor
            WHERE id_usuario = p_id_usuario;

        WHEN 'correo_electronico' THEN
            UPDATE usuarios SET correo_electronico = p_valor
            WHERE id_usuario = p_id_usuario;

        WHEN 'telefono' THEN
            UPDATE usuarios SET telefono = p_valor
            WHERE id_usuario = p_id_usuario;

        WHEN 'direccion' THEN
            UPDATE usuarios SET direccion = p_valor
            WHERE id_usuario = p_id_usuario;

        WHEN 'nickname' THEN
            UPDATE usuarios SET nickname = p_valor
            WHERE id_usuario = p_id_usuario;

        WHEN 'fecha_nacimiento' THEN
            UPDATE usuarios
            SET fecha_nacimiento = CAST(p_valor AS DATE)
            WHERE id_usuario = p_id_usuario;

        WHEN 'imagen' THEN
            UPDATE usuarios SET imagen = p_valor
            WHERE id_usuario = p_id_usuario;

        WHEN 'status' THEN
            IF p_valor IS NULL
               OR CAST(p_valor AS CHAR) NOT IN ('0', '1') THEN
                SIGNAL SQLSTATE '45000'
                SET MESSAGE_TEXT = 'status debe ser 0 o 1';
            END IF;

            UPDATE usuarios
            SET status = CAST(p_valor AS UNSIGNED)
            WHERE id_usuario = p_id_usuario;

        ELSE
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Campo de usuario no permitido';
    END CASE;
END$$


-- VENTAS

DROP PROCEDURE IF EXISTS sp_venta_validar_usuario$$
CREATE PROCEDURE sp_venta_validar_usuario(
    IN p_id_usuario INT
)
BEGIN
    SELECT status
    FROM usuarios
    WHERE id_usuario = p_id_usuario
    FOR UPDATE;
END$$


DROP PROCEDURE IF EXISTS sp_venta_validar_caja$$
CREATE PROCEDURE sp_venta_validar_caja(
    IN p_id_caja INT
)
BEGIN
    SELECT id_caja
    FROM cajas
    WHERE id_caja = p_id_caja
    FOR UPDATE;
END$$


DROP PROCEDURE IF EXISTS sp_venta_obtener_producto$$
CREATE PROCEDURE sp_venta_obtener_producto(
    IN p_id_producto INT
)
BEGIN
    SELECT id_producto, precio, existencias, status
    FROM productos
    WHERE id_producto = p_id_producto
    FOR UPDATE;
END$$


DROP PROCEDURE IF EXISTS sp_venta_crear$$
CREATE PROCEDURE sp_venta_crear(
    IN p_folio VARCHAR(20),
    IN p_id_usuario INT,
    IN p_id_caja INT,
    IN p_total DECIMAL(10,2)
)
BEGIN
    INSERT INTO ventas (
        folio, id_usuario, id_caja, fecha_venta, total
    )
    VALUES (
        p_folio, p_id_usuario, p_id_caja, NOW(), p_total
    );

    SELECT LAST_INSERT_ID() AS id_venta;
END$$


DROP PROCEDURE IF EXISTS sp_venta_agregar_detalle$$
CREATE PROCEDURE sp_venta_agregar_detalle(
    IN p_id_venta INT,
    IN p_id_producto INT,
    IN p_cantidad INT,
    IN p_precio_unitario DECIMAL(10,2),
    IN p_importe DECIMAL(10,2)
)
BEGIN
    -- Solo descuenta si el producto sigue activo y hay existencias.
    UPDATE productos
    SET existencias = existencias - p_cantidad
    WHERE id_producto = p_id_producto
      AND status = 1
      AND p_cantidad > 0
      AND existencias >= p_cantidad;

    IF ROW_COUNT() <> 1 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT =
            'Producto inexistente, inactivo o sin existencias suficientes';
    END IF;

    INSERT INTO detalle_venta (
        id_venta, id_producto, cantidad, precio_unitario, importe
    )
    VALUES (
        p_id_venta, p_id_producto, p_cantidad,
        p_precio_unitario, p_importe
    );
END$$

DELIMITER ;