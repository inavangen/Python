#!/bin/bash
# Oppgave 1.4 decompress

if [ $1 == "-h" ] || [ $1 == "-help" ]; then
	echo "decompress.sh compresses .gz files of a given math. "
	echo "    - The script takes a Path as an argument."
	echo "    - Example: compress.sh ~Desktop/Some_Folder/"
	exit 1
# Then check if correct number of args
elif [ "$#" -ne 1 ]; then
   echo "Wrong number of arguments. Type -h or -help"
   exit 1
fi


echo "Choosed path: $1" 

find $1 -name '*.gz' -exec gunzip "{}" \;

echo "Files sucessfully unpacked"