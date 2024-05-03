from lib.LTEWrapper import LTEWrapper
from lib.UDPUplinkMessageWrapper import UDPUplinkMessageWrapper
from lib.SPS30Wrapper import SPS30Wrapper
from machine import UART, deepsleep
from pycoproc import Pycoproc2
from time import sleep

CELLULAR_UDP_IP = "10.60.2.239"
CELLULAR_UDP_PORT = 4445
CELLULAR_APN = "iot.1nce.net"
CELLULAR_BAND = 20

SENSOR_WARMUP_TIME = 30
DEVICE_SLEEP_TIME = 300

# Init Pycom Coprocessor
py = Pycoproc2()

# UART and SPS30 Init
uart = UART(1, 115200)
uart.init(115200, bits=8, parity=None, stop=1, timeout_chars=100)
sps30 = SPS30Wrapper(0, uart)
sps30.start()

# idle for 30 seconds to get accurate measurements from sps30
sleep(SENSOR_WARMUP_TIME)

# read values from sps30
sps30_values = None
while sps30_values is None:
    sps30_values = sps30.read_values_raw()
print(sps30_values)

# Start LTE Connection
lte_wrapper = LTEWrapper(band=CELLULAR_BAND, apn=CELLULAR_APN)
lte_wrapper.start_lte_connection()

# Init Wrapper
message = UDPUplinkMessageWrapper(CELLULAR_UDP_IP, CELLULAR_UDP_PORT)

# Send a message to iotcreators backend
message.send(sps30_values)

# Tear down LTE
lte_wrapper.stop_lte_connection()
lte_wrapper.deinit()

# Shut off machine to restart after given amount of idle time
py.setup_sleep(DEVICE_SLEEP_TIME - SENSOR_WARMUP_TIME - lte_wrapper.elapsed_connection_time)
py.go_to_sleep(pycom_module_off=True, accelerometer_off=True, wake_interrupt=False)