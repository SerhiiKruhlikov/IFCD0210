/*
 * 
drop procedure if exists <nombre>;

delimiter $$

create procedure <nombre>()
begin


end $$

delimiter ;
 */

-- 1. Crear un procedimiento que reciba el código de un cliente y
-- devuelva la cantidad de pedidos que ha realizado
/*
drop procedure if exists pedidos_por_cliente;

delimiter $$

create procedure pedidos_por_cliente(v_cod_cliente int)
begin
	select count(*) as total
	from pedido p 
	where p.codigo_cliente = v_cod_cliente;

end $$

delimiter ;

call pedidos_por_cliente(3)
*/
-- ---------------------
-- 2. Hacer un procedimiento que reciba el código de un cliente y
-- devuelva mediante un parámetro de salida el total pagado por ese cliente
-- en la tabla pago.

/*
drop procedure if exists total_pagado;

delimiter $$

create procedure total_pagado(
								in v_cod_cliente int , 
								out total_pagos decimal(10,2))
begin

	select sum(p.total) into total_pagos 
	from pago p 
	where p.codigo_cliente = v_cod_cliente;

end $$

delimiter ;

 

call total_pagado(3,@total);

select @total;

*/

-- 3. Crear un procedimiento que reciba una gama de 
-- producto y devuelva el número de productos de esa gama.
-- Si la gama no existe debe devolver "NO EXISTE".
/*
drop procedure if exists contar_gama;

delimiter $$

create procedure contar_gama(v_gama varchar(50))
begin
	declare v_existe int;

	select count(*) into v_existe
	from producto p 
	where p.gama = v_gama;
	
	if v_existe = 0 then
		select "NO EXISTE" as respuesta;
	else
		select v_existe as respuesta;
	end if;
	

end $$

delimiter ;


call contar_gama("Frutales")
*/

-- 4. Hacer un procedimiento que inserte una nueva gama de producto, 
-- de forma que si ya existe una gama con la misma PK sedebe cancelar 
-- la opearción y devolver un mensaje de error. Si funciona devolver OK.
/*
drop procedure if exists ins_gama_producto;

delimiter $$

create procedure ins_gama_producto(
									v_gama varchar(50),
									v_desc text,
									v_desc_html text ,
									v_imagen varchar(256))
begin
	declare v_existe int;
	declare v_respuesta varchar(50)  default "OK";

	select count(*) into v_existe
	from gama_producto gp 
	where gp.gama = v_gama;
	
	if v_existe = 0 then -- No existe
		insert into gama_producto(
								gama,
								descripcion_texto,
								descripcion_html,
								imagen)
		values(v_gama,v_desc,v_desc_html,v_imagen);
	else
		set v_respuesta = "El elemento ya existe";
	end if;
	
	select v_respuesta as respuesta;
	
end $$

delimiter ;

call ins_gama_producto('Yerbas',null,null,null);
*/

-- 5. Hacer un procedimiento que dado un cliente devuelva 
-- el importe medio de sus pedidos.

drop procedure if exists importe_medio;

delimiter $$

create procedure importe_medio(v_cod_cliente int)
begin
select 
	avg(dp.cantidad * dp.precio_unidad ) as promedio
	from pedido p 
	join detalle_pedido dp 
	on p.codigo_pedido = dp.codigo_pedido
	where p.codigo_cliente = v_cod_cliente;

end $$

delimiter ;

call importe_medio(1)















