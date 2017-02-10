'''
python-lambda-local: Run lambda function in python on local machine.

Note that "python setup.py test" invokes pytest on the package. With
appropriately configured setup.cfg, this will check both xxx_test modules and
docstrings.

Copyright 2015 HDE, Inc.
Licensed under MIT.
'''
import sys
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand


# This is a plug-in for setuptools that will invoke py.test
# when you run python setup.py test
class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        sys.exit(pytest.main(self.test_args))


version = "0.1.3"

setup(name="python-lambda-local",
      version=version,
      description="Run lambda function in python on local machine.",
      long_description=open("README.rst").read(),
      classifiers=[
        'Development Status :: 1 - Planning',
        'Programming Language :: Python'
      ],
      keywords="AWS Lambda",
      author="YANG Xudong",
      author_email="xudong.yang@hde.co.jp",
      url="https://github.com/HDE/python-lambda-local",
      license="MIT",
      packages=find_packages(exclude=['examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      tests_require=['pytest'],
      cmdclass={'test': PyTest},
      install_requires=['boto3'],
      entry_points={
        'console_scripts': ['python-lambda-local=lambda_local:main']
      })
