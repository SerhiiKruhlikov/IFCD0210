drop procedure if exists comparador;

delimiter $$

create procedure comparador(primero int, segundo int)
begin

	declare relacion varchar(50);
	
	if primero > segundo then
		set relacion = "ES MAYOR QUE";
	elseif primero = segundo then
		set relacion = "ES IGUAL QUE";
	else
		set relacion = "ES MENOR QUE";
	end if;
	
	select CONCAT_WS(" ",primero,relacion,segundo) as resultado;
	

end $$

delimiter ;


call comparador(1,2);
-- --------------

drop procedure if exists compueba_nulos;

delimiter $$

create procedure compueba_nulos(cadena1 varchar(50), cadena2 varchar(50))
begin

	declare resultado varchar(100);
	declare v1 varchar(50);
	declare v2 varchar(50);
	
	set v1 = ifnull(cadena1,"");
	set v2 = ifnull(cadena2,"");
	
	-- set resultado = ifnull(concat(cadena1,cadena2),"Las cadenas son nulas");
	set resultado = concat(v1,v2);
	select resultado;

end $$

delimiter ;


call compueba_nulos(null,"dos")

-- ------------------
-- 1. Hacer un procedimiento que calcule la rentabilidad de un pedido
drop procedure if exists rentabilidad_pedido;

delimiter $$

create procedure rentabilidad_pedido(v_pedido int)
begin
	-- declare hay_pedido int default -1;
	select count(*) into @total
	from pedido p 
	where p.codigo_pedido = v_pedido;

	if @total > 0 then
		select 
		sum(dp.cantidad * dp.precio_unidad ) - 
		sum(dp.cantidad * p.precio_proveedor ) as rentabilidad
		from detalle_pedido dp 
		join producto p 
		on dp.codigo_producto = p.codigo_producto
		where dp.codigo_pedido = v_pedido;
	else
		select "El pedido no existe";
	end if;

end $$

delimiter ;


call rentabilidad_pedido(1000);











