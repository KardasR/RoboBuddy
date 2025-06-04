# this will test the person sensor from useful sensors.
import usefulsensors_persondetector as USPD
import LCD1602
import drawBoxes as DB
from time import sleep
import sys

# when to start remembering the face
face_confidence_trigger = 97
PERSON_SENSOR_DELAY = 0.1

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

    return (offset_x, offset_y)

def outputToLCD(lcd, offset_x, offset_y):
    # Describe the offset
    offx = ""
    if offset_x < -5:
        offx += f"{abs(offset_x)} left. "
    elif offset_x > 5:
        offx += f"{offset_x} right. "
    else:
        offx += "hori centered."

    offy = ""
    if offset_y < -5:
        offy += f"{abs(offset_y)} high."
    elif offset_y > 5:
        offy += f"{offset_y} low."
    else:
        offy += "vert centered."
    
    lcd.lcdPrint(offx, offy)

def CalibrateandOutput(sensor, lcd, data):
    num_faces, faces = data
    
    if (num_faces > 0):
        face = faces[0]

        if (face["is_facing"] and 
            face["id_confidence"] == 0 and
            face["box_confidence"] >= face_confidence_trigger):
            StartCal(sensor, face)

        offX, offY = getOffsetFromCenter(face["box_left"], face["box_right"], face["box_top"], face["box_bottom"])
        outputToLCD(lcd, offX, offY)

def StartCal(sensor, face):    
    sensor.setContinuousMode(1)
    sensor.setIdModelEnabled(1)
    sensor.setPersistentIds(1)
    sleep(0.1)
    sensor.calibrate(face["id"])
    sleep(5)


def main():
    with USPD.PersonDetector(sys.argv[1]) as sensor:
        with LCD1602.LCD1602() as lcd:
            while True:
                sensorOut = sensor.read()
                print(sensorOut)
                CalibrateandOutput(sensor, lcd, sensorOut)
                sleep(PERSON_SENSOR_DELAY)

if (__name__ == "__main__"):
    main()