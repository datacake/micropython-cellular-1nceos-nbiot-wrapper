"""
iotcreators.com Example for sending Pysense Air Quality Data over NB-IoT.
- Can be used with default iotcreators template on Datacake
(c) 2022 - Simon Kemper @Datacake
"""

from lib.LTEWrapper import LTEWrapper
from lib.UDPUplinkMessageWrapper import UDPUplinkMessageWrapper
from lib.pycoproc2 import Pycoproc
from lib.SI7006A20 import SI7006A20
from lib.LTR329ALS01 import LTR329ALS01
from lib.MPL3115A2 import MPL3115A2,PRESSURE
import struct
import math

IOTCREATORS_UDP_IP = "172.27.131.100"
IOTCREATORS_UDP_PORT = 15683
IOTCREATORS_APN = "cdp.iot.t-mobile.nl"
IOTCREATORS_BAND = 8
SLEEP_TIME = 300
DEBUG = True

print("\nStarting Example: pysense_send.py\n")

# Init Pysense sensors
py = Pycoproc()
dht = SI7006A20(py)

# Read Pysense sensors
temperature = dht.temperature()
humidity = dht.humidity()
battery = py.read_battery_voltage()
if DEBUG: print("Temp: {}, Hum: {}, Bat: {}\n".format(temperature, humidity, battery))

# Init Wrapper
message = UDPUplinkMessageWrapper(IOTCREATORS_UDP_IP, IOTCREATORS_UDP_PORT)

# Transform sensor data to bytearray and hex data
message_payload = bytearray()
message_payload.extend(struct.pack('>H', math.floor(temperature * 10)))
message_payload.extend(struct.pack('>H', math.floor(humidity * 10)))
message_payload.extend(struct.pack('>b', math.floor(battery * 10)))

# Start LTE Connection
lte_wrapper = LTEWrapper(band=IOTCREATORS_BAND, apn=IOTCREATORS_APN)
lte_wrapper.start_lte_connection()

# Send a message to iotcreators backend
message.send(message_payload)

# Tear down LTE
lte_wrapper.stop_lte_connection()
lte_wrapper.deinit()

# Sleep device
py.setup_sleep(SLEEP_TIME)
py.go_to_sleep(pycom_module_off=True, accelerometer_off=True, wake_interrupt=False)