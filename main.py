from lib.LTEWrapper import LTEWrapper
from lib.WIFISniffer import WIFISniffer
from lib.UDPUplinkMessageWrapper import UDPUplinkMessageWrapper
from time import sleep
import machine

IOTCREATORS_UDP_IP = "172.27.131.100"
IOTCREATORS_UDP_PORT = 15683
IOTCREATORS_APN = "cdp.iot.t-mobile.nl"
IOTCREATORS_BAND = 20

exit()

# --- iotcreators.com demo ---
try:
    print("\nStarting WiFi Sniffer...")
    
    wifi_sniffer = WIFISniffer()
    
    sleep(120)
    
    node_count = wifi_sniffer.node_count()

    print("Found nodes: {}".format(node_count))

    wifi_sniffer.deinit()
    
    print("Starting LTE and sending message...")

    lte_wrapper = LTEWrapper(band=IOTCREATORS_BAND, apn=IOTCREATORS_APN)
    lte_wrapper.start_lte_connection()
    
    elapsed_connection_time = int(lte_wrapper.elapsed_connection_time)

    message = UDPUplinkMessageWrapper(IOTCREATORS_UDP_IP, IOTCREATORS_UDP_PORT)
    message.send(bytes([node_count,elapsed_connection_time]))

    sleep(2)

    lte_wrapper.stop_lte_connection()
    lte_wrapper.deinit()

    print("Done and resetting...")

except Exception as e:
    pass
machine.reset()
