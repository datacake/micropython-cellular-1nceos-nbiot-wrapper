from lib.LTEWrapper import LTEWrapper
from lib.WIFISniffer import WIFISniffer
from lib.UDPUplinkMessageWrapper import UDPUplinkMessageWrapper
from time import sleep
import machine

IOTCREATORS_UDP_IP = "172.27.131.100"
IOTCREATORS_UDP_PORT = 15683
IOTCREATORS_APN = "cdp.iot.t-mobile.nl"
IOTCREATORS_BAND = 20

# Start LTE Connection
lte_wrapper = LTEWrapper(band=IOTCREATORS_BAND, apn=IOTCREATORS_APN)
lte_wrapper.start_lte_connection()

# Init Wrapper
message = UDPUplinkMessageWrapper(IOTCREATORS_UDP_IP, IOTCREATORS_UDP_PORT)

# Send a message to iotcreators backend
message.send(b"Hello from Pycom!")

# Tear down LTE
lte_wrapper.stop_lte_connection()
lte_wrapper.deinit()