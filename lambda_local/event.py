'''
Copyright 2015 HDE, Inc.
Licensed under MIT.
'''

import json


def read_event(path):
    with open(path) as event:
        data = json.load(event)

    return data
