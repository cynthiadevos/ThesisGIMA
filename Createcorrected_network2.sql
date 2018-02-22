-- Create table that only contains the keys with the shortest length

SELECT key as key2, min(shape_leng) as lengteinm
INTO links_zui_corr3_extra
FROM links_zui_corr3 GROUP BY key 

-- Create shapefile that only contains the keys with the shortest length 

pgsql2shp <requirements> 
"SELECT * 
FROM links_zui_corr3 AS b 
INNER JOIN links_zui_corr3_extra AS e 
ON b.key = e.key2 AND b.shape_leng = e.lengteinm"