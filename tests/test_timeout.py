import time

import pytest
from . import timeout as subject


@pytest.mark.realtime
def test_timeout_exceeded():
    with pytest.raises(subject.TimedOut):
        with subject.timeout(1):
            time.sleep(2)


@pytest.mark.realtime
def test_timeout_not_exceeded():
    with subject.timeout(1):
        pass
