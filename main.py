from client import Client
from socket_interface import SocketListener

if __name__ == '__main__':
    HOST = "127.0.0.1"
    PORT = 65432
    socket_interface = SocketListener(HOST, PORT)

    def on_accept_connection(client: Client):
        print('Accepted connection from', client.addr)

    def on_msg_received(client: Client, msg):
        print(f'Received a message from {client.addr}: {msg}', client.addr)
        socket_interface.send_msg(client, f"Si recibimos tu mensaje {client.addr}")

    socket_interface.set_on_accept(on_accept=on_accept_connection)
    socket_interface.set_on_msg_received(on_msg_received=on_msg_received)

    socket_interface.listen()
