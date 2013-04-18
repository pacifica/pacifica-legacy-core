#!/bin/bash

# this should set FILELIST SUBMITTER and TRANSACTION
eval `./filestream`

(
cat <<EOF
Proposal $PROPOSAL has new files available on MyEMSL.

https://my.emsl.pnl.gov/myemsl/files/submitter/34002/group_name/-later-/data

Added or Changed Files
=====================================
EOF
sed 's#^/myemsl/[0-9][0-9]*/bundle/[0-9][0-9]*/##' $FILELIST
) | mail -s "MyEMSL System Alert" david.brown@pnl.gov
