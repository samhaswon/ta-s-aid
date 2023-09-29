#!/bin/bash

if [ $# -ne 1 ]; then
	echo "Please give only one argument, the lab name"
	echo "Usage: get_all.sh lab05-unittest"
	exit 1
fi

IDSFILE="ids.txt"

# Look for the file of ids
if [ ! -f $IDSFILE ]; then
    echo "Could not find file: $IDSFILE"
    echo "Please make a file named $IDSFILE with the user ids of each student on one line each."
    exit 1
else
    students_array=( $(cat $IDSFILE) )
fi

echo "Getting: $1"

set -e

for student in "${students_array[@]}"
do
    echo "Getting $student's repo"
    [ -d "./$student-$1" ] || git clone git@gitlab.csc.tntech.edu:csc2310-sp23-students/$student/$student-$1
done

echo -e "\n\n\n"

for student in "${students_array[@]}"
do
    LAST_COMMIT=$(cd $student-$1;git log -1 --format=%cd)
    echo "$student's last commit was $LAST_COMMIT"
    echo
done
