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

-- Insertar articulos
INSERT INTO articulos (codigo, nombre, precio, costo, existencias, reorden) VALUES
('7508478808538', 'Sabritas Ruffles Mix', 18.00, 12.00, 36, 25),
('7500478043927', 'Sabritas original', 24.00, 14.00, 75, 25),
('7501020515343', 'Leche Lala', 28.00, 15.50, 63, 25),
('7501031311389', 'Pepsi', 15.50, 10.00, 42, 20),
('7501055302086', 'Coca-Cola', 18.50, 12.00, 97, 20),
('7501055330295', 'Coca-Cola', 18.00, 12.00, 80, 15),
('7501055628121', 'Pomada de la campana', 18.00, 12.00, 75, 5),
('7501086081046', 'Epura Agua', 16.00, 10.00, 33, 20),
('7509546084520', 'Speed Stick Gel Extreme', 35.00, 25.00, 30, 15),
('7509546084538', 'Lady Speed Stick Aloe', 35.00, 25.00, 45, 10);

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
