-- Calculate the number of traffic lights per road segment

SELECT key, count(aantstopl) as stoplicht
INTO sum_stoplicht
FROM lines_metstoplichten
GROUP BY key
ORDER BY stoplicht DESC


-- Join the number of traffic lights to the existing network

SELECT n.*, l.stoplicht as a_vrklicht
INTO network3
FROM network2 as n
LEFT JOIN sum_stoplicht as l 
On n.key = l.key

-- Adjust the new table with a new column that creates a boolean feature for accidents. 
ALTER TABLE network3 ADD COLUMN vrklicht varchar(20);

UPDATE network3
SET vrklicht = 'verkeerslicht'
WHERE a_vrklicht >= 1

UPDATE network3
SET vrklicht = 'verkeerslicht'
WHERE krp_type LIKE 'kruispunt met VR%'
