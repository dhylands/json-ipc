# This is a version of the echo server which runs on the pyboard.
#
# It parses packets received over the USB VCP (USB REPL) and when a complete
# json packet is received, this gets echoed back to the sender.

from stm_usb_port import USB_Port
from json_pkt import JSON_Packet
 
def main(serial_port):
    jpkt = JSON_Packet(serial_port)
    while True:
        byte = serial_port.read_byte()
        if byte is not None:
            obj = jpkt.process_byte(byte)
            if obj is not None:
                jpkt.send(obj)

main(USB_Port())
