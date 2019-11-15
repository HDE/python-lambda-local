'''
Copyright 2015-2019 HENNGE K.K. (formerly known as HDE, Inc.)
Licensed under MIT.
'''

import imp
import sys
import traceback
import json
import logging
import os
import timeit
import multiprocessing

from . import event
from . import context
from .environment_variables import set_environment_variables, export_variables
from .timeout import time_limit
from .timeout import TimeoutException

logging.basicConfig(stream=sys.stdout,
                    level=logging.INFO,
                    format='[%(name)s - %(levelname)s - %(asctime)s] %(message)s')


ERR_TYPE_EXCEPTION = 0
ERR_TYPE_TIMEOUT = 1

EXITCODE_ERR = 1


class ContextFilter(logging.Filter):
    def __init__(self, context):
        super(ContextFilter, self).__init__()
        self.context = context

    def filter(self, record):
        record.aws_request_id = self.context.aws_request_id
        return True


def call(func, event, context, environment_variables={}):
    export_variables(environment_variables)

    return _runner(func, event, context)


def run(args):
    # set env vars if path to json file was given
    set_environment_variables(args.environment_variables)

    e = event.read_event(args.event)
    c = context.Context(
        args.timeout,
        invoked_function_arn=args.arn_string,
        function_version=args.version_name)
    if args.library is not None:
        load_lib(args.library)
    func = load(c.aws_request_id, args.file, args.function)

    (result, err_type) = _runner(func, e, c)

    if err_type is not None:
        sys.exit(EXITCODE_ERR)


def _runner(func, event, context):
    logger = logging.getLogger()

    logger.info("Event: {}".format(event))
    logger.info("START RequestId: {} Version: {}".format(
        context.aws_request_id, context.function_version))

    queue = multiprocessing.Queue()
    p = multiprocessing.Process(
        target=execute_in_process,
        args=(queue, func, event, context,))
    p.start()
    (result, err_type, duration) = queue.get()
    p.join()

    logger.info("END RequestId: {}".format(context.aws_request_id))
    duration = "{0:.2f} ms".format(duration)
    logger.info("REPORT RequestId: {}\tDuration: {}".format(
        context.aws_request_id, duration))
    if type(result) is TimeoutException:
        logger.error("RESULT:\n{}".format(result))
    else:
        logger.info("RESULT:\n{}".format(result))

    return (result, err_type)


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

    logger = logging.getLogger()
    log_filter = ContextFilter(context)
    logger.addFilter(log_filter)

    try:
        with time_limit(context._timeout_in_seconds):
            result = func(event, context._activate())
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


def execute_in_process(queue, func, event, context):
    start_time = timeit.default_timer()
    result, err_type = execute(func, event, context)
    end_time = timeit.default_timer()
    duration = (end_time - start_time) * 1000

    queue.put((result, err_type, duration))
