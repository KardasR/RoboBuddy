import struct
import io
import fcntl
from time import sleep

# register addresses
_USEFUL_SENSOR_DEFAULT_ADDRESS = 0x62
_USEFUL_SENSOR_MODE_REGISTER = 0x01
_USEFUL_SENSOR_RUN_ID_MODEL_REGISTER = 0x02
_USEFUL_SENSOR_SINGLE_CAPTURE_REGISTER = 0x03
_USEFUL_SENSOR_CALIBRATION_REGISTER = 0x04
_USEFUL_SENSOR_PERSISTENT_IDS_REGISTER = 0x05
_USEFUL_SENSOR_ERASE_SAVED_IDS_REGISTER = 0x06
_USEFUL_SENSOR_DEBUG_MODE_REGISTER = 0x07

# We will be reading raw bytes over I2C, and we'll need to decode them into
# data structures. These strings define the format used for the decoding, and
# are derived from the layouts defined in the developer guide.
PERSON_SENSOR_I2C_HEADER_FORMAT = "BBH"
PERSON_SENSOR_I2C_HEADER_BYTE_COUNT = struct.calcsize(PERSON_SENSOR_I2C_HEADER_FORMAT)

PERSON_SENSOR_FACE_FORMAT = "BBBBBBbB"
PERSON_SENSOR_FACE_BYTE_COUNT = struct.calcsize(PERSON_SENSOR_FACE_FORMAT)

PERSON_SENSOR_FACE_MAX = 4
PERSON_SENSOR_RESULT_FORMAT = PERSON_SENSOR_I2C_HEADER_FORMAT + \
        "B" + PERSON_SENSOR_FACE_FORMAT * PERSON_SENSOR_FACE_MAX + "H"

PERSON_SENSOR_RESULT_BYTE_COUNT = struct.calcsize(PERSON_SENSOR_RESULT_FORMAT)


class PersonDetector:
    def __init__(self, channel: int):
        i2c_handle = io.open("/dev/i2c-" + str(channel), "rb", buffering=0)
        fcntl.ioctl(i2c_handle, 0x703, _USEFUL_SENSOR_DEFAULT_ADDRESS) 
        self.i2c_device = i2c_handle
        self.reg_buf = bytearray(3)
        self.cmd_buf = bytearray(1)
        print("Person Detector initialized")

    def _write_register(self, reg: int, value: int):
        """Write 16 bit value to register"""
        self.reg_buf[0] = reg
        self.reg_buf[1] = (value >> 8) & 0xFF
        self.reg_buf[2] = value & 0xFF
        self.i2c_device.write(bytearray(self.reg_buf, self.cmd_buf))

    def _write_cmd(self, reg: int):
        self.cmd_buf[0] = reg
        self.i2c_device.write(bytearray(self.reg_buf, self.cmd_buf))

    def read(self):
        try:
            result = self.i2c_device.read(PERSON_SENSOR_RESULT_BYTE_COUNT)
        except OSError as error:
            print("No person sensor data found")
            print(error)
            sleep(1)
        
        offset = 0
        (pad1, pad2, payload_bytes) = struct.unpack_from(PERSON_SENSOR_I2C_HEADER_FORMAT, result, offset)
        offset = offset + PERSON_SENSOR_I2C_HEADER_BYTE_COUNT

        (num_faces) = struct.unpack_from("B", results, offset)
        num_faces = int(num_faces[0])
        offset = offset + 1

        faces = []
        for i in range(num_faces):
            (box_confidence, box_left, box_top, box_right, box_bottom, id_confidence, id, 
             is_facing) = struct.unpack_from(PERSON_SENSOR_FACE_FORMAT, result, offset)
            offset = offset + PERSON_SENSOR_FACE_BYTE_COUNT
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
        checksum = struct.unpack_from("H", result, offset)
        
        return (num_faces, faces)

    def setStandbyMode(self):
        self._write_register(_USEFUL_SENSOR_MODE_REGISTER, 0)

    def setContinuousMode(self):
        self._write_register(_USEFUL_SENSOR_MODE_REGISTER, 1)

    def setIdModelEnabled(self, enabled):
        self._write_register(_USEFUL_SENSOR_RUN_ID_MODEL_REGISTER, int(enabled))

    def setDebugMode(self, enabled):
        self._write_register(_USEFUL_SENSOR_DEBUG_MODE_REGISTER, int(enabled))

    def setPersistentIds(self, enabled):
        self._write_register(_USEFUL_SENSOR_PERSISTENT_IDS_REGISTER, int(enabled))

    def setEraseSavedIds(self, enabled):
        self._write_register(_USEFUL_SENSOR_ERASED_SAVED_IDS_REGISTER, int(enabled))

    def singleCapture(self):
        """Write to register."""
        self.cmd_buf[0] = _USEFUL_SENSOR_SINGLE_CAPTURE_REGISTER
        with self.i2c_device as i2c:
            i2c.write(self.cmd_buf)

    def calibrate(self, id):
        self._write_register(_USEFUL_SENSOR_CALIBRATION_REGISTER, int(id))
