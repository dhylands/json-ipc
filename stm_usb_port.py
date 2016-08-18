"""This module implements the USB_Port class which allows the pyboard to
   receive serial data using the pyboard's USB_VCP class.
"""

from pyb import USB_VCP

class USB_Port:

    def __init__(self):
        self.usb_serial = USB_VCP()
        self.recv_buf = bytearray(1)
        # Disable Control-C on the USB serail port in case one comes in the 
        # data.
        self.usb_serial.setinterrupt(-1)

    def read_byte(self):
        """Reads a byte from the usb serial device."""
        if self.usb_serial.any():
            bytes_read = self.usb_serial.recv(self.recv_buf)
            if bytes_read > 0:
                return self.recv_buf[0]

    def write(self, data):
        """Writes an entire packet to the serial port."""
        self.usb_serial.write(data)

