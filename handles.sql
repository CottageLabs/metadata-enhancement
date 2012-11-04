COPY (

SELECT handle.handle
FROM handle
    JOIN item ON handle.resource_id = item.item_id 
WHERE handle.resource_type_id = 2
    AND item.in_archive IS TRUE

) TO '/var/lib/postgresql/handles.csv' WITH CSV HEADER;
