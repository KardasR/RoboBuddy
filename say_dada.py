# this will test the person sensor from useful sensors.

import usefulsensors_persondetector as USPD
import drawBoxes as DB
from time import sleep
import sys

def ShowCameraView(data):
    num_faces, faces = data
    print("Found {num_faces} faces")
    
    face = faces[0]   

    DB.clearScreen()
    DB.drawBox(face['box_left'], face['box_right'], face['box_top'], face['box_bottom'])

# connect to sensor
sensor = USPD.PersonDetector(sys.argv[1])

while True:
    sensorOut = sensor.read()
    print(sensorOut)
    ShowCameraView(sensorOut)
    sleep(0.5)