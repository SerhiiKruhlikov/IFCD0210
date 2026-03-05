BEGIN TRANSACTION;
CREATE TABLE clientes (
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	cif TEXT(10),
	nombre TEXT(40),
	direccion TEXT(40),
	telefono TEXT(10)
);
CREATE TABLE datos_factura (
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	id_cliente INTEGER,
	numero_fra TEXT(10),
	fecha TEXT(10),
	emisor TEXT(40),
	cif TEXT(10),
	ditreccion TEXT(40),
	CONSTRAINT datos_factura_clientes_FK FOREIGN KEY (id_cliente) REFERENCES clientes(id)
);
CREATE TABLE lineas_factura (
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	id_factura INTEGER NOT NULL,
	id_producto INTEGER NOT NULL,
	cantidad INTEGER,
	precio REAL,
	iva REAL,
	total REAL,
	CONSTRAINT lineas_factura_datos_factura_FK FOREIGN KEY (id_factura) REFERENCES datos_factura(id),
	CONSTRAINT lineas_factura_productos_FK FOREIGN KEY (id_producto) REFERENCES productos(id)
);
CREATE TABLE productos (
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	descripcion TEXT(40),
	stock INTEGER DEFAULT (0) NOT NULL,
	precio REAL,
	iva REAL
);
DELETE FROM "sqlite_sequence";
COMMIT;