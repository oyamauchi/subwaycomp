#!/bin/bash

for file in `ls -1 relations`
do
    echo 'Rebuilding' $file
    ./cli.py nwbr `cat relations/$file` > www/data/${file}.js
done