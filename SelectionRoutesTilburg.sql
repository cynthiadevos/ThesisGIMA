SELECT DISTINCT routeid
INTO routeid_tilburg
FROM routesftw, linknummertilburg
WHERE routesftw.linknummer = linknummertilburg.linknummer;

ALTER TABLE routeid_tilburg
RENAME COLUMN routeid TO routeid1;

SELECT *
INTO routedetailstilburg
FROM routeid_tilburg
LEFT JOIN routesftw
ON routesftw.routeid = routeid_tilburg.routeid1
ORDER BY routeid, sequence;
