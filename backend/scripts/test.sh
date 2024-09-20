#!/bin/sh

# Automatically set PYTHONPATH to the project root
export PYTHONPATH=$(pwd)

# Determine if using a virtual environment
export PREFIX=""
if [ -d '.venv' ] ; then
    export PREFIX=".venv/bin/"
fi

# Enable exit on error and command tracing
set -ex


# Run tests with coverage
${PREFIX}pytest $@
