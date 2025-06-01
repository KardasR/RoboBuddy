# this will test the person sensor from useful sensors.

import usefulsensors_persondetector as uspd
from time import sleep
import sys

# connect to sensor
sensor = uspd.PersonDetector(sys.argv[1])

while True:
    print(sensor.read())
    sleep(0.5)
