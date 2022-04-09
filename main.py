from network import LTE
from time import sleep
import time
import socket
from network import WLAN
import ubinascii

IOTCREATORS_UDP_IP = "172.27.131.100"
IOTCREATORS_UDP_PORT = 15683
DEBUG = False

class LTEWrapper():

    def __init__(self):
        self.lte = LTE()
        self.attach_lte()
        self.connect_lte()
    
    def attach_lte(self):
        self.lte.attach(band=20, apn="cdp.iot.t-mobile.nl")
        print("attaching..",end='')
        while not self.lte.isattached():
            time.sleep(0.25)
            print('.',end='')
            if DEBUG: print(self.lte.send_at_cmd('AT!="fsm"'))
        print("attached!")

    def connect_lte(self):
        self.lte.connect()
        print("connecting [##",end='')
        while not self.lte.isconnected():
            time.sleep(0.25)
            print('#',end='')
            if DEBUG: print(self.lte.send_at_cmd('AT!="showphy"'))
            if DEBUG: print(self.lte.send_at_cmd('AT!="fsm"'))
        print("] connected!")

    def deinit(self):
        self.lte.deinit()

class IOTCreatorsMessage():

    def __init__(self, message, ip=IOTCREATORS_UDP_IP, port=IOTCREATORS_UDP_PORT):
        self.lte_wrapper = LTEWrapper()
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.s.sendto(message, (ip, port))
        self.s.close()
        self.lte_wrapper.deinit()

class WIFISniffer():

    def __init__(self):
        self.nodes = []
        self.wlan = WLAN(mode=WLAN.STA, antenna=WLAN.INT_ANT)
        self.wlan.callback(trigger=WLAN.EVENT_PKT_MGMT, handler=self.pack_cb)
        self.wlan.promiscuous(True)        

    def node_count(self):
        return len(self.nodes)

    def deinit(self):
        self.wlan.promiscuous(False)
        self.wlan.deinit()

    def pack_cb(self, pack):
        mac = bytearray(6)
        pk = self.wlan.wifi_packet()
        control = pk.data[0]
        subtype = (0xF0 & control) >> 4
        if subtype == 4:
            for i in range (0,6):
                mac[i] = pk.data[10 + i]
            new_node = ubinascii.hexlify(mac)
            if new_node not in self.nodes:
                self.nodes.append(new_node)

# --- iotcreators.com demo ---

while True:
    wifi_sniffer = WIFISniffer()
    sleep(60)
    wifi_sniffer.deinit()
    print("Ended Sniffing, found: {}".format(wifi_sniffer.node_count()))
    # send to iotcreators
    message = IOTCreatorsMessage(bytes([wifi_sniffer.node_count()]))