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
        packet.add_n_byte_number(super().ONE_BYTE, batch[0].agency)
        for bet in batch:
            self.__add_bet_to_packet(bet, packet)
        packet.add_byte(super().BATCH_SENT)
        packet.send_to_socket(socket)

    def send_finished_message(self, socket, agency_id):
        packet = Packet()
        packet.add_byte(super().FINISHED_CHAR)
        packet.add_n_byte_number(super().ONE_BYTE, agency_id)
        packet.send_to_socket(socket)

    def try_to_recv_winners_documents(self, socket, agency_id):
        packet = Packet()
        packet.add_byte(super().CONSULT_WINNERS)
        packet.add_n_byte_number(super().ONE_BYTE, agency_id)
        packet.send_to_socket(socket)
        action = super()._recv_byte(socket)
        if action != super().OK_CHAR:
            return None
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
