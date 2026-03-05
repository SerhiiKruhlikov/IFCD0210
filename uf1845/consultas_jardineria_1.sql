-- Consultas sobre una tabla
-- -----------------------

-- 1. Devuelve un listado con el código de oficina y la ciudad donde hay oficinas.

select o.codigo_oficina ,o.ciudad 
from oficina o ;


-- 2. Devuelve un listado con la ciudad y el teléfono de las oficinas de España.

select o.ciudad , o.telefono 
from oficina o
where LOWER(o.pais) = "españa"


-- 3. Devuelve un listado con el nombre, apellidos y email de los empleados cuyo jefe tiene un código de jefe igual a 7.

select e.nombre ,e.apellido1 , e.apellido2 ,e.email 
from empleado e 
where e.codigo_jefe = 7;

-- 4. Devuelve el nombre del puesto, nombre, apellidos y email del jefe de la empresa.

select e.puesto,e.nombre , e.apellido1 ,e.apellido2 ,e.email 
from empleado e 
where isnull(e.codigo_jefe)

-- 5. Devuelve un listado con el nombre, apellidos y puesto de aquellos empleados que no sean representantes de ventas.

select e.nombre ,e.apellido1, e.apellido2, e.puesto 
from empleado e 
where not e.puesto = 'Representante ventas'


select
	CONCAT_WS(" ",e.nombre , e.apellido1, e.apellido2) as nombre_completo,
	e.puesto
from
	empleado e
where
	not e.puesto = 'Representante ventas'

	
select
	CONCAT_WS(" ",e.nombre , e.apellido1, e.apellido2) as nombre_completo,
	e.puesto
from
	empleado e
where
	e.puesto like "%dir%" 	
	
	

-- 6. Devuelve un listado con el nombre de los todos los clientes españoles.
	
	select c.nombre_cliente, c.pais
	from cliente c 
	where c.pais = "spain"
	
-- 7. Devuelve un listado con los distintos estados por los que puede pasar un pedido.
	
	select distinct p.estado  from pedido p 
	
-- 8. Devuelve un listado con el código de cliente de aquellos clientes que realizaron algún pago en 2008. Tenga en cuenta que deberá eliminar aquellos códigos de cliente que aparezcan repetidos. 
-- Resuelva la consulta:
-- 	• Utilizando la función YEAR de MySQL.
-- 	• Utilizando la función DATE_FORMAT de MySQL.
-- 	• Sin utilizar ninguna de las funciones anteriores.
	
select distinct p.codigo_cliente,DATE_FORMAT(p.fecha_pago ,"%Y") as anno_pago
from pago p 
where year(p.fecha_pago) = 2008

select distinct p.codigo_cliente 
from pago p 
where DATE_FORMAT(p.fecha_pago ,"%Y") = 2008

select * from pago p 
where p.fecha_pago >= "2008-01-01" and p.fecha_pago <= "2008-12-31"

select * from pago p 
where p.fecha_pago BETWEEN "2008-01-01" and "2008-12-31"

select SUBSTR(p.fecha_pago ,1,4) from pago p

	
-- 9. Devuelve un listado con el código de pedido, código de cliente, fecha esperada y fecha de entrega de los pedidos que no han sido entregados a tiempo.

select * from pedido p 
where p.fecha_entrega > p.fecha_esperada 

-- 10. Devuelve un listado con el código de pedido, código de cliente, fecha esperada y fecha de entrega de los pedidos cuya fecha de entrega ha sido al menos dos días antes de la fecha esperada.
-- 	• Utilizando la función ADDDATE de MySQL.
-- 	• Utilizando la función DATEDIFF de MySQL.
-- 	• ¿Sería posible resolver esta consulta utilizando el operador de suma + o resta -?

SELECT * 
from  pedido p 
where p.fecha_entrega + INTERVAL 2 day <= p.fecha_esperada 


