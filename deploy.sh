#!/bin/sh

cat > ~/.pypirc << EOF
[distutils]
index-servers =
    pypi

[pypi]
repository: https://upload.pypi.org/legacy/
username: ${PYPI_USERNAME}
password: ${PYPI_PASSWORD}
EOF

pip install twine

mkdir dist
cp build-py2/dist/* dist/
cp build-py37/dist/* dist/
cp build-py38/dist/* dist/

twine upload -r pypi dist/*
