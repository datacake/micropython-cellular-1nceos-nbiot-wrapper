import struct, time
#from operator import invert

class SPS30Wrapper:
    def __init__(self, port, uart):
        self.uart = uart
    
    def start(self):
        start_message = [0x7E, 0x00, 0x00, 0x02, 0x01, 0x03, 0xF9, 0x7E]
        self.uart.write(bytes(start_message))
        self.uart.read(100)
        
    def stop(self):
        stop_message = [0x7E, 0x00, 0x01, 0x00, 0xFE, 0x7E]
        self.uart.write(bytes(stop_message))
        self.uart.read(100)
    
    def read_values(self):

        # request data
        read_message = [0x7E, 0x00, 0x03, 0x00, 0xFC, 0x7E]
        self.uart.write(bytes(read_message))

        # wait for tx to be done
        while self.uart.wait_tx_done(500) is False:
            time.sleep(0.1)

        # wait for sps30 to respond - let run into timeout
        raw = self.uart.read(100)
        # print(len(raw))
        if len(raw) < 47:
            print("Response < 47 bytes - aborting...")
            return None
        if raw is None:
            print("No data was returned - aborting ...")
            return None

        # Reverse byte-stuffing
        if b'\x7D\x5E' in raw:
            raw = raw.replace(b'\x7D\x5E', b'\x7E')
        if b'\x7D\x5D' in raw:
            raw = raw.replace(b'\x7D\x5D', b'\x7D')
        if b'\x7D\x31' in raw:
            raw = raw.replace(b'\x7D\x31', b'\x11')
        if b'\x7D\x33' in raw:
            raw = raw.replace(b'\x7D\x33', b'\x13')
        
        # Discard header and tail
        rawData = raw[5:-2]
        
        # unpack data into actual values
        try:
            data = struct.unpack(">ffffffffff", rawData)
        except:
            print("unpack was wrong")
            return None
        return data

    def read_values_raw(self):

        # request data
        read_message = [0x7E, 0x00, 0x03, 0x00, 0xFC, 0x7E]
        self.uart.write(bytes(read_message))

        # wait for tx to be done
        while self.uart.wait_tx_done(500) is False:
            time.sleep(0.1)

        # wait for sps30 to respond - let run into timeout
        raw = self.uart.read(100)
        # print(len(raw))
        if len(raw) < 47:
            print("Response < 47 bytes - aborting...")
            return None
        if raw is None:
            print("No data was returned - aborting ...")
            return None

        # Reverse byte-stuffing
        if b'\x7D\x5E' in raw:
            raw = raw.replace(b'\x7D\x5E', b'\x7E')
        if b'\x7D\x5D' in raw:
            raw = raw.replace(b'\x7D\x5D', b'\x7D')
        if b'\x7D\x31' in raw:
            raw = raw.replace(b'\x7D\x31', b'\x11')
        if b'\x7D\x33' in raw:
            raw = raw.replace(b'\x7D\x33', b'\x13')
        
        # Discard header and tail
        rawData = raw[5:-2]
        return rawData
    
    def read_serial_number(self):
        self.ser.flushInput()
        self.ser.write([0x7E, 0x00, 0xD0, 0x01, 0x03, 0x2B, 0x7E])
        toRead = self.ser.inWaiting()
        while toRead < 24:
            toRead = self.ser.inWaiting()
            time.sleep(0.1)
        raw = self.ser.read(toRead)
        
        # Reverse byte-stuffing
        if b'\x7D\x5E' in raw:
            raw = raw.replace(b'\x7D\x5E', b'\x7E')
        if b'\x7D\x5D' in raw:
            raw = raw.replace(b'\x7D\x5D', b'\x7D')
        if b'\x7D\x31' in raw:
            raw = raw.replace(b'\x7D\x31', b'\x11')
        if b'\x7D\x33' in raw:
            raw = raw.replace(b'\x7D\x33', b'\x13')
        
        # Discard header, tail and decode
        serial_number = raw[5:-3].decode('ascii')
        return serial_number

    def read_firmware_version(self):
        self.ser.flushInput()
        self.ser.write([0x7E, 0x00, 0xD1, 0x00, 0x2E, 0x7E])
        toRead = self.ser.inWaiting()
        while toRead < 7:
            toRead = self.ser.inWaiting()
            time.sleep(0.1)
        raw = self.ser.read(toRead)
        
        # Reverse byte-stuffing
        if b'\x7D\x5E' in raw:
            raw = raw.replace(b'\x7D\x5E', b'\x7E')
        if b'\x7D\x5D' in raw:
            raw = raw.replace(b'\x7D\x5D', b'\x7D')
        if b'\x7D\x31' in raw:
            raw = raw.replace(b'\x7D\x31', b'\x11')
        if b'\x7D\x33' in raw:
            raw = raw.replace(b'\x7D\x33', b'\x13')
        
        # Discard header and tail
        data = raw[5:-2]
        # Unpack data
        data = struct.unpack(">bbbbbbb", data)
        firmware_version = str(data[0]) + "." + str(data[1])
        return firmware_version
    
    def close_port(self):
        pass
        #self.ser.close()