-- Consultas multitabla (Composición interna)
-- ----------------------------------------


-- 1. Obtén un listado con el nombre de cada cliente y el nombre y apellido de su representante de ventas.

select
	c.nombre_cliente ,
	CONCAT_WS(" ", e.nombre , e.apellido1 , e.apellido2 ) as nombre_repr
from
	empleado e
join cliente c 
on
	e.codigo_empleado = c.codigo_empleado_rep_ventas 


-- 2. Muestra el nombre de los clientes que hayan realizado pagos junto con el nombre de sus representantes de ventas.

select distinct
	c.nombre_cliente ,
	CONCAT_WS(" ", e.nombre , e.apellido1 , e.apellido2 ) as nombre_repr
from
cliente c join pago p 
on c.codigo_cliente = p.codigo_cliente
join empleado e 
on c.codigo_empleado_rep_ventas = e.codigo_empleado
	
-- 3. Muestra el nombre de los clientes que no hayan realizado pagos junto con el nombre de sus representantes de ventas.



-- 4. Devuelve el nombre de los clientes que han hecho pagos y el nombre de sus representantes junto con la ciudad de la oficina a la que pertenece el representante.

select distinct c.nombre_cliente ,
	CONCAT_WS(" ", e.nombre , e.apellido1 , e.apellido2 ) as nombre_repr, 
	o.ciudad 
from cliente c 
join pago p 
on c.codigo_cliente = p.codigo_cliente
join empleado e 
on c.codigo_empleado_rep_ventas = e.codigo_empleado
join oficina o 
on e.codigo_oficina = o.codigo_oficina



-- 5. Devuelve el nombre de los clientes que no hayan hecho pagos y el nombre de sus representantes junto con la ciudad de la oficina a la que pertenece el representante.




-- 6. Lista la dirección de las oficinas que tengan clientes en Fuenlabrada.

select distinct c.nombre_cliente , c.ciudad, o.codigo_oficina  ,  o.linea_direccion1 
from cliente c 
join empleado e 
on c.codigo_empleado_rep_ventas = e.codigo_empleado
join oficina o 
on e.codigo_oficina = o.codigo_oficina
WHERE c.ciudad like "%bra%"


-- 7. Devuelve el nombre de los clientes y el nombre de sus representantes junto con la ciudad de la oficina a la que pertenece el representante.



-- 8. Devuelve un listado con el nombre de los empleados junto con el nombre de sus jefes.

select
	e.codigo_empleado ,
	e.nombre ,
	e.apellido1 ,
	e.apellido2,
	jefe.codigo_empleado as cod_jefe,
	jefe.nombre as nombre_jefe,
	jefe.apellido1 as ape1_jefe,
	jefe.apellido2 ape2_jefe
from
	empleado jefe
join empleado e
on
	jefe.codigo_empleado = e.codigo_jefe


-- 9. Devuelve un listado que muestre el nombre de cada empleado, el nombre de su jefe y el nombre del jefe de sus jefe.
	
	
	
-- 10. Devuelve el nombre de los clientes a los que no se les ha entregado a tiempo un pedido.
	
	select distinct c.nombre_cliente   
	from pedido p join cliente c 
	on p.codigo_cliente = c.codigo_cliente 
	where p.fecha_entrega > p.fecha_esperada 
	and p.estado = 'Entregado'
	
-- 11. Devuelve un listado de las diferentes gamas de producto que ha comprado cada cliente.

	select distinct c.nombre_cliente ,prod.gama 
	from cliente c 
	join pedido p 
	on c.codigo_cliente = p.codigo_cliente
	join detalle_pedido dp 
	on p.codigo_pedido = dp.codigo_pedido
	join producto prod
	on dp.codigo_producto = prod.codigo_producto
	
	
	
-- Consultas multitabla (Composición externa)
-- ----------------------------------------------

-- 1. Devuelve un listado que muestre solamente los clientes que no han realizado ningún pago.
	
	select
	c.codigo_cliente ,
	p.codigo_cliente
