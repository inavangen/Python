#!/bin/bash
# Oppgave 1.4 Compress

# First check if user has asked for help
if [ $1 == "-h" ] || [ $1 == "-help" ]; then
	echo "compress.sh compresses files of a minimum size. The script takes two arguments."
	echo "    - 1st argument is a path to the directory."
	echo "    - 2nd argument is the minimum file size you of the files needs to have." 
	echo "    - Example: compress.sh ~Desktop/Some_Folder/ 150"
	exit 1
# Then check if correct number of args
elif [ "$#" -ne 2 ]; then
   echo "Wrong number of arguments. Type -h or -help"
   exit 1
fi

echo "Choosed path: $1 and only want to compress files with minimum size: $2"

find $1 -size +$2k -type f ! -name '*.gz' -exec gzip "{}" \;
gzip packed_files.tar
echo "Files sucessfully packed"