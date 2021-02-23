import logging
import socket
import threading
from typing import Generator, Tuple

import pytest
from stateful_server import queueing_socketserver as subject

from .timeout import timeout

Address = Tuple[str, int]


@pytest.fixture
def address() -> Address:
    return ("127.0.0.1", 7000)


@pytest.fixture
def server(address: Address) -> Generator[subject.QueuingServer, None, None]:
    """Starts the QueuingServer in another thread"""
    server = subject.QueuingServer(address)

    serving_thread = threading.Thread(target=server.serve_forever)
    serving_thread.start()

    yield server

    server.shutdown()
    serving_thread.join()


def test_queue_packet(server: subject.QueuingServer):
    payload = b"I AM A DATAGRAM"

    send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    send_sock.sendto(payload, server.server_address)
    send_host, send_port = send_sock.getsockname()

    with timeout(1):
        while len(server.queue) < 1:
            pass

    assert server.queue == [
        subject.PacketInfo(data=payload, client_address=("127.0.0.1", send_port))
    ]


def test_long_packet(server: subject.QueuingServer):
    payload = b"A" * 8192  # Maximum for this test without failing

    send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    send_sock.sendto(payload, server.server_address)
    send_host, send_port = send_sock.getsockname()

    with timeout(1):
        while len(server.queue) < 1:
            pass

    logging.debug(len(payload))
    logging.debug(len(server.queue[0].data))

    assert server.queue == [
        subject.PacketInfo(data=payload, client_address=("127.0.0.1", send_port))
    ]
