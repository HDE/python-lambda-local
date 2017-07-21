'''
Copyright 2015-2017 HDE, Inc.
Licensed under MIT.
'''

import json
import os
import subprocess


def read_event(path):
    if os.path.isfile(path) and os.access(path, os.X_OK):
        r = subprocess.run(path, stdout=subprocess.PIPE)
        data = json.loads(r.stdout)
    else:
        with open(path) as event:
            data = json.load(event)

    return data
