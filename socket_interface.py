import socket
import selectors
from collections.abc import Callable

from client import Client


class SocketListener:
    def __init__(self, ip: str, port: int, on_accept=None, on_msg_received=None):
        self.ip = ip
        self.port = port
        self.sock = socket.socket()
        self.sel = selectors.DefaultSelector()
        self.on_accept = on_accept
        self.on_msg_received = on_msg_received

    def set_on_accept(self, on_accept: Callable):
        self.on_accept = on_accept

    def set_on_msg_received(self, on_msg_received: Callable):
        self.on_msg_received = on_msg_received


    def send_msg(self, client: Client, msg: str):
        client.conn.send(msg.encode())


    def read(self, conn, mask):
        data = conn.recv(1000)
        host, addr = conn.getpeername()
        client = Client(conn, host)
        if data:
            self.on_msg_received(client, data)
        else:
            print('Closing connection to', conn)
            self.sel.unregister(conn)
            conn.close()

    def accept(self, sock, mask):
        conn, addr = sock.accept()
        client = Client(conn, addr)
        conn.setblocking(False)
        # Usar funcion recibida en el constructor
        self.on_accept(client)
        self.sel.register(conn, selectors.EVENT_READ, self.read)

    def listen(self):
        self.sock.bind((self.ip, self.port))
        self.sock.listen(100)
        self.sock.setblocking(False)
        self.sel.register(self.sock, selectors.EVENT_READ, self.accept)
        print(f'Server listening on {self.ip}:{self.port}')
        while True:
            events = self.sel.select()
            for key, mask in events:
                callback = key.data
                callback(key.fileobj, mask)
