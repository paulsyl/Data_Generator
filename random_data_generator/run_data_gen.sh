#!/bin/bash

if [ -z ${DATA_DICTIONARY} ]; then
    # Check that a Data Dictionary Schema has been provided
    echo "DATA_DICTIONARY not provided"
    exit
fi

if [ -z ${OUTPUT_TYPE} ]; then
    # Check the output type has been supplied, if none supplied, output to CSV.
    echo "OUTPUT_TYPE not provided"
    ${OUTPUT_TYPE} = 'C'
fi

echo "Data Gen Started : `date`"
python make_relational_data.py -dd ${DATA_DICTIONARY} -ot ${OUTPUT_TYPE} 
echo "Data Gen Finished : `date`"
