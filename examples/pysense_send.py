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
from machine import WDT, Timer
import struct
import math

CELLULAR_UDP_IP = "10.60.2.239"
CELLULAR_UDP_PORT = 4445
CELLULAR_APN = "iot.1nce.net"
CELLULAR_BAND = 20

SLEEP_TIME = 300
WATCHDOG_TIMEOUT = 90000
DEBUG = True

print("\nStarting Example: pysense_send.py\n")

# Watchdog Timer
wdt = WDT(timeout=WATCHDOG_TIMEOUT)

# Runtime Stopwatch
stopwatch = Timer.Chrono()
stopwatch.start()

# Init Pysense sensors
py = Pycoproc()
dht = SI7006A20(py)
ltr = LTR329ALS01(py)
mpl = MPL3115A2(py,mode=PRESSURE)

# Read Pysense sensors
temperature = dht.temperature()
humidity = dht.humidity()
pressure = mpl.pressure() / 100.0
light = ltr.lux()
battery = py.read_battery_voltage()
if DEBUG: print("Temp: {}, Hum: {}, Pres: {}, Light: {}, Bat: {}\n".format(temperature, humidity, pressure, light, battery))

# Init iotcreators message wrapper for udp
message = UDPUplinkMessageWrapper(CELLULAR_UDP_IP, CELLULAR_UDP_PORT)

# Transform sensor data to bytearray and hex data as payload for udp message
message_payload = bytearray()
message_payload.extend(struct.pack('>H', math.floor(temperature * 10)))
message_payload.extend(struct.pack('>H', math.floor(humidity * 10)))
message_payload.extend(struct.pack('>b', math.floor(battery * 10)))
message_payload.extend(struct.pack('>H', math.floor(pressure)))
message_payload.extend(struct.pack('>H', math.floor(light)))

# Start LTE connection
lte_wrapper = LTEWrapper(band=CELLULAR_BAND, apn=CELLULAR_APN)
lte_wrapper.start_lte_connection()

# Add LTE connection time to payload for benchmarking
message_payload.extend( struct.pack('>H', math.floor( lte_wrapper.elapsed_connection_time )))

# Send a message to iotcreators backend via udp wrapper
message.send(message_payload)

# We are done and we can now sleep the device
py.setup_sleep(SLEEP_TIME - stopwatch.read())
py.go_to_sleep(pycom_module_off=True, accelerometer_off=True, wake_interrupt=False)