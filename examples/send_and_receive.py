from lib.LTEWrapper import LTEWrapper
from lib.UDPUplinkMessageWrapper import UDPUplinkMessageWrapper
import ubinascii

IOTCREATORS_UDP_IP = "172.27.131.100"
IOTCREATORS_UDP_PORT = 15683
IOTCREATORS_APN = "cdp.iot.t-mobile.nl"
IOTCREATORS_BAND = 20

# Please queue up Downlink on iotcreators before running this!!!

# Start LTE Connection
lte_wrapper = LTEWrapper(band=IOTCREATORS_BAND, apn=IOTCREATORS_APN)
lte_wrapper.start_lte_connection()

# Init Wrapper
message = UDPUplinkMessageWrapper(IOTCREATORS_UDP_IP, IOTCREATORS_UDP_PORT, downlink=True)

# Send a message to iotcreators backend
message.send(b"Hello from Pycom!")

# If downlink was queued we now have something in the downlink payload variable
print("Received downlink: {}".format( ubinascii.unhexlify(message.downlink_payload) ) )