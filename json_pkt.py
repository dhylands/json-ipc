# This code should run fine on MicroPython or CPython.
#
# It allows objects which can be represented as JSON objects to be sent
# between two python programs (running on the same or different computers).

import json
from dump_mem import dump_mem

SOH = 0x01
STX = 0x02
ETX = 0x03
EOT = 0x04

# <SOH><LenLow><LenHigh><STX><PAYLOAD><ETX><LRC><EOT>

def lrc(str):
    sum = 0
    for b in str:
        sum = (sum + b) & 0xff
    return ((sum ^ 0xff) + 1) & 0xff

class JSON_Packet:

    STATE_SOH = 0
    STATE_LEN_0 = 1
    STATE_LEN_1 = 2
    STATE_STX = 3
    STATE_PAYLOAD = 4
    STATE_ETX = 5
    STATE_LRC = 6
    STATE_EOT = 7

    def __init__(self, serial_port, show_packets=False):
        self.serial_port = serial_port
        self.show_packets = show_packets
        self.pkt_len = 0
        self.pkt_idx = 0
        self.pkt = None
        self.lrc = 0
        self.state = JSON_Packet.STATE_SOH

    def send(self, obj):
        """Converts a python object into its json representation and then sends
           it using the 'serial_port' passed in the constructor.
        """
        j_str = json.dumps(obj).encode('ascii')
        j_len = len(j_str)
        j_lrc = lrc(j_str)
        hdr = bytearray((SOH, j_len & 0xff, j_len >> 8, STX))
        ftr = bytearray((ETX, j_lrc, EOT))
        if self.show_packets:
            data = hdr + j_str + ftr
            dump_mem(data, 'Send')
        self.serial_port.write(hdr)
        self.serial_port.write(j_str)
        self.serial_port.write(ftr)

    def process_byte(self, byte):
        """Processes a single byte. Returns a json object when one is
           successfully parsed, otherwise returns None.
        """
        if self.show_packets:
            if byte >= ord(' ') and byte <= ord('~'):
                print('Rcvd 0x%02x \'%c\'' % (byte, byte))
            else:
                print('Rcvd 0x%02x' % byte)
        if self.state == JSON_Packet.STATE_SOH:
            if byte == SOH:
                self.state = JSON_Packet.STATE_LEN_0
        elif self.state == JSON_Packet.STATE_LEN_0:
            self.pkt_len = byte
            self.state = JSON_Packet.STATE_LEN_1
        elif self.state == JSON_Packet.STATE_LEN_1:
            self.pkt_len += (byte << 8)
            self.state = JSON_Packet.STATE_STX
        elif self.state == JSON_Packet.STATE_STX:
            if byte == STX:
                self.state = JSON_Packet.STATE_PAYLOAD
                self.pkt_idx = 0
                self.pkt = bytearray(self.pkt_len)
                self.lrc = 0
            else:
                self.state = JSON_Packet.STATE_SOH
        elif self.state == JSON_Packet.STATE_PAYLOAD:
            self.pkt[self.pkt_idx] = byte
            self.lrc = (self.lrc + byte) & 0xff
            self.pkt_idx += 1
            if self.pkt_idx >= self.pkt_len:
                self.state = JSON_Packet.STATE_ETX
        elif self.state == JSON_Packet.STATE_ETX:
            if byte == ETX:
                self.state = JSON_Packet.STATE_LRC
            else:
                self.state = JSON_Packet.STATE_SOH
        elif self.state == JSON_Packet.STATE_LRC:
            self.lrc = ((self.lrc ^ 0xff) + 1) & 0xff
            if self.lrc == byte:
                self.state = JSON_Packet.STATE_EOT
            else:
                self.state = JSON_Packet.STATE_SOH
        elif self.state == JSON_Packet.STATE_EOT:
            self.state = JSON_Packet.STATE_SOH
            if byte == EOT:
                return json.loads(str(self.pkt, 'ascii'))

