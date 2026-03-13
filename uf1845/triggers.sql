-- Triggers
-- -------------------------------------
/*

drop trigger if exists <nombre>
delimiter $$

CREATE trigger <nombre>
<before|after> <insert|update|delete> on <tabla>
for each row
begin
	
end $$

delimiter ;
*/


/*
delimiter $$

CREATE trigger trg_primero
before insert on gama_producto
for each row
begin
	if NEW.descripcion_texto is null then
		set NEW.descripcion_texto = "Sin descripción";
	end if;
	
end $$

delimiter ;




insert into gama_producto (gama)
values('prueba_trigger')

*/

-- --------------------------------------------
/*
drop trigger if exists trg_prueba_upd;
delimiter $$


CREATE trigger trg_prueba_upd
before update on gama_producto
for each row
begin
	declare desc_html varchar(50) default  "<h1>producto</h1>";
	if NEW.descripcion_texto = OLD.descripcion_texto then
		set NEW.descripcion_html = desc_html;
	end if;

	insert into tabla_log(texto)
	values(concat_ws(" ","Gama Producto Actualizado:",NEW.gama));
	
end $$

delimiter ;


insert into gama_producto (gama)
values('prueba_trigger');

update gama_producto gp 
set gp.descripcion_texto = 'Hola___'
where gp.gama ='prueba_trigger';

*/

-- -----------------------------
/*
drop trigger if exists trg_comprobar_cantidad;

delimiter $$

CREATE trigger trg_comprobar_cantidad
before update on producto
for each row
begin
	if NEW.cantidad_en_stock > OLD.cantidad_en_stock then
		SIGNAL SQLSTATE '45000' 
		SET MESSAGE_TEXT = "No se puede sacar más de lo que hay.";
	else
		set NEW.cantidad_en_stock =  
		OLD.cantidad_en_stock - NEW.cantidad_en_stock;
	end if;
end $$

delimiter ;


update producto set cantidad_en_stock = -15
where codigo_producto = '11679';

*/
-- -----------------------
-- crear un trigger after insert en detalle_pedido que acualice 
-- el campo cantidad_en_stock descontando la cantidad vendida


drop trigger if exists trg_actualiza_stock; 
delimiter $$

CREATE trigger trg_actualiza_stock
after insert on detalle_pedido
for each row
begin
	update producto 
	set cantidad_en_stock = cantidad_en_stock - NEW.cantidad
	where codigo_producto = NEW.codigo_producto;
end $$

delimiter ;


insert into detalle_pedido(codigo_pedido,
							codigo_producto,
							cantidad,
							precio_unidad,
							numero_linea)
values(126,'11679',100,101,99);










