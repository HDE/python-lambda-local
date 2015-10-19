#!/usr/bin/env python2.7

import imp
import sys
import traceback
import json
import logging
import uuid
import os

import event
import context
from timeout import time_limit
from timeout import TimeoutException

logging.basicConfig(stream=sys.stdout,
                    level=logging.INFO,
                    format='[%(levelname)s %(asctime)s] %(message)s')


def run(args):
    e = event.read_event(args.event)
    c = context.Context(args.timeout)
    if args.library is not None:
        load_lib(args.library)
    request_id = uuid.uuid4()
    func = load(request_id, args.file, args.function)

    logger = logging.getLogger()

    logger.info("Event: {}".format(e))

    logger.info("START RequestId: {}".format(request_id))
    try:
        result = execute(func, e, c)
    except TimeoutException as e:
        result = e
    logger.info("END RequestId: {}".format(request_id))

    if type(result) is TimeoutException:
        logger.error("RESULT: {}".format(result))
    else:
        logger.info("RESULT: {}".format(result))


def load_lib(path):
    sys.path.append(os.path.abspath(path))


def load(request_id, path, function_name):
    mod_name = 'request-' + str(request_id)
    mod = imp.load_source(mod_name, path)
    func = getattr(mod, function_name)
    return func


def execute(func, event, context):
    try:
        with time_limit(context.timeout):
            result = func(event, context)
    except TimeoutException as err:
        raise err
    except:
        err = sys.exc_info()
        result = json.dumps({
            "errorMessage": str(err[1]),
            "stackTrace": traceback.extract_tb(err[2]),
            "errorType": err[0].__name__
        }, indent=4, separators=(',', ': '))

    return result
