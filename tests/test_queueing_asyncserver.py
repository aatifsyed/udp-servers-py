import asyncio
import logging
import socket
import time

import pytest
from stateful_server import queueing_asyncserver as subject

logger = logging.getLogger(__name__)


@pytest.mark.asyncio
async def test_async():
    await asyncio.sleep(0.1)
    assert True


async def length_of(l: list, equal_to: int):
    while len(l) != equal_to:
        await asyncio.sleep(0)


@pytest.mark.asyncio
async def test_asyncserver(event_loop: asyncio.AbstractEventLoop):
    server_host, server_port = server_address = ("127.0.0.1", 7070)
    payload = b"I AM A PAYLOAD"

    protocol: subject.QueuingDatagramProtocol

    transport, protocol = await event_loop.create_datagram_endpoint(  # type: ignore
        protocol_factory=subject.QueuingDatagramProtocol.factory(),
        local_addr=server_address,
    )

    assert protocol.received == []

    # We are the client
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(payload, server_address)
    (
        client_host,  # BUG? This is 0.0.0.0
        client_port,
    ) = sock.getsockname()  # Function won't return correct port until after we send

    await asyncio.wait_for(length_of(l=protocol.received, equal_to=1), timeout=1)

    assert protocol.received == [
        subject.Datagram(data=payload, address=(server_host, client_port))
    ]
