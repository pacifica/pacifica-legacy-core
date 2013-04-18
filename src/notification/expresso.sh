#!/bin/bash

# this should set FILELIST SUBMITTER and TRANSACTION
eval `./filestream`

MYEMSL_MOUNT="/myemsl"

REMOTE_DIR=$(dirname $(head -n 1 $FILELIST | sed 's#/myemsl/##'))
ssh svc-expresso@expresso.emsl.pnl.gov "mkdir -p $REMOTE_DIR; cp -a solid-auto/* $REMOTE_DIR/"

TMP_CONF=$(mktemp -d -p $PWD)
cat > $TMP_CONF/simplescan <<EOF
[scanners]
scanner = list $FILELIST

[workers]
workers = scp /myemsl/$SUBMITTER/bundle/$TRANSACTION svc-expresso expresso.emsl.pnl.gov /home/svc-expresso/$SUBMITTER/bundle/$TRANSACTION/Input 1
EOF
FSCrawler -d $TMP_CONF
echo rm -rf $TMP_CONF
ssh expresso.emsl.pnl.gov "cd $SUBMITTER/bundle/$TRANSACTION; ./submit"
