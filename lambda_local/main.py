'''
Copyright 2015 HDE, Inc.
Licensed under MIT.
'''

import imp
import sys
import traceback
import json
import logging
import uuid
import os
import timeit
from botocore.vendored.requests.packages import urllib3

import event
import context
from timeout import time_limit
from timeout import TimeoutException

logging.basicConfig(stream=sys.stdout,
                    level=logging.INFO,
                    format='[%(name)s - %(levelname)s - %(asctime)s] %(message)s')
urllib3.disable_warnings()


ERR_TYPE_EXCEPTION = 0
ERR_TYPE_TIMEOUT = 1

EXITCODE_ERR = 1


def run(args):
    e = event.read_event(args.event)
    c = context.Context(args.timeout, args.arn_string, args.version_name)
    if args.library is not None:
        load_lib(args.library)
    request_id = uuid.uuid4()
    func = load(request_id, args.file, args.function)

    logger = logging.getLogger()
    result = None

    logger.info("Event: {}".format(e))

    logger.info("START RequestId: {}".format(request_id))

    start_time = timeit.default_timer()
    result, err_type = execute(func, e, c)
    end_time = timeit.default_timer()

    logger.info("END RequestId: {}".format(request_id))

    if type(result) is TimeoutException:
        logger.error("RESULT:\n{}".format(result))
    else:
        logger.info("RESULT:\n{}".format(result))

    duration = "{0:.2f} ms".format((end_time - start_time) * 1000)
    logger.info("REPORT RequestId: {}\tDuration: {}".format(
        request_id, duration))

    if err_type is not None:
        sys.exit(EXITCODE_ERR)


def load_lib(path):
    sys.path.append(os.path.abspath(path))


def load(request_id, path, function_name):
    mod_name = 'request-' + str(request_id)

    file_path = os.path.abspath(path)
    file_directory = os.path.dirname(file_path)
    sys.path.append(file_directory)

    mod = imp.load_source(mod_name, path)
    func = getattr(mod, function_name)
    return func


def execute(func, event, context):
    err_type = None

    try:
        with time_limit(context.timeout):
            result = func(event, context.activate())
    except TimeoutException as err:
        result = err
        err_type = ERR_TYPE_TIMEOUT
    except:
        err = sys.exc_info()
        result = json.dumps({
            "errorMessage": str(err[1]),
            "stackTrace": traceback.extract_tb(err[2]),
            "errorType": err[0].__name__
        }, indent=4, separators=(',', ': '))
        err_type = ERR_TYPE_EXCEPTION

    return result, err_type
