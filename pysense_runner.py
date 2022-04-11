from network import LTE
from time import sleep
import time
import socket
from network import WLAN
import ubinascii
from LIS2HH12 import LIS2HH12
from SI7006A20 import SI7006A20
from LTR329ALS01 import LTR329ALS01
from MPL3115A2 import MPL3115A2,ALTITUDE,PRESSURE

class SensorDevice():

    def __init__(self):
        self.lte = LTE()
        self.coprocessor = Pycoproc2()
        self.pressure_sensor = MPL3115A2(self.coprocessor, mode=PRESSURE)
        self.temperature_sensor = SI7006A20(self.coprocessor)

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

    def start_lte_connection(self):
        self.attach_lte()
        self.connect_lte()

    def stop_lte_connection(self):
        self.lte.disconnect()
        self.lte.detach(reset=True)

    def send_udp_message(self, message, ip=IOTCREATORS_UDP_IP, port=IOTCREATORS_UDP_PORT):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.s.sendto(message, (ip, port))
        self.s.close()    
