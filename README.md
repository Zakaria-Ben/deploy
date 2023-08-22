# DexDeploy

This project is related to the [DeXMS](https://gitlab.inria.fr/zefxis/DeXMS) and
[DeXMS-Service](https://gitlab.inria.fr/zefxis/DeXMS-Service) projects.

DexDeploy provides the necessary scripts to generate and deploy a mediator for a specific service. This project 
assumes a DeXMS service is available online at a specified URL (check the [README](https://gitlab.inria.fr/zefxis/DeXMS-Service) from the project above in order 
to build and deploy the DeXMS's service). 

In order to generate a mediator, the following information is required:
* the service's DexIDL file.
* the name of the service
* the protocol to be supported (e.g., mqtt, ...)
* the target service IP address and port
* the address and port to be provided by the mediator

## Generate and test the mediator

To generate and test a mediator directly, first go into the scripts folder, and then call the Python (3.6 
or above) mediator_service_request.py to generate the jar file.

```
python3 mediator_service_request.py http://localhost:8080/dexms-service-1.0.0-SNAPSHOT/dexms/mediator \
    laxparking.gidl \
    mqtt \
    laxparking \
    127.0.0.1 \
    1112 \
    3.17.183.219 \
    1883 \
    generated_mediator.jar
```

With the command above, a mediator is generated that gets data from an online REST service (Laxparking) and 
forwards this information to the I3 MQQT Broker. In this example, a single mediator is generated. The data to be
forwarded is defined in the Laxparking DexIDL. Also, the mediator interconnect two services (REST and MQTT). It is 
therefore assumed that an additional component is deployed that periodically pulls data from the Laxparking service
and send it to the mediator's endpoint.

In the above command
- the mediator endpoint is 127.0.0.1:1112
- the MQTT server endpoint is 3.17.183.219:1883

Also, login and password information for the I3 MQTT server is expected to be set in the environment variables.

Once generated, the jar file can then be tested directly with the command

```java -jar generated_mediator.jar```

## Generate and start the mediator's Dockerfile

To generate the mediator inside a Dockerfile and launch the container, first go into the scripts folder, and then call 
the following command:

```
sh mediator_dockerfile_generation.sh SERVICE_GIDL \
    SERVICE_NAME \
    SERVICE_VERSION \
    BUS_ADDRESS \
    BUS_PORT \
    PROTOCOL \
    TARGET_SERVICE_ADDRESS \
    TARGET_SERVICE_PORT
```

For example, to generate the Dockerfile for the laxparking service as above, the command is:


```
./mediator_dockerfile_generation.sh laxparking.gidl \
    laxparking \
    1.0 \
    3.17.183.219 \
    1883 \
    mqtt \
    127.0.0.1 \
    1112
```

Once the Dockerfile is generated, the Docker image is then automatically created. Once
the image generation is completed, 

```docker run -e I3MQTTUNAME=[LOGIN] -e I3MQTTPWD=[PASSWORD] -p 1112:1112 -d mediator_laxparking:1.0```

As the root (DigiCert) and intermediate (Terena) certificates may not be available on the host, a PEM chain file is 
generated with both certificates and passed to the requests post command in order to validate the https connection.
- TERENA SSL CA 3 : https://www.digicert.com/digicert-root-community-certificates.htm#terena
- DigiCert Assured ID Root CA : https://www.digicert.com/digicert-root-certificates.htm

```
python3 mediator_service_request.py https://sed-webtests.paris.inria.fr/dexms-service-1.1.0-SNAPSHOT/dexms/mediator \
    laxparking.gidl \
    mqtt \
    laxparking \
    127.0.0.1 1112 \
    3.17.183.219 1883 \
    generated_mediator_v1_1.jar
```