from
	cliente c
left join pago p 
on
	c.codigo_cliente = p.codigo_cliente
where
	p.codigo_cliente is null

-- 2. Devuelve un listado que muestre solamente los clientes que no han realizado ningún pedido.
	
	select c.nombre_cliente 
	from cliente c left join pedido p 
	on c.codigo_cliente = p.codigo_cliente
	where p.codigo_cliente is null
	
	
-- 3. Devuelve un listado que muestre los clientes que no han realizado ningún pago y los que no han realizado ningún pedido.
	
	select c.nombre_cliente 
	from cliente c left join pedido p 
	on c.codigo_cliente = p.codigo_cliente
	where p.codigo_cliente is null
	UNION 
	select c.nombre_cliente
	from
	cliente c left join pago p 
	on 	c.codigo_cliente = p.codigo_cliente
	where 	p.codigo_cliente is null
	
	
-- 4. Devuelve un listado que muestre solamente los empleados que no tienen una oficina asociada.
	
	
	
-- 5. Devuelve un listado que muestre solamente los empleados que no tienen un cliente asociado.
	
	select e2.codigo_empleado , c.codigo_cliente 
	from empleado e2  
	left join cliente c 
	on e2.codigo_empleado = c.codigo_empleado_rep_ventas
	where c.codigo_empleado_rep_ventas is null
	
	
	
-- 6. Devuelve un listado que muestre solamente los empleados que no tienen un cliente asociado junto con los datos de la oficina donde trabajan.
	
	select e2.codigo_empleado , c.codigo_cliente , o.*
	from empleado e2  
	left join cliente c 
	on e2.codigo_empleado = c.codigo_empleado_rep_ventas
	join oficina o 
	on e2.codigo_oficina = o.codigo_oficina 
	where c.codigo_empleado_rep_ventas is null	
	
-- 7. Devuelve un listado que muestre los empleados que no tienen una oficina asociada y los que no tienen un cliente asociado.
	
	
	
-- 8. Devuelve un listado de los productos que nunca han aparecido en un pedido.
	
	select p.codigo_producto
	from producto p 
	left join detalle_pedido dp 
	on p.codigo_producto = dp.codigo_producto
	WHERE dp.codigo_producto is null
	
-- 9. Devuelve un listado de los productos que nunca han aparecido en un pedido. El resultado debe mostrar el nombre, la descripción y la imagen del producto.
	
	
-- 10. Devuelve las oficinas donde no trabajan ninguno de los empleados que hayan sido los representantes de ventas de algún cliente que haya realizado la compra de algún producto de la gama Frutales.
	
	
	
-- 11. Devuelve un listado con los clientes que han realizado algún pedido pero no han realizado ningún pago.
	
	SELECT distinct c.codigo_cliente ,c.nombre_cliente 
	FROM cliente c 
	left join pago p 
	on c.codigo_cliente = p.codigo_cliente
	join pedido pd
	on c.codigo_cliente = pd.codigo_cliente 
	where p.codigo_cliente is null
	
	
-- 12. Devuelve un listado con los datos de los empleados que no tienen clientes asociados y el nombre de su jefe asociado.

	select e.codigo_empleado , e.nombre ,
	jefes.codigo_empleado as cod_jefe,
	jefes.nombre as nombre_jefe
	from empleado e 
	left join cliente c 
	on e.codigo_empleado = c.codigo_empleado_rep_ventas
	join empleado jefes
	on e.codigo_jefe = jefes.codigo_empleado 
	where c.codigo_empleado_rep_ventas is null
	
	
-- Consultas resumen
-- --------------------

-- 1. ¿Cuántos empleados hay en la compañía?
	
	select count(*) as num_empleados
	from empleado e 
	
-- 2. ¿Cuántos clientes tiene cada país?
	
	select c.pais ,count(*) as total
	from cliente c 
	group by c.pais
	
	
