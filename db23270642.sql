SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

CREATE SCHEMA IF NOT EXISTS `seveneleven` DEFAULT CHARACTER SET utf8;
USE `seveneleven`;

CREATE TABLE IF NOT EXISTS `categoria` (
  `id_categorias` INT NOT NULL,
  `nombre` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`id_categorias`)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `unidad` (
  `id_unidad` INT NOT NULL,
  `nombre` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id_unidad`)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `articulo` (
  `codigo` CHAR(13) NOT NULL,
  `nombre` VARCHAR(75) NOT NULL,
  `marca` VARCHAR(45) NOT NULL,
  `precio` DECIMAL(10,2) NOT NULL,
  `costo` DECIMAL(10,2) NOT NULL,
  `stock` INT NOT NULL,
  `reorden` INT NOT NULL,
  `id_categorias` INT NOT NULL,
  `id_unidad` INT NOT NULL,
  PRIMARY KEY (`codigo`),
  INDEX `fk_articulos_categorias_idx` (`id_categorias` ASC),
  INDEX `fk_articulo_unidad1_idx` (`id_unidad` ASC),
  CONSTRAINT `fk_articulos_categorias`
    FOREIGN KEY (`id_categorias`)
    REFERENCES `categoria` (`id_categorias`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_articulo_unidad1`
    FOREIGN KEY (`id_unidad`)
    REFERENCES `unidad` (`id_unidad`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `proveedor` (
  `id_proveedor` INT NOT NULL,
  `nombre` VARCHAR(50) NOT NULL,
  `telefono` CHAR(10) NOT NULL,
  `correo` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`id_proveedor`)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `cliente` (
  `telefono` CHAR(10) NOT NULL,
  `nombre` VARCHAR(50) NOT NULL,
  `genero` ENUM('M', 'F') NOT NULL,
  `correo` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`telefono`)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `empleado` (
  `id_empleado` INT NOT NULL,
  `nombre` VARCHAR(45) NOT NULL,
  `genero` ENUM('F', 'M') NOT NULL,
  `puesto` ENUM('cajero', 'encargado', 'administrador') NOT NULL,
  `sueldo` DECIMAL(10,2) NOT NULL,
  `clave` CHAR(32) NOT NULL,
  PRIMARY KEY (`id_empleado`)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `caja` (
  `id_caja` INT NOT NULL AUTO_INCREMENT,
  `estado` ENUM('Activo', 'Inactivo') NOT NULL DEFAULT 'Inactivo',
  `empleado_id_empleado` INT NOT NULL,
  PRIMARY KEY (`id_caja`),
  INDEX `empleado1_idx` (`empleado_id_empleado` ASC),
  CONSTRAINT `fk_caja_empleado`
    FOREIGN KEY (`empleado_id_empleado`)
    REFERENCES `empleado` (`id_empleado`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `venta` (
  `id_venta` INT NOT NULL AUTO_INCREMENT,
  `fecha` DATE NOT NULL,
  `importe` DECIMAL(10,2) NOT NULL,
  `telefono` CHAR(10) NOT NULL,
  `id_caja` INT NOT NULL,
  PRIMARY KEY (`id_venta`),
  INDEX `fk_venta_cliente1_idx` (`telefono` ASC),
  INDEX `fk_venta_caja_idx` (`id_caja` ASC),
  CONSTRAINT `fk_venta_cliente1`
    FOREIGN KEY (`telefono`)
    REFERENCES `cliente` (`telefono`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_venta_caja`
    FOREIGN KEY (`id_caja`)
    REFERENCES `caja` (`id_caja`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `compra` (
  `id_compra` INT NOT NULL AUTO_INCREMENT,
  `fecha` DATETIME NOT NULL,
  `importe` DECIMAL(10,2) NOT NULL,
  `estado` ENUM('Realizado', 'Pendiente') NOT NULL,
  `id_proveedor` INT NOT NULL,
  PRIMARY KEY (`id_compra`),
  INDEX `fk_compra_proveedores1_idx` (`id_proveedor` ASC),
  CONSTRAINT `fk_compra_proveedores1`
    FOREIGN KEY (`id_proveedor`)
    REFERENCES `proveedor` (`id_proveedor`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `detalle_comp` (
  `id_compra` INT NOT NULL,
  `codigo` CHAR(13) NOT NULL,
  `cantidad` INT NOT NULL,
  `importe` DECIMAL(10,2) NOT NULL,
  PRIMARY KEY (`id_compra`, `codigo`),
  INDEX `fk_detalles_comp_compra1_idx` (`id_compra` ASC),
  INDEX `fk_detalles_comp_articulos1_idx` (`codigo` ASC),
  CONSTRAINT `fk_detalles_comp_compra1`
    FOREIGN KEY (`id_compra`)
    REFERENCES `compra` (`id_compra`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_detalles_comp_articulos1`
    FOREIGN KEY (`codigo`)
    REFERENCES `articulo` (`codigo`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `detalle_venta` (
  `id_venta` INT NOT NULL,
  `codigo` CHAR(13) NOT NULL,
  `cantidad` INT NOT NULL,
  `importe` DECIMAL(10,2) NOT NULL,
  `metodo_pago` ENUM('Tarjeta', 'Efectivo') NOT NULL,
  PRIMARY KEY (`id_venta`, `codigo`),
  INDEX `fk_detalles_venta_venta1_idx` (`id_venta` ASC),
  INDEX `fk_detalles_venta_articulos1_idx` (`codigo` ASC),
  CONSTRAINT `fk_detalles_venta_venta1`
    FOREIGN KEY (`id_venta`)
    REFERENCES `venta` (`id_venta`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_detalles_venta_articulos1`
    FOREIGN KEY (`codigo`)
    REFERENCES `articulo` (`codigo`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS `factura` (
  `id_factura` INT NOT NULL AUTO_INCREMENT,
  `fecha` DATE NOT NULL,
  `detalles` VARCHAR(100) NOT NULL,
  `venta_id_venta` INT NOT NULL,
  PRIMARY KEY (`id_factura`),
  INDEX `fk_factura_venta_idx` (`venta_id_venta` ASC),
  CONSTRAINT `fk_factura_venta`
    FOREIGN KEY (`venta_id_venta`)
    REFERENCES `venta` (`id_venta`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
) ENGINE=InnoDB;

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
