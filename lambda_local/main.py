'''
Copyright 2015-2019 HENNGE K.K. (formerly known as HDE, Inc.)
Licensed under MIT.
'''

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


class FunctionLoader():
    def __init__(self,
                 request_id=None,
                 source=None,
                 function_name=None,
                 library_path=None,
                 func=None):
        self.request_id = request_id
        self.source = source
        self.function_name = function_name
        self.library_path = library_path

        self.func = func

    def load(self):
        if self.library_path is not None:
            load_lib(self.library_path)

        self.func = load_source(
            self.request_id, self.source, self.function_name)


def call(func, event, context, environment_variables={}):
    export_variables(environment_variables)
    loader = FunctionLoader(func=func)
    return _runner(loader, event, context)


def run(args):
    # set env vars if path to json file was given
    set_environment_variables(args.environment_variables)

    e = event.read_event(args.event)
    c = context.Context(
        args.timeout,
        invoked_function_arn=args.arn_string,
        function_version=args.version_name)
    loader = FunctionLoader(
        request_id=c.aws_request_id,
        source=args.file,
        function_name=args.function,
        library_path=args.library)

    (result, err_type) = _runner(loader, e, c)

    if err_type is not None:
        sys.exit(EXITCODE_ERR)


def _runner(loader, event, context):
    logger = logging.getLogger()

    logger.info("Event: {}".format(event))
    logger.info("START RequestId: {} Version: {}".format(
        context.aws_request_id, context.function_version))

    queue = multiprocessing.Queue()
    p = multiprocessing.Process(
        target=execute_in_process,
        args=(queue, loader, event, context,))
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


def load_source(request_id, path, function_name):
    mod_name = 'request-' + str(request_id)

    file_path = os.path.abspath(path)
    file_directory = os.path.dirname(file_path)
    sys.path.append(file_directory)

    if sys.version_info.major == 2:
        import imp
        mod = imp.load_source(mod_name, path)
    elif sys.version_info.major == 3 and sys.version_info.minor >= 5:
        import importlib
        spec = importlib.util.spec_from_file_location(mod_name, path)
        mod = importlib.util.module_from_spec(spec)
        sys.modules[mod_name] = mod
        spec.loader.exec_module(mod)
    else:
        raise Exception("unsupported python version")

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
            "stackTrace": traceback.format_tb(err[2]),
            "errorType": err[0].__name__
        }, indent=4, separators=(',', ': '))
        err_type = ERR_TYPE_EXCEPTION

    return result, err_type


def execute_in_process(queue, loader, event, context):
    if loader.func is None:
        loader.load()
    start_time = timeit.default_timer()
    result, err_type = execute(loader.func, event, context)
    end_time = timeit.default_timer()
    duration = (end_time - start_time) * 1000

    queue.put((result, err_type, duration))
