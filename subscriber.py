import base64
import os
from pathlib import Path
import paho.mqtt.client as mqtt
import time
import json
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
from asymmetric import verify


class subscriber:

    def __init__(self):
        self.traffic_offense_payload = None 
        self.weather_forecast_payload = None 
        self.collision_payload = None
        self.public_key = None
        self.client = mqtt.Client("Client2")
        self.broker_hostname = "10.172.22.42"
        self.port = 1883
        # change with your user and password auth
        self.client.username_pw_set(username="user1", password="password1")
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        public_key_path = Path("public.pem")

        try:
            if public_key_path.exists():
                public_pem = public_key_path.read_bytes()
                self.public_key = serialization.load_pem_public_key(
                    public_pem, backend=default_backend()
                )
            else:
                print("Public key file not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

        self.client.connect(self.broker_hostname, self.port)
        self.client.loop_start()

    def on_connect(self, client, userdata, flags, return_code):
        if return_code == 0:
            print("connected")
            self.client.subscribe("collision")
            self.client.subscribe("weatherConditions")
            self.client.subscribe("trafficOffense")
            self.client.subscribe("publicKey")
            if (self.public_key):
                self.publish_public_key()
        else:
            print("could not connect, return code:", return_code)


    def on_message(self, client, userdata, message):
        signature_bytes = None
        message_data = json.loads(message.payload.decode('utf-8'))
        received_data = message_data.get("data")
     
        if (message_data.get("signature") != None):
            received_signature = message_data.get("signature")
            signature_bytes = bytes.fromhex(received_signature)
    
        # Verify the signature
        if signature_bytes != None and self.public_key is not None:
            if verify(signature_bytes, json.dumps(received_data).encode('utf-8'), self.public_key):
                print("Signature verified. Message:", received_data)
                #Checking message type
                if message_data.get("data") != None:
                    message_data = message_data.get("data")
                    if message_data.get("Temperature") != None:
                        self.weather_forecast_payload = message_data
                    elif message_data.get("Detection") != None:
                        self.collision_payload = message_data
                    elif message_data.get("Message") != None:
                        self.traffic_offense_payload = message_data
                    #else:
                        #print("Unknown message")
                else:
                    print("Unknown message type")
        elif message_data.get("public_key"):
            if not self.public_key:
                public_key_data = message_data.get("public_key").encode('utf-8')
                self.public_key = serialization.load_pem_public_key(
                    message_data.get("public_key"),
                    backend=default_backend()
                )
        else:
            print("Signature verification failed. Discarding message.")


    def process_collision(self):
        if self.collision_payload is not None:
            print("Received Collision:", str(self.collision_payload))
            # file_path = './static/trafficCollision.jpg'
            # image = self.collision_payload.get("Image")
            # if image is not None:
            #     with open(file_path, 'wb') as file:
            #         file.write(base64.b64decode(image[0]))
            # pass this to the dashboard
            return self.collision_payload


    def process_weather_forecast(self):
        if self.weather_forecast_payload is not None:
            print("Received Weather Forecast:", str(self.weather_forecast_payload))
            #pass this to the dashboard
            return self.weather_forecast_payload
        

    def process_traffic_offense(self):
        if self.traffic_offense_payload is not None:
            print("Received Traffic Offense:", str(self.collision_payload))
            # file_path = './static/trafficOffense.jpg'
            # image = self.traffic_offense_payload.get("Image")
            # if image is not None:
            #     with open(file_path, 'wb') as file:
            #         file.write(base64.b64decode(image[0]))
            # pass this to the dashboard
            return self.traffic_offense_payload


    def publish_public_key(self):
        public_key_data = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        message = {"public_key": public_key_data.decode('utf-8')}
        self.client.publish("publicKey", payload=json.dumps(message))
