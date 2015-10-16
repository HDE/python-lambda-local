#!/usr/bin/env python2.7

import imp
import sys
import traceback
import json
import logging
import uuid

import event
import context

logging.basicConfig(stream=sys.stdout,
                    level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def run(args):
    e = event.read_event(args.event)
    c = context.Context(args.timeout)
    func = load(args.file, args.function)

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    request_id = uuid.uuid4()

    logger.info("Event: {}".format(e))

    logger.info("START RequestId: {}".format(request_id))
    result = execute(func, e, c)
    logger.info("END RequestId: {}".format(request_id))

    logger.info("RESULT: {}".format(result))


def load(path, function_name):
    mod = imp.load_source('', path)
    func = getattr(mod, function_name)
    return func


def execute(func, event, context):
    try:
        result = func(event, context)
    except:
        err = sys.exc_info()
        result = json.dumps({
            "errorMessage": str(err[1]),
            "stackTrace": traceback.extract_tb(err[2]),
            "errorType": err[0].__name__
        }, indent=4, separators=(',', ': '))

    return result
