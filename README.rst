python-lambda-local
===================

|Join the chat at https://gitter.im/HDE/python-lambda-local| |wercker
status| |PyPI version|

Run lambda function on local machine

Prepare development environment
-------------------------------

Please use a newly created virtualenv of Python 2.7 or Python 3.6.

Installation
------------

Within virtualenv, run the following command.

.. code:: bash

   $ pip install python-lambda-local

This will install the package with name ``python-lambda-local`` in the
virtualenv. Now you can use the command ``python-lambda-local`` to run
your AWS Lambda function written in Python on your own machine.

Usage as a shell command
------------------------

Run ``python-lambda-local -h`` to see the help.

::

   usage: python-lambda-local [-h] [-l LIBRARY_PATH] [-f HANDLER_FUNCTION]
                              [-t TIMEOUT] [-a ARN_STRING] [-v VERSION_NAME]
                              [-e ENVIRONMENT_VARIABLES] [--version]
                              FILE EVENT

   Run AWS Lambda function written in Python on local machine.

   positional arguments:
     FILE                  lambda function file name
     EVENT                 event data file name

   optional arguments:
     -h, --help            show this help message and exit
     -l LIBRARY_PATH, --library LIBRARY_PATH
                           path of 3rd party libraries
     -f HANDLER_FUNCTION, --function HANDLER_FUNCTION
                           lambda function handler name, default: "handler"
     -t TIMEOUT, --timeout TIMEOUT
                           seconds until lambda function timeout, default: 3
     -a ARN_STRING, --arn-string ARN_STRING
                           ARN string for lambda function
     -v VERSION_NAME, --version-name VERSION_NAME
                           lambda function version name
     -e ENVIRONMENT_VARIABLES, --environment-variables ENVIRONMENT_VARIABLES
                           path to flat json file with environment variables
     --version             print the version of python-lambda-local and exit

Prepare development directory
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Project directory structure
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Suppose your project directory is like this:

::

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

The handler’s code is in ``test.py`` and the function name of the
handler is ``handler``. The source depends on 3rd party library ``rx``
and it is installed in the directory ``lib``. The test event in json
format is in ``event.json`` file.

Content of ``test.py``:
^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

   from __future__ import print_function
   from rx import Observable


   def handler(event, context):
       xs = Observable.from_(range(event['answer']))
       ys = xs.to_blocking()
       zs = (x*x for x in ys if x % 7 == 0)
       for x in zs:
           print(x)

Content of ``event.json``:
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: json

   {
     "answer": 42
   }

Run the lambda function
^^^^^^^^^^^^^^^^^^^^^^^

Within the project root directory, you can run the lambda function with
the following command

::

   python-lambda-local -l lib/ -f handler -t 5 test.py event.json

The output will be like:

::

   [root - INFO - 2018-11-20 17:10:53,352] Event: {'answer': 42}
   [root - INFO - 2018-11-20 17:10:53,352] START RequestId: 3c8e6db4-886a-43da-a1c7-5e6f715de531 Version: 
   0
   49
   196
   441
   784
   1225
   [root - INFO - 2018-11-20 17:10:53,359] END RequestId: 3c8e6db4-886a-43da-a1c7-5e6f715de531
   [root - INFO - 2018-11-20 17:10:53,360] REPORT RequestId: 3c8e6db4-886a-43da-a1c7-5e6f715de531  Duration: 2.17 ms
   [root - INFO - 2018-11-20 17:10:53,360] RESULT:
   None

Usage as a library
------------------

API signature
~~~~~~~~~~~~~

.. code:: python

   call(func, event, context, environment_variables={})

Call a handler function ``func`` with given ``event``, ``context`` and
custom ``environment_variables``.

Sample
~~~~~~

1. Make sure the 3rd party libraries used in the AWS Lambda function can
   be imported.

.. code:: bash

   pip install rx

2. To call the lambda function above with your python code:

.. code:: python

   from lambda_local.main import call
   from lambda_local.context import Context

   import test

   event = {
       "answer": 42
   }
   context = Context(5)

   call(test.handler, event, context)

.. |Join the chat at https://gitter.im/HDE/python-lambda-local| image:: https://badges.gitter.im/Join%20Chat.svg
   :target: https://gitter.im/HDE/python-lambda-local?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge
.. |wercker status| image:: https://app.wercker.com/status/04f5bc5b7de3d5c6f13eb5b871035226/s
   :target: https://app.wercker.com/project/bykey/04f5bc5b7de3d5c6f13eb5b871035226
.. |PyPI version| image:: https://badge.fury.io/py/python-lambda-local.svg
   :target: https://badge.fury.io/py/python-lambda-local
