import socket

class UDPUplinkMessageWrapper():

    def __init__(self, ip, port, downlink=False):
        self.ip = ip
        self.port = port
        self.donwlink_enabled = downlink
        self.downlink_payload = False

    def send(self, message):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.s.sendto(message, (self.ip, self.port))
        if self.donwlink_enabled is True:
            self.downlink_payload = self.s.recv(1024)
        self.s.close()