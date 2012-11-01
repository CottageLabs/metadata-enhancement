COPY (

SELECT item2bundle.item_id, bitstream.name 
FROM item2bundle 
    JOIN bundle ON item2bundle.bundle_id = bundle.bundle_id 
    JOIN bundle2bitstream ON bundle.bundle_id = bundle2bitstream.bundle_id 
    JOIN bitstream ON bundle2bitstream.bitstream_id = bitstream.bitstream_id 
WHERE bundle.name = 'URL_BUNDLE';

) TO '[path/to/out.csv]' WITH CSV HEADER;