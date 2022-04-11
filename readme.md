# Pycom GPy iotcreators Wrapper

This is a wrapper for the Pycom GPy NB-IoT IoT Development Boards and its firmware. 

Less than 10 lines of code are required to connect to the NB-IoT network and transmit uplinks (including receiving downlinks).

## How to

In the Libraries folder you will find two wrappers for Pycom firmware functions:

- lib/LTEWrapper.py
- lib/UDPUplinkMessageWrapper.py

Both abstract the functions of the already quite simple Pycom firmware API and make working with NB-IoT and iotcreators even easier.

### LTEWrapper.py

This wrapper provides functions for initializing the NB-IoT modem of the Pycom GPy as well as for establishing a connection. 

You can try the commands directly on the REPL console of your Pycom GPy (i.e. via the serial console). But make sure that you have uploaded the libraries to your Pycom GPy.

```
>>> IOTCREATORS_APN = "cdp.iot.t-mobile.nl"
>>> IOTCREATORS_BAND = 20
>>> from lib.LTEWrapper import LTEWrapper
>>> lte_wrapper = LTEWrapper(band=IOTCREATORS_BAND, apn=IOTCREATORS_APN)
>>> lte_wrapper.start_lte_connection()
```

Now you see the connection start and the current progress is displayed in the REPL Console. If the connection is successful, you will also see the total time in seconds that was needed to establish the connection.

```
attaching...............attached!
connecting [##] connected!
LTE Connection took: 10.63652 seconds...
```

That's it, the connection over the NB-IoT network to iotcreators has been successfully established. Now you can go ahead and exchange data via UDP (or CoAP) with the iotcreators backend. For this purpose there is another abstraction library and how to use it you will see in the following section.

### UDPUplinkMessageWrapper.py

```
>>> IOTCREATORS_UDP_IP = "172.27.131.100"
>>> IOTCREATORS_UDP_PORT = 15683
>>> from lib.UDPUplinkMessage import UDPUplinkMessageWrapper
>>> message = UDPUplinkMessageWrapper(IOTCREATORS_UDP_IP, IOTCREATORS_UDP_PORT)
>>> message.send(b"Hello from Pycom!")
```

Alternatively you can send bytes, but then you have to transfer a buffer.

```
>>> message.send(b"Hello from Pycom!")
>>> message.send(bytes([32, 43]))
```

### Downlinks

Yes, that's right! You can also receive downlinks from the iotcreators backend, i.e. from the cloud via NB-IoT and this works exactly the same way as with LoRaWAN.

If you send a downlink in the iotcreators backend, it will be queued. The next time your Pycom GPy sends a UDP message, the downlink will be read directly from the queue and sent to your device.

The UDPWrapper provides a function for receiving the downlink.

```
>>> message = UDPUplinkMessageWrapper(IOTCREATORS_UDP_IP, IOTCREATORS_UDP_PORT, downlink=True)
>>> message.send(b"Hello")
>>> message.downlink_payload
b'48656c6c6f2066726f6d20436c6f756421'
```

The variable `message.downlink_payload` then contains the payload of the downlink. 
