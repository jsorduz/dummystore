#!/bin/bash
apps="config common app_*"

if [ ${1:-n} != -t ]
then
    python -m black $(echo $apps)
    python -m isort $(echo $apps)
    python -m flake8
    python -m mypy $(echo $apps)
    python -m pylint $(echo $apps)
fi

python -m pytest --cov
