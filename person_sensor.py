# Example of accessing the Person Sensor from Useful Sensors on a Pi using
# Python. See https://usfl.ink/ps_dev for the full developer guide.

import io
import fcntl
import struct
import time
import sys

"""
Byte Offset | Meaning
0 	Reserved
1 	Reserved
2 	Data Length (first byte)
3 	Data Length (second byte)
4 	Number of Faces
5 	Face #0 Box Confidence
6 	Face #0 Box Left
7 	Face #0 Box Top
8 	Face #0 Box Right
9 	Face #0 Box Bottom
10 	Face #0 Recognition Confidence
11 	Face #0 Recognition ID
12 	Face #0 Is Looking At
13 	Face #1 Box Confidence
14 	Face #1 Box Left
15 	Face #1 Box Top
16 	Face #1 Box Right
17 	Face #1 Box Bottom
18 	Face #1 Recognition Confidence
19 	Face #1 Recognition ID
20 	Face #1 Is Looking At
21 	Face #2 Box Confidence
22 	Face #2 Box Left
23 	Face #2 Box Top
24 	Face #2 Box Right
25 	Face #2 Box Bottom
26 	Face #2 Recognition Confidence
27 	Face #2 Recognition ID
28 	Face #2 Is Looking At
29 	Face #3 Box Confidence
30 	Face #3 Box Left
31 	Face #3 Box Top
32 	Face #3 Box Right
33 	Face #3 Box Bottom
34 	Face #3 Recognition Confidence
35 	Face #3 Recognition ID
36 	Face #3 Is Looking At
37 	Checksum (first byte)
38 	Checksum (second byte)
"""

# We will be reading raw bytes from the I2C so we need to decode them.
headerFormat = "BBH"
headerByteCount = struct.calcsize(headerFormat)

faceFormat = "BBBBBBbB"
faceByteCount = struct.calcsize(faceFormat)

faceMax = 4
resultFormat = headerFormat + \
    "B" + faceFormat * faceMax + "H"
resultByteCount = struct.calcsize(resultFormat)

# The person sensor has the I2C ID of hex 62
addy = 0x62

# I2C channel will be given through the first arg
channel = sys.argv[1]
peripheral = 0x703

# How long to pause between sensor polls.
delay = 0.2

i2cHandle = io.open("/dev/i2c-" + str(channel), "rb", buffering=0)
fcntl.ioctl(i2cHandle, peripheral, addy)

while True:
    try:
        readBytes = i2cHandle.read(resultByteCount)
    except OSError as error:
        print("No person sensor data found")
        print(error)
        time.sleep(delay)
        continue
    offset = 0
    (pad1, pad2, payload_bytes) = struct.unpack_from(
        headerFormat, readBytes, offset)
    offset = offset + headerByteCount

    (numFaces) = struct.unpack_from("B", readBytes, offset)
    numFaces = int(numFaces[0])
    offset = offset + 1

    faces = []
    for i in range(numFaces):
        (box_confidence, box_left, box_top, box_right, box_bottom, id_confidence, id,
            is_facing) = struct.unpack_from(faceFormat, readBytes, offset)
        offset = offset + faceByteCount
        face = {
            "box_confidence": box_confidence,
            "box_left": box_left,
            "box_top": box_top,
            "box_right": box_right,
            "box_bottom": box_bottom,
            "id_confidence": id_confidence,
            "id": id,
            "is_facing": is_facing,
        }
        faces.append(face)
    checksum = struct.unpack_from("H", readBytes, offset)
    print(numFaces, faces)
    time.sleep(delay)
