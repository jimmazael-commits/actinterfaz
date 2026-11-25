USE punto_venta;

SHOW PROCEDURE STATUS
WHERE Db = 'punto_venta';

CALL sp_usuarios_listar();

-- Usa un ID que exista en tu tabla.
CALL sp_usuario_por_id(1);