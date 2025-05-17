-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema seveneleven
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `seveneleven` DEFAULT CHARACTER SET utf8;
USE `seveneleven`;

-- -----------------------------------------------------
-- Table `seveneleven`.`categoria`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `seveneleven`.`categoria` (
  `id_categoria` VARCHAR(45) NOT NULL,
  `nombre` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id_categoria`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `seveneleven`.`unidad`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `seveneleven`.`unidad` (
  `id_unidad` VARCHAR(45) NOT NULL,
  `nombre` VARCHAR(45) NOT NULL,
  `valor` INT NOT NULL,
  PRIMARY KEY (`id_unidad`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `seveneleven`.`articulo`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `seveneleven`.`articulo` (
  `codigo` CHAR(13) NOT NULL,
  `nombre` VARCHAR(75) NOT NULL,
  `precio` DECIMAL(10,2) NOT NULL,
  `costo` DECIMAL(10,2) NOT NULL,
  `existencias` INT NOT NULL,
  `reorden` INT NOT NULL,
  `id_categoria` VARCHAR(45) NULL,
  `id_unidad` VARCHAR(45) NULL,
  PRIMARY KEY (`codigo`),
  INDEX `fk_articulos_categorias_idx` (`id_categoria` ASC),
  INDEX `fk_articulo_unidad1_idx` (`id_unidad` ASC),
  CONSTRAINT `fk_articulos_categorias`
    FOREIGN KEY (`id_categoria`)
    REFERENCES `seveneleven`.`categoria` (`id_categoria`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_articulo_unidad1`
    FOREIGN KEY (`id_unidad`)
    REFERENCES `seveneleven`.`unidad` (`id_unidad`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `seveneleven`.`proveedor`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `seveneleven`.`proveedor` (
  `id_proveedor` INT NOT NULL,
  `nombre` VARCHAR(50) NOT NULL,
  `telefono` VARCHAR(20) NOT NULL,
  `correo` VARCHAR(30) NOT NULL,
  PRIMARY KEY (`id_proveedor`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `seveneleven`.`empleado`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `seveneleven`.`empleado` (
  `id_empleado` INT NOT NULL,
  `nombre` VARCHAR(45) NOT NULL,
  `genero` ENUM('F', 'M') NOT NULL,
  `puesto` ENUM('cajero', 'encargado') NOT NULL,
  `sueldo` DECIMAL(10,2) NOT NULL,
  `clave` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id_empleado`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `seveneleven`.`caja`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `seveneleven`.`caja` (
  `id_caja` INT NOT NULL AUTO_INCREMENT,
  `estado` ENUM('Activo', 'Inactivo') NOT NULL,
  `id_empleado` INT NOT NULL,
  PRIMARY KEY (`id_caja`),
  INDEX `empleado1_idx` (`id_empleado` ASC),
  CONSTRAINT `empleado1`
    FOREIGN KEY (`id_empleado`)
    REFERENCES `seveneleven`.`empleado` (`id_empleado`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `seveneleven`.`cliente`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `seveneleven`.`cliente` (
  `telefono` CHAR(10) NOT NULL,
  `nombre` VARCHAR(75) NOT NULL,
  `correo` VARCHAR(100) NOT NULL,
  `genero` ENUM('M', 'F') NOT NULL,
  PRIMARY KEY (`telefono`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `seveneleven`.`venta`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `seveneleven`.`venta` (
  `id_venta` INT NOT NULL,
  `fecha` DATE NOT NULL,
  `importe` DECIMAL(10,2) NOT NULL,
  `id_caja` INT NOT NULL,
  `telefono` CHAR(10) NOT NULL,
  PRIMARY KEY (`id_venta`),
  INDEX `caja1_idx` (`id_caja` ASC),
  INDEX `cliente1_idx` (`telefono` ASC),
  CONSTRAINT `caja1`
    FOREIGN KEY (`id_caja`)
    REFERENCES `seveneleven`.`caja` (`id_caja`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `cliente1`
    FOREIGN KEY (`telefono`)
    REFERENCES `seveneleven`.`cliente` (`telefono`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `seveneleven`.`compra`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `seveneleven`.`compra` (
  `id_compra` INT NOT NULL,
  `fecha` DATE NOT NULL,
  `importe` DECIMAL(10,2) NOT NULL,
  `estado` ENUM('Realizado', 'Pendiente') NOT NULL,
  `id_proveedor` INT NOT NULL,
  PRIMARY KEY (`id_compra`),
  INDEX `fk_compra_proveedores1_idx` (`id_proveedor` ASC),
  CONSTRAINT `fk_compra_proveedores1`
    FOREIGN KEY (`id_proveedor`)
    REFERENCES `seveneleven`.`proveedor` (`id_proveedor`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `seveneleven`.`detalle_comp`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `seveneleven`.`detalle_comp` (
  `id_compra` INT NOT NULL,
  `codigo` CHAR(13) NOT NULL,
  `cantidad` INT NOT NULL,
  `subtotal` DECIMAL(10,2) NOT NULL,
  PRIMARY KEY (`id_compra`, `codigo`),
  INDEX `fk_detalles_comp_compra1_idx` (`id_compra` ASC),
  INDEX `fk_detalles_comp_articulos1_idx` (`codigo` ASC),
  CONSTRAINT `fk_detalles_comp_compra1`
    FOREIGN KEY (`id_compra`)
    REFERENCES `seveneleven`.`compra` (`id_compra`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_detalles_comp_articulos1`
    FOREIGN KEY (`codigo`)
    REFERENCES `seveneleven`.`articulo` (`codigo`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `seveneleven`.`detalle_venta`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `seveneleven`.`detalle_venta` (
  `id_venta` INT NOT NULL,
  `codigo` CHAR(13) NOT NULL,
  `cantidad` INT NOT NULL,
  `subtotal` DECIMAL(10,2) NOT NULL,
  `metodo_pago` ENUM('Efectivo', 'Tarjeta') NOT NULL,
  PRIMARY KEY (`id_venta`, `codigo`),
  INDEX `fk_detalles_venta_venta1_idx` (`id_venta` ASC),
  INDEX `fk_detalles_venta_articulos1_idx` (`codigo` ASC),
  CONSTRAINT `fk_detalles_venta_venta1`
    FOREIGN KEY (`id_venta`)
    REFERENCES `seveneleven`.`venta` (`id_venta`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_detalles_venta_articulos1`
    FOREIGN KEY (`codigo`)
    REFERENCES `seveneleven`.`articulo` (`codigo`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `seveneleven`.`factura`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `seveneleven`.`factura` (
  `id_factura` INT NOT NULL,
  `fecha` DATE NOT NULL,
  `detalles` VARCHAR(100) NULL,
  `rfc_emisor` VARCHAR(13) NOT NULL,
  `rfc_receptor` VARCHAR(13) NOT NULL,
  `id_venta` INT NOT NULL,
  PRIMARY KEY (`id_factura`),
  INDEX `fk_factura_venta1_idx` (`id_venta` ASC),
  CONSTRAINT `fk_factura_venta1`
    FOREIGN KEY (`id_venta`)
    REFERENCES `seveneleven`.`venta` (`id_venta`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

-- Artículos 
INSERT INTO `articulo` (`codigo`, `nombre`, `precio`, `costo`, `existencias`, `reorden`) 
VALUES ('7501031311309', 'Pepsi', 15.50, 10.00, 50, 20), ('7501055302086 ', 'Coca-Cola', 18.50, 12.00, 100, 20),
('7500478043927', 'Sabritas original', 24.00, 14.00, 80, 25), ('7501055302925', 'Coca-Cola', 28.00, 20.00, 80, 15), 
('7500478030538', 'Sabritas Ruffles Mix', 18.00, 12.00, 40, 25), ('7501020515343', 'Leche Lala', 28.00, 15.50, 70, 25), 
('7509546045368', 'Lady Speed Stick Aloe', 35.00, 25.00, 45, 10), ('7509546045320', 'Speed Stick Gel Extreme', 35.00, 25.00, 30, 15),
('7501065628121', 'Pomada de la campana', 18.00, 12.00, 75, 5), ('7501086801046', 'Epura Agua', 16.00, 10.00, 55, 20);

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;