#!/bin/bash

for n in `seq 0 16384`;
do
    original="/dev/shm/$n.original"
    head --bytes $n < /dev/urandom > $original
    md5original=$(md5sum $original | cut -c -32)
    #echo $md5original
    encoded="/dev/shm/$n.encoded"
    ./base91 -e $original $encoded
    decoded="/dev/shm/$n.decoded"
    ./base91 -d $encoded $decoded
    md5decoded=$(md5sum $decoded | cut -c -32)
    if [[ "$md5decoded" != "$md5original" ]];
    then
        echo "Mismatch:$md5original ~ $md5decoded";
        exit 1
    fi
    rm $original $encoded $decoded
done

echo PASS
