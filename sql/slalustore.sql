select
a.name,
cast(replace(REPLACE(a.price,'Rp',''),'.','') as integer)+5000 price,
b.images descr,
replace(c.images,'gr','') weight,
--d.images,
'https://bluploads.smvi.co'||substr(f.images1,instr(f.images1,'/39726631_'),LENGTH(f.images1)+1-instr(f.images1,'/39726631_'))||'.jpg',
'https://bluploads.smvi.co'||substr(case when instr(f.images2,'data:image') = 1 then null else f.images2 END,instr(case when instr(f.images2,'data:image') = 1 then null else f.images2 END,'/39726631_'),LENGTH(case when instr(f.images2,'data:image') = 1 then null else f.images2 END)+1-instr(case when instr(f.images2,'data:image') = 1 then null else f.images2 END,'/39726631_'))||'.jpg',
'https://bluploads.smvi.co'||substr(case when instr(f.images3,'data:image') = 1 then null else f.images3 END,instr(case when instr(f.images3,'data:image') = 1 then null else f.images3 END,'/39726631_'),LENGTH(case when instr(f.images3,'data:image') = 1 then null else f.images3 END)+1-instr(case when instr(f.images3,'data:image') = 1 then null else f.images3 END,'/39726631_'))||'.jpg',
'https://bluploads.smvi.co'||substr(case when instr(f.images4,'data:image') = 1 then null else f.images4 END,instr(case when instr(f.images4,'data:image') = 1 then null else f.images4 END,'/39726631_'),LENGTH(case when instr(f.images4,'data:image') = 1 then null else f.images4 END)+1-instr(case when instr(f.images4,'data:image') = 1 then null else f.images4 END,'/39726631_'))||'.jpg',
'https://bluploads.smvi.co'||substr(case when instr(f.images5,'data:image') = 1 then null else f.images5 END,instr(case when instr(f.images5,'data:image') = 1 then null else f.images5 END,'/39726631_'),LENGTH(case when instr(f.images5,'data:image') = 1 then null else f.images5 END)+1-instr(case when instr(f.images5,'data:image') = 1 then null else f.images5 END,'/39726631_'))||'.jpg'
from SLALUKSTORE_MASTER a 
inner JOIN SLALUKSTORE_DESC b on a.name=b.name
inner join SLALUKSTORE_WEIGHT c on a.name=c.name
inner join SLALUKSTORE_IMAGES f on a.name=f.name
--left join SLALUKSTORE_VARIANT d on a.name=d.name
--where lower(a.name) like '%case%'
;

select * from SLALUKSTORE_IMAGES;
select * from SLALUKSTORE_WEIGHT;
select * from SLALUKSTORE_VARIANT;
select * from SLALUKSTORE_DESC;

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
from SLALUKSTORE_MASTER a
inner join SLALUKSTORE_DESC b on a.name=b.name
inner join SLALUKSTORE_WEIGHT c on a.name=c.name
left join (select * from SLALUKSTORE_VARIANT where images not in ('L','XL','XXL')) d on a.name=d.name
left join (select * from SLALUKSTORE_VARIANT where images in ('L','XL','XXL')) e on a.name=e.name
inner join SLALUKSTORE_IMAGES f on a.name=f.name;