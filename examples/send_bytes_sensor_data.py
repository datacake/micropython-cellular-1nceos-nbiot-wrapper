"""
iotcreators.com Example for sending sensor data as hex bytes.
- Can be used with default iotcreators template on Datacake
(c) 2022 - Simon Kemper @Datacake
"""

from lib.LTEWrapper import LTEWrapper
from lib.UDPUplinkMessageWrapper import UDPUplinkMessageWrapper
import struct
import math

IOTCREATORS_UDP_IP = "172.27.131.100"
IOTCREATORS_UDP_PORT = 15683
IOTCREATORS_APN = "cdp.iot.t-mobile.nl"
IOTCREATORS_BAND = 8 

print("\nStarting Example: send_bytes_sensor_data.py\n")

# Start LTE Connection
lte_wrapper = LTEWrapper(band=IOTCREATORS_BAND, apn=IOTCREATORS_APN)
lte_wrapper.start_lte_connection()

# Init Wrapper
message = UDPUplinkMessageWrapper(IOTCREATORS_UDP_IP, IOTCREATORS_UDP_PORT)

# Create some senor data (put your sensor data here)
temperature = 25.46
humidity = 54.43
battery = 3.12

# Transform sensor data to bytearray and hex data
message_payload = bytearray()
message_payload.extend(struct.pack('>H', math.floor(temperature * 10)))
message_payload.extend(struct.pack('>H', math.floor(humidity * 10)))
message_payload.extend(struct.pack('>b', math.floor(battery * 10)))

# Send a message to iotcreators backend
message.send(message_payload)

# Tear down LTE
lte_wrapper.stop_lte_connection()
lte_wrapper.deinit()