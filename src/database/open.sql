-- ==========================================
-- BASE DE DATOS PARA APP DE EMPRENDEDORES
-- Proyecto: OpenMarket
-- ==========================================

CREATE DATABASE IF NOT EXISTS openmarket;
USE openmarket;

-- ==========================================
-- TABLA DE USUARIOS
-- ==========================================
CREATE TABLE usuarios (
    id_usuario INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    correo VARCHAR(150) UNIQUE NOT NULL,
    contraseña VARCHAR(255) NOT NULL,
    telefono VARCHAR(20),
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ==========================================
-- TABLA DE CLIENTES
-- ==========================================
CREATE TABLE clientes (
    id_cliente INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    telefono VARCHAR(20),
    correo VARCHAR(150),
    direccion TEXT,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ==========================================
-- TABLA DE PROVEEDORES
-- ==========================================
CREATE TABLE proveedores (
    id_proveedor INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    correo VARCHAR(150),
    telefono VARCHAR(20),
    producto_que_vende VARCHAR(150),
    direccion TEXT,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ==========================================
-- TABLA DE PRODUCTOS
-- ==========================================
CREATE TABLE productos (
    id_producto INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    precio DECIMAL(10,2) NOT NULL,
    stock INT DEFAULT 0,
    categoria VARCHAR(100),
    id_proveedor INT,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (id_proveedor)
        REFERENCES proveedores(id_proveedor)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);

-- ==========================================
-- TABLA DE VENTAS
-- ==========================================
CREATE TABLE ventas (
    id_venta INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT,
    id_usuario INT,
    total DECIMAL(10,2) NOT NULL,
    metodo_pago VARCHAR(50),
    fecha_venta TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (id_cliente)
        REFERENCES clientes(id_cliente)
        ON DELETE SET NULL
        ON UPDATE CASCADE,

    FOREIGN KEY (id_usuario)
        REFERENCES usuarios(id_usuario)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);

-- ==========================================
-- DETALLE DE VENTAS
-- ==========================================
CREATE TABLE detalle_ventas (
    id_detalle INT AUTO_INCREMENT PRIMARY KEY,
    id_venta INT NOT NULL,
    id_producto INT NOT NULL,
    cantidad INT NOT NULL,
    precio_unitario DECIMAL(10,2) NOT NULL,
    subtotal DECIMAL(10,2) NOT NULL,

    FOREIGN KEY (id_venta)
        REFERENCES ventas(id_venta)
        ON DELETE CASCADE
        ON UPDATE CASCADE,

    FOREIGN KEY (id_producto)
        REFERENCES productos(id_producto)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

-- ==========================================
-- TABLA DE PEDIDOS
-- ==========================================
CREATE TABLE pedidos (
    id_pedido INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT,
    estado ENUM('Pendiente', 'En proceso', 'Entregado') DEFAULT 'Pendiente',
    total DECIMAL(10,2),
    fecha_pedido TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (id_cliente)
        REFERENCES clientes(id_cliente)
        ON DELETE SET NULL
        ON UPDATE CASCADE
);

-- ==========================================
-- CORTE DE CAJA
-- ==========================================
CREATE TABLE corte_caja (
    id_corte INT AUTO_INCREMENT PRIMARY KEY,
    fecha DATE NOT NULL,
    ventas_totales DECIMAL(10,2) DEFAULT 0,
    pedidos_totales INT DEFAULT 0,
    pendientes INT DEFAULT 0,
    observaciones TEXT
);

-- ==========================================
-- INSERTS DE EJEMPLO
-- ==========================================
INSERT INTO clientes(nombre, telefono, correo)
VALUES
('Juan Pérez', '6561234567', 'juan@gmail.com'),
('María López', '6569876543', 'maria@gmail.com');

INSERT INTO proveedores(nombre, correo, producto_que_vende)
VALUES
('Distribuidora Norte', 'contacto@norte.com', 'Refrescos'),
('Papelería Central', 'ventas@papeleria.com', 'Útiles escolares');

INSERT INTO productos(nombre, descripcion, precio, stock, categoria, id_proveedor)
VALUES
('Coca Cola 600ml', 'Refresco embotellado', 20.00, 50, 'Bebidas', 1),
('Cuaderno Profesional', 'Cuaderno de rayas', 45.00, 30, 'Papelería', 2);

-- ==========================================
-- CONSULTAS ÚTILES
-- ==========================================

-- Ver todos los productos
SELECT * FROM productos;

-- Ver ventas con nombre del cliente
SELECT 
    ventas.id_venta,
    clientes.nombre AS cliente,
    ventas.total,
    ventas.fecha_venta
FROM ventas
INNER JOIN clientes
ON ventas.id_cliente = clientes.id_cliente;

-- Ver productos y proveedores
SELECT 
    productos.nombre AS producto,
    proveedores.nombre AS proveedor,
    productos.precio,
    productos.stock
FROM productos
INNER JOIN proveedores
ON productos.id_proveedor = proveedores.id_proveedor;
