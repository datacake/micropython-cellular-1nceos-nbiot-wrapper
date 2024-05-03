# MicroPython (Pycom GPy) Cellular (1NCE OS) Wrapper

This is a wrapper for the MicroPython (Pycom GPy compatible) NB-IoT IoT Development Boards and its firmware. 

Less than 10 lines of code are required to connect to the NB-IoT network and transmit uplinks (including receiving downlinks).

- Note: This is a ported code based on a Pycom GPy code.

## Compatibility

- 1NCE OS: Works perfectly with 1NCE OS UDP message broker: https://1nce.com/de-de/1nce-os
- Datacake: Works perfectly with Datacake 1NCE OS integration, including downlink: https://docs.datacake.de/integrations/1nce-os and https://datacake.co/
- DPTechnics Walter: https://www.crowdsupply.com/dptechnics/walter

## How to

In the Libraries folder you will find two wrappers for MicroPython (Pycom) firmware functions:

- lib/LTEWrapper.py
- lib/UDPUplinkMessageWrapper.py

Both abstract the functions of the already quite simple MicroPython (Pycom) firmware API and make working with NB-IoT and 1NCE OS even easier.

### LTEWrapper.py

This wrapper provides functions for initializing the NB-IoT modem of the MicroPython (Pycom) GPy as well as for establishing a connection. 

You can try the commands directly on the REPL console of your MicroPython (Pycom) GPy (i.e. via the serial console). But make sure that you have uploaded the libraries to your MicroPython (Pycom) GPy.

```
>>> CELLULAR_APN = "iot.1nce.net"
>>> CELLULAR_BAND = 20
>>> from lib.LTEWrapper import LTEWrapper
>>> lte_wrapper = LTEWrapper(band=CELLULAR_BAND, apn=CELLULAR_APN)
>>> lte_wrapper.start_lte_connection()
```

Now you see the connection start and the current progress is displayed in the REPL Console. If the connection is successful, you will also see the total time in seconds that was needed to establish the connection.

```
attaching...............attached!
connecting [##] connected!
LTE Connection took: 10.63652 seconds...
```

That's it, the connection over the NB-IoT network to 1NCE OS has been successfully established. Now you can go ahead and exchange data via UDP (or CoAP) with the 1NCE OS backend. For this purpose there is another abstraction library and how to use it you will see in the following section.

### UDPUplinkMessageWrapper.py

```
>>> CELLULAR_UDP_IP = "10.60.2.239"
>>> CELLULAR_UDP_PORT = 4445
>>> from lib.UDPUplinkMessage import UDPUplinkMessageWrapper
>>> message = UDPUplinkMessageWrapper(CELLULAR_UDP_IP, CELLULAR_UDP_PORT)
>>> message.send(b"Hello from MicroPython!")
```

Alternatively you can send bytes, but then you have to transfer a buffer.

```
>>> message.send(b"Hello from MicroPython!")
>>> message.send(bytes([32, 43]))
```

### Downlinks

Yes, that's right! You can also receive downlinks from the 1NCE OS backend, i.e. from the cloud via NB-IoT and this works exactly the same way as with LoRaWAN.

If you send a downlink in the 1NCE OS backend, it will be queued. The next time your MicroPython Device sends a UDP message, the downlink will be read directly from the queue and sent to your device.

The UDPWrapper provides a function for receiving the downlink.

```
>>> message = UDPUplinkMessageWrapper(CELLULAR_UDP_IP, CELLULAR_UDP_PORT, downlink=True)
>>> message.send(b"Hello")
>>> message.downlink_payload
b'48656c6c6f2066726f6d20436c6f756421'
```

The variable `message.downlink_payload` then contains the payload of the downlink. 

## Best Practices

### Periodic connecting

It is recommended that you disconnect and then reconnect to the network between phases when you want to send data over the network.

This is because a continuous NB-IoT connection may cause the current cell tower to reject the connection of the MicroPython Device's modem.
