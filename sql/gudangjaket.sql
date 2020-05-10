select 
--desc, 
substr("desc",0,CASE when instr("desc",">> KALIAN")<>0 then instr("desc",">> KALIAN") when instr("desc",">>KALIAN")<>0 then instr("desc",">>KALIAN") else length(desc) end), 
--CASE when instr("desc",">> KALIAN")<>0 then instr("desc",">> KALIAN") when instr("desc",">>KALIAN")<>0 then instr("desc",">>KALIAN") else length(desc) end 
from GUDANGJAKET;

select title, colour, "size", cast(replace(REPLACE(price,'Rp',''),'.','') as integer)+10000, 
REPLACE(weight,'gr',''), image,
substr("desc",0,CASE when instr("desc",">> KALIAN")<>0 then instr("desc",">> KALIAN") when instr("desc",">>KALIAN")<>0 then instr("desc",">>KALIAN") else length(desc) end)
from GUDANGJAKET_SESI3 where colour <> 'XXL';

select * from GUDANGJAKET_MASTER;
select * from master_product_gudangjaket;

select * from GUDANGJAKET_MASTER a left join GUDANGJAKET_IMAGES b on a.name=b.name where b.name is null;
select * from GUDANGJAKET_IMAGES;
select * from GUDANGJAKET_DESC;
select * from GUDANGJAKET_WEIGHT;
select * from GUDANGJAKET_VARIANT;

select DISTINCT
a.name,
cast(replace(REPLACE(a.price,'Rp',''),'.','') as integer)+(cast(replace(REPLACE(a.price,'Rp',''),'.','') as integer)*0.15) price,
substr(b.images,0,CASE when instr(b.images,">> KALIAN")<>0 then instr(b.images,">> KALIAN") when instr(b.images,">>KALIAN")<>0 then instr(b.images,">>KALIAN") else length(b.images) end) desc,
replace(c.images,'gr','') weight,
d.images variant,
e.images sizes,
f.images1,
f.images2,
f.images3,
f.images4,
f.images5
from GUDANGJAKET_MASTER a
inner join GUDANGJAKET_DESC b on a.name=b.name
inner join GUDANGJAKET_WEIGHT c on a.name=c.name
inner join (select * from GUDANGJAKET_VARIANT where images not in ('L','XL','XXL')) d on a.name=d.name
inner join (select * from GUDANGJAKET_VARIANT where images in ('L','XL','XXL')) e on a.name=e.name
inner join GUDANGJAKET_IMAGES f on a.name=f.name
;

select * from GUDANGJAKET_MASTER where name='JAKET PARKA COWOK';