-- 3. ¿Cuál fue el pago medio en 2009?
	
	select avg(p.total) as promedio 
	from pago p
	where year(p.fecha_pago ) = "2009"
	
	select year(p.fecha_pago ) as annio,
	avg(p.total) as promedio 
	from pago p
	group by annio 
	order by annio desc
	limit 1

	
	select year(p.fecha_pago ) as annio,
	avg(p.total) as promedio 
	from pago p
	where year(p.fecha_pago ) in (2006,2009,2008)
	group by annio 
	
-- 4. ¿Cuántos pedidos hay en cada estado? Ordena el resultado de forma descendente por el número de pedidos.
	
	select count(*) as total_pedidos, estado
	from pedido
	group by estado
	order by total_pedidos desc
	
	
-- 5. Calcula el precio de venta del producto más caro y más barato en una misma consulta.
	
	select max(p.precio_venta) as maximo,
	min(p.precio_venta) as minimo
	from producto p 
	
	-- Producto más rentable
	
	select
	p.codigo_producto,
	p.nombre ,
	(p.precio_venta -p.precio_proveedor) as margen
from
	producto p
order by
	margen desc
limit 1
	
	
-- 6. Calcula el número de clientes que tiene la empresa.

select count(*) as total_clientes
from cliente c 


-- 7. ¿Cuántos clientes existen con domicilio en la ciudad de Madrid?

select count(*) from cliente c 
where c.ciudad ="Madrid"

-- 8. ¿Calcula cuántos clientes tiene cada una de las ciudades que empiezan por M?

select
	c.ciudad,
	count(*) as total
from
	cliente c
where
	c.ciudad like "M%"
group by
	c.ciudad
order by
	total desc

-- 9. Devuelve el nombre de los representantes de ventas y el número de clientes al que atiende cada uno.
	
	SELECT
	e.nombre ,
	count(c.codigo_cliente) as total
from
	empleado e
join cliente c 
	on
	e.codigo_empleado = c.codigo_empleado_rep_ventas
group by
	e.nombre
order by
	total desc
	
	
-- 10. Calcula el número de clientes que no tiene asignado representante de ventas.
	
	
	
-- 11. Calcula la fecha del primer y último pago realizado por cada uno de los clientes. El listado deberá mostrar el nombre y los apellidos de cada cliente.
	
	select 
	min(p.fecha_pago ) as minimo,
	max(p.fecha_pago ) as maximo,
	sum(p.total ) as importe,
	c.nombre_cliente 
	from cliente c 
	join pago p 
	on c.codigo_cliente = p.codigo_cliente
	group by c.nombre_cliente 
	
	
	
-- 12. Calcula el número de productos diferentes que hay en cada uno de los pedidos.
-- 13. Calcula la suma de la cantidad total de todos los productos que aparecen en cada uno de los pedidos.

-- 14. Devuelve un listado de los 20 productos más vendidos y el número total de unidades que se han vendido de cada uno. El listado deberá estar ordenado por el número total de unidades vendidas.
-- 15. La facturación que ha tenido la empresa en toda la historia, indicando la base imponible, el IVA y el total facturado. La base imponible se calcula sumando el coste del producto por el número de unidades vendidas de la tabla detalle_pedido. El IVA es el 21 % de la base imponible, y el total la suma de los dos campos anteriores.
-- 16. La misma información que en la pregunta anterior, pero agrupada por código de producto.
-- 17. La misma información que en la pregunta anterior, pero agrupada por código de producto filtrada por los códigos que empiecen por OR.
-- 18. Lista las ventas totales de los productos que hayan facturado más de 3000 euros. Se mostrará el nombre, unidades vendidas, total facturado y total facturado con impuestos (21% IVA).
-- 19. Muestre la suma total de todos los pagos que se realizaron para cada uno de los años que aparecen en la
tabla pagos.








