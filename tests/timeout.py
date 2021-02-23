import contextlib
import signal
from typing import Generator
import dataclasses
import time


class TimedOut(Exception):
    pass


@contextlib.contextmanager
def timeout(seconds: int) -> Generator[None, None, None]:
    """Must be called from main thread of main interpreter."""

    def raise_timeout(signum, frame):
        raise TimedOut

    existing_handler = signal.getsignal(signal.SIGALRM)  # Save off the existing handler
    signal.signal(signal.SIGALRM, raise_timeout)  # Set our own handler
    signal.alarm(seconds)  # Kick off the alarm

    try:
        yield
    finally:
        signal.alarm(0)  # Unset the alarm
        signal.signal(signal.SIGALRM, existing_handler)  # Reset the handler


# @dataclasses.dataclass
# class CheckedTimeout:
#     duration: float
#     started: float = dataclasses.field(default_factory=time.monotonic, init=False)

#     def check(self):
#         deadline = self.started + self.duration
#         if deadline > time.monotonic():
#             raise TimedOut


# @contextlib.contextmanager
# def checked_timeout(seconds: float) -> Generator[CheckedTimeout, None, None]:
#     yield CheckedTimeout(seconds)