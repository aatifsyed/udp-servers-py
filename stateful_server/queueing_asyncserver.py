import asyncio
import logging
from typing import List, Tuple, Union
import dataclasses

logger = logging.getLogger(__name__)

Address = Tuple[str, int]


@dataclasses.dataclass
class Datagram:
    data: bytes
    address: Address


class QueuingDatagramProtocol(asyncio.DatagramProtocol):
    def __init__(self) -> None:
        self.received: List[Datagram] = list()

    @classmethod
    def factory(cls):
        """Convenience method"""
        return lambda: cls()

    # Base Protocol: Connection callbacks
    def connection_made(self, transport: asyncio.BaseTransport):
        logger.debug(f"connection_made:\n\ttransport={transport}")

    def connection_lost(self, exc: Union[Exception, None]):
        logger.debug(f"connection_lost:\n\texc={exc}")

    # Base Protocol: Flow control callbacks
    def pause_writing(self):
        logger.debug(f"pause_writing")

    def resume_writing(self):
        logger.debug(f"resume_writing")

    # Datagram Protocols
    def datagram_received(self, data: bytes, addr):
        logger.debug(f"datagram_received:\n\tdata={data!r}\n\taddr={addr}")
        self.received.append(Datagram(data=data, address=addr))

    def error_received(self, exc: Exception):
        logger.debug(f"error_received:\n\texc={exc}")
