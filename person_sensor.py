# Example of accessing the Person Sensor from Useful Sensors on a Pi using
# Python. See https://usfl.ink/ps_dev for the full developer guide.

import io
import fcntl
import struct
import time
import sys

# The person sensor has the I2C ID of hex 62
addy = 0x62

# We will be reading raw bytes from the I2C so we need to decode them.
headerFormat = "BBH"
headerByteCount = struct.calcsize(headerFormat)

faceFormat = "BBBBBBbB"
faceByteCount = struct.calcsize(faceFormat)

faceMax = 4
resultFormat = headerFormat + \
    "B" + faceFormat * faceMax + "H"
resultByteCount = struct.calcsize(resultFormat)

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
