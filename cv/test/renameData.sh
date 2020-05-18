#!/bin/bash


# Rename all the files in a directory from their original name to sequential name 01, 02, 03, 04...
# Ordering is completely random
# Do not change files, just copy renamed versions to renameDataOutput folder...

if [ -z $1 ]
then
	echo "Give directory path as argument"
fi

mkdir -p renameDataOutput

counter=0
for filename in $1/*
do
	echo "Processing $filename..."

	dest_name=$counter
	if [ $counter -lt 10 ]
	then
		dest_name=$(echo "0$counter")
	fi

	extension="${filename##*.}"

	cp "$filename" "renameDataOutput/$dest_name.$extension"


	counter=$(($counter+1))
done


	
