import logging

from .protocol import Protocol
from .packet import Packet

class ClientProtocol(Protocol):

    def __init__(self):
        super(ClientProtocol, self).__init__()

    def send_bet(self, socket, bet):
        packet = Packet()

        packet.add_byte(super().BET_CHAR)
        packet.add_n_byte_number(super().ONE_BYTE, bet.agency)
        packet.add_string_and_length(bet.first_name)
        packet.add_string_and_length(bet.last_name)
        packet.add_n_byte_number(super().FOUR_BYTES, bet.document)
        packet.add_date(bet.birthdate)
        packet.add_n_byte_number(super().FOUR_BYTES, bet.number)

        packet.send_to_socket(socket)
        
    def recv_ok(self, socket):
        super()._recv_byte(socket)
