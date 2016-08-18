#!/usr/bin/env python3
#
# This is a test program which runs on the host. It can talk to echo_server.py
# via socket interface (on the host) or to json_echo.py (on the pyboard) via
# USB-serial.

import argparse
from json_pkt import JSON_Packet
import sys

TEST = [
    [1, 2, 3],
    {'a': 11, 'b': 22, 'c':33},
    {'d': 'This is a test'},
]

def test(serial_port, show_packets):
    jpkt = JSON_Packet(serial_port, show_packets=show_packets)
    for t in TEST:
        print('Sending', t)
        jpkt.send(t)
        while True:
            byte = serial_port.read_byte()
            if byte is not None:
                obj = jpkt.process_byte(byte)
                if obj is not None:
                    print('   Rcvd', obj)
                    break

def main():
    parser = argparse.ArgumentParser(
        description='Test JSON packetizer',
    )
    parser.add_argument(
        '-v', '--verbose',
        dest='verbose',
        action='store_true',
        help='Turn on verbose messages',
        default=False
    )
    parser.add_argument(
        '--socket',
        dest='socket',
        action='store_true',
        help='Send data over a socket',
        default=False
    )
    parser.add_argument(
        '--serial',
        dest='serial',
        help='Send data over a serial port',
        default=None
    )

    args = parser.parse_args(sys.argv[1:])

    if args.socket:
        import socket
        from socket_port import SocketPort

        IP_ADDR = '127.0.0.1'
        IP_PORT = 7788
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((IP_ADDR, IP_PORT))
        port = SocketPort(s)
    elif args.serial:
        from serial_port import SerialPort
        port = SerialPort(args.serial)
    else:
        print('No comms method specified')
        return

    test(port, args.verbose)

main()
