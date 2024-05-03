from lib.LTEWrapper import LTEWrapper
from lib.WIFISniffer import WIFISniffer
from lib.UDPUplinkMessageWrapper import UDPUplinkMessageWrapper
from time import sleep
import machine

CELLULAR_UDP_IP = "10.60.2.239"
CELLULAR_UDP_PORT = 4445
CELLULAR_APN = "iot.1nce.net"
CELLULAR_BAND = 20

try:
    
    # Start the sniffer
    print("\nStarting WiFi Sniffer...")
    wifi_sniffer = WIFISniffer()
    
    # Let sniffer sniff devices in background
    sleep(120)
    
    # Get results
    node_count = wifi_sniffer.node_count()
    print("Found nodes: {}".format(node_count))

    # Deinit sniffer
    wifi_sniffer.deinit()
    
    # Init LTE
    print("Starting LTE and sending message...")
    lte_wrapper = LTEWrapper(band=CELLULAR_BAND, apn=CELLULAR_APN)
    lte_wrapper.start_lte_connection()
    elapsed_connection_time = int(lte_wrapper.elapsed_connection_time)

    # Create message
    message = UDPUplinkMessageWrapper(CELLULAR_UDP_IP, CELLULAR_UDP_PORT)
    message.send(bytes([node_count,elapsed_connection_time]))

    print("Done and resetting...")

except Exception as e:
    pass

# Reset machine to start over
machine.reset()
