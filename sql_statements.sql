CREATE TABLE my_osm_new_adresses (node_id integer NOT NULL , adress TEXT); 

Select AddGeometryColumn('my_osm_new_adresses', 'geom', 3857, 'POINT', 'XY');	

CREATE TABLE my_osm_addresses_merged_a 
AS SELECT a.node_id as node_id, 
a.Geometry as geometry, group_concat(a.v, ' ') as address 
FROM my_osm_adresses as a group by a.node_id;

INSERT INTO my_osm_new_adresses (node_id,adress,geom) 
SELECT a.node_id,a.address, ST_Transform(a.geometry, 3857)as geom 
FROM my_osm_addresses_merged_a as a;

SELECT CreateSpatialIndex('my_osm_new_adresses', 'geom');



