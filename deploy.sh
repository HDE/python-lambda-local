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
twine upload -r pypi dist/*

