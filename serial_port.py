"""This module implements the SerialPort class, which allows the host to talk
   to another device using a serial like interface over a UART.
"""

import serial
import select

class SerialPort(object):
    """Implements a PySerial port."""

    def __init__(self, port, baud=115200):
        self.serial_port = serial.Serial(port=port,
                                         baudrate=baud,
                                         timeout=0.1,
                                         bytesize=serial.EIGHTBITS,
                                         parity=serial.PARITY_NONE,
                                         stopbits=serial.STOPBITS_ONE,
                                         xonxoff=False,
                                         rtscts=False,
                                         dsrdtr=False)

    def is_byte_available(self):
        readable, _, _ = select.select([self.serial_port.fileno()], [], [], 0)
        return bool(readable)

    def read_byte(self):
        """Reads a byte from the serial port."""
        if self.is_byte_available():
            data = self.serial_port.read()
            if data:
                return data[0]

    def write(self, data):
        """Write data to a serial port."""
        self.serial_port.write(data)
