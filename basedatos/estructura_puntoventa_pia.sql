-- Crear base de datos
CREATE DATABASE punto_venta;

USE punto_venta;

-- Tabla de usuarios
CREATE TABLE usuarios (
    id_usuario INT NOT NULL AUTO_INCREMENT,
    nombre VARCHAR(50) NOT NULL,
    apellido VARCHAR(50) NOT NULL,
    correo_electronico VARCHAR(100) NOT NULL,
    contrasena VARCHAR(255) NOT NULL,
    telefono VARCHAR(20),
    direccion VARCHAR(255),
    imagen BLOB,
    nickname VARCHAR(50),
    fecha_nacimiento DATE NOT NULL,
    status BIT NOT NULL DEFAULT 1,
    PRIMARY KEY (id_usuario),
    UNIQUE (correo_electronico)
);

-- Tabla de cajas
CREATE TABLE cajas (
    id_caja INT NOT NULL AUTO_INCREMENT,
    numero_caja INT NOT NULL,
    estatus VARCHAR(20) NOT NULL,
    PRIMARY KEY (id_caja),
    UNIQUE (numero_caja)
);

-- Tabla de productos
CREATE TABLE productos (
    id_producto INT NOT NULL AUTO_INCREMENT,
    codigo VARCHAR(50) NOT NULL,
    descripcion VARCHAR(255) NOT NULL,
    precio DECIMAL(10,2) NOT NULL,
    existencias INT NOT NULL,
    estatus VARCHAR(20) NOT NULL,
    unidades VARCHAR(20) NOT NULL,
    imagen BLOB,
    status BIT NOT NULL DEFAULT 1,
    PRIMARY KEY (id_producto),
    UNIQUE (codigo)
);

-- Tabla de ventas
CREATE TABLE ventas (
    id_venta INT NOT NULL AUTO_INCREMENT,
    folio VARCHAR(20) NOT NULL,
    id_usuario INT NOT NULL,
    id_caja INT NOT NULL,
    fecha_venta DATETIME NOT NULL,
    total DECIMAL(10,2) NOT NULL,
    PRIMARY KEY (id_venta),
    UNIQUE (folio),
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id_usuario),
    FOREIGN KEY (id_caja) REFERENCES cajas(id_caja)
);

-- Detalle de los productos vendidos
CREATE TABLE detalle_venta (
    id_detalle INT NOT NULL AUTO_INCREMENT,
    id_venta INT NOT NULL,
    id_producto INT NOT NULL,
    cantidad INT NOT NULL,
    precio_unitario DECIMAL(10,2) NOT NULL,
    importe DECIMAL(10,2) NOT NULL,
    PRIMARY KEY (id_detalle),
    FOREIGN KEY (id_venta) REFERENCES ventas(id_venta),
    FOREIGN KEY (id_producto) REFERENCES productos(id_producto),
    UNIQUE (id_venta, id_producto)
);