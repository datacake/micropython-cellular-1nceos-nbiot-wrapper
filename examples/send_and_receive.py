from lib.LTEWrapper import LTEWrapper
from lib.UDPUplinkMessageWrapper import UDPUplinkMessageWrapper
import ubinascii

CELLULAR_UDP_IP = "172.27.131.100"
CELLULAR_UDP_PORT = 15683
CELLULAR_APN = "cdp.iot.t-mobile.nl"
CELLULAR_BAND = 20

# Please queue up Downlink on iotcreators before running this!!!

# Start LTE Connection
lte_wrapper = LTEWrapper(band=CELLULAR_BAND, apn=CELLULAR_APN)
lte_wrapper.start_lte_connection()

# Init Wrapper
message = UDPUplinkMessageWrapper(CELLULAR_UDP_IP, CELLULAR_UDP_PORT, downlink=True)

# Send a message to iotcreators backend
message.send(b"Hello from Pycom!")

# If downlink was queued we now have something in the downlink payload variable
print("Received downlink: {}".format( ubinascii.unhexlify(message.downlink_payload) ) )

# Tear down LTE
lte_wrapper.stop_lte_connection()
lte_wrapper.deinit()