#!/usr/bin/env python2.7

import json


def read_event(path):
    with open(path) as event:
        data = json.load(event)

    return data
