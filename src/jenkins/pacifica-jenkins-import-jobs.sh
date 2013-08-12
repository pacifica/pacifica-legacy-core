#!/bin/bash
set -x
DIR="$(cd "$(dirname "$0")" && pwd)"
if [ "x${JENKINS_JAR}" = "x" ]
then
	JENKINS_JAR=/tmp/jenkins-cli.jar
fi
if [ "x${JENKINS_URL}" = "x" ]
then
	JENKINS_URL=http://127.0.0.1:8080
fi
if [ "x${JENKINS_CONFIG_PREFIX}" = "x" ]
then
	JENKINS_CONFIG_PREFIX="$DIR/jobs"
fi
JENKINS_OPTIONS=""
if [ "x${JENKINS_USERNAME}" != "x" ]
then
	JENKINS_OPTIONS="${JENKINS_OPTIONS} --username ${JENKINS_USERNAME}"
fi
if [ "x${JENKINS_PASSWD_FILE}" != "x" ]
then
	JENKINS_OPTIONS="${JENKINS_OPTIONS} --password-file ${JENKINS_PASSWD_FILE}"
fi
if [ ! -f ${JENKINS_JAR} ]
then
	curl -o ${JENKINS_JAR} ${JENKINS_URL}/jnlpJars/jenkins-cli.jar
fi
if [ "x${JENKINS_JOBS}" == "x" ]
then
	JENKINS_JOBS="qt47 go libbuhfsutil amalgam pacifica-core elasticsearch-download elasticsearch service-poke slurm gdb pprof pacifica-builddeps pacifica-auth pacifica-web-basicauth pacifica-devel-brand pacifica-test-data pacifica-uploader pacifica-devel-vm pacifica-virtual-appliance pymongo"
fi

for jobname in ${JENKINS_JOBS};
do
	java -jar ${JENKINS_JAR} -s ${JENKINS_URL} delete-job $jobname ${JENKINS_OPTIONS}
	java -jar ${JENKINS_JAR} -s ${JENKINS_URL} create-job $jobname ${JENKINS_OPTIONS} < ${JENKINS_CONFIG_PREFIX}/$jobname-config.xml
done
