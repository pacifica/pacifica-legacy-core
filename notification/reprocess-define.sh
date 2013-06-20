#!/bin/bash

PASSWORD=""
read -s -p "PASSWORD:" PASSWORD

CURL="curl -L --insecure --cookie-jar cookie.txt --cookie cookie.txt"
URL="https://a3.my.emsl.pnl.gov/myemsl"
AURL="https://a4.my.emsl.pnl.gov/myemsl"

cat > foo.xml <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<reprocessor>
    <groups>
        <group name="proposal" value="45791"/>
        <group name="Tag" value=".*"/>
    </groups>
    <callbacks>
        <callback type="command">
            <command>
<![CDATA[#!/bin/bash
/usr/bin/curl 'http://jenkins.emsl.pnl.gov/jenkins/job/test-reprocessor/buildWithParameters?token=MYEMSL_RULEZ&cause=reprocess+trigger&PROPOSAL='\$proposal'&TAG='\$Tag
]]>
            </command>
        </callback>
    </callbacks>
</reprocessor>
EOF

$CURL -u "`whoami`:$PASSWORD" $AURL/auth?url=/myemsl/search/simple
$CURL -X PUT -T foo.xml $URL/reprocess/myprocess
$CURL $URL/reprocess/myprocess
