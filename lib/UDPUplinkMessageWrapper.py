import socket

UDP_DOWNLINK_TIMEOUT = 10
UDP_DOWNLINK_BUFFER_SIZE = 128 # Max NB-IoT message size

class UDPUplinkMessageWrapper():

    def __init__(self, ip, port, downlink=True):
        self.ip = ip
        self.port = port
        self.downlink_enabled = downlink
        self.downlink_payload = False

    def send(self, message):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.s.bind(('',self.port))
        self.s.setblocking(True)
        self.s.sendto(message, (self.ip, self.port))
        if self.downlink_enabled is True:
            self.s.settimeout(UDP_DOWNLINK_TIMEOUT)
            try:
                self.downlink_payload = self.s.recv(UDP_DOWNLINK_BUFFER_SIZE)
            except socket.timeout as e:
                # If this happens you likely have downlinks enabled but no dl queued up?
                # Or try increasing timeout seconds
                print("ERROR: Downlink Timeout Raised. No Downlink queued up? Timeout too short?")
        self.s.close()