from network import LTE
from machine import Timer
import time

DEBUG = False

class LTEWrapper():

    def __init__(self, band, apn):
        self.lte_timer = Timer.Chrono()
        self.lte = LTE()
        self.band = band
        self.apn = apn

    def start_lte_connection(self):
        self.lte_timer.start()
        self.attach_lte()
        self.connect_lte()
        self.lte_timer.stop()
        self.elapsed_connection_time = self.lte_timer.read()
        print("LTE Connection took: {} seconds...".format(self.elapsed_connection_time))

    def attach_lte(self):
        if self.band is None:
            self.lte.attach(apn=self.apn)
        else:
            self.lte.attach(band=self.band, apn=self.apn)
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

    def stop_lte_connection(self):
        self.lte.disconnect()
        self.lte.detach(reset=False)