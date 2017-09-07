'''
Copyright 2015-2017 HDE, Inc.
Licensed under MIT.
'''

import signal
from contextlib import contextmanager


class TimeoutException(Exception):
    pass


@contextmanager
def time_limit(seconds):
    def signal_handler(signum, frame):
        raise TimeoutException("Timeout after {} seconds.".format(seconds))
    if hasattr(signal, "SIGALRM"):
        signal.signal(signal.SIGALRM, signal_handler)
        signal.alarm(seconds)
    try:
        yield
    finally:
        if hasattr(signal, "SIGALRM"):
            signal.alarm(0)
