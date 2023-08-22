#!/usr/bin/python
"""
test_sub.py is an example of a publisher subscribing to a topic
"""

import sys
import paho.mqtt.client as mqtt
import time
import requests
import json
import os
import paho.mqtt.client as mqtt

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected  and subscribe to topic: "+str(topic))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(topic)


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

if __name__ == '__main__':
	
	if len(sys.argv) != 6:
		print (f'usage: python3 {sys.argv[0]} HOST PORT TOPIC USER PASSWORD')
		print (f'usage: python3 {sys.argv[0]} 3.17.183.219 1883 laxparking_through_dexms user password')
		sys.exit(0)
		
    # parameters
	host = sys.argv[1]
	port = int(sys.argv[2])
	topic = sys.argv[3]
	user = sys.argv[4]
	password = sys.argv[5]
	
	#Create MQTT client instance and connect
	client = mqtt.Client()
	client.on_connect = on_connect
	client.on_message = on_message
	
	#Set credential to subscribe to the topic
	client.username_pw_set(user, password)
	
	#Connect
	client.connect(host, port, 60)
	
	# Blocking call that processes network traffic, dispatches callbacks and
	# handles reconnecting
	client.loop_forever()

