'''
Copyright 2015 HDE, Inc.
Licensed under MIT.
'''

from datetime import datetime
from datetime import timedelta


class Context(object):
    def __init__(self, timeout, arn_string, version_name):
        self.function_name = "undefined"
        self.function_version = version_name
        self.invoked_function_arn = arn_string
        self.memory_limit_in_mb = 0
        self.aws_request_id = "undefined"
        self.log_group_name = "undefined"
        self.log_stream_name = "undefined"
        self.identity = None
        self.client_context = None
        self.timeout = timeout
        self.duration = timedelta(seconds=timeout)

    def get_remaining_time_in_millis(self):
        if self.timelimit is None:
            raise Exception("Context not activated.")
        return millis_interval(datetime.now(), self.timelimit)

    def activate(self):
        self.timelimit = datetime.now() + self.duration
        return self


def millis_interval(start, end):
    """start and end are datetime instances"""
    diff = end - start
    millis = diff.days * 24 * 60 * 60 * 1000
    millis += diff.seconds * 1000
    millis += diff.microseconds / 1000
    return millis
