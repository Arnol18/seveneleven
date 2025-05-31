-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema seveneleven
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `seveneleven` DEFAULT CHARACTER SET utf8;
USE `seveneleven` ;

-- -----------------------------------------------------
-- Table `categoria`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `categoria` (
  `id_categoria` VARCHAR(45) NOT NULL,
  `nombre` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id_categoria`)
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `unidad`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `unidad` (
  `id_unidad` VARCHAR(45) NOT NULL,
  `nombre` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id_unidad`)
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `proveedor`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `proveedor` (
  `id_proveedor` INT NOT NULL,
  `nombre` VARCHAR(50) NOT NULL,
  `telefono` VARCHAR(20) NOT NULL,
  `correo` VARCHAR(30) NOT NULL,
  PRIMARY KEY (`id_proveedor`)
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `articulo`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `articulo` (
  `codigo` CHAR(13) NOT NULL,
  `nombre` VARCHAR(75) NOT NULL,
  `precio` DECIMAL(10,2) NOT NULL,
  `costo` DECIMAL(10,2) NOT NULL,
  `existencias` INT NOT NULL,
  `reorden` INT NOT NULL,
  `id_categoria` VARCHAR(45) NULL,
  `id_unidad` VARCHAR(45) NULL,
  `id_proveedor` INT NULL,
  PRIMARY KEY (`codigo`),
  INDEX `fk_articulos_categorias_idx` (`id_categoria` ASC),
  INDEX `fk_articulo_unidad1_idx` (`id_unidad` ASC),
  INDEX `proveedor1_idx` (`id_proveedor` ASC),
  CONSTRAINT `fk_articulos_categorias`
    FOREIGN KEY (`id_categoria`)
    REFERENCES `categoria` (`id_categoria`)
    ON DELETE SET NULL
    ON UPDATE CASCADE,
  CONSTRAINT `fk_articulo_unidad1`
    FOREIGN KEY (`id_unidad`)
    REFERENCES `unidad` (`id_unidad`)
    ON DELETE SET NULL
    ON UPDATE CASCADE,
  CONSTRAINT `proveedor1`
    FOREIGN KEY (`id_proveedor`)
    REFERENCES `proveedor` (`id_proveedor`)
    ON DELETE SET NULL
    ON UPDATE CASCADE
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `cliente`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `cliente` (
  `telefono` CHAR(10) NOT NULL,
  `nombre` VARCHAR(75) NOT NULL,
  `correo` VARCHAR(100) NOT NULL,
  `genero` ENUM('M', 'F') NOT NULL,
  PRIMARY KEY (`telefono`)
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `empleado`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `empleado` (
  `id_empleado` INT NOT NULL,
  `nombre` VARCHAR(45) NOT NULL,
  `genero` ENUM('F', 'M') NOT NULL,
  `puesto` ENUM('cajero', 'encargado', 'administrador') NOT NULL,
  `sueldo` DECIMAL(10,2) NOT NULL,
  `clave` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id_empleado`)
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `venta`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `venta` (
  `id_venta` INT NOT NULL AUTO_INCREMENT,
  `fecha` DATETIME NOT NULL,
  `tipo` ENUM('Ticket') NOT NULL,
  `metodo_pago` ENUM('Efectivo', 'Tarjeta') NOT NULL,
  `pago` DECIMAL(10,2) NOT NULL,
  `cambio` DECIMAL(10,2) NOT NULL,
  `importe` DECIMAL(10,2) NOT NULL,
  `nombre_cliente` VARCHAR(45) NOT NULL,
  `telefono` CHAR(10) NULL,
  `id_empleado` INT NOT NULL,
  PRIMARY KEY (`id_venta`),
  INDEX `cliente1_idx` (`telefono` ASC),
  INDEX `empleado1_idx` (`id_empleado` ASC),
  CONSTRAINT `cliente1`
    FOREIGN KEY (`telefono`)
    REFERENCES `cliente` (`telefono`)
    ON DELETE SET NULL
    ON UPDATE CASCADE,
  CONSTRAINT `empleado1`
    FOREIGN KEY (`id_empleado`)
    REFERENCES `empleado` (`id_empleado`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `compra`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `compra` (
  `id_compra` INT NOT NULL,
  `fecha` DATETIME NOT NULL,
  `importe` DECIMAL(10,2) NOT NULL,
  `id_proveedor` INT NOT NULL,
  PRIMARY KEY (`id_compra`),
  INDEX `fk_compra_proveedores1_idx` (`id_proveedor` ASC),
  CONSTRAINT `fk_compra_proveedores1`
    FOREIGN KEY (`id_proveedor`)
    REFERENCES `proveedor` (`id_proveedor`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `detalle_compra`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `detalle_compra` (
  `id_compra` INT NOT NULL,
  `codigo` CHAR(13) NOT NULL,
  `costo` DECIMAL(10,2) NOT NULL,
  `cantidad` INT NOT NULL,
  `subtotal` DECIMAL(10,2) NOT NULL,
  PRIMARY KEY (`id_compra`, `codigo`),
  INDEX `fk_detalles_comp_compra1_idx` (`id_compra` ASC),
  INDEX `fk_detalles_comp_articulos1_idx` (`codigo` ASC),
  CONSTRAINT `fk_detalles_comp_compra1`
    FOREIGN KEY (`id_compra`)
    REFERENCES `compra` (`id_compra`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_detalles_comp_articulos1`
    FOREIGN KEY (`codigo`)
    REFERENCES `articulo` (`codigo`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table `detalle_venta`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `detalle_venta` (
  `id_venta` INT NOT NULL,
  `codigo` CHAR(13) NOT NULL,
  `precio_unitario` DECIMAL(10,2) NOT NULL,
  `cantidad` INT NOT NULL,
  `subtotal` DECIMAL(10,2) NOT NULL,
  PRIMARY KEY (`id_venta`, `codigo`),
  INDEX `fk_detalles_venta_venta1_idx` (`id_venta` ASC),
  INDEX `fk_detalles_venta_articulos1_idx` (`codigo` ASC),
  CONSTRAINT `fk_detalles_venta_venta1`
    FOREIGN KEY (`id_venta`)
    REFERENCES `venta` (`id_venta`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_detalles_venta_articulos1`
    FOREIGN KEY (`codigo`)
    REFERENCES `articulo` (`codigo`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE
) ENGINE = InnoDB;

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

-- Configuración inicial
SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- Crear esquema
DROP SCHEMA IF EXISTS `seveneleven`;
CREATE SCHEMA IF NOT EXISTS `seveneleven` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `seveneleven`;

-- -----------------------------------------------------
-- Tabla `categoria`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `categoria` (
  `id_categoria` VARCHAR(45) NOT NULL,
  `nombre` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id_categoria`)
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- Tabla `unidad`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `unidad` (
  `id_unidad` VARCHAR(45) NOT NULL,
  `nombre` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id_unidad`)
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- Tabla `proveedor`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `proveedor` (
  `id_proveedor` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(50) NOT NULL,
  `telefono` VARCHAR(20) NOT NULL,
  `correo` VARCHAR(30) NOT NULL,
  PRIMARY KEY (`id_proveedor`)
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- Tabla `articulo`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `articulo` (
  `codigo` CHAR(13) NOT NULL,
  `nombre` VARCHAR(75) NOT NULL,
  `precio` DECIMAL(10,2) NOT NULL,
  `costo` DECIMAL(10,2) NOT NULL,
  `existencias` INT NOT NULL,
  `reorden` INT NOT NULL,
  `id_categoria` VARCHAR(45) NULL,
  `id_unidad` VARCHAR(45) NULL,
  `id_proveedor` INT NULL,
  PRIMARY KEY (`codigo`),
  INDEX `fk_articulos_categorias_idx` (`id_categoria` ASC),
  INDEX `fk_articulo_unidad1_idx` (`id_unidad` ASC),
  INDEX `proveedor1_idx` (`id_proveedor` ASC),
  CONSTRAINT `fk_articulos_categorias`
    FOREIGN KEY (`id_categoria`)
    REFERENCES `categoria` (`id_categoria`)
    ON DELETE SET NULL
    ON UPDATE CASCADE,
  CONSTRAINT `fk_articulo_unidad1`
    FOREIGN KEY (`id_unidad`)
    REFERENCES `unidad` (`id_unidad`)
    ON DELETE SET NULL
    ON UPDATE CASCADE,
  CONSTRAINT `proveedor1`
    FOREIGN KEY (`id_proveedor`)
    REFERENCES `proveedor` (`id_proveedor`)
    ON DELETE SET NULL
    ON UPDATE CASCADE
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- Tabla `cliente`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `cliente` (
  `telefono` CHAR(10) NOT NULL,
  `nombre` VARCHAR(75) NOT NULL,
  `correo` VARCHAR(100) NOT NULL,
  `genero` ENUM('M', 'F') NOT NULL,
  PRIMARY KEY (`telefono`)
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- Tabla `empleado`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `empleado` (
  `id_empleado` INT NOT NULL,
  `nombre` VARCHAR(45) NOT NULL,
  `genero` ENUM('F', 'M') NOT NULL,
  `puesto` ENUM('cajero', 'encargado', 'administrador') NOT NULL,
  `sueldo` DECIMAL(10,2) NOT NULL,
  `clave` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id_empleado`)
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- Tabla `venta`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `venta` (
  `id_venta` INT NOT NULL AUTO_INCREMENT,
  `fecha` DATETIME NOT NULL,
  `tipo` ENUM('Ticket') NOT NULL,
  `metodo_pago` ENUM('Efectivo', 'Tarjeta') NOT NULL,
  `pago` DECIMAL(10,2) NOT NULL,
  `cambio` DECIMAL(10,2) NOT NULL,
  `importe` DECIMAL(10,2) NOT NULL,
  `nombre_cliente` VARCHAR(45) NOT NULL,
  `telefono` CHAR(10) NULL,
  `id_empleado` INT NOT NULL,
  PRIMARY KEY (`id_venta`),
  INDEX `cliente1_idx` (`telefono` ASC),
  INDEX `empleado1_idx` (`id_empleado` ASC),
  CONSTRAINT `cliente1`
    FOREIGN KEY (`telefono`)
    REFERENCES `cliente` (`telefono`)
    ON DELETE SET NULL
    ON UPDATE CASCADE,
  CONSTRAINT `empleado1`
    FOREIGN KEY (`id_empleado`)
    REFERENCES `empleado` (`id_empleado`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- Tabla `compra`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `compra` (
  `id_compra` INT NOT NULL,
  `fecha` DATETIME NOT NULL,
  `importe` DECIMAL(10,2) NOT NULL,
  `id_proveedor` INT NOT NULL,
  PRIMARY KEY (`id_compra`),
  INDEX `fk_compra_proveedores1_idx` (`id_proveedor` ASC),
  CONSTRAINT `fk_compra_proveedores1`
    FOREIGN KEY (`id_proveedor`)
    REFERENCES `proveedor` (`id_proveedor`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- Tabla `detalle_compra`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `detalle_compra` (
  `id_compra` INT NOT NULL,
  `codigo` CHAR(13) NOT NULL,
  `costo` DECIMAL(10,2) NOT NULL,
  `cantidad` INT NOT NULL,
  `subtotal` DECIMAL(10,2) NOT NULL,
  PRIMARY KEY (`id_compra`, `codigo`),
  INDEX `fk_detalles_comp_compra1_idx` (`id_compra` ASC),
  INDEX `fk_detalles_comp_articulos1_idx` (`codigo` ASC),
  CONSTRAINT `fk_detalles_comp_compra1`
    FOREIGN KEY (`id_compra`)
    REFERENCES `compra` (`id_compra`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_detalles_comp_articulos1`
    FOREIGN KEY (`codigo`)
    REFERENCES `articulo` (`codigo`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- Tabla `detalle_venta`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `detalle_venta` (
  `id_venta` INT NOT NULL,
  `codigo` CHAR(13) NOT NULL,
  `precio_unitario` DECIMAL(10,2) NOT NULL,
  `cantidad` INT NOT NULL,
  `subtotal` DECIMAL(10,2) NOT NULL,
  PRIMARY KEY (`id_venta`, `codigo`),
  INDEX `fk_detalles_venta_venta1_idx` (`id_venta` ASC),
  INDEX `fk_detalles_venta_articulos1_idx` (`codigo` ASC),
  CONSTRAINT `fk_detalles_venta_venta1`
    FOREIGN KEY (`id_venta`)
    REFERENCES `venta` (`id_venta`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `fk_detalles_venta_articulos1`
    FOREIGN KEY (`codigo`)
    REFERENCES `articulo` (`codigo`)
    ON DELETE RESTRICT
    ON UPDATE CASCADE
) ENGINE = InnoDB;

-- Configuración inicial
SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- Insertar categorías
INSERT INTO `categoria` (`id_categoria`, `nombre`) VALUES
('CAT001', 'Botanas'),
('CAT002', 'Bebidas'),
('CAT003', 'Lácteos'),
('CAT004', 'Cuidado Personal'),
('CAT005', 'Dulces'),
('CAT006', 'Cuidado del Hogar'),
('CAT007', 'Panadería'),
('CAT008', 'Alimentos Enlatados');

-- Insertar unidades
INSERT INTO `unidad` (`id_unidad`, `nombre`) VALUES
('UN001', 'Pieza'),
('UN002', 'Litro'),
('UN003', 'Kilogramo'),
('UN004', 'Gramo'),
('UN005', 'Mililitro'),
('UN006', 'Paquete'),
('UN007', 'Caja'),
('UN008', 'Botella');

-- Insertar proveedores 
INSERT INTO `proveedor` (`id_proveedor`, `nombre`, `telefono`, `correo`) VALUES
(1, 'Sabritas S.A. de C.V.', '9611234567', 'contacto@sabritas.com'),
(2, 'PepsiCo México', '9617654321', 'ventas@pepsico.com.mx'),
(3, 'Coca-Cola FEMSA', '9619876543', 'proveedores@cocacolafemsa.com'),
(4, 'Grupo Lala', '9614567890', 'distribucion@lala.com.mx'),
(5, 'Colgate-Palmolive', '9616789012', 'ventas@colgate.com'),
(6, 'Bimbo', '9612345678', 'proveedores@bimbo.com'),
(7, 'Nestlé México', '9618901234', 'contacto@nestle.mx'),
(8, 'Unilever México', '9613456789', 'proveedores@unilever.com');

-- Insertar artículos 
INSERT INTO `articulo` (`codigo`, `nombre`, `precio`, `costo`, `existencias`, `reorden`, `id_categoria`, `id_unidad`, `id_proveedor`) VALUES
('7500478030538', 'Sabritas Ruffles Mix', 18.00, 12.00, 36, 25, 'CAT001', 'UN001', 1),
('7500478043927', 'Sabritas original', 24.00, 14.00, 75, 25, 'CAT001', 'UN001', 1),
('7501020513543', 'Leche Lala', 19.00, 15.50, 63, 20, 'CAT003', 'UN002', 4),
('7501013311380', 'Pepsi', 15.50, 10.00, 42, 20, 'CAT002', 'UN008', 2),
('7501055320886', 'Coca-Cola', 18.50, 12.00, 97, 20, 'CAT002', 'UN008', 3),
('7501055328925', 'Coca-Cola 2L', 28.00, 20.00, 80, 15, 'CAT002', 'UN008', 3),
('7501065281211', 'Pomada de la campana', 28.00, 12.00, 75, 5, 'CAT004', 'UN001', 5),
('7501083681406', 'Epura Agua', 16.00, 10.00, 53, 20, 'CAT002', 'UN008', 3),
('7509540645232', 'Speed Stick Gel Extreme', 25.00, 25.00, 30, 15, 'CAT004', 'UN001', 5),
('7509540645368', 'Lady Speed Stick Aloe', 35.00, 25.00, 45, 10, 'CAT004', 'UN001', 5),
('7501001311025', 'Gansito Marinela', 12.50, 8.00, 50, 20, 'CAT005', 'UN001', 6),
('7501003123456', 'Pan Bimbo Blanco', 32.00, 25.00, 40, 15, 'CAT007', 'UN006', 6),
('7501008765432', 'Nescafé Clásico', 45.00, 35.00, 25, 10, 'CAT002', 'UN006', 7),
('7501034567890', 'Aceite Capullo', 28.50, 22.00, 30, 10, 'CAT006', 'UN008', 8),
('7501045678901', 'Atún Dolores', 18.00, 12.50, 45, 15, 'CAT008', 'UN001', 7),
('7501076543210', 'Cloralex', 22.00, 15.00, 35, 10, 'CAT006', 'UN008', 5),
('7501098765432', 'Mazapan De la Rosa', 6.50, 4.00, 60, 30, 'CAT005', 'UN001', 6),
('7501123456789', 'Jugo Del Valle', 14.00, 9.50, 40, 20, 'CAT002', 'UN008', 4),
('7501135792468', 'Galletas Oreo', 15.00, 10.00, 55, 25, 'CAT005', 'UN006', 8),
('7501146803579', 'Queso Philadelphia', 42.00, 32.00, 20, 10, 'CAT003', 'UN001', 4);

-- Insertar cliente general y clientes 
INSERT INTO `cliente` (`telefono`, `nombre`, `correo`, `genero`) VALUES
('9619999999', 'Cliente General', 'cliente.general@seveneleven.com', 'M'),
('9611112233', 'María González', 'maria.gonzalez@mail.com', 'F'),
('9612223344', 'Juan Pérez', 'juan.perez@mail.com', 'M'),
('9613334455', 'Ana López', 'ana.lopez@mail.com', 'F'),
('9614445566', 'Carlos Sánchez', 'carlos.sanchez@mail.com', 'M'),
('9615556677', 'Laura Martínez', 'laura.martinez@mail.com', 'F');

-- Insertar empleados
INSERT INTO `empleado` (`id_empleado`, `nombre`, `genero`, `puesto`, `sueldo`, `clave`) VALUES
(1, 'Admin', 'M', 'administrador', 25000.00, 'admin123'),
(2, 'Roberto Jiménez', 'M', 'encargado', 15000.00, 'roberto123'),
(3, 'Sofía Hernández', 'F', 'cajero', 10000.00, 'sofia123'),
(4, 'Miguel Ángel Cruz', 'M', 'cajero', 10000.00, 'miguel123'),
(5, 'Patricia Vázquez', 'F', 'cajero', 10000.00, 'patricia123');

-- Insertar compras 
INSERT INTO `compra` (`id_compra`, `fecha`, `importe`, `id_proveedor`) VALUES
(1, '2023-01-15 10:30:00', 5000.00, 1),
(2, '2023-01-20 11:45:00', 3200.00, 2),
(3, '2023-02-05 09:15:00', 2800.00, 3),
(4, '2023-02-10 16:20:00', 4500.00, 4),
(5, '2023-02-15 14:00:00', 3800.00, 5);

-- Insertar detalles de compra 
INSERT INTO `detalle_compra` (`id_compra`, `codigo`, `costo`, `cantidad`, `subtotal`) VALUES
(1, '7500478030538', 12.00, 100, 1200.00),
(1, '7500478043927', 14.00, 100, 1400.00),
(2, '7501013311380', 10.00, 150, 1500.00),
(3, '7501055320886', 12.00, 120, 1440.00),
(3, '7501055328925', 20.00, 50, 1000.00),
(4, '7501020513543', 15.50, 100, 1550.00),
(5, '7501065281211', 12.00, 50, 600.00),
(5, '7509540645232', 25.00, 40, 1000.00),
(5, '7509540645368', 25.00, 40, 1000.00);

-- Insertar ventas 
INSERT INTO `venta` (`id_venta`, `fecha`, `tipo`, `metodo_pago`, `pago`, `cambio`, `importe`, `nombre_cliente`, `telefono`, `id_empleado`) VALUES
(1, '2023-03-01 08:15:00', 'Ticket', 'Efectivo', 100.00, 12.50, 87.50, 'Cliente General', '9619999999', 3),
(2, '2023-03-01 10:30:00', 'Ticket', 'Tarjeta', 150.00, 0.00, 150.00, 'María González', '9611112233', 3),
(3, '2023-03-01 12:45:00', 'Ticket', 'Efectivo', 200.00, 45.25, 154.75, 'Juan Pérez', '9612223344', 4),
(4, '2023-03-02 09:20:00', 'Ticket', 'Tarjeta', 80.00, 0.00, 80.00, 'Ana López', '9613334455', 5),
(5, '2023-03-02 14:10:00', 'Ticket', 'Efectivo', 500.00, 120.50, 379.50, 'Carlos Sánchez', '9614445566', 3);

-- Insertar detalles de venta 
INSERT INTO `detalle_venta` (`id_venta`, `codigo`, `precio_unitario`, `cantidad`, `subtotal`) VALUES
(1, '7500478030538', 18.00, 2, 36.00),
(1, '7501013311380', 15.50, 1, 15.50),
(1, '7501001311025', 12.50, 2, 25.00),
(1, '7501098765432', 6.50, 1, 6.50),
(2, '7501055320886', 18.50, 3, 55.50),
(2, '7501020513543', 19.00, 2, 38.00),
(2, '7501003123456', 32.00, 1, 32.00),
(2, '7501123456789', 14.00, 1, 14.00),
(3, '7501055328925', 28.00, 2, 56.00),
(3, '7501065281211', 28.00, 1, 28.00),
(3, '7501146803579', 42.00, 1, 42.00),
(3, '7501034567890', 28.50, 1, 28.50),
(4, '7509540645368', 35.00, 1, 35.00),
(4, '7501076543210', 22.00, 1, 22.00),
(4, '7501135792468', 15.00, 1, 15.00),
(5, '7500478043927', 24.00, 5, 120.00),
(5, '7501083681406', 16.00, 3, 48.00),
(5, '7501008765432', 45.00, 2, 90.00),
(5, '7501045678901', 18.00, 3, 54.00),
(5, '7509540645232', 25.00, 2, 50.00);

-- Restaurar configuraciones
SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;