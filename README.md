Allows python objects to be sent over a serial like interface from one device
to another.

# Files

| File            | Description |
| --------------- | ----------- |
| json_pkt.py     | Implements JSON Packet parsing and sending. |
| json_echo.py    | Echo server which runs on the pyboard. |
| stm_usb_port.py | Pyboard serial interface over USB_VCP. |
| dump_mem.py     | Utility function for dumping memory. |
| echo_server.py  | Echo server which runs on the host. |
| json_test.py    | Echo client which runs on the host. |
| serial_port.py  | Host serial interface over UART. |
| socket_port.py  | Host serial interface over Socket. |

# Example

In one window on the PC, run ```echo_server.py```, and in another window run 
```json_test.py --socket```. You should see the following from the 
echo_server.py window:
```
2248 >./echo_server.py 
Waiting for connection
Connection from: ('127.0.0.1', 53328)
type of conn <class 'socket.socket'>
type of addr <class 'tuple'>
Got [1, 2, 3]
Got {'b': 22, 'c': 33, 'a': 11}
Got {'d': 'This is a test'}
```
and you should see this:
```
2044 >./json_test.py --socket
Sending [1, 2, 3]
   Rcvd [1, 2, 3]
Sending {'a': 11, 'b': 22, 'c': 33}
   Rcvd {'a': 11, 'b': 22, 'c': 33}
Sending {'d': 'This is a test'}
   Rcvd {'d': 'This is a test'}
```
from the json_test.py window.

To test on the pyboard, copy json_pkt.py, json_echo.py, dump_mem.py and
stm_usb_port.py to /flash and import json_echo to run the echo server on the
pyboard.

IMPORTANT NOTE: Remember to disconnect your terminal emulator after starting
json_echo.py on the pyboard and before running json_test.py on the host.

Now run ```json_test.py --serial /dev/tyACM0``` on the host and you should see:
```
2250 >./json_test.py --serial /dev/ttyACM0
Sending [1, 2, 3]
   Rcvd [1, 2, 3]
Sending {'b': 22, 'c': 33, 'a': 11}
   Rcvd {'c': 33, 'b': 22, 'a': 11}
Sending {'d': 'This is a test'}
   Rcvd {'d': 'This is a test'}
```

