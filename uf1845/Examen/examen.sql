-- Ejercicio 1: Obtener el nombre y precio de venta de todos los productos.
SELECT p.nombre, p.precio_venta
FROM producto p;


-- Ejercicio 2: Mostrar los clientes que pertenecen a España.
SELECT *
FROM cliente c
WHERE c.pais = "Spain";


-- Ejercicio 3: Mostrar los productos ordenados por precio de venta de mayor a menor.
SELECT *
FROM producto p
ORDER BY p.precio_venta DESC;


-- Ejercicio 4: Mostrar el nombre del cliente y el código de los pedidos que ha realizado.
SELECT c.nombre_cliente , p.codigo_pedido 
FROM cliente c
INNER JOIN pedido p ON c.codigo_cliente = p.codigo_cliente;


-- Ejercicio 5: Mostrar el nombre del cliente, el código del pedido y el nombre del producto comprado.
SELECT c.nombre_cliente, p.codigo_pedido, p2.nombre 
FROM cliente c
INNER JOIN pedido p ON c.codigo_cliente = p.codigo_cliente
INNER JOIN detalle_pedido dp ON p.codigo_pedido = dp.codigo_pedido
INNER JOIN producto p2 ON dp.codigo_producto = p2.codigo_producto;


-- Ejercicio 6: Contar cuántos clientes hay registrados en la base de datos.
SELECT COUNT(*) AS cantidad_clientes FROM cliente c;


-- Ejercicio 7: Calcular el precio medio de venta de los productos.
SELECT AVG(p.precio_venta) AS precio_medio_venta
FROM producto p;


-- Ejercicio 8: Mostrar cuántos productos hay en cada gama de productos.
SELECT g.gama, COUNT(p.codigo_producto) AS cantidad_por_gama
FROM gama_producto g
LEFT JOIN producto p ON g.gama = p.gama
GROUP BY g.gama;


-- Ejercicio 9: Actualizar el teléfono del cliente con código 10 a '600123456'.
UPDATE cliente c
SET c.telefono = '600123456'
WHERE c.codigo_cliente = 10;


-- Ejercicio 10: Eliminar los pagos realizados antes del 1 de enero de 2005.
DELETE FROM pago p WHERE p.fecha_pago < "2005-01-01";
