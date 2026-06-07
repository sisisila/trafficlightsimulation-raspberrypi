from pathlib import Path
import paho.mqtt.client as mqtt 
import json
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from asymmetric import sign


broker_address = "localhost"
broker_port = 1883


def extract_private_key():
    private_pem = Path("key.pem").read_bytes()

    private_key = serialization.load_pem_private_key(
        private_pem,
        password=b"my secret", 
     )
    

    return private_key

private_key = extract_private_key()

def on_connect(client, userdata, flags, return_code):
    print("CONNACK received with code %s." % return_code)
    if return_code == 0:
        print("connected")
    else:
        print("could not connect, return code:", return_code)

client = mqtt.Client(client_id="Client1", userdata=None)
client.on_connect = on_connect

client.username_pw_set(username="user1", password="password1")


client.connect(broker_address, broker_port, 60)
client.loop_start()

def publishCollision(traffic_offense):
    topic = "collision"
    try:
        # Sign the message
        signature = sign(json.dumps(traffic_offense).encode('utf-8'), private_key)

        # Include the signature and data in the payload
        payload = {
            "data": traffic_offense,
            "signature": signature.hex()
        }

        result = client.publish(topic=topic, payload=json.dumps(payload))
        status = result[0]
        if status == 0:
            print("Message " + json.dumps(payload) + " is published to topic " + topic)
        else:
            print("Failed to send message to topic " + topic)
    finally:
        client.loop_stop()


def publishWeatherCondition(weather_forecast):
    topic = "weatherConditions"
    try:
        # Sign the message
        signature = sign(json.dumps(weather_forecast).encode('utf-8'), private_key)

        # Include the signature and data in the payload
        payload = {
            "data": weather_forecast,
            "signature": signature.hex()
        }

        result = client.publish(topic=topic, payload=json.dumps(payload))
        status = result[0]
        if status == 0:
            print("Message " + json.dumps(payload) + " is published to topic " + topic)
        else:
            print("Failed to send message to topic " + topic)
    finally:
        client.loop_stop()

def publishTrafficOffense(traffic_offense):
    topic = "trafficOffense"
    try:
        # Sign the message
        signature = sign(json.dumps(traffic_offense).encode('utf-8'), private_key)

        # Include the signature and message in the payload
        payload = {
            "data": traffic_offense,
            "signature": signature.hex()
        }

        result = client.publish(topic=topic, payload=json.dumps(payload))
        status = result[0]
        if status == 0:
            print("Message " + json.dumps(payload) + " is published to topic " + topic)
        else:
            print("Failed to send message to topic " + topic)
    finally:
        client.loop_stop()