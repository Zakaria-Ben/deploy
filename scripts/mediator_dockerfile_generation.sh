#!/bin/bash

## This script generates a Dockerfile to build an ubuntu/java image that
## contains a dynamically generated mediator (jar file) derived from the
## Dex IDL description provided.


## Script variables setup

# URL of the mediator service to use for the mediator generation
MEDIATOR_SERVICE_URL=${MEDIATOR_SERVICE_URL:-"http://localhost:8080/dexms-service-1.2.0-SNAPSHOT/dexms/mediator"}

# name of the (Docker)file to generate
MEDIATOR_DFILE="Dockerfile"

# temporary filename where the mediator jar should be saved
MEDIATOR_JARFILE="generated_mediator.jar"

# check that all required parameters are provided
if [ $# -ne 8 ]
  then
	  echo "usage: $0 SERVICE_GIDL SERVICE_NAME SERVICE_VERSION BUS_ADDRESS BUS_PORT PROTOCOL TARGET_SERVICE_ADDRESS TARGET_SERVICE_PORT"
      echo "   example: $0 myrestsrv.gidl mqtt myrestsrv 1.0 443 80 8080"
	  exit
fi

# target service description
SERVICE_IDL=${1:-"service.gidl"}

# info for tagging the Docker image
NAME=$2
VERSION=$3

# Addresses and ports for the target service and provided bus (mediator ?)
BUS_ADDRESS=$4
BUS_PORTS=$5

# protocol of the service (protocol, ip address, port)
PROTOCOL=$6
ENDPOINT_ADDRESS=$7
ENDPOINT_PORT=$8

# login and password for the i3 MQTT server
# since set in the Dockerfile, it will leave some traces when building the image
# not an issue currently. If no traces are required, use multi-stage build
# https://vsupalov.com/build-docker-image-clone-private-repo-ssh-key/
I3MQTTUNAME=${I3MQTTUNAME:-"guest"}
I3MQTTPWD=${I3MQTTPWD:-"password"}

##
## Processing
##

# delte file if exist and retrieve
echo "Call the Mediator service at $MEDIATOR_SERVICE_URL with the service definition $SERVICE_IDL "
rm -rf $MEDIATOR_JARFILE MEDIATOR_DFILE
# call the python script instead. Default to mqtt, and use the mediator's name a the service name
python3 mediator_service_request.py $MEDIATOR_SERVICE_URL $SERVICE_IDL $PROTOCOL $NAME $ENDPOINT_ADDRESS $ENDPOINT_PORT $BUS_ADDRESS $BUS_PORTS  $MEDIATOR_JARFILE
# curl -X POST -H "Content-Type: application/txt" -o $MEDIATOR_JARFILE -d @SERVICE_IDL $MEDIATOR_SERVICE_URL

# start generating the dockerfile
echo "## Generated mediator Dockerfile" >> $MEDIATOR_DFILE

echo "FROM openjdk:8u201-jre-alpine" >> $MEDIATOR_DFILE
echo " " >> $MEDIATOR_DFILE
echo "WORKDIR ." >> $MEDIATOR_DFILE
echo " " >> $MEDIATOR_DFILE
echo "# copy generated mediator jar file " >> $MEDIATOR_DFILE
echo "COPY $MEDIATOR_JARFILE ." >> $MEDIATOR_DFILE

echo " " >> $MEDIATOR_DFILE
for port in ${BUS_PORTS//,/ }
do
    echo "EXPOSE $port" >> $MEDIATOR_DFILE
done
echo " " >> $MEDIATOR_DFILE
echo "CMD java -jar $MEDIATOR_JARFILE" >> $MEDIATOR_DFILE


# now build the image from the dockerfile
docker build -t="mediator_$NAME:$VERSION" .
