import base64
import datetime
import os
import time
from picamera2 import Picamera2
from publisher import publishTrafficOffense, publishCollision

class Camera:
    def __init__(self, delay=0.5):
        self.time_to_sleep = delay
        
    def offenceCommitted(self, isRedOn, isMotionOn, end_program):
        while True:
            if end_program.is_set():
                return 
            if isMotionOn.is_set() and isRedOn.is_set():
                time.sleep(2)
                t = time.localtime(time.time())
                timestamp = f'{t.tm_year}/{t.tm_mon}/{t.tm_mday} - {t.tm_hour}h {t.tm_min}min {t.tm_sec}sec'
                
                message = f'Car detected at red light! Date & Time: {timestamp}'
                traffic_offense = {
                    'Message': message,
                    'Image': []
                }
                #self.takePics()
                image_data = self.takePics()
                print("-----------------------TRAFFIC OFFENCE PHOTO------------------------------")
                traffic_offense['Image'].append(image_data)
                # publish message and pictures here
                publishTrafficOffense(traffic_offense) 

    def collisionCommitted(self, message, end_program):
        if end_program.is_set():
            return 
        collision = {
            'Message': message,
            'Image': []
        }
        image_data = self.takePics()
        print('----------------------------COLLISION PHOTO------------------------')
        collision['Image'].append(image_data)
        # publish message and pictures here
        publishCollision(collision)
        
                    
    def takePics(self):
        picam2 = Picamera2()
        camera_config = picam2.create_preview_configuration()
        picam2.configure(camera_config)
        
        picam2.start()
           
        os.makedirs("TrafficEvents", exist_ok = True)
        timestamp= datetime.datetime.now()
        photopath= "TrafficEvents/" + "event_" + str(timestamp)
        picam2.capture_file(photopath+".jpg")
        
        #So that photos can be in payload
        with open(photopath + ".jpg", "rb") as image_file:
            image_data = base64.b64encode(image_file.read()).decode('utf-8')   

        picam2.stop()
        picam2.close()
        return image_data
