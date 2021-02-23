import dataclasses
import logging
import socket
import socketserver
from collections import deque
from typing import List, Tuple


@dataclasses.dataclass
class PacketInfo:
    data: bytes
    client_address: Tuple[str, int]


class QueuingHandler(socketserver.BaseRequestHandler):
    """Appends received packets to the queue of the calling server"""

    def handle(self) -> None:
        self.server: QueuingServer
        self.request: Tuple[bytes, socket.socket]
        data, recv_socket = self.request

        self.server.queue.append(
            PacketInfo(data=data, client_address=self.client_address)
        )
        self.server.logger.debug(
            f"""Handled datagram:
        data = {data!r}
        recv_socket = {recv_socket}
        client_address = {self.client_address}"""
        )


class QueuingServer(socketserver.UDPServer):
    """Keeps track of all packets that it receives in self.queue"""

    def __init__(
        self,
        server_address: Tuple[str, int],
        bind_and_activate: bool = True,
    ) -> None:
        host, port = server_address

        self.queue: List[PacketInfo] = list()  # Can be properly hinted in 3.9
        self.logger = logging.getLogger(f"{self.__class__.__name__}@{port}")

        super().__init__(
            server_address, QueuingHandler, bind_and_activate=bind_and_activate
        )
