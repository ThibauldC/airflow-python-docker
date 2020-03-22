#!/bin/bash

# Exit immediately if a  .
set -e

if [ "$1" = 'test-version' ]; then
    exec python --version
elif [ "$1" = 'run-download' ]; then
    exec python -m download.__init__
elif [ "$1" = 'run-preprocessing' ]; then
    exec python -m preprocessing.__init__
elif [ "$1" = 'run-processing' ]; then
    exec python -m processing.__init__
fi

exec "$@"