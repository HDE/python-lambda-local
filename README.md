# python-lambda-local

[![Join the chat at https://gitter.im/HDE/python-lambda-local](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/HDE/python-lambda-local?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
[![wercker status](https://app.wercker.com/status/04f5bc5b7de3d5c6f13eb5b871035226/s "wercker status")](https://app.wercker.com/project/bykey/04f5bc5b7de3d5c6f13eb5b871035226)
[![PyPI version](https://badge.fury.io/py/python-lambda-local.svg)](https://badge.fury.io/py/python-lambda-local)

Run lambda function on local machine

## Prepare development environment

Please use a newly created virtualenv of Python 2.7 or Python 3.6 .

## Installation

Within virtualenv, run the following command.

``` bash
$ pip install python-lambda-local
```

This will install the package with name `python-lambda-local` in the virtualenv.
Now you can use the command `python-lambda-local` to run your AWS Lambda function written in Python on your own machine.

## Usage

Run `python-lambda-local -h` to see the help.

```
usage: python-lambda-local [-h] [-l LIBRARY_PATH] [-f HANDLER_FUNCTION]
                           [-t TIMEOUT] [-a ARN_STRING] [-v VERSION_NAME]
                           FILE EVENT

Run AWS Lambda function written in Python on local machine.

positional arguments:
  FILE                  Lambda function file name
  EVENT                 Event data file name.

optional arguments:
  -h, --help            show this help message and exit
  -l LIBRARY_PATH, --library LIBRARY_PATH
                        Path of 3rd party libraries.
  -f HANDLER_FUNCTION, --function HANDLER_FUNCTION
                        Lambda function handler name. Default: "handler".
  -t TIMEOUT, --timeout TIMEOUT
                        Seconds until lambda function timeout. Default: 3
  -a ARN_STRING, --arn-string ARN_STRING
                        arn string for function
  -v VERSION_NAME, --version-name VERSION_NAME
                        function version name
```

### Prepare development directory

#### Project directory structure

Suppose your project directory is like this:

```
├── event.json
├── lib
│   ├── rx
│   │   ├── abstractobserver.py
│   │   ├── ... (package content of rx)
...
│   │       └── testscheduler.py
│   └── Rx-1.2.3.dist-info
│       ├── DESCRIPTION.rst
│       ├── METADATA
│       ├── metadata.json
│       ├── pbr.json
│       ├── RECORD
│       ├── top_level.txt
│       ├── WHEEL
│       └── zip-safe
└── test.py
```

The handler's code is in `test.py` and the function name of the handler is `handler`.
The source depends on 3rd party library `rx` and it is installed in the directory `lib`.
The test event in json format is in `event.json` file.

#### Content of `test.py`:

``` python
from __future__ import print_function
from rx import Observable


def handler(event, context):
    xs = Observable.from_(range(event['answer']))
    ys = xs.to_blocking()
    zs = (x*x for x in ys if x % 7 == 0)
    for x in zs:
        print(x)
```

#### Content of `event.json`:

``` json
{
  "answer": 42
}
```

#### Run the lambda function

Within the project root directory, you can run the lambda function with the following command

```
python-lambda-local -l lib/ -f handler -t 5 test.py event.json
```

The output will be like:

```
[root - INFO - 2017-04-19 12:39:05,512] Event: {u'answer': 42}
[root - INFO - 2017-04-19 12:39:05,512] START RequestId: b918f9ae-0ca1-44af-9937-dd5f9eeedcc1
0
49
196
441
784
1225
[root - INFO - 2017-04-19 12:39:05,515] END RequestId: b918f9ae-0ca1-44af-9937-dd5f9eeedcc1
[root - INFO - 2017-04-19 12:39:05,515] RESULT:
None
[root - INFO - 2017-04-19 12:39:05,515] REPORT RequestId: b918f9ae-0ca1-44af-9937-dd5f9eeedcc1	Duration: 2.27 ms
```
