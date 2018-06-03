#!/bin/bash

# echo "1."
# python zipper.py ./dataset1/Demospongiae1.txt ./dataset1/Demospongiae1_output.txt
# echo "2."
# python zipper.py ./dataset1/Demospongiae2.txt ./dataset1/Demospongiae2_output.txt
# echo "3."
# python zipper.py ./dataset1/Demospongiae3.txt ./dataset1/Demospongiae3_output.txt
# echo "4."
# python zipper.py ./dataset1/Demospongiae4.txt ./dataset1/Demospongiae4_output.txt
# echo "5."
# python zipper.py ./dataset1/Demospongiae5.txt ./dataset1/Demospongiae5_output.txt

#python file_divider.py ./dataset4/Demospongiae.txt

i=1
for file in ./dataset4/*
do
    echo "$i."
    python zipper.py $file "$file-result"
    cat $file <(echo) "$file-result" > "$file-output"
    ((i++))
done

#cat $(ls ./dataset4/*-output) > ./dataset2/Hexactinellida-output.txt
