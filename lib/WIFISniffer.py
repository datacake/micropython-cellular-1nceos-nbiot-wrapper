from network import WLAN
import ubinascii

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