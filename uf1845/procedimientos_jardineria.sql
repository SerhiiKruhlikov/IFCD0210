use jardineria;

-- Plantilla de procedimiento almacenado

/*
drop procedure if exists <nombre>;

delimiter $$

create procedure <nombre>()
begin


end $$

delimiter ;




*/

drop procedure if exists saludo;

delimiter $$

create procedure saludo()
begin
	select "Bienvenido al maravilloso mundo del SQL.";
end $$

delimiter ;

call saludo();  

-- ---------------------------

drop procedure if exists saludo_p;

delimiter $$

create procedure saludo_p(in v_persona varchar(10))
begin
	select concat("Bienvenido al maravilloso mundo del SQL",
				  ", "
				 ,v_persona) ;
end $$

delimiter ;


call jardineria.saludo_p("Teo");

-- -------------------
-- 1. Devuelve un  listado con el código de oficina y la ciudad donde hay oficinas

drop procedure if exists oficina_ciudad;

delimiter $$

create procedure oficina_ciudad()
begin
	select o.codigo_oficina , o.ciudad 
	from oficina o ;

end $$

delimiter ;


call oficina_ciudad();

-- ------------------
drop procedure if exists oficina_ciudad_pais;

delimiter $$

create procedure oficina_ciudad_pais(v_pais varchar(50), out ok varchar(50))
begin
	select o.codigo_oficina , o.ciudad 
	from oficina o 
	where o.pais = v_pais;
	
	set ok = "Todo perfecto";

end $$

delimiter ;


call oficina_ciudad_pais('España', @resultado);

select @resultado;


-- 2. Procedimieto de insert en gama_producto

drop procedure if exists ins_gama_producto;

delimiter $$

create procedure ins_gama_producto(
							v_gama varchar(50),
							v_desc varchar(100),
							v_desc_html varchar(100),
							v_imagen varchar(256)
							)
begin

	insert into gama_producto (gama,descripcion_texto,descripcion_html,imagen)
	values(v_gama,v_desc,v_desc_html,v_imagen);
	
	select * from gama_producto gp where gp.gama = v_gama;
end $$

delimiter ;


call ins_gama_producto('Nada','Productos de prueba',null,null)



-- -------------------
-- 3. Borrado de una gama

drop procedure if exists del_gama_producto;

delimiter $$

create procedure del_gama_producto(v_gama varchar(50))
begin
	delete from gama_producto where gama = v_gama;

end $$

delimiter ;

-- -------------------------

-- 4. Hacer un procedimiento que dado el identificador 
-- de un pedido muestre todos sus datos

drop procedure if exists resumen_pedido;

delimiter $$

create procedure resumen_pedido(v_codigo_pedido int)
begin

	select c.nombre_cliente,
	p.codigo_pedido ,dp.codigo_producto ,dp.cantidad,
	dp.precio_unidad ,dp.codigo_producto ,prod.gama 
	from pedido p 
	join cliente c 
	on p.codigo_cliente = c.codigo_cliente
	join detalle_pedido dp 
	on p.codigo_pedido = dp.codigo_pedido
	join producto prod
	on dp.codigo_producto = prod.codigo_producto
	where p.codigo_pedido = v_codigo_pedido;


end $$

delimiter ;


-- -------------------
-- 4. Hacer un procedimiento que dado el identificador 
-- de un pedido muestre todos sus datos

drop procedure if exists resumen_pedido_2;

delimiter $$

create procedure resumen_pedido_2(v_codigo_pedido int)
begin

	select * from resumen_pedidos
	where codigo_pedido = v_codigo_pedido;


end $$

delimiter ;

-- -----------------------


call resumen_pedido_2(11)

-- -------------------------

-- 5. Hacer un procedimiento que dado un código de pedido 
-- devuelva el importe total

drop procedure if exists total_pedido;

delimiter $$

create procedure total_pedido(v_cod_pedido int)
begin
	
	select sum(dp.cantidad  * dp.precio_unidad ) as total
	from detalle_pedido dp 
	where dp.codigo_pedido = v_cod_pedido;

end $$

delimiter ;


-- ----------------------
call total_pedido(11)


-- ----------------
-- 6. Hacer un procedimiento que calcule el importe total de
-- compras de un cliente. Debe devolver el nombre del cliente y la cantidad.

drop procedure if exists total_cliente;

delimiter $$

create procedure total_cliente(v_cod_cliente int)
begin
	select c.nombre_cliente ,
	sum(dp.cantidad *dp.precio_unidad ) as total
	from cliente c 
	join pedido p 
	on c.codigo_cliente = p.codigo_cliente
	join detalle_pedido dp 
	on p.codigo_pedido = dp.codigo_pedido
	where c.codigo_cliente = v_cod_cliente
	group by c.nombre_cliente; 

end $$

delimiter ;



call total_cliente(400)

-- -------------------------

-- 7. Hacer un procedimiento que calcule el porcentaje de ventas de un
-- cliente sobre el total de ventas

drop procedure if exists porcentaje_cliente;

delimiter $$

create procedure porcentaje_cliente(v_cod_cliente int)
begin
	select sum(dp.cantidad *dp.precio_unidad ) 
	into @total_global
	from detalle_pedido dp;
	
	select sum(dp.cantidad *dp.precio_unidad ) into @total_cliente
	from pedido p
	join detalle_pedido dp 
	on p.codigo_pedido = dp.codigo_pedido
	where p.codigo_cliente = v_cod_cliente;
	
	select (@total_cliente/@total_global) * 100;

end $$

delimiter ;



call porcentaje_cliente(1)








