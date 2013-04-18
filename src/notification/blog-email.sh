#!/bin/bash

# this should set FILELIST SUBMITTER and TRANSACTION
eval `./filestream`

(
cat <<EOF
to:Kevin.Fox@pnnl.gov, myemsldemo@gmail.com, myemsldemo2@gmail.com
from:MyEMSL<myemsl@emsl.pnnl.gov>
subject:MyEMSL Proposal $PROPOSAL Activity

Proposal $PROPOSAL has new files available in MyEMSL.

For discussion please use the following link:
http://myemsl-dev5.emsl.pnl.gov/wordpress/

The data is available here:
https://myemsl-dev1.emsl.pnl.gov/myemsl/files/transaction/$TRANSACTION/data

Added or Changed Files
=====================================
EOF
sed 's#^/myemsl/[0-9][0-9]*/bundle/[0-9][0-9]*/##' $FILELIST
) | sendmail -t 

(
grep '.jpg$' $FILELIST
) | while read line
do 
	echo "$line" | sed 's#^/myemsl/[0-9][0-9]*/bundle/\([0-9][0-9]*\)/\(.*\)#<img class="myemsl_inst_image" width="400" height="400" src="http://myemsl-dev1.emsl.pnl.gov/myemsl/files-basic/index.php?dir=transaction/\1/data\&file=\2">#' | ./test.php
done

