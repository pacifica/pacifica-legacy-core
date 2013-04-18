#!/bin/bash

# this should set FILELIST SUBMITTER and TRANSACTION
eval `./filestream`

(
cat <<EOF
Proposal $PROPOSAL has new files available on MyEMSL.

https://a9.emsl.pnl.gov/myemsl/files/index.php?dir=proposal/$PROPOSAL/data

Added or Changed Files
=====================================
EOF
sed 's#^/myemsl/[0-9][0-9]*/bundle/[0-9][0-9]*/##' $FILELIST
) | mail -s "MyEMSL System Alert" david.brown@pnl.gov
