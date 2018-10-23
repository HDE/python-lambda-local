'''
python-lambda-local: Test Direct Inovactions 
(command-line and direct).

Meant for use with py.test.

Copyright 2015 HDE, Inc.
Licensed under MIT
'''
import json
import argparse
from multiprocessing import Process
import os
from lambda_local.main import run as lambda_run
from lambda_local.main import call as lambda_call


def my_lambda_function(event, context):
    print("Hello World from My Lambda Function!")
    return 42

def test_function_call_for_pytest():
    request = json.dumps({})
    (result, error_type) = lambda_call(func=my_lambda_function, event=request, timeout=1)

    assert error_type is None

    assert result == 42


def test_check_command_line():
    request = json.dumps({})
    request_file = 'check_command_line_event.json'
    with open (request_file, "w") as f:
        f.write(request)

    args = argparse.Namespace(event=request_file,
                              file='tests/test_direct_invocations.py',
                              function='my_lambda_function',
                              timeout=1,
                              environment_variables='',
                              library=None,
                              version_name='',
                              arn_string=''
                              )
    p = Process(target=lambda_run, args=(args,))
    p.start()
    p.join()

    os.remove(request_file)
    assert p.exitcode == 0
    