
select * from LARIS88_MASTER;

select * from LARIS88_CATEGORY order by images;
select * from LARIS88_IMAGES where images1 like 'data%';
select * from LARIS88_WEIGHT;
select * from LARIS88_DESC;
select * from LARIS88_VARIANT;


select count(*) from LARIS88_MASTER a left join LARIS88_IMAGES b on a.name=b.name where b.name is null;


select * from LARIS88_MASTERCAT;