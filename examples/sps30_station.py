from lib.LTEWrapper import LTEWrapper
from lib.UDPUplinkMessageWrapper import UDPUplinkMessageWrapper
from lib.SPS30Wrapper import SPS30Wrapper
from machine import UART, deepsleep
from time import sleep

IOTCREATORS_UDP_IP = "172.27.131.100"
IOTCREATORS_UDP_PORT = 15683
IOTCREATORS_APN = "cdp.iot.t-mobile.nl"
IOTCREATORS_BAND = 20

SENSOR_WARMUP_TIME = 30
DEVICE_SLEEP_TIME = 300

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
lte_wrapper = LTEWrapper(band=IOTCREATORS_BAND, apn=IOTCREATORS_APN)
lte_wrapper.start_lte_connection()

# Init Wrapper
message = UDPUplinkMessageWrapper(IOTCREATORS_UDP_IP, IOTCREATORS_UDP_PORT)

# Send a message to iotcreators backend
message.send(sps30_values)

# Tear down LTE
lte_wrapper.stop_lte_connection()
lte_wrapper.deinit()

# Deep sleep machine to restart after given amount of idle time
sleep_amount = (DEVICE_SLEEP_TIME - SENSOR_WARMUP_TIME - lte_wrapper.elapsed_connection_time) * 1000
deepsleep(sleep_amount)