#!/bin/bash
if [ "x${JENKINS_CONFIG}" = "x" ]
then
	JENKINS_CONFIG=/var/lib/jenkins/config.xml
fi
DIR="$(cd "$(dirname "$0")" && pwd)"
$DIR/pacifica-jenkins-import-jobs.sh
$DIR/pacifica-jenkins-import-views.py ${JENKINS_CONFIG}
