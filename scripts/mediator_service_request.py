import sys
import requests
import json
from pathlib import Path


## simple script to generate a mediator based on a dex idl declaration

if len(sys.argv) != 10:
    print (f"usage: python3 {sys.argv[0]} MEDIATOR_SERVICE_URL SERVICE_IDL PROTOCOL SERVICE_NAME SERVICE_ENDPOINT_ADDRESS SERVICE_ENDPOINT_PORT BUS_ENPOINT_ADDRESS BUS_ENPOINT_PORT MEDIATOR_JAR_NAME")

    print (f"usage: python3 {sys.argv[0]} http://localhost:8080/dexms-service-1.0.0-SNAPSHOT/dexms/mediator laxparking.gidl mqtt laxparking 127.0.0.1 1113 3.17.183.219 1883 generated_mediator.jar")

    sys.exit(0)

# parameters
url = sys.argv[1]
gidl_file = sys.argv[2]
protocol = sys.argv[3]
service_name = sys.argv[4]
service_endpoint_address = sys.argv[5]
service_endpoint_port = sys.argv[6]
bus_endpoint_address = sys.argv[7]
bus_endpoint_port = sys.argv[8]
mediator_file = sys.argv[9]
		
# read content from file
file_content = Path(gidl_file).read_text()

# build json object
jsonobj = {}
jsonobj['gidl'] = file_content
jsonobj['protocol'] = protocol
jsonobj['mediator_name'] = service_name
jsonobj['service_endpoint_address'] = service_endpoint_address
jsonobj['service_endpoint_port'] = service_endpoint_port
jsonobj['bus_endpoint_address'] = bus_endpoint_address
jsonobj['bus_endpoint_port'] = bus_endpoint_port

# print gidl file
print(jsonobj)

# POST API call
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
response = requests.post(url, data=json.dumps(jsonobj), headers=headers, verify='chain.pem')

# print response
# print(x.text)

# if fine write content into jar file in binary mode
if response.status_code == 200:
    with open(mediator_file, 'wb') as f:
        for chunk in response.iter_content(1024):
            f.write(chunk)
    f.close()


