python-lambda-local
===================

Run lambda function on local machine

Prepare development environment
-------------------------------

Please use a newly created virtualenv for python2.7.

Installation
------------

Within virtualenv, run the following command.

.. code:: bash

    $ cd $PROJECT_ROOT
    $ pip install ./

This will install the package with name ``python-lambda-local`` in the
virtualenv. Now you can use the command ``python-lambda-local`` to run
your AWS Lambda function written in Python on your own machine.

Usage
-----

Run ``python-lambda-local -h`` to see the help.

::

    usage: python-lambda-local [-h] [-l LIBRARY_PATH] [-f HANDLER_FUNCTION]
                               [-t TIMEOUT]
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

Prepare development directory
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Project directory structure
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Suppose your project directory is like this:

::

    ├── event.json
    ├── lib
    │   ├── rx
    │   │   ├── abstractobserver.py
    │   │   ├── ... (package content of rx)
    ...
    │   │       └── testscheduler.py
    │   └── Rx-1.2.3.dist-info
    │       ├── DESCRIPTION.rst
    │       ├── METADATA
    │       ├── metadata.json
    │       ├── pbr.json
    │       ├── RECORD
    │       ├── top_level.txt
    │       ├── WHEEL
    │       └── zip-safe
    └── test.py

In the handler's code is in ``test.py`` and the function name of the
handler is ``handler``. The source depends on 3rd party library ``rx``
and it is install in the directory ``lib``. The test event of json
format is in ``event.json`` file.

Content of ``test.py``:
^^^^^^^^^^^^^^^^^^^^^^^

.. code:: python

    from rx import Observable


    def handler(event, context):
        xs = Observable.from_([1, 2, 3, 4, 5, 6])
        ys = xs.to_blocking()
        zs = (x*x for x in ys if x > 3)
        for x in zs:
            print x

Content of ``event.json``:
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code:: json

    {
      "key": "value"
    }

Run the lambda function
^^^^^^^^^^^^^^^^^^^^^^^

Within the project root directory, you can run the lambda function with
the following command

::

    python-lambda-local -l lib/ -f handler -t 5 test.py event.json

The output will be like:

::

    [INFO 2015-10-16 18:21:14,774] Event: {'key': 'value'}
    [INFO 2015-10-16 18:21:14,774] START RequestId: 324cb1c5-fa9b-4f39-8ad9-01c95f7d5744
    16
    25
    36
    [INFO 2015-10-16 18:21:14,775] END RequestId: 324cb1c5-fa9b-4f39-8ad9-01c95f7d5744
    [INFO 2015-10-16 18:21:14,775] RESULT: None
