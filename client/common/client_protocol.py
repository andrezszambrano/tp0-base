from .protocol import Protocol
from .packet import Packet

class ClientProtocol(Protocol):

    def __init__(self):
        super(ClientProtocol, self).__init__()

    def __add_bet_to_packet(self, bet, packet):
        packet.add_byte(super().BET_CHAR)
        packet.add_string_and_length(bet.first_name)
        packet.add_string_and_length(bet.last_name)
        packet.add_n_byte_number(super().FOUR_BYTES, bet.document)
        packet.add_date(bet.birthdate)
        packet.add_n_byte_number(super().FOUR_BYTES, bet.number)

    def send_batch(self, socket, batch):
        packet = Packet()
        packet.add_byte(super().START_BATCH)
        for bet in batch:
            self.__add_bet_to_packet(bet, packet)
        packet.add_byte(super().BATCH_SENT)
        packet.send_to_socket(socket)

    def send_agency_number(self, socket, agency_number):
        super()._send_n_byte_number(socket, super().ONE_BYTE, agency_number)

    def send_finished_message(self, socket):
        super()._send_byte(socket, super().FINISHED_CHAR)

    def recv_winners_documents(self, socket, agency_id):
        packet = Packet()
        packet.add_byte(super().CONSULT_WINNERS)
        packet.send_to_socket(socket)
        return self.__recv_winners_documents(socket)

    def __recv_winners_documents(self, socket):
        winners = []
        while True:
            action = super()._recv_byte(socket)
            if action == super().FINISHED_CHAR:
                break
            winners.append(super()._recv_n_byte_number(socket, super().FOUR_BYTES))
        return winners

    def recv_ok(self, socket):
        super()._recv_byte(socket)
