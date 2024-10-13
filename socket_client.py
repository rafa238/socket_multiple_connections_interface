#!/usr/bin python3

import socket

HOST = "127.0.0.1"  # Hostname o  dirección IP del servidor
PORT = 65432  # Puerto del servidor
buffer_size = 1024

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as TCPClientSocket:
    TCPClientSocket.connect((HOST, PORT))
    while(True):

        msg = input("Ingresa un mensaje a enviar")
        TCPClientSocket.sendall(msg.encode())
        data = TCPClientSocket.recv(buffer_size)
        print("Servidor dice: ,", repr(data), " de", TCPClientSocket.getpeername())