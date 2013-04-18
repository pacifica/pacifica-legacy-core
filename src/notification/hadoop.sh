#!/bin/bash

# this should set FILELIST SUBMITTER and TRANSACTION
eval `./filestream`

MYEMSL_MOUNT="/myemsl"

REMOTE_DIR=$(dirname $(head -n 1 $FILELIST | sed 's#/myemsl/##'))
#ssh dmlb2000@h01.emsl.pnl.gov '/bin/bash -l -c "hadoop fs -mkdir /dmlb2000/'$REMOTE_DIR'"'
ssh dmlb2000@h01.emsl.pnl.gov '/bin/bash -l -c "mkdir /home/dmlb2000/'$REMOTE_DIR'"'

TMP_CONF=$(mktemp -d -p $PWD)
cat > $TMP_CONF/simplescan <<EOF
[scanners]
scanner = list $FILELIST

[workers]
workers = pythonworker hadoop_copy dmlb2000 h01.emsl.pnl.gov /myemsl /home/dmlb2000
EOF
FSCrawler -d $TMP_CONF
echo rm -rf $TMP_CONF
