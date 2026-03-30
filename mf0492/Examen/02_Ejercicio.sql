-- Ejercicio a: Devuelve un listado de todos los pedidos que fueron rechazados en 2009.
SELECT * FROM pedido WHERE estado = 'Rechazado' AND YEAR(fecha_pedido) = 2009;


-- Ejercicio b: Devuelve un listado de todos los pedidos que han sido entregados en el mes de enero de cualquier año.
SELECT * FROM pedido WHERE estado = 'Entregado' AND MONTH(fecha_entrega) = 1;


-- Ejercicio c: Devuelve un listado con todos los productos que pertenecen a la gama ornamentales y que tienen más de 100 unidades en stock. El listado deberá estar ordenado por su precio de venta, mostrando en primer lugar los de mayor precio.
SELECT * FROM producto WHERE gama = 'Ornamentales' AND cantidad_en_stock > 100 ORDER BY precio_venta DESC;


-- Ejercicio d: Devuelve un listado de las diferentes gamas de producto que ha comprado cada cliente.
SELECT DISTINCT c.codigo_cliente, c.nombre_cliente, p.gama
FROM cliente c
INNER JOIN pedido ped ON c.codigo_cliente = ped.codigo_cliente
INNER JOIN detalle_pedido dp ON ped.codigo_pedido = dp.codigo_pedido
INNER JOIN producto p ON dp.codigo_producto = p.codigo_producto
ORDER BY c.codigo_cliente, p.gama;