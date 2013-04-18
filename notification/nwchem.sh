#!/bin/bash

# this should set FILELIST SUBMITTER and TRANSACTION
eval `./filestream`

MYEMSL_MOUNT="/archive/kfox2/archivetest"
WORKING_DIR="$PWD/dft_siosi3/$TRANSACTION"
mkdir -p $WORKING_DIR

cat $FILELIST | 
sed "s#/myemsl#$MYEMSL_MOUNT#" |
grep '\.nw$' |
while read file
do
	cp $file $WORKING_DIR/input.nw
done
/home/kfox/test.sh $TRANSACTION $PROPOSAL
