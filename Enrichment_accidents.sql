-- Calculate the number of accidents per road segment

SELECT key, sum(ong) as ongeval
INTO sum_ongeval
FROM lines_metong
GROUP BY key
ORDER BY ongeval DESC

-- Join the number of accidents to the existing network

SELECT n.*, l.ongeval as a_ongeval
INTO network2
FROM network22 as n
LEFT JOIN sum_ongeval as l 
On n.key = l.key

-- Adjust the new table with a new column that creates a boolean feature for accidents. 
ALTER TABLE network2 ADD COLUMN ongeval varchar(20);

UPDATE network2
SET ongeval = 'ongeval'
WHERE a_ongeval >= 1

