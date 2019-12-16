#!/bin/bash

# Script to create weekly report directory by correct links and files
# Why? Files in common folder does not appear in overleaf as a single week can be uploaded each time.

## What it does?
# 1) Unzip the template and create the WeekX directory
# 2) Create symbolic links for each dependency to ../common folder
# 3) Create the WeekX.zip file to upload to overleaf

# Also add symbolic links to ./.gitignore please


# Check if week number is given,
if [ -z $1 ]
then
	echo "Use : "
	echo "bash CreateNextWeek.sh WeekX # where WeekX is the week number of the next, Week3 for example"
	exit 1
fi

dirName=$1

echo "Creating week $dirName"
# 1)
mkdir $dirName
cd $dirName
cp -r ../ReportTemplateWeekly/* ./
# 2)
ln -s ../common/titlepage.tex customTitlepageFile.tex
ln -s ../common/METU_Logo.jpg METU_Logo.jpg
#gitignore
echo "$dirName/titlepage.tex" >> ../.gitignore
echo "$dirName/METU_Logo.jpg" >> ../.gitignore
# 3)
cd ..
zip Week$dirName.zip $dirName -r
chmod 777 $dirName -R
rm -r $dirName
