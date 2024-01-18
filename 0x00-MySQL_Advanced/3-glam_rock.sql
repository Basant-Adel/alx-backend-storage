-- Write a SQL script that lists all bands with Glam rock

SELECT band_name, 
CASE 
    WHEN split IS NULL 
    THEN 2022 - formed
    ELSE split - formed
END AS lifespan
FROM metal_bands
WHERE STYLE like '%Glam rock%'
ORDER BY lifespan DESC;
