#!/bin/sh

cat > ~/.pypirc << EOF
[distutils]
index-servers = pypi

[pypi]
repository = https://pypi.python.org/pypi
username = $PYPI_USERNAME
password = $PYPI_PASSWORD
EOF

cat ~/.pypirc
python setup.py sdist upload
