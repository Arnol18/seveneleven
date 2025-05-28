SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema seveneleven
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS seveneleven DEFAULT CHARACTER SET utf8;
USE seveneleven ;

-- -----------------------------------------------------
-- Table seveneleven.categoria
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS seveneleven.categoria (
  id_categoria VARCHAR(45) NOT NULL,
  nombre VARCHAR(45) NOT NULL,
  PRIMARY KEY (id_categoria))
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table seveneleven.unidad
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS seveneleven.unidad (
  id_unidad VARCHAR(45) NOT NULL,
  nombre VARCHAR(45) NOT NULL,
  PRIMARY KEY (id_unidad))
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table seveneleven.proveedor
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS seveneleven.proveedor (
  id_proveedor INT NOT NULL,
  nombre VARCHAR(50) NOT NULL,
  telefono VARCHAR(20) NOT NULL,
  correo VARCHAR(30) NOT NULL,
  PRIMARY KEY (id_proveedor))
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table seveneleven.articulo
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS seveneleven.articulo (
  codigo CHAR(13) NOT NULL,
  nombre VARCHAR(75) NOT NULL,
  precio DECIMAL(10,2) NOT NULL,
  costo DECIMAL(10,2) NOT NULL,
  existencias INT NOT NULL,
  reorden INT NOT NULL,
  id_categoria VARCHAR(45) NULL,
  id_unidad VARCHAR(45) NULL,
  id_proveedor INT NULL,
  PRIMARY KEY (codigo),
  INDEX fk_articulos_categorias_idx (id_categoria ASC),
  INDEX fk_articulo_unidad1_idx (id_unidad ASC),
  INDEX proveedor1_idx (id_proveedor ASC),
  CONSTRAINT fk_articulos_categorias
    FOREIGN KEY (id_categoria)
    REFERENCES seveneleven.categoria (id_categoria)
    ON DELETE SET NULL
    ON UPDATE CASCADE,
  CONSTRAINT fk_articulo_unidad1
    FOREIGN KEY (id_unidad)
    REFERENCES seveneleven.unidad (id_unidad)
    ON DELETE SET NULL
    ON UPDATE CASCADE,
  CONSTRAINT proveedor1
    FOREIGN KEY (id_proveedor)
    REFERENCES seveneleven.proveedor (id_proveedor)
    ON DELETE SET NULL
    ON UPDATE CASCADE)
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table seveneleven.cliente
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS seveneleven.cliente (
  telefono CHAR(10) NOT NULL,
  nombre VARCHAR(75) NOT NULL,
  correo VARCHAR(100) NOT NULL,
  genero ENUM('M', 'F') NOT NULL,
  PRIMARY KEY (telefono))
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table seveneleven.empleado
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS seveneleven.empleado (
  id_empleado INT NOT NULL,
  nombre VARCHAR(45) NOT NULL,
  genero ENUM('F', 'M') NOT NULL,
  puesto ENUM('cajero', 'encargado', 'administrador') NOT NULL,
  sueldo DECIMAL(10,2) NOT NULL,
  clave VARCHAR(45) NOT NULL,
  PRIMARY KEY (id_empleado))
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table seveneleven.venta
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS seveneleven.venta (
  id_venta INT NOT NULL AUTO_INCREMENT,
  fecha DATE NOT NULL,
  importe DECIMAL(10,2) NOT NULL,
  telefono CHAR(10) NULL,
  id_empleado INT NULL,
  PRIMARY KEY (id_venta),
  INDEX cliente1_idx (telefono ASC),
  INDEX empleado1_idx (id_empleado ASC),
  CONSTRAINT cliente1
    FOREIGN KEY (telefono)
    REFERENCES seveneleven.cliente (telefono)
    ON DELETE SET NULL
    ON UPDATE CASCADE,
  CONSTRAINT empleado1
    FOREIGN KEY (id_empleado)
    REFERENCES seveneleven.empleado (id_empleado)
    ON DELETE SET NULL
    ON UPDATE CASCADE)
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table seveneleven.compra
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS seveneleven.compra (
  id_compra INT NOT NULL,
  fecha DATE NOT NULL,
  importe DECIMAL(10,2) NOT NULL,
  id_proveedor INT NOT NULL,
  PRIMARY KEY (id_compra),
  INDEX fk_compra_proveedores1_idx (id_proveedor ASC),
  CONSTRAINT fk_compra_proveedores1
    FOREIGN KEY (id_proveedor)
    REFERENCES seveneleven.proveedor (id_proveedor)
    ON DELETE RESTRICT
    ON UPDATE CASCADE)
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table seveneleven.detalle_comp
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS seveneleven.detalle_comp (
  id_compra INT NOT NULL,
  codigo CHAR(13) NOT NULL,
  cantidad INT NOT NULL,
  subtotal DECIMAL(10,2) NOT NULL,
  PRIMARY KEY (id_compra, codigo),
  INDEX fk_detalles_comp_compra1_idx (id_compra ASC),
  INDEX fk_detalles_comp_articulos1_idx (codigo ASC),
  CONSTRAINT fk_detalles_comp_compra1
    FOREIGN KEY (id_compra)
    REFERENCES seveneleven.compra (id_compra)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_detalles_comp_articulos1
    FOREIGN KEY (codigo)
    REFERENCES seveneleven.articulo (codigo)
    ON DELETE RESTRICT
    ON UPDATE CASCADE)
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table seveneleven.detalle_venta
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS seveneleven.detalle_venta (
  id_venta INT NOT NULL,
  codigo CHAR(13) NOT NULL,
  cantidad INT NOT NULL,
  subtotal DECIMAL(10,2) NOT NULL,
  PRIMARY KEY (id_venta, codigo),
  INDEX fk_detalles_venta_venta1_idx (id_venta ASC),
  INDEX fk_detalles_venta_articulos1_idx (codigo ASC),
  CONSTRAINT fk_detalles_venta_venta1
    FOREIGN KEY (id_venta)
    REFERENCES seveneleven.venta (id_venta)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT fk_detalles_venta_articulos1
    FOREIGN KEY (codigo)
    REFERENCES seveneleven.articulo (codigo)
    ON DELETE RESTRICT
    ON UPDATE CASCADE)
ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table seveneleven.factura
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS seveneleven.factura (
  id_factura INT NOT NULL,
  fecha DATE NOT NULL,
  detalles VARCHAR(100) NULL,
  rfc_emisor VARCHAR(13) NOT NULL,
  rfc_receptor VARCHAR(13) NOT NULL,
  id_venta INT NOT NULL,
  PRIMARY KEY (id_factura),
  INDEX fk_factura_venta1_idx (id_venta ASC),
  CONSTRAINT fk_factura_venta1
    FOREIGN KEY (id_venta)
    REFERENCES seveneleven.venta (id_venta)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

-- Insertar unidades
INSERT INTO unidad (id_unidad, nombre) VALUES 
('U001', 'pieza'),
('U002', 'litro'),
('U003', 'gramo'),
('U004', 'kilogramo'),
('U005', 'mililitro'),
('U006', 'sobre'),
('U007', 'unidad');

-- Insertar categorias
INSERT INTO categoria (id_categoria, nombre) VALUES
('CAT001', 'Lacteos'),
('CAT002', 'Salsas y Aderezos'),
('CAT003', 'Bebidas'),
('CAT004', 'Panaderia y Pasteleria'),
('CAT005', 'Cafe y Te'),
('CAT006', 'Harinas y Cereales'),
('CAT007', 'Snacks y Dulces'),
('CAT008', 'Suplementos Alimenticios'),
('CAT009', 'Condimentos'),
('CAT010', 'Galletas y Snacks');

-- Insertar proveedores
INSERT INTO proveedor (id_proveedor, nombre, telefono, correo) VALUES
(1, 'Grupo Lala', '5551234567', 'contacto@lala.com.mx'),
(2, 'Clemente Jacques', '5552345678', 'ventas@clemente.com.mx'),
(3, 'Danone México', '5553456789', 'info@danone.com.mx'),
(4, 'Gamesa', '5554567890', 'contacto@gamesa.com.mx'),
(5, 'Pisa Farmacéutica', '5555678901', 'ventas@pisa.com.mx'),
(6, 'Nestlé México', '5556789012', 'contacto@nestle.mx'),
(7, 'Maseca', '5557890123', 'info@maseca.com'),
(8, 'Herdez', '5558901234', 'ventas@herdez.com.mx'),
(9, 'Great Value', '5559012345', 'contacto@greatvalue.com'),
(10, 'Sabritas', '5550123456', 'info@sabritas.com.mx');

-- Insertar articulos
INSERT INTO articulo (codigo, nombre, precio, costo, existencias, reorden, id_categoria, id_proveedor, id_unidad) VALUES
('7501020565959', 'Leche semidescremada Lala 1 lt', 22.50, 18.00, 50, 10, 'CAT001', 1, 'U002'),
('7501052472195', 'Catsup Clemente Jacques 220g', 18.00, 12.50, 100, 20, 'CAT002', 2, 'U003'),
('7501040090028', 'Yoghurt Yoplait Batido Natural 1Kg', 35.00, 28.00, 60, 15, 'CAT001', 1, 'U004'),
('7501032398477', 'Vitalinea sin azucar sabor Manzana Verde - Danone', 24.00, 20.00, 40, 10, 'CAT001', 3, 'U003'),
('7501000630363', 'Mini Mamut Gamesa 12 g', 6.00, 4.00, 120, 30, 'CAT007', 4, 'U003'),
('7501125149221', 'Electrolit sabor Fresa/Kiwi 625 ml', 28.00, 22.00, 80, 20, 'CAT003', 5, 'U005'),
('7506495020224', 'Media crema 252gr', 26.00, 20.00, 70, 15, 'CAT001', 1, 'U003'),
('7501079016235', 'Italpasta pasta tallarin largo 200 gr', 14.00, 11.00, 90, 25, 'CAT006', 6, 'U003'),
('7501005110242', 'Harina Maizena Natural 95Gr', 16.00, 12.00, 75, 20, 'CAT006', 6, 'U003'),
('7501052474076', 'Mermelada Clemente Jacques Fresa 470g', 38.00, 30.00, 55, 15, 'CAT002', 2, 'U003');

-- Insertar clientes (incluyendo el cliente general)
INSERT INTO cliente (telefono, nombre, correo, genero) VALUES
('1', 'CLIENTE GENERAL', 'cliente.general@tienda.com', 'M'),
('9611234567', 'María González Pérez', 'maria.gonzalez@email.com', 'F'),
('9612345678', 'Juan Martínez López', 'juan.martinez@email.com', 'M'),
('9613456789', 'Ana Rodríguez Sánchez', 'ana.rodriguez@email.com', 'F'),
('9614567890', 'Carlos Hernández García', 'carlos.hernandez@email.com', 'M'),
('9615678901', 'Laura Díaz Martínez', 'laura.diaz@email.com', 'F'),
('9616789012', 'Pedro Sánchez González', 'pedro.sanchez@email.com', 'M'),
('9617890123', 'Sofía Ramírez Hernández', 'sofia.ramirez@email.com', 'F'),
('9618901234', 'Jorge Torres Díaz', 'jorge.torres@email.com', 'M'),
('9619012345', 'Patricia Castro Ruiz', 'patricia.castro@email.com', 'F');

-- Insertar empleados
INSERT INTO empleado (id_empleado, nombre, genero, puesto, sueldo, clave) VALUES
(1, 'Roberto Mendoza Jiménez', 'M', 'administrador', 18000.00, 'admin123'),
(2, 'Adriana López García', 'F', 'encargado', 15000.00, 'encargado456'),
(3, 'Fernando Castro Ruiz', 'M', 'cajero', 12000.00, 'cajero789'),
(4, 'Isabel Vargas Martínez', 'F', 'cajero', 12000.00, 'cajero012'),
(5, 'Miguel Ángel Soto Díaz', 'M', 'cajero', 12000.00, 'cajero345'),
(6, 'Daniela Ortega Sánchez', 'F', 'encargado', 15000.00, 'encargado678'),
(7, 'Oscar Pérez González', 'M', 'cajero', 12000.00, 'cajero901'),
(8, 'Lucía Méndez Ramírez', 'F', 'cajero', 12000.00, 'cajero234'),
(9, 'Raúl Herrera Torres', 'M', 'cajero', 12000.00, 'cajero567'),
(10, 'Carmen Silva Castro', 'F', 'cajero', 12000.00, 'cajero890');

-- Insertar ventas (con fechas en 2025)
INSERT INTO venta (id_venta, fecha, importe, telefono, id_empleado) VALUES
(1, '2025-01-15', 125.50, '9611234567', 3),
(2, '2025-01-16', 89.75, '9612345678', 4),
(3, '2025-01-17', 210.25, '9613456789', 3),
(4, '2025-01-18', 56.00, '1', 5),
(5, '2025-01-19', 178.50, '9614567890', 4),
(6, '2025-01-20', 92.00, '9615678901', 7),
(7, '2025-01-21', 145.75, '9616789012', 8),
(8, '2025-01-22', 63.25, '9617890123', 3),
(9, '2025-01-23', 112.00, '9618901234', 5),
(10, '2025-01-24', 204.50, '9619012345', 4);

-- Insertar detalles de venta
INSERT INTO detalle_venta (id_venta, codigo, cantidad, subtotal) VALUES
(1, '7501020565959', 2, 45.00),
(1, '7501052472195', 1, 18.00),
(1, '7501000630363', 5, 30.00),
(1, '7501125149221', 1, 28.00),
(1, '7501005110242', 1, 16.00),
(2, '7501040090028', 1, 35.00),
(2, '7501032398477', 2, 48.00),
(2, '7506495020224', 1, 26.00),
(3, '7501079016235', 3, 42.00),
(3, '7501052474076', 2, 76.00),
(3, '7501020565959', 4, 90.00),
(4, '7501000630363', 10, 60.00),
(5, '7501125149221', 2, 56.00),
(5, '7501052472195', 2, 36.00),
(5, '7506495020224', 1, 26.00),
(6, '7501032398477', 1, 24.00),
(6, '7501005110242', 2, 32.00),
(7, '7501040090028', 2, 70.00),
(7, '7501079016235', 1, 14.00),
(8, '7501052474076', 1, 38.00),
(9, '7501020565959', 3, 67.50),
(10, '7501052472195', 3, 54.00),
(10, '7501000630363', 8, 48.00),
(10, '7501125149221', 2, 56.00);

-- Insertar compras (con fechas en 2025)
INSERT INTO compra (id_compra, fecha, importe, id_proveedor) VALUES
(1, '2025-01-05', 1800.00, 1),
(2, '2025-01-06', 1250.00, 2),
(3, '2025-01-07', 1680.00, 3),
(4, '2025-01-08', 480.00, 4),
(5, '2025-01-09', 1760.00, 5),
(6, '2025-01-10', 990.00, 6),
(7, '2025-01-11', 1400.00, 1),
(8, '2025-01-12', 1500.00, 2),
(9, '2025-01-13', 900.00, 3),
(10, '2025-01-14', 800.00, 4);

-- Insertar detalles de compra
INSERT INTO detalle_comp (id_compra, codigo, cantidad, subtotal) VALUES
(1, '7501020565959', 100, 1800.00),
(2, '7501052472195', 100, 1250.00),
(3, '7501032398477', 80, 1600.00),
(4, '7501000630363', 300, 1200.00),
(5, '7501125149221', 80, 1760.00),
(6, '7501005110242', 75, 900.00),
(7, '7501040090028', 60, 1680.00),
(8, '7501052474076', 50, 1500.00),
(9, '7506495020224', 70, 1400.00),
(10, '7501079016235', 90, 990.00);

-- Insertar facturas
INSERT INTO factura (id_factura, fecha, detalles, rfc_emisor, rfc_receptor, id_venta) VALUES
(1, '2025-01-15', 'Venta al público en general', 'TIE250115ABC', 'XAXX010101000', 1),
(2, '2025-01-16', 'Venta con descuento especial', 'TIE250116ABC', 'XAXX010101000', 2),
(3, '2025-01-17', 'Venta al mayoreo', 'TIE250117ABC', 'XAXX010101000', 3),
(4, '2025-01-18', 'Venta sin cliente registrado', 'TIE250118ABC', 'XAXX010101000', 4),
(5, '2025-01-19', 'Venta con tarjeta de crédito', 'TIE250119ABC', 'XAXX010101000', 5),
(6, '2025-01-20', 'Venta con promoción', 'TIE250120ABC', 'XAXX010101000', 6),
(7, '2025-01-21', 'Venta al contado', 'TIE250121ABC', 'XAXX010101000', 7),
(8, '2025-01-22', 'Venta con puntos de lealtad', 'TIE250122ABC', 'XAXX010101000', 8),
(9, '2025-01-23', 'Venta con descuento por volumen', 'TIE250123ABC', 'XAXX010101000', 9),
(10, '2025-01-24', 'Venta con pago en efectivo', 'TIE250124ABC', 'XAXX010101000', 10);