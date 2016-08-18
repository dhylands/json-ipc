#!/usr/bin/env python3
#
# Test code which runs on the host, for testing json_pkt.
#
# This runs a server, which you connect to via a socket interface. It parses
# incoming packets and when a complete json object is received, it sends
# it back to the sender.

import argparse
import socket
import sys

from json_pkt import JSON_Packet
from socket_port import SocketPort

IP_ADDR = '127.0.0.1'
IP_PORT = 7788

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((IP_ADDR, IP_PORT))

    while True:
        print("Waiting for connection")
        s.listen(1)

        conn, addr = s.accept()
        print('Connection from:', addr)
        print('type of conn', type(conn))
        print('type of addr', type(addr))

        socket_port = SocketPort(conn)
        jpkt = JSON_Packet(socket_port, show_packets=False)
        while True:
            byte = socket_port.read_byte()
            if byte is not None:
                obj = jpkt.process_byte(byte)
                if obj is not None:
                    print('Got', obj)
                    jpkt.send(obj)
        conn.close()

main()
