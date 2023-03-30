from .protocol import Protocol
from .packet import Packet

class ClientProtocol(Protocol):

    def __init__(self):
        super(ClientProtocol, self).__init__()

    def send_batch(self, socket, batch):
        packet = Packet()
        packet.add_n_byte_number(super().ONE_BYTE, batch[0].agency)
        for bet in batch:
            self.__add_bet_to_packet(bet, packet)
        packet.add_byte(super().BATCH_SENT)
        packet.send_to_socket(socket)


    def __add_bet_to_packet(self, bet, packet):
        packet.add_byte(super().BET_CHAR)
        packet.add_string_and_length(bet.first_name)
        packet.add_string_and_length(bet.last_name)
        packet.add_n_byte_number(super().FOUR_BYTES, bet.document)
        packet.add_date(bet.birthdate)
        packet.add_n_byte_number(super().FOUR_BYTES, bet.number)
        
    def recv_ok(self, socket):
        super()._recv_byte(socket)
