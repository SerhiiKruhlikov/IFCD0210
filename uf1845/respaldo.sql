BEGIN TRANSACTION;
CREATE TABLE clientes (
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	nombre TEXT
, cif TEXT(10), direccion TEXT, telefono TEXT);
CREATE TABLE facturas (
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	numero TEXT,
	fecha_creacion TEXT NOT NULL,
	id_cliente INTEGER NOT NULL,
	CONSTRAINT facturas_clientes_FK FOREIGN KEY (id_cliente) REFERENCES clientes(id)
);
CREATE TABLE facturas_productos (
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	id_factura INTEGER NOT NULL,
	id_producto INTEGER NOT NULL,
	cantidad REAL DEFAULT (0.00) NOT NULL,
	precio REAL DEFAULT (0.00) NOT NULL,
	iva REAL DEFAULT (0.00) NOT NULL,
	total REAL DEFAULT (0.00) NOT NULL,
	CONSTRAINT facturas_productos_productos_FK FOREIGN KEY (id_producto) REFERENCES productos(id),
	CONSTRAINT facturas_productos_facturas_FK FOREIGN KEY (id_factura) REFERENCES facturas(id)
);
CREATE TABLE productos (
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	nombre TEXT
, stock INTEGER DEFAULT (0) NOT NULL, precio REAL DEFAULT (0.00) NOT NULL, iva REAL DEFAULT (0.00) NOT NULL, articulo TEXT NOT NULL);
DELETE FROM "sqlite_sequence";
INSERT INTO "sqlite_sequence" VALUES('facturas_productos',0);
INSERT INTO "sqlite_sequence" VALUES('facturas',0);
COMMIT;
