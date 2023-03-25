from .socket import Socket

class ClientProtocol:

    def send_default_message(self, socket, client_id, msg_id):
        msg = "[CLIENT {}] Message N°{}".format(client_id, msg_id).encode('utf-8')
        socket.send(msg, len(msg))

    def recv_message(self, socket):
        return socket.recv(1024).rstrip().decode('utf-8')
