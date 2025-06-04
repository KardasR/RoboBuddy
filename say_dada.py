# this will test the person sensor from useful sensors.

import usefulsensors_persondetector as USPD
import drawBoxes as DB
from time import sleep
import sys

def getOffsetFromCenter(left, right, top, bottom):
    # Get the center of the face
    face_center_x = (left + right) // 2
    face_center_y = (top + bottom) // 2

    # Sensor FOV center
    center_x = 127
    center_y = 127

    # Offset (positive means right/down, negative means left/up)
    offset_x = face_center_x - center_x
    offset_y = face_center_y - center_y

    # Describe the offset
    retstr = ""
    if offset_x < -5:
        retstr += f"Face is {abs(offset_x)} left of center. "
    elif offset_x > 5:
        retstr += f"Face is {offset_x} right of center. "
    else:
        retstr += "Face is horizontally centered. "

    if offset_y < -5:
        retstr += f"{abs(offset_y)} above center."
    elif offset_y > 5:
        retstr += f"{offset_y} below center."
    else:
        retstr += "Vertically centered."

    return retstr

def ShowCameraView(data):
    num_faces, faces = data
    print("Found {num_faces} faces")
    
    if (num_faces > 0):
        face = faces[0]

        left = face['box_left']
        right = face['box_right']
        top = face['box_top']
        bottom = face['box_bottom']

        print(getOffsetFromCenter(left, right, top, bottom))

        #DB.clearScreen()
        #DB.drawBox(left, right, top, bottom)

# connect to sensor
sensor = USPD.PersonDetector(sys.argv[1])

while True:
    sensorOut = sensor.read()
    print(sensorOut)
    ShowCameraView(sensorOut)
    sleep(0.5)