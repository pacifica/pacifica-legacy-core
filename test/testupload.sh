#!/bin/bash

#set -e

PROTO='http'
SERVER='myemsl-dev0.emsl.pnl.gov'

OPTIONS='--negotiate'

while getopts ":s:f:p:k" opt; do
  case $opt in
    s)
      SERVER="$OPTARG"
      ;;
    f)
      FILE="$OPTARG"
      ;;
    p)
      PROTO="$OPTARG"
      ;;
    k)
      OPTIONS="$OPTIONS --insecure"
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      exit 1
      ;;
    :)
      echo "Option -$OPTARG requires an argument." >&2
      exit 1
      ;;
  esac
done

URL="$PROTO://$SERVER"

if [ "x$FILE" = "x" ]
then
	echo "You must specify a file with -f"
	exit 1
fi
echo "Server URL: $URL"
echo "File: $FILE"

user=':'
#user=kfox

if [ "x$1" == "x" ]
then
	echo "Specify file!"
	exit 1
fi

eval `curl $OPTIONS -s -u "$user" "$URL/myemsl/cgi-bin/preallocate" | sed -n 's/^Server: \([0-9a-zA-Z_.-]*\)$/server='"'"'\1'"'"'/p;s/^Location: \([@0-9a-zA-Z_./-]*\)$/location='"'"'\1'"'"'/p'`
echo "Server: $server"
echo "Location: $location"
if [ "x$location" = "x" -o "x$server" = "x" ]
then
	echo "Failed to get proper location information from server"
	exit 1
fi

URL="$PROTO://$server"

curl $OPTIONS -u "$user" -T "$FILE" "$URL$location"

if [ $? != 0 ]
then
	echo "Failed to upload"
fi
echo "Finishing"
curl $OPTIONS -u "$user" "$URL/myemsl/cgi-bin/finish$location" 
