COPY (

SELECT item2bundle.item_id, bitstreamformatregistry.mimetype
    FROM bitstream 
        JOIN bundle2bitstream ON bitstream.bitstream_id = bundle2bitstream.bitstream_id 
        JOIN item2bundle ON bundle2bitstream.bundle_id = item2bundle.bundle_id 
        JOIN bitstreamformatregistry ON bitstream.bitstream_format_id = bitstreamformatregistry.bitstream_format_id
        JOIN bundle ON bundle2bitstream.bundle_id = bundle.bundle_id
    WHERE bundle.name = 'ORIGINAL'

) TO '[path/to/out.csv]' WITH CSV HEADER;