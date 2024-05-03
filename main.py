from lib.LTEWrapper import LTEWrapper
from lib.UDPUplinkMessageWrapper import UDPUplinkMessageWrapper

# Basic example on how to send and receive
# You can find more examples in examples/ folder
# Load and start each example on boot.py

# Make sure you queued a downlink via cellular backend (1NCE, or on Datacake) before

CELLULAR_UDP_IP = "10.60.2.239"
CELLULAR_UDP_PORT = 4445
CELLULAR_APN = "iot.1nce.net"
CELLULAR_BAND = 20

# Start LTE Connection
lte_wrapper = LTEWrapper(band=CELLULAR_BAND, apn=CELLULAR_APN)
lte_wrapper.start_lte_connection()

# Init Wrapper
message = UDPUplinkMessageWrapper(CELLULAR_UDP_IP, CELLULAR_UDP_PORT)

# Send a message to iotcreators backend
message.send(b"Hello from Pycom!")

# Print received downlink
print("Received downlink: {}".format( message.downlink_payload ) )

# Tear down LTE
lte_wrapper.stop_lte_connection()
lte_wrapper.deinit()