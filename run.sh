#!/usr/bin/env bash
if ! hash python3; then
    echo "python3 is not installed"
    exit 1
fi
if ! hash pyvenv; then
    echo "venv is not installed"
    exit 1
fi
ver=$(python3 -V 2>&1 | sed 's/.* \([0-9]\).\([0-9]\).*/\1\2/')
if [ "$ver" -lt "36" ]; then
    echo "This script requires python 3.6 or greater"
    exit 1
fi

DIR=".virtualenv/challenge/"
if [ ! -d "$DIR" ]; then
    echo "Creating virtual environment."
    mkdir -p $DIR
    python3 -m venv $DIR
    source ${DIR}bin/activate
    echo "Installing pip modules."
    python3 -m pip install -r requirements.txt
    echo -e "Virtual environment created.\n"
else
    source ${DIR}bin/activate
fi

python3 challenge/src/challenge.py
