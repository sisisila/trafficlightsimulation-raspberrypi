import random
import time
from threading import Thread, Event
import requests
import json
from mqtt.jwt import authenticate
from publisher import publishCollision, publishWeatherCondition
from random import randint

from camera import Camera
isRedOn = Event()
isMotionOn = Event()
end_program = Event()
postal_codes = ["h2k1f7", "h3k1t5", "f4s5f3", "j8f6r2", "g4r6t7"]


class TrafficLight:
    def __init__(self, delay=0.001):
        self.time_to_sleep = delay 
        
    def runSimulation(self, isRedOn):
        currentColor = "Green"
        while True:
            time.sleep(self.time_to_sleep)
            if end_program.is_set():
                return
            if isRedOn.is_set():
                isRedOn.clear()
            if currentColor == "Green":
                print("***********************************************BLUE***********************************************")
                isRedOn.clear()
                currentColor = "Blue"
                time.sleep(15)
            elif currentColor == "Blue":
                print("***********************************************RED***********************************************")
                isRedOn.set()
                currentColor = "Red"
                time.sleep(15)
            elif currentColor == "Red":
                print("***********************************************GREEN***********************************************")
                isRedOn.clear()
                currentColor = "Green"
                time.sleep(15)
            if end_program.is_set():
                return  
            
        

class MovementSensor:
    def __init__(self, delay=2):
        self.time_to_sleep = delay

    def detectMovement(self):
        counter = 0
        while True:
            if end_program.is_set():
                return
            time.sleep(5)
            value = randint(0,1)

            if isRedOn.is_set() and value == 0:
                counter += 1
                print("Traffic offence recorded")
                isMotionOn.set()
            else:
                counter = 0
                isMotionOn.clear()

            if counter >= self.time_to_sleep:
                counter = 0


def make_requests(camera):
    token = authenticate()
    while True:
        time.sleep(3)
        selected_postal_code = random.choice(postal_codes)
        make_request_Traffic(selected_postal_code, token, camera)
        make_request_Weather(selected_postal_code, token)

def make_request_Traffic(postal_code, token, camera):
    url = f"http://172.21.0.1:5081/trafficoffense/{postal_code}"

    try:
        response = requests.get(url + "?token=" + json.dumps(token))
        response.raise_for_status()  # Check for HTTP errors

        # Check if the response is not empty
        if response.text:
            response_json = response.json()
            collision = response_json.get('Detection')
            is_collision = collision.get('value')
            if (is_collision and not (isMotionOn.is_set() and isRedOn.is_set())):
                camera.collisionCommitted(response_json, end_program)
                isMotionOn.set()
            else:
                publishCollision(response_json)
            return response_json
        else:
            print("Empty response from the traffic offense API.")

    except requests.RequestException as e:
        print(f"Error making request to traffic offense API: {e}")

def make_request_Weather(postal_code, token):
    url = f"http://172.21.0.1:5080/weatherforecast/{postal_code}"

    try:
        response = requests.get(url + "?token=" + json.dumps(token))
        response.raise_for_status()  # Check for HTTP errors

        # Check if the response is not empty
        if response.text:
            response_json = response.json()
            publishWeatherCondition(response_json)
            return response_json
        else:
            print("Empty response from the weather conditions API.")

    except requests.RequestException as e:
        print(f"Error making request to weather conditions API: {e}")


class TrafficOffence:
    def main():
        end_program.clear()
        
        trafficLight = TrafficLight(1)
        trafficThread = Thread(target=trafficLight.runSimulation, args=(isRedOn,)) 
        
        movementSensor = MovementSensor()
        movementSensorThread = Thread(target=movementSensor.detectMovement)
        
        camera = Camera()
        cameraThread = Thread(target=camera.offenceCommitted, args=(isRedOn, isMotionOn, end_program,))
        
        requestsThread = Thread(target=make_requests, args=(camera,))

        movementSensorThread.start()
        cameraThread.start()
        trafficThread.start()
        requestsThread.start()
        
        movementSensorThread.join()
        cameraThread.join()
        trafficThread.join()
        requestsThread.join()




    def destroy():
        end_program.set()   

    if __name__ == '__main__':     # Program entrance
        print ('Program is starting ... ')
        try:
            main()
        except KeyboardInterrupt:  # Press ctrl-c to end the program.
            destroy()
