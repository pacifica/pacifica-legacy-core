#!/bin/bash

# this should set FILELIST SUBMITTER and TRANSACTION
eval `./filestream`

BDIR="/myemsl/$SUBMITTER/bundle/$TRANSACTION"

BUNDLER="/home/dmlb2000/svn-repos/myemsl2/myemsl2/trunk/src/ingest_core/myemsl_bundler"

mkdir $TRANSACTION/test
cat $BDIR/test/a > $TRANSACTION/test/a
hostname >> $TRANSACTION/test/a
$BUNDLER -c $TRANSACTION -i From-$(hostname -s) -b $PWD/$TRANSACTION.zip -f .
